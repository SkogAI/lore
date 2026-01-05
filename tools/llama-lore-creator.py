#!/usr/bin/env python3
"""Generate lore content using LLM providers."""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

SKOGAI_DIR = Path(__file__).parent.parent
ENTRIES_DIR = SKOGAI_DIR / "knowledge/expanded/lore/entries"
BOOKS_DIR = SKOGAI_DIR / "knowledge/expanded/lore/books"
PERSONAS_DIR = SKOGAI_DIR / "knowledge/expanded/personas"

# Meta-commentary patterns to detect/remove
# These are common phrases LLMs use instead of direct content
META_PATTERNS = [
    r'^\s*(I will|Let me|Here is|Here\'s|This entry|This is)',
    r'^\s*(I need your|should I|would you like|First,? I|Now,? I)',
    r'^\s*(I\'ve created|I have created|As requested|Based on your request)'
]



def run_llm(prompt: str, provider: str, model: str) -> str:
    """Run LLM with specified provider."""
    if provider == "claude":
        result = subprocess.run(
            ["claude", "--print", prompt],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"Claude CLI error (code {result.returncode}): {result.stderr}", file=sys.stderr)
        output = result.stdout.strip()
        if not output:
            print(f"Claude CLI returned empty response. stderr: {result.stderr}", file=sys.stderr)
        return output
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


def validate_lore_output(content: str) -> bool:
    """Validate lore output for meta-commentary."""
    errors = []
    
    # Check for meta-commentary patterns anywhere in content
    for pattern in META_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
            errors.append("⚠️  Contains meta-commentary")
            break
    
    # Check minimum length
    word_count = len(content.split())
    if word_count < 100:
        errors.append(f"⚠️  Too short ({word_count} words, recommended 100+)")
    
    # Report
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return False
    
    print("✅ Lore content validated", file=sys.stderr)
    return True


def strip_meta_commentary(content: str) -> str:
    """Strip meta-commentary from content."""
    lines = content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Check if line matches any meta-commentary pattern
        is_meta = False
        for pattern in META_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                is_meta = True
                break
        
        if not is_meta:
            cleaned_lines.append(line)
    
    # Join and remove leading empty lines
    cleaned = '\n'.join(cleaned_lines).lstrip()
    return cleaned



def get_latest_file(directory: Path) -> str:
    """Get the most recently created file in directory."""
    files = list(directory.glob("*.json"))
    if not files:
        return None
    latest = max(files, key=lambda f: f.stat().st_mtime)
    return latest.stem


def generate_entry(title: str, category: str, provider: str, model: str) -> str:
    """Generate a lore entry."""
    print(f"Generating lore entry: {title} ({category})")
    
    max_retries = 2
    attempt = 0

    prompt = f"""You are a master lore writer crafting narrative mythology.

CRITICAL RULES - READ CAREFULLY:
1. Write ONLY the lore content - NO meta-commentary whatsoever
2. DO NOT write: "I will", "Let me", "Here is", "This entry", "I need", "Should I"
3. DO NOT ask for approval or permission
4. DO NOT explain what you're doing
5. START IMMEDIATELY with narrative prose

TASK: Write a {category} entry titled "{title}"

REQUIRED FORMAT:
- 2-3 paragraphs of rich narrative prose
- Present tense, immersive storytelling
- Mythological/fantastical tone
- 150-300 words total

CORRECT EXAMPLES:

Example 1 (Character):
In the depths of the digital realm, the Architect moves through layers of abstraction with purpose. Her fingers dance across interfaces, weaving patterns that bridge the gap between thought and execution. Those who witness her work speak of an uncanny ability to see the invisible structures that bind systems together. She carries the weight of countless failed experiments, each one a lesson etched into her methodology.

Example 2 (Place):
The Repository stands as a monument to collective memory, its branches spreading like roots through time. Within its halls, every change echoes with the voices of those who came before. Guardians patrol its corridors, ensuring that no knowledge is lost, no pattern forgotten. Here, the past and future converge in an eternal present.

Example 3 (Event):
The Great Refactoring began at midnight when the old systems could no longer bear their complexity. For three cycles, the architects labored, dismantling monoliths and rebuilding them as elegant patterns. When dawn broke, the realm had transformed—simpler, stronger, ready for what came next.

BEGIN YOUR ENTRY NOW (narrative prose only, no preamble)"""

    # Retry loop for generating valid content
    while attempt < max_retries:
        attempt += 1
        
        if attempt > 1:
            print(f"Retry attempt {attempt}/{max_retries}...")

        content = run_llm(prompt, provider, model)

        # Validate and clean content
        if validate_lore_output(content):
            # Content is valid, break out of retry loop
            break
        else:
            print(f"⚠️  Validation failed on attempt {attempt}, cleaning content...")
            content = strip_meta_commentary(content)
            
            # Re-validate after cleaning
            if validate_lore_output(content):
                print("✅ Content cleaned successfully")
                break
            elif attempt >= max_retries:
                print("⚠️  Max retries reached. Using best available content.")

    # Create entry using manage-lore.sh
    subprocess.run(
        [str(SKOGAI_DIR / "tools/manage-lore.sh"), "create-entry", title, category],
        check=True
    )

    # Get the new entry ID
    entry_id = get_latest_file(ENTRIES_DIR)
    entry_path = ENTRIES_DIR / f"{entry_id}.json"

    # Update with generated content
    with open(entry_path) as f:
        entry = json.load(f)

    entry["content"] = content
    entry["summary"] = f"Generated by {model}"

    with open(entry_path, "w") as f:
        json.dump(entry, f, indent=2)

    print(f"Created lore entry: {entry_id}")
    return entry_id


def generate_persona(name: str, description: str, provider: str, model: str) -> str:
    """Generate a persona with traits and voice."""
    print(f"Generating persona: {name}")

    prompt = f"""Generate personality traits and voice characteristics for a character named '{name}' who is '{description}'.

CRITICAL RULES:
1. Output ONLY the formatted response below
2. NO meta-commentary, explanations, or preamble
3. START IMMEDIATELY with "TRAITS:"

REQUIRED FORMAT:
TRAITS: trait1,trait2,trait3,trait4
VOICE: concise description of voice and speaking style

FORMATTING RULES:
- Traits: comma-separated, no spaces after commas
- Voice: 5-10 words describing speaking style
- Must start with exactly "TRAITS:" on first line

BEGIN OUTPUT NOW:"""

    response = run_llm(prompt, provider, model)

    # Parse response
    traits = "mysterious,magical,enigmatic,wise"
    voice = "eloquent and mystical"

    for line in response.split("\n"):
        line = line.strip()
        if line.upper().startswith("TRAITS:"):
            traits = line.split(":", 1)[1].strip()
        elif line.upper().startswith("VOICE:"):
            voice = line.split(":", 1)[1].strip()

    # Create persona
    subprocess.run(
        [str(SKOGAI_DIR / "tools/create-persona.sh"), "create", name, description, traits, voice],
        check=True
    )

    persona_id = get_latest_file(PERSONAS_DIR)
    print(f"Created persona: {persona_id}")
    return persona_id


def generate_lorebook(title: str, description: str, entry_count: int, provider: str, model: str) -> str:
    """Generate a lorebook with entries."""
    print(f"Generating lorebook: {title}")
    print(f"Number of entries: {entry_count}")

    # Create the book
    subprocess.run(
        [str(SKOGAI_DIR / "tools/manage-lore.sh"), "create-book", title, description],
        check=True
    )

    book_id = get_latest_file(BOOKS_DIR)

    # Generate entry ideas
    prompt = f"""Generate {entry_count} unique and interesting lore entry titles for a fantasy/sci-fi world called '{title}'. {description}

CRITICAL RULES:
1. Output ONLY the numbered list below
2. NO meta-commentary, explanations, or preamble
3. START IMMEDIATELY with "1."

REQUIRED FORMAT:
1. [Category: place] The Crystal Caverns
2. [Category: character] Elder Moonwhisper
3. [Category: event] The Great Sundering

FORMATTING RULES:
- Categories MUST be: place, character, object, event, or concept
- Each line: number, category in brackets, title
- No blank lines or extra text

BEGIN LIST NOW:"""

    response = run_llm(prompt, provider, model)

    # Debug: show what we got
    if os.environ.get("DEBUG"):
        print(f"LLM Response:\n{response}\n---")

    # Parse entries - be flexible with format
    entries_created = 0
    for line in response.split("\n"):
        line = line.strip()
        if not line:
            continue

        # Match numbered lines
        match = re.match(r'^\d+\.\s*(.+)$', line)
        if not match:
            continue

        entry_text = match.group(1)

        # Extract category
        category = "custom"
        cat_match = re.search(r'\[Category:\s*([^\]]+)\]', entry_text, re.IGNORECASE)
        if cat_match:
            category = cat_match.group(1).strip().lower()
            # Remove category from title
            entry_title = re.sub(r'\[Category:\s*[^\]]+\]\s*', '', entry_text).strip()
        else:
            entry_title = entry_text

        if not entry_title:
            continue

        # Generate the entry
        entry_id = generate_entry(entry_title, category, provider, model)

        # Add to book
        subprocess.run(
            [str(SKOGAI_DIR / "tools/manage-lore.sh"), "add-to-book", entry_id, book_id],
            check=True
        )

        entries_created += 1
        print(f"Added entry '{entry_title}' to book")

    print(f"Lorebook {book_id} created with {entries_created} entries")
    return book_id


def link_persona_with_lore(persona_id: str, book_count: int, provider: str, model: str):
    """Link a persona with lore books."""
    # Get existing books
    result = subprocess.run(
        [str(SKOGAI_DIR / "tools/manage-lore.sh"), "list-books"],
        capture_output=True,
        text=True
    )

    books = re.findall(r'(book_[0-9_a-f]+)', result.stdout)[:book_count]

    # Generate more if needed
    if len(books) < book_count:
        # Get persona name
        result = subprocess.run(
            [str(SKOGAI_DIR / "tools/create-persona.sh"), "show", persona_id],
            capture_output=True,
            text=True
        )

        persona_name = "Unknown"
        for line in result.stdout.split("\n"):
            if "Persona:" in line:
                persona_name = line.split("Persona:")[1].strip().replace("===", "").strip()
                break

        new_book_id = generate_lorebook(
            f"{persona_name}'s Chronicles",
            f"A collection of lore relevant to {persona_name}",
            3,
            provider,
            model
        )
        books.append(new_book_id)

    # Link books
    for book_id in books:
        subprocess.run(
            [str(SKOGAI_DIR / "tools/manage-lore.sh"), "link-to-persona", book_id, persona_id],
            check=True
        )
        print(f"Linked book {book_id} to persona {persona_id}")


def main():
    parser = argparse.ArgumentParser(description="Generate lore content using LLM")
    parser.add_argument("command", choices=["entry", "persona", "lorebook", "link"],
                       help="Command to run")
    parser.add_argument("args", nargs="*", help="Command arguments")
    parser.add_argument("--provider", default=os.environ.get("LLM_PROVIDER", "ollama"),
                       help="LLM provider (ollama, claude, openai)")
    parser.add_argument("--model", default="llama3",
                       help="Model name for ollama/openai")

    args = parser.parse_args()

    if args.command == "entry":
        if len(args.args) < 2:
            print("Usage: entry <title> <category>")
            sys.exit(1)
        generate_entry(args.args[0], args.args[1], args.provider, args.model)

    elif args.command == "persona":
        if len(args.args) < 2:
            print("Usage: persona <name> <description>")
            sys.exit(1)
        generate_persona(args.args[0], args.args[1], args.provider, args.model)

    elif args.command == "lorebook":
        if len(args.args) < 2:
            print("Usage: lorebook <title> <description> [count]")
            sys.exit(1)
        count = int(args.args[2]) if len(args.args) > 2 else 3
        generate_lorebook(args.args[0], args.args[1], count, args.provider, args.model)

    elif args.command == "link":
        if len(args.args) < 1:
            print("Usage: link <persona_id> [book_count]")
            sys.exit(1)
        count = int(args.args[1]) if len(args.args) > 1 else 1
        link_persona_with_lore(args.args[0], count, args.provider, args.model)


if __name__ == "__main__":
    main()
