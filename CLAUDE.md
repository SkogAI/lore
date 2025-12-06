# Lore - Digital Mythology Generation System

A multi-agent system that generates narrative lore entries stored as JSON files, organized into books and linked to AI personas.

## What Gets Created

The system outputs structured JSON data stored in `knowledge/expanded/lore/`:

**Entries:** `knowledge/expanded/lore/entries/entry_<timestamp>_<hash>.json`
- Individual narrative pieces
- Contains: id, title, content (the actual story/narrative), category, tags, metadata
- Used as building blocks for lore books

**Books:** `knowledge/expanded/lore/books/book_<timestamp>_<hash>.json`
- Collections of related entries
- Contains: id, title, description, entries[] (list of entry IDs), readers[] (persona IDs), structure
- Used to organize entries by theme/persona/topic

**Personas:** `knowledge/expanded/personas/persona_<timestamp>.json`
- AI character profiles with unique voices
- Contains: id, name, role, traits, background, voice characteristics
- Used to generate content with consistent character perspective

**Current Data:**
- 88 books
- 300+ entries
- 73 personas

## How It Works

1. **Agent System (`agents/`)** - Creates content via LLMs
   - `api/agent_api.py` - Calls OpenRouter for research/outline/writing
   - `api/lore_api.py` - CRUD operations for books/entries/personas
   - `implementations/` - Prompt templates for different agent types

2. **Orchestrator (`orchestrator/`)** - Coordinates agents
   - Loads numbered knowledge modules (00=core, 10-89=expanded)
   - Builds prompts with appropriate context
   - Routes requests to specialized agents

3. **CLI (`Argcfile.sh`)** - Direct access to data
   - `argc list-books` - Show all 88 books
   - `argc show-book <id>` - Display book metadata
   - `argc read-book-entries <id>` - Output all entries in a book
   - `argc create-entry/create-book` - Add new data

## Directory Structure

```
@agents/               Multi-agent content creation
  @agents/api/         LLM wrappers and data management
  @agents/implementations/  Agent templates
  @agents/templates/   Base templates

@knowledge/            Data storage
  @knowledge/core/     Schemas (00-09)
  @knowledge/expanded/lore/books/     → 88 JSON book files
  @knowledge/expanded/lore/entries/   → 300+ JSON entry files
  @knowledge/expanded/personas/       → 73 JSON persona files

@orchestrator/         Central coordinator
  @orchestrator/orchestrator.py       Main logic
  @orchestrator/identity/             System prompts
  @orchestrator/variants/             Operation modes

@integration/          Automation workflows
@context/             Session state (archive/current/templates)
@scripts/             Pre-commit validation
```

## What It's Used For

**Content Generation Pipeline:**
1. Agent receives topic/request
2. Generates narrative in persona voice
3. Creates entry JSON with content
4. Adds entry to persona's chronicle book
5. Data persists as JSON for future use

**Practical Use:**
- Transform code commits into narrative lore (via integration/)
- Build character-driven documentation
- Create interconnected story universes
- Generate consistent character voices across content

## Environment Requirements

```bash
export OPENROUTER_API_KEY="sk-or-v1-..."  # Required for agent_api.py
```

## Path Standards

All code uses relative paths via `Path(__file__).parent` pattern:

```python
repo_root = Path(__file__).parent.parent
books_dir = repo_root / "knowledge" / "expanded" / "lore" / "books"
```

```bash
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
entries_dir="$REPO_ROOT/knowledge/expanded/lore/entries"
```

Validation: `./scripts/pre-commit/validate.sh`
