#!/usr/bin/env python3
"""
Tool to generate specialized lore books for agents based on their purpose.
"""

import os
import sys
import json
import argparse
import logging
import time
import subprocess
import requests
from typing import Dict, Any, List, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import LoreAPI from agents/api
from agents.api.lore_api import LoreAPI

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("agent_lore_generator")

def run_llm(model: str, prompt: str, provider: str = "ollama") -> str:
    """Run LLM with the given model and prompt using specified provider."""

    if provider == "ollama":
        try:
            result = subprocess.run(
                ["ollama", "run", model, prompt],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logger.error(f"Error running Ollama: {e}")
            logger.error(f"Stderr: {e.stderr}")
            return ""

    elif provider == "claude":
        # Use Claude CLI binary with system prompt
        try:
            system_prompt_file = os.path.expandvars("$SKOGAI_LORE/orchestrator/lore-writer.md")
            with open(system_prompt_file, 'r') as f:
                system_prompt = f.read()

            result = subprocess.run(
                ["claude", "-p", "--system-prompt", system_prompt, prompt],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except FileNotFoundError as e:
            if "lore-writer.md" in str(e):
                logger.error(f"Lore writer prompt not found: {system_prompt_file}")
            else:
                logger.error("Claude CLI not found. Install with: npm install -g @anthropic-ai/claude-code")
            return ""
        except subprocess.CalledProcessError as e:
            logger.error(f"Error running Claude CLI: {e}")
            logger.error(f"Stderr: {e.stderr}")
            return ""

    elif provider == "openai":
        # OpenAI-compatible API (works with OpenRouter, OpenAI, etc.)
        api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("OPENROUTER_API_KEY")
        base_url = os.environ.get("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")

        if not api_key:
            logger.error("No API key found. Set OPENAI_API_KEY or OPENROUTER_API_KEY")
            return ""

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 2048,
        }

        try:
            response = requests.post(
                f"{base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=120
            )

            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                logger.error(f"API error: {response.status_code} - {response.text}")
                return ""
        except requests.RequestException as e:
            logger.error(f"Request error: {str(e)}")
            return ""

    else:
        logger.error(f"Unknown provider: {provider}")
        return ""


# Backwards compatibility alias
def run_ollama(model: str, prompt: str) -> str:
    """Deprecated: Use run_llm() instead."""
    return run_llm(model, prompt, "ollama")

def determine_agent_needs(agent_type: str, agent_description: str, model: str, provider: str = "ollama") -> Dict[str, Any]:
    """Determine the types of lore an agent needs based on its purpose."""
    prompt = f"""Analyze this AI agent's role and determine what types of lore entries would be most helpful for it to have in its context. The agent is a {agent_type} with this description: "{agent_description}"

For each category (character, place, object, event, concept), suggest 0-3 specific lore entries that would be helpful. Format your response exactly like JSON:

{{
  "character": [
    {{"title": "Character Name", "reason": "Brief explanation of relevance"}},
    ...
  ],
  "place": [...],
  "object": [...],
  "event": [...],
  "concept": [...]
}}

Only include categories that are relevant to this agent type."""

    result = run_llm(model, prompt, provider)

    try:
        # Extract JSON from the response (in case there's any preamble/postamble)
        json_start = result.find('{')
        json_end = result.rfind('}') + 1
        if json_start >= 0 and json_end > json_start:
            json_str = result[json_start:json_end]
            return json.loads(json_str)
        else:
            logger.error("Could not find JSON in Ollama response")
            return {}
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON from Ollama response: {e}")
        logger.debug(f"Response was: {result}")
        return {}

def generate_lore_entry(title: str, category: str, agent_type: str, model: str, provider: str = "ollama") -> str:
    """Generate content for a lore entry specifically tailored for an agent type."""
    prompt = f"""Create detailed lore content about '{title}' for a {category} entry. This lore will be used by a {agent_type} AI agent, so make it specifically useful for that purpose.

Your response should include:
- Rich descriptive details relevant to a {agent_type}
- Connections to how this might affect the agent's work
- Unique characteristics that matter for this agent type
- Important background information the agent should know

Write 2-3 paragraphs of rich, evocative content that would help the agent perform better."""

    return run_llm(model, prompt, provider)

def create_specialized_lorebook(api: LoreAPI, agent_type: str, agent_description: str,
                             model: str = "llama3", provider: str = "ollama") -> Dict[str, Any]:
    """Create a specialized lorebook for an agent based on its type."""
    logger.info(f"Creating specialized lorebook for {agent_type} agent using {provider}")

    # Determine what types of lore this agent needs
    lore_needs = determine_agent_needs(agent_type, agent_description, model, provider)
    # Create the lorebook
    timestamp = int(time.time())
    book = api.create_lore_book(
        title=f"Specialized Lore for {agent_type.title()} Agent",
        description=f"Lore collection specifically created for {agent_type} agents: {agent_description}"
    )
    # Process each category
    for category, entries in lore_needs.items():
        if not entries:
            continue
            # Create the entry
            entry = api.create_lore_entry(
                title=title,
                content=content,
                category=category,
                tags=[agent_type, category],
                summary=summary
            )
    # Update book categories
    book = api.get_lore_book(book["id"])
    if book:
        book["categories"] = entries_by_category

        # Update book file
        book_path = os.path.join(api.lore_books_dir, f"{book['id']}.json")
        with open(book_path, 'w') as f:
            json.dump(book, f, indent=2)

    return {
        "success": True,
        "book_id": book["id"],
        "categories": entries_by_category,
        "entry_count": sum(len(entries) for entries in entries_by_category.values())
    }

def link_to_existing_persona(api: LoreAPI, book_id: str, persona_id: str) -> Dict[str, Any]:
    """Link the specialized lorebook to an existing persona."""
    success = api.link_book_to_persona(book_id, persona_id)

    if success:
        return {
            "success": True,
            "persona_id": persona_id,
            "book_id": book_id
        }
    else:
        return {
            "success": False,
            "error": f"Failed to link book {book_id} to persona {persona_id}"
        }

def create_persona_with_lore(api: LoreAPI, agent_type: str, model: str,
                           book_id: str = None, provider: str = "ollama") -> Dict[str, Any]:
    """Create a new persona for the agent type and link it to the specialized lorebook."""
    # Use LLM to generate persona details
    prompt = f"""Generate details for an AI persona that would be good at being a {agent_type}.

Format your response exactly like this:
NAME: [creative name]
DESCRIPTION: [1-2 sentences about the persona]
TRAITS: [4-6 personality traits, comma-separated]
VOICE: [description of voice and speaking style]"""

    result = run_llm(model, prompt, provider)

    # Parse the response
    name = "Agent"
    description = f"A specialized {agent_type} agent"
    traits = ["professional", "knowledgeable", "helpful", "focused"]
    voice = "Clear and informative"

    for line in result.split('\n'):
        if line.startswith("NAME:"):
            name = line.replace("NAME:", "").strip()
        elif line.startswith("DESCRIPTION:"):
            description = line.replace("DESCRIPTION:", "").strip()
        elif line.startswith("TRAITS:"):
            traits_str = line.replace("TRAITS:", "").strip()
            traits = [t.strip() for t in traits_str.split(',')]
        elif line.startswith("VOICE:"):
            voice = line.replace("VOICE:", "").strip()

    # Create the persona
    persona = api.create_persona(
        name=name,
        core_description=description,
        personality_traits=traits,
        voice_tone=voice
    )

    logger.info(f"Created persona: {persona['id']} - {name}")

    # Link to the specialized lorebook if provided
    if book_id:
        link_result = link_to_existing_persona(api, book_id, persona["id"])
        if not link_result.get("success", False):
            logger.warning(f"Failed to link book {book_id} to persona {persona['id']}")

    return {
        "success": True,
        "persona_id": persona["id"],
        "name": name,
        "description": description
    }

def main():
    parser = argparse.ArgumentParser(description="Generate specialized lore for agents")
    parser.add_argument("--agent-type", required=True, help="Type of agent (writer, researcher, planner, etc.)")
    parser.add_argument("--description", help="Description of the agent's purpose")
    parser.add_argument("--model", default="llama3", help="Model to use (e.g., llama3, claude-sonnet-4-20250514, gpt-4)")
    parser.add_argument("--provider", default="ollama", choices=["ollama", "claude", "openai"],
                       help="LLM provider: ollama (local), claude (CLI), openai (API)")
    parser.add_argument("--persona", help="Link to existing persona ID")
    parser.add_argument("--create-persona", action="store_true", help="Create a new persona for this agent type")
    parser.add_argument("--export", help="Export as SillyTavern lorebook to this path")

    args = parser.parse_args()

    # Initialize API
    api = LoreAPI()

    # Create the specialized lorebook
    description = args.description or f"A {args.agent_type} agent that helps with {args.agent_type} tasks"
    result = create_specialized_lorebook(api, args.agent_type, description, args.model, args.provider)
    # Link to existing persona if specified
    if args.persona:
        link_result = link_to_existing_persona(api, result["book_id"], args.persona)
        if link_result.get("success", False):
            print(f"Linked lorebook to persona: {args.persona}")
        else:
            print(f"Failed to link to persona: {link_result.get('error', 'Unknown error')}")

    # Create a new persona if requested
    if args.create_persona:
        persona_result = create_persona_with_lore(api, args.agent_type, args.model, result["book_id"], args.provider)
        if persona_result.get("success", False):
            print(f"Created new persona: {persona_result['persona_id']} - {persona_result['name']}")

            # If export is requested, export the persona's lore to SillyTavern format
            if args.export:
                sys.path.append(os.path.dirname(os.path.abspath(__file__)))
                from st_lore_export import export_persona_lore
                export_result = export_persona_lore(
                    api, persona_result["persona_id"], export_dir,
                    persona_result["name"], "{{user}}"
                )

                if export_result.get("success", False):
                    print(f"Exported lorebooks to {export_dir}")
                    for book in export_result.get("exported_books", []):
                        print(f"- {book.get('title')} ({book.get('entry_count')} entries)")
                else:
                    print(f"Failed to export: {export_result.get('error', 'Unknown error')}")
        else:
            print(f"Failed to create persona: {persona_result.get('error', 'Unknown error')}")

    # Export directly if requested without creating a persona
    elif args.export and result.get("book_id"):
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from st_lore_export import export_to_sillytavern
        export_result = export_to_sillytavern(
            api, result["book_id"], export_path,
            "{{char}}", "{{user}}", True
        )

        if export_result.get("success", False):
            print(f"Exported lorebook to {export_path}")
        else:
            print(f"Failed to export: {export_result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()
