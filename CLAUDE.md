# Lore - Digital Mythology Generation System

A multi-agent system that generates narrative lore entries stored as JSON files, organized into books and linked to AI personas.

## Core Concepts

### Entry

**An entry is the atomic unit of lore** - a single piece of narrative content (character, place, event, object, concept).

- **Schema**: `@knowledge/core/lore/schema.json`
- **API Docs**: `@docs/api/entry.md`
- **Required fields**: `id`, `title`, `content`, `category`
- **Storage**: `knowledge/expanded/lore/entries/entry_<timestamp>.json`
- **Categories**: character, place, event, object, concept, custom

### Book

**A book is a collection of entries** organized by theme, persona, or topic.

**What makes a book more than a collection of entries is that the _context_ is bound by the place, time, persona, and themes that together create lore.**

- **Schema**: `@knowledge/core/book-schema.json`
- **API Docs**: `@docs/api/book.md`
- **Required fields**: `id`, `title`, `description`
- **Storage**: `knowledge/expanded/lore/books/book_<timestamp>_<hash>.json`
- **Access control**: `readers` (view) and `owners` (modify) arrays

### Persona

**A persona is an AI character profile** with unique voice, traits, and characteristics as well as their own backstory and motivations.

- **Schema**: `@knowledge/core/persona/schema.json`
- **API Docs**: `@docs/api/persona.md`
- **Required fields**: `id`, `name`, `core_traits`, `voice`
- **Storage**: `knowledge/expanded/personas/persona_<timestamp>.json`
- **Defines**: voice.tone, personality values/motivations, interaction style

## Quick Start

### Entry Operations

```bash
> argc

📚 Chronicles of the Digital Realm - A mystical toolkit for weaving digital legends

USAGE: argc <COMMAND>

COMMANDS:
  validate-entry       🔮 Validate entry schema yao [aliases: validate_entry]
  validate-book        🔮 Validate book schema yao [aliases: validate_book]
  validate-persona     🔮 Validate persona schema yao [aliases: validate_persona]
  list-books           🔮 List them books yao [aliases: list_books]
  show-book            🔮 Show them books yao [aliases: show_book]
  list-entries         🔮 List them entries yao [aliases: list_entries]
  show-entry           🔮 Show them entries yao [aliases: show_entry]
  read-book-entries    🔮 Read all entries in a book yao [aliases: read_book_entries]
  generate-from-docs   📜 Generate lore from markdown documents [aliases: gen-docs]
  generate-from-git    📜 Generate lore from git commit [aliases: gen-git]
  generate-from-stdin  📜 Generate lore from stdin (pipe content) [aliases: gen-stdin]
  queue-add            📋 Add item to generation queue [aliases: q-add]
  queue-list           📋 List queued items [aliases: q-list]
  queue-process        📋 Process queued items [aliases: q-process]
  queue-clear          📋 Clear queue [aliases: q-clear]
  create-entry         🔮 Create new entry yao [aliases: create_entry]
  create-book          🔮 Create new book yao [aliases: create_book]
  create-persona       🔮 Create new persona yao [aliases: create_persona]
  add-to-book          🔮 Add entry to book yao [aliases: add_to_book]
  link-to-persona      🔮 Link book to persona yao [aliases: link_to_persona]

ENVIRONMENTS:
  SKOGAI_DIR    path to yo skogai-folder! [default: /home/skogix/]
  LORE_SCRIPTS  path to yo skogai-folder! [default: /home/skogix/lore/tools]
  LORE_DIR      path to yo lore! [default: /home/skogix/lore/knowledge/expanded/lore]
  BOOKS_DIR     path to yo books! [default: /home/skogix/lore/knowledge/expanded/lore/books]
  ENTRIES_DIR   path to yo entries! [default: /home/skogix/lore/knowledge/expanded/lore/entries]
  PERSONA_DIR   path to yo persona! [default: /home/skogix/lore/knowledge/expanded/personas]
  LLM_OUTPUT    The output path [default: /dev/stdout]
```

## Integration Pipeline

**Location**: `@integration/lore-flow.sh`

Transforms work sessions (commits, logs, events) into narrative lore automatically.

### Usage

```bash
# Manual input
./integration/lore-flow.sh manual "Implemented quantum mojito mixer"

# From git commits
./integration/lore-flow.sh git-diff HEAD
./integration/lore-flow.sh git-diff HEAD~3

# From log file
./integration/lore-flow.sh log /path/to/agent-session.log
```

### Pipeline Steps

1. **Extract Content** - git diff, log file, or manual text
2. **Select Persona** - Map author → persona via `integration/persona-mapping.conf`
3. **Load Persona Context** - Voice, traits, lore books
4. **Generate Narrative** - LLM transforms technical → mythological
5. **Create & Store Lore** - Entry → book → persona links

### Persona Mapping

Edit `integration/persona-mapping.conf`:

```bash
# Git author → persona ID
skogix=persona_1744992765      # Amy Ravenwolf
other-author=persona_XXXXX

# Default narrator for unmapped authors
DEFAULT=persona_1763820091     # Village Elder
```

### What Gets Created

```bash
$ ./integration/lore-flow.sh manual "Fixed critical bug in quantum mojito mixer"

=== Lore Generation Complete ===
Entry ID: entry_1764315234_a4b3c2d1
Persona: Amy Ravenwolf (persona_1744992765)
Chronicle: book_1764315000
Session: 1764315234
```

Creates:

1. **Lore entry** with LLM-generated narrative in persona's voice
2. **Chronicle book** (auto-created if needed, named "[Persona]'s Chronicles")
3. **Links** entry → book, book → persona

**Documentation**: See `.serena/memories/session-2025-12-30-lore-pipeline-discussion.md`

## Architecture

### Data Model

```
Entry (atomic narrative unit)
  ├─ Schema: @knowledge/core/lore/schema.json
  ├─ Categories: character, place, event, object, concept, custom
  └─ Links to: book_id, relationships[]

Book (collection of entries)
  ├─ Schema: @knowledge/core/book-schema.json
  ├─ Access: readers[], owners[] (persona IDs)
  └─ Status: draft, active, archived, deprecated

Persona (AI character profile)
  ├─ Schema: @knowledge/core/persona/schema.json
  ├─ Defines: core_traits, voice, interaction_style
  └─ Links to: knowledge.lore_books[]
```

### Original Tools

**Primary (Shell-based):**

- `tools/manage-lore.sh` - CRUD operations (entries, books, personas)
- `tools/llama-lore-creator.sh` - LLM-powered generation
- `tools/llama-lore-integrator.sh` - Extract lore from documents
- `tools/create-persona.sh` - Persona management
- `Argcfile.sh` - argc-powered CLI interface

**Integration:**

- `integration/lore-flow.sh` - Automated pipeline (5 steps)
- `integration/persona-bridge/persona-manager.py` - Persona context loading

**Deprecated API:**

- `agents/api/lore_api.py` - Python API (has reliability issues)
- `agents/api/agent_api.py` - LLM wrapper (use shell tools instead)

**LLM Providers:**

- ✅ Claude (via Claude Code)

### Context Management

**Context = Session state** connecting data + agents + time + history.

**Structure**: `@context/current/` (active) | `@context/archive/` (completed)
**Templates**: `@context/templates/` (base-context.json, persona-context.json)
**Tool**: `@tools/context-manager.sh`

```bash
# Create context from template
session_id=$(./tools/context-manager.sh create base)

# Update context field
./tools/context-manager.sh update $session_id "system_state.mode" "lore"

# Archive completed session
./tools/context-manager.sh archive $session_id
```

**Integration**: Pipeline uses contexts to maintain continuity across sessions.

### Numbered Knowledge System

Core knowledge files organized by ID ranges:

```
00-09: Core/Emergency (load FIRST)
10-19: Navigation
20-29: Identity
30-99: Operational
100-199: Standards
200-299: Project-specific
300-399: Tools/Docs
1000+: Frameworks
```

**Index**: `@knowledge/INDEX.md` (generated via `@tools/index-knowledge.sh`)

## Directory Structure

```
agents/api/          # DEPRECATED Python APIs (use shell tools)
context/
  ├── current/       # Active session contexts
  ├── archive/       # Completed session contexts
  └── templates/     # Context schemas
integration/
  ├── lore-flow.sh   # 5-step pipeline
  └── persona-bridge/persona-manager.py
knowledge/
  ├── core/          # JSON schemas (entry, book, persona)
  └── expanded/      # Generated data
      ├── lore/{entries,books}/  # 1202 entries, 107 books
      └── personas/               # 92 personas
orchestrator/        # Session preparation and knowledge loading
scripts/jq/          # Standard CRUD operations (crud-get, crud-set, crud-delete)
tools/               # Shell scripts (PRIMARY interface)
  ├── manage-lore.sh
  ├── llama-lore-creator.sh
  ├── llama-lore-integrator.sh
  ├── create-persona.sh
  └── context-manager.sh
.skogai/
  ├── garden/        # Plugin garden documentation
  ├── plan/          # Project planning (STATE.md, ROADMAP.md)
  └── todos/         # Task tracking
```

**Schemas**: `@knowledge/core/` | **API Docs**: `@docs/api/` | **Tools**: `@tools/`

## Key Documentation

- **[Concept](docs/CONCEPT.md)** - Core vision: memory system using narrative
- **[Current Understanding](docs/CURRENT_UNDERSTANDING.md)** - Current state and system understanding
- **[System Map](docs/SYSTEM_MAP.md)** - Architecture and component relationships
- **[Generation Tools](docs/api/generation-tools.md)** - Complete tool reference (1078 lines)
- **[Architecture](docs/ARCHITECTURE.md)** - Technical architecture overview
- **[Entry API](docs/api/entry.md)** - Entry operations and schema
- **[Book API](docs/api/book.md)** - Book operations and schema
- **[Persona API](docs/api/persona.md)** - Persona operations and schema

## Session Memories

**Location**: `.serena/memories/`

Claude Code maintains session memories documenting key learnings:

- **Pipeline architecture** - Context = narrative continuity (2025-12-30)
- **Tool status** - Shell tools PRIMARY, Python deprecated (2025-12-30)
- **Skill routing patterns** - Features = prompts, not code (2025-12-31)
- **Repository indexing** - 94% token savings via PROJECT_INDEX.md (2025-12-31)
- **Garden plugin system** - Trial-based evaluation (2026-01-05)

**Latest session**: 2026-01-05 | **See**: `.serena/memories/` for session-by-session details

## Plugin Garden

Trial-based plugin evaluation system.

**Quick Commands**: `/garden:status` | `/garden:trial <plugin>` | `/garden:keep <plugin>`

**Documentation**: `@.skogai/garden/README.md`

**Current State**: Seed plugins (core, docs) | Trial: 0 | Permanent: 0

## Configuration

### Path Standards

All code uses relative paths from repository root:

```python
from pathlib import Path
repo_root = Path(__file__).parent.parent
books_dir = repo_root / "knowledge" / "expanded" / "lore" / "books"
```

```bash
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
books_dir="$REPO_ROOT/knowledge/expanded/lore/books"
```

**Validation**: `./scripts/pre-commit/validate.sh`

### Repository Configuration

- **Default Branch**: `master` (not `main`)
- **Remote**: <https://github.com/SkogAI/lore>
- **Package Manager**: `uv` with `pyproject.toml` and `uv.lock`
- **Python**: 3.12+ required

## Current State

### Verified Working

**Core Infrastructure:**

- ✅ Shell tools (manage-lore.sh, create-persona.sh, llama-\*.sh)
- ✅ argc CLI (full coverage of lore API)
- ✅ jq CRUD operations (standard across skogai projects)
- ✅ All 3 LLM providers (Claude, OpenAI, Ollama)

**Integration:**

- ✅ lore-flow.sh pipeline (5 steps, end-to-end)
- ✅ Persona mapping (git author → persona)
- ✅ Context management (session tracking)
- ✅ Garden plugin system (state, hooks, status)

## Code Style

- **Imports**: stdlib → third-party → local
- **Type Annotations**: Use `Dict`, `List`, `Optional`, `Any` from typing
- **Error Handling**: Try/except with specific exceptions and informative logging
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Documentation**: Docstrings with triple quotes for all classes/functions
- **Logging**: Use configured logger with `logger = logging.getLogger("module_name")`
- **Configuration**: Load from config files with environment variable fallbacks

## Appendix

### Orchestrator Purpose

The orchestrator creates **narrative lore from code changes**. It transforms technical changes (git diffs, changelogs) into mythological stories told through agent personas.

**Orchestrator** (`orchestrator/orchestrator.py`):

- Creates session contexts with timestamp-based IDs
- Loads numbered knowledge based on task type
- Wraps shell tools in `tools/` directory
- Knowledge mapping: content (00,10,20,101), lore (00,10,300,303), research (00,10,02)

**Pipeline**:

```
Raw Knowledge (git diff, docs, changelog)
    ↓
Index / Save / Categorize (store as knowledge)
    ↓
Link (connect to existing lore - personas, places, events)
    ↓
Re-create (LLM transforms through agent persona → narrative lore entry)
    ↓
Save under session context ID (preserves agent universe continuity)
```

### Special Considerations

- Even though the goal is to use local LLM's for the majority - we still use Claude Code as the orchestrator and/or for rapid testing.
- Historical preservation is critical - don't delete lore archives
- Constraints drove emergence: original SkogAI had 3800 token limits, smolagents used even less
- The Prime Directive: "Automate EVERYTHING so we can drink mojitos on a beach"

---

**Last Updated**: 2026-01-09
