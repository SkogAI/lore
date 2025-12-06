#!/usr/bin/env python3
"""
SkogAI Orchestrator - Creates starting data and coordinates existing tools.

1. Creates session context
2. Loads and categorizes numbered knowledge
3. Builds prompts for LLM tasks
4. Calls existing shell tools
"""

import os
import sys
import json
import time
import subprocess
import re
from typing import Dict, Any, List, Optional

SKOGAI_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Knowledge category definitions
KNOWLEDGE_CATEGORIES = {
    "core": (0, 9),        # Emergency/critical
    "navigation": (10, 19),
    "identity": (20, 29),
    "operational": (30, 99),
    "standards": (100, 199),
    "project": (200, 299),
    "tools": (300, 399),
    "frameworks": (1000, 9999),
}


def categorize_knowledge(knowledge: Dict[str, str]) -> Dict[str, Dict[str, str]]:
    """Sort knowledge files into categories by number prefix."""
    categorized = {cat: {} for cat in KNOWLEDGE_CATEGORIES}

    for filename, content in knowledge.items():
        # Extract number from filename
        match = re.match(r'^(\d+)', filename)
        if not match:
            continue

        num = int(match.group(1))

        # Find category
        for cat_name, (low, high) in KNOWLEDGE_CATEGORIES.items():
            if low <= num <= high:
                categorized[cat_name][filename] = content
                break

    return categorized


def build_prompt(task_type: str, knowledge: Dict[str, str],
                 persona: Optional[Dict] = None, topic: str = "") -> str:
    """Build LLM prompt based on task type, knowledge, and persona."""

    # Categorize knowledge
    categorized = categorize_knowledge(knowledge)

    # Start with core knowledge (always included)
    prompt_parts = []

    # System context from core
    if categorized["core"]:
        prompt_parts.append("## Core System Context")
        for filename, content in categorized["core"].items():
            prompt_parts.append(f"### {filename}\n{content[:500]}...")

    # Task-specific sections
    if task_type == "lore":
        prompt_parts.append("\n## Task: Generate Lore")
        prompt_parts.append("Create rich, evocative lore entries that fit the SkogAI universe.")

        if categorized["tools"]:
            prompt_parts.append("\n## Available Tools")
            for filename, content in categorized["tools"].items():
                prompt_parts.append(f"### {filename}\n{content[:300]}...")

    elif task_type == "content":
        prompt_parts.append("\n## Task: Generate Content")
        prompt_parts.append("Create well-structured content following the workflow phases.")

        if categorized["standards"]:
            prompt_parts.append("\n## Standards")
            for filename, content in categorized["standards"].items():
                prompt_parts.append(f"### {filename}\n{content[:300]}...")

    elif task_type == "research":
        prompt_parts.append("\n## Task: Research")
        prompt_parts.append("Gather and analyze information, identify key facts and concepts.")

    # Add persona voice if provided
    if persona:
        prompt_parts.append(f"\n## Voice: {persona.get('name', 'Agent')}")
        prompt_parts.append(f"Tone: {persona.get('voice', {}).get('tone', 'neutral')}")
        traits = persona.get('core_traits', {}).get('values', [])
        if traits:
            prompt_parts.append(f"Traits: {', '.join(traits)}")

    # Add topic
    if topic:
        prompt_parts.append(f"\n## Topic\n{topic}")

    return "\n\n".join(prompt_parts)


def load_persona(persona_id: str) -> Optional[Dict]:
    """Load persona from JSON file."""
    persona_path = os.path.join(
        SKOGAI_DIR, "knowledge/expanded/personas", f"{persona_id}.json"
    )
    if os.path.exists(persona_path):
        with open(persona_path, 'r') as f:
            return json.load(f)
    return None


def load_numbered_knowledge(numbers: List[str]) -> Dict[str, str]:
    """Load knowledge files by number prefix from goose-memory-backup."""
    knowledge_base = os.path.join(
        SKOGAI_DIR, "lorefiles/skogai/current/goose-memory-backup"
    )
    knowledge = {}

    if not os.path.exists(knowledge_base):
        return knowledge

    for filename in sorted(os.listdir(knowledge_base)):
        for num in numbers:
            if filename.startswith(num):
                filepath = os.path.join(knowledge_base, filename)
                with open(filepath, 'r') as f:
                    knowledge[filename] = f.read()
                break

    return knowledge


def create_context(task_type: str = "content") -> Dict[str, Any]:
    """Create a new session context with loaded knowledge."""
    session_id = str(int(time.time()))

    # Knowledge mapping
    knowledge_map = {
        "content": ["00", "10", "20", "101"],
        "lore": ["00", "10", "300", "303"],
        "research": ["00", "10", "02"],
    }

    numbers = knowledge_map.get(task_type, ["00", "10"])
    knowledge = load_numbered_knowledge(numbers)

    context = {
        "session_id": session_id,
        "created": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "system_state": {
            "orchestrator_mode": task_type,
            "memory_priority": "core"
        },
        "active_knowledge": list(knowledge.keys())
    }

    # Save context
    context_dir = os.path.join(SKOGAI_DIR, "context/current")
    os.makedirs(context_dir, exist_ok=True)

    with open(os.path.join(context_dir, f"context-{session_id}.json"), 'w') as f:
        json.dump(context, f, indent=2)

    return {"context": context, "knowledge": knowledge}


def call_tool(tool_name: str, *args) -> str:
    """Call existing shell tool."""
    tool_path = os.path.join(SKOGAI_DIR, "tools", tool_name)
    result = subprocess.run([tool_path] + list(args), capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else result.stderr


# Wrappers for existing tools
def create_persona(name, description, traits, voice):
    return call_tool("create-persona.sh", "create", name, description, traits, voice)

def create_entry(title, category):
    return call_tool("manage-lore.sh", "create-entry", title, category)

def create_book(title, description=""):
    return call_tool("manage-lore.sh", "create-book", title, description)

def add_to_book(entry_id, book_id):
    return call_tool("manage-lore.sh", "add-to-book", entry_id, book_id)

def link_to_persona(book_id, persona_id):
    return call_tool("manage-lore.sh", "link-to-persona", book_id, persona_id)


def prepare_task(task_type: str, topic: str = "", persona_id: str = None) -> Dict[str, Any]:
    """
    Prepare a complete task with context, knowledge, and prompt.

    Returns everything needed for LLM execution.
    """
    # Create context and load knowledge
    result = create_context(task_type)
    context = result["context"]
    knowledge = result["knowledge"]

    # Load persona if specified
    persona = None
    if persona_id:
        persona = load_persona(persona_id)

    # Categorize knowledge
    categorized = categorize_knowledge(knowledge)

    # Build prompt
    prompt = build_prompt(task_type, knowledge, persona, topic)

    # Update context with preparation details
    context["prepared"] = {
        "topic": topic,
        "persona_id": persona_id,
        "categories": {k: list(v.keys()) for k, v in categorized.items() if v}
    }

    # Save updated context
    context_file = os.path.join(
        SKOGAI_DIR, "context/current", f"context-{context['session_id']}.json"
    )
    with open(context_file, 'w') as f:
        json.dump(context, f, indent=2)

    return {
        "context": context,
        "knowledge": knowledge,
        "categorized": categorized,
        "prompt": prompt,
        "persona": persona
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python orchestrator.py init [content|lore|research]")
        print("  python orchestrator.py prepare <type> <topic> [persona_id]")
        sys.exit(1)

    if sys.argv[1] == "init":
        task_type = sys.argv[2] if len(sys.argv) > 2 else "content"
        result = create_context(task_type)
        print(f"Session: {result['context']['session_id']}")
        print(f"Knowledge: {result['context']['active_knowledge']}")

    elif sys.argv[1] == "prepare":
        task_type = sys.argv[2] if len(sys.argv) > 2 else "lore"
        topic = sys.argv[3] if len(sys.argv) > 3 else ""
        persona_id = sys.argv[4] if len(sys.argv) > 4 else None

        result = prepare_task(task_type, topic, persona_id)

        print(f"Session: {result['context']['session_id']}")
        print(f"\nCategories loaded:")
        for cat, files in result['categorized'].items():
            if files:
                print(f"  {cat}: {len(files)} files")

        print(f"\n--- PROMPT ---\n{result['prompt'][:1000]}")
        if len(result['prompt']) > 1000:
            print(f"... [{len(result['prompt']) - 1000} more chars]")
