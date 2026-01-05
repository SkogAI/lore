# External Integrations

## LLM Provider APIs

The system supports **three LLM providers** via environment variables:

### 1. Ollama (Local - Default)
- **Provider:** Local inference
- **Model:** `llama3.2:3b` (configurable via `LLM_MODEL`)
- **Command:** `ollama run <model> <prompt>`
- **Auth:** None required (runs locally)
- **Use Case:** Free, offline generation

### 2. OpenRouter (Cloud Gateway)
- **Endpoint:** `https://openrouter.ai/api/v1`
- **Auth:** `OPENROUTER_API_KEY` environment variable
- **Models:** GPT-4o, Claude variants, custom models
- **Configuration:** `OPENROUTER_BASE_URL`, `OPENROUTER_API_KEY`
- **Used By:** `agent_api.py`, `llama-lore-creator.sh`, `llama-lore-integrator.sh`

### 3. Anthropic Claude (Direct)
- **Interface:** Claude Code CLI (`claude --print`)
- **Auth:** `ANTHROPIC_API_KEY` or Claude Code authorization
- **Command:** `LLM_PROVIDER=claude`
- **Auto-detection:** Shell scripts detect automatically

### 4. OpenAI (Legacy via OpenRouter)
- **Endpoint:** `OPENAI_BASE_URL` (defaults to OpenRouter)
- **Auth:** `OPENAI_API_KEY`
- **Gateway:** Uses OpenRouter for compatibility

## Data Storage

### JSON-Based File Storage
**No database** - All data stored as schema-validated JSON files:

- **Lore Entries:** `knowledge/expanded/lore/entries/entry_<timestamp>.json`
- **Lore Books:** `knowledge/expanded/lore/books/book_<timestamp>.json`
- **Personas:** `knowledge/expanded/personas/persona_<timestamp>.json`
- **Schemas:** `knowledge/core/{lore,book,persona}/schema.json`
- **Session Contexts:** `context/current/`, `context/archive/`

### Knowledge Base
- **Numbered Knowledge:** `knowledge/` (00-1999 range, categorized by prefix)
- **Legacy Knowledge:** `lorefiles/skogai/current/goose-memory-backup/`
- **Generated Index:** `knowledge/INDEX.md`

## External Tools & Services

### Git Integration
- **Purpose:** Extract commits, diffs, authorship for lore generation
- **Pre-commit Hooks:** `scripts/pre-commit/` for validation
- **Author Mapping:** `integration/persona-mapping.conf` (git author → persona ID)
- **Commands:** `git log`, `git diff`, `git show`

### jq Operations Library
- **Purpose:** Standard JSON CRUD operations (60+ transformations)
- **Location:** `scripts/jq/`
- **Operations:** `crud-get/`, `crud-set/`, `crud-delete/`, `crud-merge/`
- **Capabilities:** Field extraction, validation, type checking, statistics

### Version Control & Environment
- **direnv:** `.envrc` for environment configuration
- **Pre-commit:** `.pre-commit-config.yaml` for git hooks
- **Git Ignore:** `.gitignore` for untracked files

## Integration Pipeline

### Orchestrator Layer
- **orchestrator.py** - Session context creation, knowledge categorization, prompt building
- **context-manager.sh** - Session lifecycle management

### Integration Layer
- **lore-flow.sh** - 5-step pipeline: extract → select persona → load context → generate → store
- **persona-manager.py** - Persona context loading and prompt rendering
- **Service Management:** `integration/services/` (lore service, agent service setup)

## API Architecture

### agent_api.py - LLM Integration Layer
- Calls OpenRouter API via HTTP (requests library)
- Manages session context and phase orchestration
- Supports research, outline, writing agents
- Configurable temperature, max_tokens per agent type

### lore_api.py - Lore CRUD Operations
- Schema validation from JSON Schema files
- ID generation (timestamp-based)
- JSON file I/O for entries, books, personas
- Bidirectional linking operations

### Argcfile.sh - CLI Interface (argc)
- Commands: list/show/create/validate operations
- Dynamic argument completion via bash functions
- Environment variable binding
- Requires: `jq` for data extraction

## Environment Configuration

### Required for API Access
```bash
OPENROUTER_API_KEY=sk-or-v1-...    # OpenRouter gateway
OPENAI_API_KEY=sk-...               # OpenAI (optional, via OpenRouter)
ANTHROPIC_API_KEY=sk-ant-...        # Claude direct (optional)
```

### Tool Configuration
```bash
LLM_PROVIDER=ollama|claude|openai   # Provider selection
LLM_MODEL=llama3.2:3b               # Model for ollama
LLM_OUTPUT=/dev/stdout              # Output redirection
```

### Directory Mappings (direnv)
```bash
SKOGAI_DIR=<project_root>
LORE_SCRIPTS=<tools_dir>
LORE_DIR=<knowledge/expanded/lore>
BOOKS_DIR=<books_path>
ENTRIES_DIR=<entries_path>
PERSONA_DIR=<personas_path>
```

## Data Models

All data validated against JSON Schemas:

### Lore Entry (`knowledge/core/lore/schema.json`)
- **Required:** id, title, content, category
- **Categories:** character, place, event, object, concept, custom
- **Features:** Relationships, tags, visibility controls

### Lore Book (`knowledge/core/book-schema.json`)
- **Required:** id, title, description
- **Access Control:** owners (modify), readers (view)
- **Status:** draft, active, archived, deprecated
- **Structure:** Hierarchical sections/subsections

### Persona (`knowledge/core/persona/schema.json`)
- **Required:** id, name, core_traits, voice
- **Core Traits:** temperament, values, motivations
- **Voice:** tone, patterns, vocabulary
- **Interaction:** formality, humor, directness (enums)

## Current Data Volume

As of 2026-01-05:
- **1,202 lore entries**
- **107 lore books**
- **92 personas**
- **13 active session contexts**
- **5 archived session contexts**
