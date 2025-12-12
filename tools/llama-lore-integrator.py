#!/usr/bin/env python3
"""Analyze and integrate existing content into the lore/persona system using LLM."""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

SKOGAI_DIR = Path(__file__).parent.parent
ENTRIES_DIR = SKOGAI_DIR / "knowledge/expanded/lore/entries"
BOOKS_DIR = SKOGAI_DIR / "knowledge/expanded/lore/books"
PERSONAS_DIR = SKOGAI_DIR / "knowledge/expanded/personas"


def run_llm(prompt: str, provider: str, model: str) -> str:
    """Run LLM with specified provider."""
    if provider == "claude":
        result = subprocess.run(
            ["claude", "-p", prompt],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    elif provider == "ollama":
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    elif provider == "openai":
        import requests
        api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("OPENROUTER_API_KEY")
        base_url = os.environ.get("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")

        response = requests.post(
            f"{base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 2048
            }
        )
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise ValueError(f"Unknown provider: {provider}")


def get_latest_file(directory: Path) -> str:
    """Get the most recently created file in directory."""
    files = list(directory.glob("*.json"))
    if not files:
        return None
    latest = max(files, key=lambda f: f.stat().st_mtime)
    return latest.stem


def extract_lore(file_path: str, output_format: str, provider: str, model: str) -> str:
    """Extract lore from a text file."""
    print(f"Analyzing file: {file_path}")

    path = Path(file_path)
    if not path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)

    # Read first 8000 chars
    content = path.read_text()[:8000]

    if output_format == "json":
        prompt = f"""Analyze the following text and extract structured lore information from it.

TEXT:
{content}

Extract lore entities as structured JSON. Include entries for characters, places, objects, events, or concepts mentioned in the text.

Format your response as valid JSON like this:
{{
  "entries": [
    {{
      "title": "Entity Name",
      "category": "character/place/object/event/concept",
      "summary": "Brief description",
      "content": "Detailed description based on text",
      "tags": ["tag1", "tag2"]
    }}
  ]
}}

Only include your JSON output, nothing else."""
    else:
        prompt = f"""Analyze the following text and extract lore information from it.

TEXT:
{content}

Extract 3-5 key lore elements (characters, places, objects, events, or concepts) mentioned in the text.

For each element, format your response like this:

## [CATEGORY: character/place/object/event/concept] TITLE
SUMMARY: Brief one-sentence description
CONTENT: 1-2 paragraphs of expanded details based on the text
TAGS: tag1, tag2, tag3

Be concise and focus on the most important lore elements."""

    result = run_llm(prompt, provider, model)
    print(result)
    return result


def create_entries_from_analysis(analysis: str, book_id: str = None):
    """Create lore entries from LLM analysis output."""

    # Try to parse as JSON first
    try:
        # Find JSON in the response
        json_match = re.search(r'\{[\s\S]*"entries"[\s\S]*\}', analysis)
        if json_match:
            data = json.loads(json_match.group())
            entries = data.get("entries", [])

            print("Processing JSON lore entries...")

            for entry in entries:
                title = entry.get("title", "")
                category = entry.get("category", "custom")
                summary = entry.get("summary", "")
                content = entry.get("content", "")
                tags = entry.get("tags", [])

                if not title:
                    continue

                # Create entry
                subprocess.run(
                    [str(SKOGAI_DIR / "tools/manage-lore.sh"), "create-entry", title, category],
                    check=True
                )

                entry_id = get_latest_file(ENTRIES_DIR)
                entry_path = ENTRIES_DIR / f"{entry_id}.json"

                # Update with content
                with open(entry_path) as f:
                    entry_data = json.load(f)

                entry_data["content"] = content
                entry_data["summary"] = summary
                entry_data["tags"] = tags if isinstance(tags, list) else [t.strip() for t in tags.split(",")]

                with open(entry_path, "w") as f:
                    json.dump(entry_data, f, indent=2)

                print(f"Created lore entry: {title} ({entry_id})")

                if book_id:
                    subprocess.run(
                        [str(SKOGAI_DIR / "tools/manage-lore.sh"), "add-to-book", entry_id, book_id],
                        check=True
                    )
                    print(f"Added entry to book: {book_id}")

            return
    except (json.JSONDecodeError, AttributeError):
        pass

    # Parse as markdown
    print("Processing Markdown lore entries...")

    # Split by ## headers
    sections = re.split(r'^## ', analysis, flags=re.MULTILINE)

    for section in sections:
        if not section.strip():
            continue

        lines = section.strip().split("\n")
        header = lines[0]

        # Extract category and title from header
        cat_match = re.search(r'\[(?:CATEGORY:\s*)?([^\]]+)\]', header, re.IGNORECASE)
        category = cat_match.group(1).strip().lower() if cat_match else "custom"

        # Remove category bracket from title
        title = re.sub(r'\[(?:CATEGORY:\s*)?[^\]]+\]\s*', '', header).strip()

        if not title:
            continue

        # Extract other fields
        summary = ""
        content = ""
        tags = []

        body = "\n".join(lines[1:])

        # Find SUMMARY
        sum_match = re.search(r'^SUMMARY:\s*(.+)$', body, re.MULTILINE)
        if sum_match:
            summary = sum_match.group(1).strip()

        # Find TAGS
        tags_match = re.search(r'^TAGS:\s*(.+)$', body, re.MULTILINE)
        if tags_match:
            tags = [t.strip() for t in tags_match.group(1).split(",")]

        # Find CONTENT
        content_match = re.search(r'^CONTENT:\s*(.+?)(?=^TAGS:|$)', body, re.MULTILINE | re.DOTALL)
        if content_match:
            content = content_match.group(1).strip()

        # Create entry
        subprocess.run(
            [str(SKOGAI_DIR / "tools/manage-lore.sh"), "create-entry", title, category],
            check=True
        )

        entry_id = get_latest_file(ENTRIES_DIR)
        entry_path = ENTRIES_DIR / f"{entry_id}.json"

        # Update with content
        with open(entry_path) as f:
            entry_data = json.load(f)

        entry_data["content"] = content
        entry_data["summary"] = summary
        entry_data["tags"] = tags

        with open(entry_path, "w") as f:
            json.dump(entry_data, f, indent=2)

        print(f"Created lore entry: {title} ({entry_id})")

        if book_id:
            subprocess.run(
                [str(SKOGAI_DIR / "tools/manage-lore.sh"), "add-to-book", entry_id, book_id],
                check=True
            )
            print(f"Added entry to book: {book_id}")


def create_persona_from_text(file_path: str, provider: str, model: str) -> str:
    """Create a persona from text analysis."""
    print(f"Creating persona from: {file_path}")

    path = Path(file_path)
    if not path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)

    content = path.read_text()[:8000]

    prompt = f"""Analyze the following text and extract information about a character or persona.

TEXT:
{content}

Based on this text, create a detailed persona profile with the following:

NAME: The character's name
DESCRIPTION: A brief description (1-2 sentences)
TRAITS: List 4-6 personality traits, comma-separated
VOICE: Description of their speaking style and voice
BACKGROUND: Their origin or background story
EXPERTISE: Areas of knowledge or skill, comma-separated
LIMITATIONS: Weaknesses or gaps in knowledge, comma-separated

Format your response exactly as shown above, with each field on a separate line."""

    response = run_llm(prompt, provider, model)

    # Parse response
    fields = {}
    for line in response.split("\n"):
        for field in ["NAME", "DESCRIPTION", "TRAITS", "VOICE", "BACKGROUND", "EXPERTISE", "LIMITATIONS"]:
            if line.upper().startswith(f"{field}:"):
                fields[field.lower()] = line.split(":", 1)[1].strip()

    name = fields.get("name", "Unknown")
    description = fields.get("description", "A mysterious character")
    traits = fields.get("traits", "mysterious,enigmatic")
    voice = fields.get("voice", "cryptic")

    if not name or name == "Unknown":
        print("Failed to extract persona name from text")
        sys.exit(1)

    # Create persona
    subprocess.run(
        [str(SKOGAI_DIR / "tools/create-persona.sh"), "create", name, description, traits, voice],
        check=True
    )

    persona_id = get_latest_file(PERSONAS_DIR)
    persona_path = PERSONAS_DIR / f"{persona_id}.json"

    # Update with additional fields
    with open(persona_path) as f:
        persona = json.load(f)

    if "background" in fields:
        persona["background"]["origin"] = fields["background"]
    if "expertise" in fields:
        persona["knowledge"]["expertise"] = [e.strip() for e in fields["expertise"].split(",")]
    if "limitations" in fields:
        persona["knowledge"]["limitations"] = [l.strip() for l in fields["limitations"].split(",")]

    with open(persona_path, "w") as f:
        json.dump(persona, f, indent=2)

    print(f"Created persona: {name} ({persona_id})")
    return persona_id


def analyze_connections(book_id: str, provider: str, model: str):
    """Analyze and create connections between entries in a book."""
    print(f"Analyzing connections in lorebook: {book_id}")

    book_path = BOOKS_DIR / f"{book_id}.json"
    if not book_path.exists():
        print(f"Error: Book not found: {book_id}")
        sys.exit(1)

    with open(book_path) as f:
        book = json.load(f)

    entry_ids = book.get("entries", [])

    # Gather entry data
    entry_data = []
    for entry_id in entry_ids:
        entry_path = ENTRIES_DIR / f"{entry_id}.json"
        if entry_path.exists():
            with open(entry_path) as f:
                entry = json.load(f)
            entry_data.append({
                "id": entry_id,
                "title": entry.get("title", ""),
                "category": entry.get("category", ""),
                "summary": entry.get("summary", "")
            })

    if not entry_data:
        print("No entries found in book")
        return

    # Format for prompt
    entries_text = "\n\n".join([
        f"ID: {e['id']}\nTITLE: {e['title']}\nCATEGORY: {e['category']}\nSUMMARY: {e['summary']}"
        for e in entry_data
    ])

    prompt = f"""Analyze these lore entries and identify meaningful connections between them:

{entries_text}

For each connection you find, format your response like this:

## CONNECTION
SOURCE: [entry_id of source]
TARGET: [entry_id of target]
RELATIONSHIP: [describe relationship type: part_of, located_in, created_by, opposes, allies_with, etc.]
DESCRIPTION: [1-2 sentences describing the connection]

Identify at least 3-5 meaningful connections."""

    response = run_llm(prompt, provider, model)

    # Parse connections
    connections = re.split(r'^## CONNECTION\s*$', response, flags=re.MULTILINE)

    for conn in connections:
        if not conn.strip():
            continue

        # Extract fields
        source = ""
        target = ""
        rel_type = ""
        description = ""

        for line in conn.split("\n"):
            line = line.strip()
            if line.upper().startswith("SOURCE:"):
                source = line.split(":", 1)[1].strip()
            elif line.upper().startswith("TARGET:"):
                target = line.split(":", 1)[1].strip()
            elif line.upper().startswith("RELATIONSHIP:"):
                rel_type = line.split(":", 1)[1].strip()
            elif line.upper().startswith("DESCRIPTION:"):
                description = line.split(":", 1)[1].strip()

        if not source or not target:
            continue

        # Update source entry with relationship
        source_path = ENTRIES_DIR / f"{source}.json"
        if source_path.exists():
            with open(source_path) as f:
                entry = json.load(f)

            if "relationships" not in entry:
                entry["relationships"] = []

            entry["relationships"].append({
                "target_id": target,
                "relationship_type": rel_type,
                "description": description
            })

            with open(source_path, "w") as f:
                json.dump(entry, f, indent=2)

            print(f"Added connection: {source} -> {target} ({rel_type})")
        else:
            print(f"Warning: Source entry not found: {source}")

    print("Connections analysis complete")


def import_directory(dir_path: str, book_title: str, book_description: str, provider: str, model: str):
    """Create a lorebook from a directory of files."""
    print(f"Creating lorebook from directory: {dir_path}")

    path = Path(dir_path)
    if not path.is_dir():
        print(f"Error: Directory not found: {dir_path}")
        sys.exit(1)

    # Create the book
    subprocess.run(
        [str(SKOGAI_DIR / "tools/manage-lore.sh"), "create-book", book_title, book_description],
        check=True
    )

    book_id = get_latest_file(BOOKS_DIR)

    # Process each text file
    for file_path in path.iterdir():
        if not file_path.is_file():
            continue

        # Check if it's a text file
        try:
            content = file_path.read_text()
        except:
            continue

        print(f"Analyzing file: {file_path.name}")

        # Extract lore
        analysis = extract_lore(str(file_path), "json", provider, model)

        # Create entries
        create_entries_from_analysis(analysis, book_id)

    # Analyze connections
    analyze_connections(book_id, provider, model)

    print(f"Lorebook creation complete: {book_id}")


def main():
    parser = argparse.ArgumentParser(description="Analyze and integrate content into lore system")
    parser.add_argument("command",
                       choices=["extract-lore", "create-entries", "create-persona",
                               "analyze-connections", "import-directory"],
                       help="Command to run")
    parser.add_argument("args", nargs="*", help="Command arguments")
    parser.add_argument("--provider", default=os.environ.get("LLM_PROVIDER", "ollama"),
                       help="LLM provider (ollama, claude, openai)")
    parser.add_argument("--model", default="llama3.2",
                       help="Model name for ollama/openai")

    args = parser.parse_args()

    if args.command == "extract-lore":
        if len(args.args) < 1:
            print("Usage: extract-lore <file> [json/lore]")
            sys.exit(1)
        fmt = args.args[1] if len(args.args) > 1 else "lore"
        extract_lore(args.args[0], fmt, args.provider, args.model)

    elif args.command == "create-entries":
        if len(args.args) < 1:
            print("Usage: create-entries <analysis> [book_id]")
            sys.exit(1)
        book_id = args.args[1] if len(args.args) > 1 else None
        create_entries_from_analysis(args.args[0], book_id)

    elif args.command == "create-persona":
        if len(args.args) < 1:
            print("Usage: create-persona <file>")
            sys.exit(1)
        create_persona_from_text(args.args[0], args.provider, args.model)

    elif args.command == "analyze-connections":
        if len(args.args) < 1:
            print("Usage: analyze-connections <book_id>")
            sys.exit(1)
        analyze_connections(args.args[0], args.provider, args.model)

    elif args.command == "import-directory":
        if len(args.args) < 3:
            print("Usage: import-directory <dir> <title> <description>")
            sys.exit(1)
        import_directory(args.args[0], args.args[1], args.args[2], args.provider, args.model)


if __name__ == "__main__":
    main()
