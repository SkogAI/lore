#!/usr/bin/env python3

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add the parent directory to the path so we can import our modules
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from agents.api.lore_api import LoreAPI

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("persona_manager")


class PersonaManager:
    """
    Manages persona selection, activation, and context integration for the SkogAI system.
    Acts as a bridge between the persona storage and the agent system.
    """

    def __init__(self, base_dir: str = None):
        """Initialize the PersonaManager."""
        self.base_dir = base_dir or os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        self.lore_api = LoreAPI(self.base_dir)
        self.templates_dir = os.path.join(self.base_dir, "agents/templates/personas")
        self.context_template_path = os.path.join(
            self.base_dir, "context/templates/persona-context.json"
        )
        self.active_persona = None

        # Load the persona template
        self.load_persona_template()

    def load_persona_template(self):
        """Load the base persona template."""
        try:
            with open(os.path.join(self.templates_dir, "base-persona.md"), "r") as f:
                self.base_template = f.read()
            logger.info("Loaded base persona template")
        except Exception as e:
            logger.error(f"Failed to load base persona template: {e}")
            self.base_template = "# {{name}}\n\n{{core_description}}"

        try:
            with open(self.context_template_path, "r") as f:
                self.context_template = json.load(f)
            logger.info("Loaded persona context template")
        except Exception as e:
            logger.error(f"Failed to load persona context template: {e}")
            self.context_template = {"schema": {}, "template_mappings": {}}

    def list_available_personas(self) -> List[Dict[str, Any]]:
        """List all available personas."""
        return self.lore_api.list_personas()

    def get_persona(self, persona_id: str) -> Optional[Dict[str, Any]]:
        """Get a persona by ID."""
        return self.lore_api.get_persona(persona_id)

    def activate_persona(self, persona_id: str) -> bool:
        """Set a persona as active."""
        persona = self.get_persona(persona_id)
        if not persona:
            logger.error(f"Cannot activate persona {persona_id}: not found")
            return False

        self.active_persona = persona
        logger.info(f"Activated persona: {persona['name']} ({persona_id})")
        return True

    def deactivate_persona(self) -> bool:
        """Clear the active persona."""
        if self.active_persona:
            logger.info(f"Deactivated persona: {self.active_persona['name']}")
            self.active_persona = None
            return True
        return False

    def get_active_persona(self) -> Optional[Dict[str, Any]]:
        """Get the currently active persona."""
        return self.active_persona

    def create_persona(
        self, name: str, description: str, traits: List[str], voice: str
    ) -> Optional[Dict[str, Any]]:
        """Create a new persona."""
        persona = self.lore_api.create_persona(name, description, traits, voice)
        logger.info(f"Created new persona: {name} ({persona['id']})")
        return persona

    def get_persona_template_variables(self, persona: Dict[str, Any]) -> Dict[str, Any]:
        """Extract template variables from a persona definition."""
        variables = {
            "name": persona.get("name", "Unnamed Persona"),
            "core_description": persona.get("core_description", ""),
            "personality_traits": self._format_list(
                persona.get("core_traits", {}).get("values", [])
            ),
            "voice_description": persona.get("voice", {}).get("tone", ""),
            "speech_patterns": self._format_list(
                persona.get("voice", {}).get("patterns", [])
            ),
            "vocabulary_level": persona.get("voice", {}).get("vocabulary", "standard"),
            "background": self._format_background(persona.get("background", {})),
            "expertise_list": self._format_list(
                persona.get("knowledge", {}).get("expertise", [])
            ),
            "limitations_list": self._format_list(
                persona.get("knowledge", {}).get("limitations", [])
            ),
            "special_instructions": persona.get("interaction_style", {}).get(
                "special_instructions", ""
            ),
            "lore_books": self._format_lore_books(
                persona.get("knowledge", {}).get("lore_books", [])
            ),
        }
        return variables

    def _format_list(self, items: List[str]) -> str:
        """Format a list of items as a bulleted markdown list."""
        if not items:
            return "None specified"
        return "\n".join([f"- {item}" for item in items])

    def _format_background(self, background: Dict[str, Any]) -> str:
        """Format the background section of a persona."""
        parts = []

        if "origin" in background and background["origin"]:
            parts.append(f"**Origin**: {background['origin']}")

        if "significant_events" in background and background["significant_events"]:
            events = "\n".join(
                [f"- {event}" for event in background["significant_events"]]
            )
            parts.append(f"**Significant Events**:\n{events}")

        if "connections" in background and background["connections"]:
            connections = "\n".join(
                [
                    f"- {conn.get('entity', '')}: {conn.get('relationship', '')}"
                    for conn in background["connections"]
                ]
            )
            parts.append(f"**Connections**:\n{connections}")

        return "\n\n".join(parts) if parts else "No background information available."

    def _format_lore_books(self, book_ids: List[str]) -> str:
        """Format the lore books section with book titles."""
        if not book_ids:
            return "None"

        books = []
        for book_id in book_ids:
            book = self.lore_api.get_lore_book(book_id)
            if book:
                books.append(f"- {book['title']} ({book_id})")
            else:
                books.append(f"- Unknown Book ({book_id})")

        return "\n".join(books)

    def render_persona_prompt(self, persona_id: Optional[str] = None) -> str:
        """Render a persona as a prompt template."""
        # Use specified persona or active persona
        persona = None
        if persona_id:
            persona = self.get_persona(persona_id)
        elif self.active_persona:
            persona = self.active_persona

        if not persona:
            logger.error("No persona specified or active")
            return "# No Active Persona\n\nPlease activate a persona first."

        # Get template variables
        variables = self.get_persona_template_variables(persona)

        # Render template
        prompt = self.base_template
        for key, value in variables.items():
            prompt = prompt.replace(f"{{{{{key}}}}}", value)

        return prompt

    def render_lore_generation_prompt(
        self, persona_id: Optional[str] = None, technical_content: str = ""
    ) -> str:
        """
        Render an optimized prompt for lore generation in the persona's voice.
        This prompt reduces meta-commentary and ensures direct narrative output.
        """
        # Use specified persona or active persona
        persona = None
        if persona_id:
            persona = self.get_persona(persona_id)
        elif self.active_persona:
            persona = self.active_persona

        if not persona:
            logger.error("No persona specified or active")
            return ""

        # Extract persona details
        name = persona.get("name", "Unknown")
        voice_tone = persona.get("voice", {}).get("tone", "narrative")
        traits = ", ".join(persona.get("core_traits", {}).get("values", []))

        # Build optimized lore generation prompt
        prompt = f"""# ROLE
You are {name}, speaking in your distinctive voice.

# VOICE SIGNATURE
Tone: {voice_tone}
Core traits: {traits}

# YOUR TASK
Transform this technical event into a lore entry AS IF you are narrating your own story.

## Constraints
- Write in first person ("I discovered...", "I crafted...")
- NO meta-commentary ("I will write", "Let me explain", "Here is")
- Start IMMEDIATELY with narrative
- 2-3 paragraphs, past tense for completed work
- Reflect your personality through word choice and pacing

## Technical Event
{technical_content}

## Your Chronicle Entry (write NOW, no preamble):"""

        return prompt

    def get_persona_context(self, persona_id: Optional[str] = None) -> Dict[str, Any]:
        """Get the full context for a persona, including lore."""
        # Use specified persona or active persona
        persona = None
        if persona_id:
            persona = self.get_persona(persona_id)
        elif self.active_persona:
            persona = self.active_persona

        if not persona:
            logger.error("No persona specified or active")
            return {"error": "No persona specified or active"}

        # Get lore context
        return self.lore_api.get_persona_lore_context(persona["id"])

    def format_persona_for_agent(
        self, persona_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Format persona data for use by the agent system."""
        context = self.get_persona_context(persona_id)
        if "error" in context:
            return {"error": context["error"]}

        persona = context["persona"]

        # Format lore entries
        lore_content = []
        for entry in context.get("lore_entries", []):
            lore_content.append(
                {
                    "title": entry.get("title", ""),
                    "content": entry.get("content", ""),
                    "category": entry.get("category", ""),
                    "tags": entry.get("tags", []),
                }
            )

        # Create agent-compatible format
        agent_data = {
            "persona": {
                "id": persona.get("id", ""),
                "name": persona.get("name", ""),
                "description": persona.get("core_description", ""),
            },
            "traits": {
                "values": persona.get("core_traits", {}).get("values", []),
                "temperament": persona.get("core_traits", {}).get("temperament", ""),
            },
            "voice": {
                "tone": persona.get("voice", {}).get("tone", ""),
                "patterns": persona.get("voice", {}).get("patterns", []),
            },
            "lore": lore_content,
            "prompt": self.render_persona_prompt(persona.get("id", "")),
        }

        return agent_data


# CLI interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Persona Manager CLI")
    parser.add_argument("--persona", help="Persona ID to operate on")
    parser.add_argument("--get-name", action="store_true", help="Get persona name only")
    parser.add_argument("--render-prompt", action="store_true", help="Render full persona prompt")
    parser.add_argument("--list", action="store_true", help="List all personas")

    args = parser.parse_args()

    manager = PersonaManager()

    # Handle --list
    if args.list:
        personas = manager.list_available_personas()
        print(f"Found {len(personas)} personas:")
        for p in personas:
            print(f"- {p['name']} ({p['id']})")
        sys.exit(0)

    # Handle persona-specific operations
    if args.persona:
        persona = manager.get_persona(args.persona)
        if not persona:
            print(f"Error: Persona {args.persona} not found", file=sys.stderr)
            sys.exit(1)

        # Get name only
        if args.get_name:
            print(persona.get("name", "Unknown"))
            sys.exit(0)

        # Render prompt
        if args.render_prompt:
            manager.activate_persona(args.persona)
            prompt = manager.render_persona_prompt()
            print(prompt)
            sys.exit(0)

    # Default demo behavior when no args
    if len(sys.argv) == 1:
        # List available personas
        personas = manager.list_available_personas()
        print(f"Found {len(personas)} personas:")
        for p in personas:
            print(f"- {p['name']} ({p['id']})")

        # Create a new persona if none exist
        if not personas:
            print("\nCreating a new persona...")
            persona = manager.create_persona(
                name="Test Persona",
                description="A test persona for demonstration",
                traits=["curious", "helpful", "knowledgeable"],
                voice="friendly and informative",
            )
            print(f"Created: {persona['name']} ({persona['id']})")
        else:
            # Activate Amy Ravenwolf for demo
            persona = manager.get_persona("persona_1744992765")

            if persona:
                manager.activate_persona(persona["id"])
                print(f"\nActivated: {persona['name']} ({persona['id']})")

                # Get and display the persona prompt
                prompt = manager.render_persona_prompt()
                print("\nPersona Prompt:")
                print("==============")
                print(prompt[:300] + "..." if len(prompt) > 300 else prompt)

                # Get formatted persona data for agent
                agent_data = manager.format_persona_for_agent()
                print("\nAgent Data (summary):")
                print("===================")
                print(f"Name: {agent_data['persona']['name']}")
                print(f"Traits: {', '.join(agent_data['traits']['values'])}")
                print(f"Voice tone: {agent_data['voice']['tone']}")
                print(f"Lore entries: {len(agent_data['lore'])}")
