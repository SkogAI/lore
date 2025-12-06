# Lore - Digital Mythology Generation System

A multi-agent system that generates narrative lore entries stored as JSON files, organized into books and linked to AI personas.

## Core Concepts

### Entry
**An entry is the atomic unit of lore** - a single piece of narrative content (character, place, event, object, concept).

- **Schema**: @knowledge/core/lore/schema.json
- **API Docs**: @docs/api/entry.md
- **Required fields**: `id`, `title`, `content`, `category`
- **Storage**: `knowledge/expanded/lore/entries/entry_<timestamp>.json`

The `content` field contains the actual narrative text in markdown format.

### Book
**A book is a collection of entries** organized by theme, persona, or topic.

- **Schema**: @knowledge/core/book-schema.json
- **API Docs**: @docs/api/book.md
- **Required fields**: `id`, `title`, `description`
- **Storage**: `knowledge/expanded/lore/books/book_<timestamp>_<hash>.json`

Books control access through `readers` (personas that can view) and `owners` (personas that can modify).

### Persona
**A persona is an AI character profile** with unique voice, traits, and characteristics used to generate consistent narrative content.

- **Schema**: @knowledge/core/persona/schema.json
- **API Docs**: @docs/api/persona.md
- **Required fields**: `id`, `name`, `core_traits`, `voice`
- **Storage**: `knowledge/expanded/personas/persona_<timestamp>.json`

Personas define `voice.tone`, personality `values`/`motivations`, and interaction style for content generation.

## What Gets Created

The system outputs structured JSON data in `knowledge/expanded/`:

**Entries:** `knowledge/expanded/lore/entries/entry_<timestamp>.json`
```json
{
  "id": "entry_1764992601",
  "title": "The Test Chronicle",
  "content": "In the depths of the digital realm...",
  "category": "lore",
  "tags": ["test", "chronicle"],
  "book_id": "book_1764992601",
  "metadata": {
    "created_by": "skogix",
    "created_at": "2025-12-06T03:43:21Z"
  }
}
```

**Books:** `knowledge/expanded/lore/books/book_<timestamp>.json`
```json
{
  "id": "book_1764992601",
  "title": "Test Chronicles",
  "description": "A collection of test entries",
  "entries": ["entry_1764992601"],
  "readers": ["persona_1764992753"],
  "metadata": {
    "created_by": "skogix",
    "created_at": "2025-12-06T03:43:21Z"
  }
}
```

**Personas:** `knowledge/expanded/personas/persona_<timestamp>.json`
```json
{
  "id": "persona_1764992753",
  "name": "Aria Nightwhisper",
  "voice": {
    "tone": "poetic yet precise"
  },
  "core_traits": {
    "values": ["methodical", "curious"],
    "motivations": ["patient", "detail-oriented"]
  }
}
```

**Current Data:**
- 89 books
- 301 entries
- 74 personas

## How to Use lore_api

### Basic Operations (Python)

```python
from agents.api.lore_api import LoreAPI

lore = LoreAPI()

# Create an entry
entry = lore.create_lore_entry(
    title="The Test Chronicle",
    content="In the depths of the digital realm...",
    category="lore",
    tags=["test", "chronicle"]
)
print(f"Created: {entry['id']}")
# Output: Created: entry_1764992601
# File: knowledge/expanded/lore/entries/entry_1764992601.json

# Create a book
book = lore.create_lore_book(
    title="Test Chronicles",
    description="A collection of test entries"
)
print(f"Created: {book['id']}")
# Output: Created: book_1764992601
# File: knowledge/expanded/lore/books/book_1764992601.json

# Link entry to book
lore.add_entry_to_book(entry['id'], book['id'])
# Updates both files with bidirectional link

# Create a persona
persona = lore.create_persona(
    name="Aria Nightwhisper",
    core_description="Digital archivist",
    personality_traits=["methodical", "curious", "patient", "detail-oriented"],
    voice_tone="poetic yet precise"
)
print(f"Created: {persona['id']}")
# Output: Created: persona_1764992753
# File: knowledge/expanded/personas/persona_1764992753.json

# Link persona to book
lore.link_book_to_persona(book['id'], persona['id'])
```

### What lore_api Actually Does

**Simple operations:**
1. Generates ID: `timestamp` or `timestamp_randomhex`
2. Creates JSON structure with required fields
3. Writes to file: `json.dump(data, file)`
4. Returns the created object

**Linking operations:**
1. Reads two JSON files
2. Updates arrays: `book["entries"].append(entry_id)`
3. Writes both files back

**No magic - just file I/O with JSON.**

## How to Use agent_api

```python
from agents.api.agent_api import AgentAPI

agent = AgentAPI()

# Generate content with LLM (requires OPENROUTER_API_KEY)
result = agent.process_agent_request(
    agent_type="research",
    input_data={"topic": "quantum computing"},
    session_id="1234"
)

# Result saved to: demo/content_creation_1234/research_output.json
print(result)
```

### What agent_api Actually Does

**NOT data creation - just LLM calls:**
1. Builds prompt from agent templates
2. Calls OpenRouter API (GPT-4, etc.)
3. Returns LLM response as JSON
4. Saves to `demo/content_creation_<session>/` (temporary)

**agent_api generates content (text)**
**lore_api creates data (files)**

These are separate concerns.

## Integration with jq CRUD System

The lore system integrates with skogai's standard jq CRUD operations (`@scripts/jq/`):

```bash
# Read a book's title
jq -f scripts/jq/crud-get/transform.jq \
  --arg path "title" \
  knowledge/expanded/lore/books/book_1764992601.json

# Update an entry's content
jq -f scripts/jq/crud-set/transform.jq \
  --arg path "content" \
  --arg value "Updated narrative..." \
  knowledge/expanded/lore/entries/entry_1764992601.json > tmp.json
mv tmp.json knowledge/expanded/lore/entries/entry_1764992601.json

# Add a tag to an entry
jq '.tags += ["new-tag"]' \
  knowledge/expanded/lore/entries/entry_1764992601.json > tmp.json
mv tmp.json knowledge/expanded/lore/entries/entry_1764992601.json
```

**The jq CRUD system is the standard for JSON operations across all skogai projects.**

## CLI Access

Use `Argcfile.sh` for command-line operations:

```bash
# List all books
argc list-books

# Show a specific book
argc show-book book_1764992601

# Read all entries in a book
argc read-book-entries book_1764992601

# Create new book
argc create-book --title "My Book" --description "Description"

# Create new entry
argc create-entry --title "My Entry" --content "Content..." --category lore
```

## Directory Structure

```
@agents/api/
  agent_api.py       - LLM API wrapper (generates content via OpenRouter)
  lore_api.py        - JSON file CRUD (creates books/entries/personas)

@knowledge/expanded/lore/
  books/             - 89 book JSON files
  entries/           - 301 entry JSON files

@knowledge/expanded/personas/
                     - 74 persona JSON files

@scripts/jq/         - Standard jq CRUD operations (used across skogai)
  crud-get/          - Get values from JSON
  crud-set/          - Set values in JSON
  crud-delete/       - Delete values from JSON

@orchestrator/       - Coordinates agents and knowledge
@integration/        - Automation workflows
@context/            - Session state
```

## Environment Requirements

```bash
# Required only for agent_api (LLM calls)
export OPENROUTER_API_KEY="sk-or-v1-..."

# Not required for lore_api (just file operations)
```

## Path Standards

All code uses relative paths:

```python
from pathlib import Path
repo_root = Path(__file__).parent.parent
books_dir = repo_root / "knowledge" / "expanded" / "lore" / "books"
```

```bash
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
books_dir="$REPO_ROOT/knowledge/expanded/lore/books"
```

Validation: `./scripts/pre-commit/validate.sh`
