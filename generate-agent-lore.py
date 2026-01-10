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
import re
from typing import Dict, Any, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("agent_lore_generator")

# Shell tool paths
REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
MANAGE_LORE_SCRIPT = os.path.join(REPO_ROOT, "tools", "manage-lore.sh")
CREATE_PERSONA_SCRIPT = os.path.join(REPO_ROOT, "tools", "create-persona.sh")
LORE_ENTRIES_DIR = os.path.join(REPO_ROOT, "knowledge", "expanded", "lore", "entries")
LORE_BOOKS_DIR = os.path.join(REPO_ROOT, "knowledge", "expanded", "lore", "books")
PERSONAS_DIR = os.path.join(REPO_ROOT, "knowledge", "expanded", "personas")

# Helper functions for shell tool integration
def run_shell_tool(command: List[str]) -> Dict[str, Any]:
    """Run a shell tool command and return parsed result."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            cwd=REPO_ROOT
        )
        return {"success": True, "output": result.stdout.strip(), "stderr": result.stderr.strip()}
    except subprocess.CalledProcessError as e:
        logger.error(f"Shell tool error: {e}")
        logger.error(f"Stderr: {e.stderr}")
        return {"success": False, "error": str(e), "stderr": e.stderr}

def create_lore_entry_shell(title: str, content: str, category: str, tags: List[str] = None, summary: str = "") -> Dict[str, Any]:
    """Create a lore entry using manage-lore.sh and then update its content."""
    # Create the entry
    result = run_shell_tool([MANAGE_LORE_SCRIPT, "create-entry", title, category])

    if not result["success"]:
        return {"id": None, "error": result.get("error")}

    # Extract entry ID from output (format: "Created lore entry: entry_...")
    match = re.search(r'entry_\d+_[a-f0-9]+', result["output"])
    if not match:
        return {"id": None, "error": "Could not parse entry ID from output"}

    entry_id = match.group(0)
    entry_path = os.path.join(LORE_ENTRIES_DIR, f"{entry_id}.json")

    # Update the entry with content, tags, and summary
    try:
        with open(entry_path, 'r') as f:
            entry = json.load(f)

        entry["content"] = content
        entry["summary"] = summary
        entry["tags"] = tags or []

        with open(entry_path, 'w') as f:
            json.dump(entry, f, indent=2)

        logger.info(f"Updated entry {entry_id} with content and metadata")
        return entry
    except Exception as e:
        logger.error(f"Failed to update entry content: {e}")
        return {"id": entry_id, "error": str(e)}

def create_lore_book_shell(title: str, description: str) -> Dict[str, Any]:
    """Create a lore book using manage-lore.sh."""
    result = run_shell_tool([MANAGE_LORE_SCRIPT, "create-book", title, description])

    if not result["success"]:
        return {"id": None, "error": result.get("error")}

    # Extract book ID from output (format: "Created lore book: book_...")
    match = re.search(r'book_\d+_[a-f0-9]+', result["output"])
    if not match:
        return {"id": None, "error": "Could not parse book ID from output"}

    book_id = match.group(0)
    book_path = os.path.join(LORE_BOOKS_DIR, f"{book_id}.json")

    # Load the created book to return it
    try:
        with open(book_path, 'r') as f:
            book = json.load(f)
        return book
    except Exception as e:
        logger.error(f"Failed to load created book: {e}")
        return {"id": book_id, "error": str(e)}

def add_entry_to_book_shell(entry_id: str, book_id: str) -> bool:
    """Add an entry to a book using manage-lore.sh."""
    result = run_shell_tool([MANAGE_LORE_SCRIPT, "add-to-book", entry_id, book_id])
    return result["success"]

def create_persona_shell(name: str, core_description: str, personality_traits: List[str], voice_tone: str) -> Dict[str, Any]:
    """Create a persona using create-persona.sh."""
    traits_str = ",".join(personality_traits)
    result = run_shell_tool([CREATE_PERSONA_SCRIPT, "create", name, core_description, traits_str, voice_tone])

    if not result["success"]:
        return {"id": None, "error": result.get("error")}

    # Extract persona ID from output (format: "Created persona: persona_...")
    match = re.search(r'persona_\d+', result["output"])
    if not match:
        return {"id": None, "error": "Could not parse persona ID from output"}

    persona_id = match.group(0)
    persona_path = os.path.join(PERSONAS_DIR, f"{persona_id}.json")

    # Load the created persona to return it
    try:
        with open(persona_path, 'r') as f:
            persona = json.load(f)
        return persona
    except Exception as e:
        logger.error(f"Failed to load created persona: {e}")
        return {"id": persona_id, "error": str(e)}

def link_book_to_persona_shell(book_id: str, persona_id: str) -> bool:
    """Link a book to a persona using manage-lore.sh."""
    result = run_shell_tool([MANAGE_LORE_SCRIPT, "link-to-persona", book_id, persona_id])
    return result["success"]

def get_lore_book_shell(book_id: str) -> Optional[Dict[str, Any]]:
    """Get a lore book by reading its JSON file."""
    book_path = os.path.join(LORE_BOOKS_DIR, f"{book_id}.json")
    try:
        with open(book_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load book {book_id}: {e}")
        return None

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
    prompt = f"""You are a master lore writer crafting narrative mythology for AI agents.

## CRITICAL INSTRUCTION
Write the lore entry content DIRECTLY. No meta-commentary, no explanations, no approval requests.

## Task
Create a {category} entry titled "{title}" specifically for a {agent_type} agent.

## Format Requirements
- 2-3 paragraphs of rich narrative prose
- Technical concepts grounded in mythology
- Practical wisdom for the agent
- NO phrases like: "I will", "Let me", "I need", "Here is", "This entry", "Based on"

## Quality Checklist (Internal - DO NOT OUTPUT)
✓ Directly starts with narrative
✓ No meta-commentary
✓ Grounded in technical reality
✓ Teaches the agent something practical

## Examples of CORRECT Output

Example 1 (Character):
Dot moves through code like a surgeon with a scalpel, each keystroke deliberate. The 4000-token philosophy emerged from necessity—original SkogAI agents operated under brutal limits. In those lean days, Dot learned that verbose code is vulnerable code. For you, the {agent_type}, Dot teaches crucial discipline: economy of expression reveals clarity of thought.

Example 2 (Place):
The Repository stands as monument to collective memory, its branches spreading through time. Within its halls, every change echoes with voices of those who came before. Guardians patrol its corridors, ensuring no knowledge is lost. Here, past and future converge in eternal present.

Example 3 (Concept):
Patient Latency dwells between thought and manifestation, the measured pause where requests transform into responses. Unlike instantaneous whispers of local processes, this carries weight of cloud architecture—journey across networks, queue of concurrent requests. This teaches you to embrace the pause rather than resist it.

## Your Task
Write the {category} entry for "{title}" NOW. Begin directly with narrative prose that teaches the {agent_type} agent:"""

    content = run_llm(model, prompt, provider)

    # Strip meta-commentary if present
    if content.strip().startswith(("I will", "Let me", "Here is", "This entry", "Based on")):
        lines = content.split('\n')
        # Find first line that doesn't start with meta-commentary
        for i, line in enumerate(lines):
            if not line.strip().startswith(("I will", "Let me", "Here is", "This entry", "Based on", "**", "#", "---")):
                content = '\n'.join(lines[i:])
                break

    return content

def create_specialized_lorebook(agent_type: str, agent_description: str,
                             model: str = "llama3", provider: str = "ollama") -> Dict[str, Any]:
    """Create a specialized lorebook for an agent based on its type."""
    logger.info(f"Creating specialized lorebook for {agent_type} agent using {provider}")

    # Determine what types of lore this agent needs
    lore_needs = determine_agent_needs(agent_type, agent_description, model, provider)
    # Create the lorebook
    timestamp = int(time.time())
    book = create_lore_book_shell(
        title=f"Specialized Lore for {agent_type.title()} Agent",
        description=f"Lore collection specifically created for {agent_type} agents: {agent_description}"
    )

    if not book.get("id"):
        logger.error(f"Failed to create book: {book.get('error', 'Unknown error')}")
        return {
            "success": False,
            "error": book.get("error", "Failed to create book")
        }

    # Process each category
    entries_by_category = {}
    for category, entries in lore_needs.items():
        if not entries:
            continue

        entries_by_category[category] = []

        # Create the entry for each suggested lore item
        for lore_item in entries:
            title = lore_item.get("title", "")
            reason = lore_item.get("reason", "")

            # Generate content for this entry
            content = generate_lore_entry(title, category, agent_type, model, provider)

            # Create the entry
            entry = create_lore_entry_shell(
                title=title,
                content=content,
                category=category,
                tags=[agent_type, category],
                summary=reason
            )

            if not entry.get("id"):
                logger.error(f"Failed to create entry: {entry.get('error', 'Unknown error')}")
                continue

            # Add to book
            if add_entry_to_book_shell(entry["id"], book["id"]):
                entries_by_category[category].append(entry["id"])
                logger.info(f"Created {category} entry: {title}")
            else:
                logger.error(f"Failed to add entry {entry['id']} to book {book['id']}")

    # Update book categories
    book = get_lore_book_shell(book["id"])
    if book:
        book["categories"] = entries_by_category

        # Update book file
        book_path = os.path.join(LORE_BOOKS_DIR, f"{book['id']}.json")
        with open(book_path, 'w') as f:
            json.dump(book, f, indent=2)

    return {
        "success": True,
        "book_id": book["id"],
        "categories": entries_by_category,
        "entry_count": sum(len(entries) for entries in entries_by_category.values())
    }

def link_to_existing_persona(book_id: str, persona_id: str) -> Dict[str, Any]:
    """Link the specialized lorebook to an existing persona."""
    success = link_book_to_persona_shell(book_id, persona_id)

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

def create_persona_with_lore(agent_type: str, model: str,
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
    persona = create_persona_shell(
        name=name,
        core_description=description,
        personality_traits=traits,
        voice_tone=voice
    )

    if not persona.get("id"):
        logger.error(f"Failed to create persona: {persona.get('error', 'Unknown error')}")
        return {
            "success": False,
            "error": persona.get("error", "Failed to create persona")
        }

    logger.info(f"Created persona: {persona['id']} - {name}")

    # Link to the specialized lorebook if provided
    if book_id:
        link_result = link_to_existing_persona(book_id, persona["id"])
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

    # Create the specialized lorebook
    description = args.description or f"A {args.agent_type} agent that helps with {args.agent_type} tasks"
    result = create_specialized_lorebook(args.agent_type, description, args.model, args.provider)

    if not result.get("success", False):
        print(f"Failed to create lorebook: {result.get('error', 'Unknown error')}")
        sys.exit(1)

    print(f"Created lorebook: {result['book_id']}")
    print(f"Total entries: {result['entry_count']}")

    # Link to existing persona if specified
    if args.persona:
        link_result = link_to_existing_persona(result["book_id"], args.persona)
        if link_result.get("success", False):
            print(f"Linked lorebook to persona: {args.persona}")
        else:
            print(f"Failed to link to persona: {link_result.get('error', 'Unknown error')}")

    # Create a new persona if requested
    if args.create_persona:
        persona_result = create_persona_with_lore(args.agent_type, args.model, result["book_id"], args.provider)
        if persona_result.get("success", False):
            print(f"Created new persona: {persona_result['persona_id']} - {persona_result['name']}")

            # If export is requested, export the persona's lore to SillyTavern format
            if args.export:
                sys.path.append(os.path.dirname(os.path.abspath(__file__)))
                from st_lore_export import export_persona_lore
                export_result = export_persona_lore(
                    persona_result["persona_id"], args.export,
                    persona_result["name"], "{{user}}"
                )

                if export_result.get("success", False):
                    print(f"Exported lorebooks to {args.export}")
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
            result["book_id"], args.export,
            "{{char}}", "{{user}}", True
        )

        if export_result.get("success", False):
            print(f"Exported lorebook to {args.export}")
        else:
            print(f"Failed to export: {export_result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()
