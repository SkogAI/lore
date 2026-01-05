# Directory Structure

## Repository Layout

```
/home/skogix/lore/
├── agents/                          # Agent system
│   ├── api/
│   │   ├── lore_api.py             # Lore CRUD operations (280 lines)
│   │   └── agent_api.py            # LLM provider wrapper
│   ├── implementations/
│   │   └── small_model_agents.py   # Constrained token agents
│   ├── prompts -> /home/skogix/docs/prompts/  # Prompt templates (symlink)
│   └── templates/                  # Agent templates
│
├── context/                         # Session management
│   ├── current/                    # Active session contexts (13 JSON files)
│   ├── archive/                    # Completed session contexts (5 JSON files)
│   └── templates/                  # Context schema templates
│       ├── base-context.json       # Basic session state template
│       └── persona-context.json    # Persona-specific context schema
│
├── knowledge/                       # Data and schemas
│   ├── core/
│   │   ├── lore/
│   │   │   ├── schema.json         # Entry schema contract
│   │   │   └── book-schema.json    # Book schema contract (deprecated location)
│   │   ├── book-schema.json        # Book schema contract (canonical)
│   │   ├── persona/
│   │   │   └── schema.json         # Persona schema contract
│   │   ├── 00/                     # Core knowledge (load FIRST)
│   │   └── 20/                     # Identity knowledge
│   ├── expanded/
│   │   ├── lore/
│   │   │   ├── entries/            # 368 lore entry JSON files
│   │   │   └── books/              # 88 lore book JSON files
│   │   ├── personas/               # 53 persona JSON files
│   │   └── 20/                     # Content-creation-workflow.md
│   ├── archived/                   # Historical personas (61+)
│   ├── implementation/             # Implementation knowledge
│   └── goose-memory-backup/        # Legacy knowledge
│
├── orchestrator/                    # Session coordination
│   ├── orchestrator.py             # Main orchestrator (200+ lines)
│   ├── identity/                   # Orchestrator identity configs
│   ├── lore-writer.md              # Lore writing specs
│   └── variants/                   # Orchestrator variants
│
├── integration/                     # Pipeline automation
│   ├── lore-flow.sh               # 5-step pipeline (main entry point)
│   ├── orchestrator-flow.sh       # Orchestrator pipeline (stub)
│   ├── persona-bridge/
│   │   └── persona-manager.py     # Persona context loading
│   ├── persona-mapping.conf       # Git author → persona mapping
│   ├── services/                  # Service daemon scripts
│   │   ├── skogai-lore-service.sh
│   │   └── skogai-agent-small-service.sh
│   └── workflows/                 # Automation workflows
│
├── tools/                          # Primary CRUD interface
│   ├── manage-lore.sh             # Main CRUD tool (800+ lines)
│   ├── create-persona.sh          # Persona creation
│   ├── context-manager.sh         # Context lifecycle
│   ├── llama-lore-creator.sh      # LLM-powered generation
│   ├── llama-lore-creator.py      # Python version
│   ├── llama-lore-integrator.sh   # Extract from documents
│   ├── llama-lore-integrator.py   # Python version
│   ├── index-knowledge.sh         # Generate knowledge index
│   ├── lore_tui.py                # TUI interface
│   └── worktree-todo-manager.sh   # Worktree TODO management
│
├── scripts/
│   ├── jq/                        # Standard jq CRUD operations
│   │   ├── crud-get/              # Read JSON values
│   │   ├── crud-set/              # Update JSON values
│   │   ├── crud-delete/           # Delete JSON values
│   │   └── crud-merge/            # Merge JSON values
│   └── pre-commit/
│       ├── validate.sh            # Shell script path validation
│       └── validate.py            # Python pre-commit validation
│
├── docs/                           # Documentation
│   ├── CLAUDE.md                  # Main project doc (CANONICAL)
│   ├── CURRENT_UNDERSTANDING.md   # System state
│   ├── ARCHITECTURE.md            # Technical architecture
│   ├── SYSTEM_MAP.md              # System overview
│   ├── CONCEPT.md                 # Core vision
│   ├── api/
│   │   ├── entry.md               # Entry API docs
│   │   ├── book.md                # Book API docs
│   │   ├── persona.md             # Persona API docs
│   │   └── generation-tools.md    # Tool reference (1078 lines)
│   ├── analysis/                  # Analysis docs
│   └── project/                   # Project documentation
│       └── handover.md            # Session handover notes
│
├── .skogai/                        # SkogAI workflow state
│   └── plan/
│       └── codebase/              # Codebase analysis (THIS MAP)
│
├── .serena/                        # Claude Code session memories
│   └── memories/                  # Session learnings (5 files)
│
├── .github/                        # GitHub configuration
│   ├── workflows/                 # CI/CD workflows
│   │   ├── claude.yml             # Claude Code integration
│   │   ├── lore-growth.yml        # Growth monitoring
│   │   └── doc-updater.yml        # Documentation updates
│   └── workflows-old/             # Archived workflows
│
├── Argcfile.sh                     # CLI interface (argc-powered)
├── generate-agent-lore.py          # Specialized lore generation
├── CLAUDE.md                       # Project instructions (CANONICAL)
├── pyproject.toml                  # Python project config
├── uv.lock                         # Python dependencies lock file
├── .pre-commit-config.yaml         # Pre-commit hooks config
├── .envrc                          # Direnv environment config
└── .gitignore                      # Git ignore patterns
```

## Module Organization

### Data Layer
- **Location:** `knowledge/`, `agents/api/`
- **Purpose:** JSON schemas and storage
- **Files:**
  - Schemas: `knowledge/core/{lore,book,persona}/schema.json`
  - Data: `knowledge/expanded/lore/{entries,books}/`, `knowledge/expanded/personas/`

### API Layer
- **Location:** `agents/api/`
- **Purpose:** CRUD operations
- **Files:**
  - `lore_api.py` (280 lines) - JSON file CRUD
  - `agent_api.py` - LLM provider integration

### Tool Layer
- **Location:** `tools/`
- **Purpose:** Primary CLI interface (shell + Python)
- **Files:**
  - `manage-lore.sh` (800+ lines) - Main CRUD tool
  - `llama-lore-creator.sh` - LLM generation
  - `llama-lore-integrator.sh` - Extract from documents
  - `create-persona.sh` - Persona management
  - `context-manager.sh` - Session lifecycle

### Integration Layer
- **Location:** `integration/`
- **Purpose:** Pipeline orchestration
- **Files:**
  - `lore-flow.sh` - 5-step pipeline (main entry point)
  - `persona-manager.py` - Persona context loading
  - `persona-mapping.conf` - Git author mapping

### Orchestration Layer
- **Location:** `orchestrator/`
- **Purpose:** Session coordination and context management
- **Files:**
  - `orchestrator.py` (200+ lines) - Main orchestrator
  - `identity/` - Orchestrator identity configs

### Context Layer
- **Location:** `context/`
- **Purpose:** Session binding and state tracking
- **Structure:**
  - `templates/` - Context schemas
  - `current/` - Active sessions (13 contexts)
  - `archive/` - Completed sessions (5 contexts)

### Scripts Layer
- **Location:** `scripts/jq/`
- **Purpose:** Standard JSON operations (reusable across projects)
- **Operations:** crud-get, crud-set, crud-delete, crud-merge

## Key Locations

### Data Storage
- **Lore Entries:** `/home/skogix/lore/knowledge/expanded/lore/entries/` (368 files)
- **Lore Books:** `/home/skogix/lore/knowledge/expanded/lore/books/` (88 files)
- **Personas:** `/home/skogix/lore/knowledge/expanded/personas/` (53 files)

### Schemas (Contracts)
- **Entry Schema:** `/home/skogix/lore/knowledge/core/lore/schema.json`
- **Book Schema:** `/home/skogix/lore/knowledge/core/book-schema.json`
- **Persona Schema:** `/home/skogix/lore/knowledge/core/persona/schema.json`

### Context Management
- **Templates:** `/home/skogix/lore/context/templates/`
- **Active Sessions:** `/home/skogix/lore/context/current/` (13 contexts)
- **Archive:** `/home/skogix/lore/context/archive/` (5 contexts)

### Pipeline
- **Main Pipeline:** `/home/skogix/lore/integration/lore-flow.sh`
- **Persona Manager:** `/home/skogix/lore/integration/persona-bridge/persona-manager.py`
- **Author Mapping:** `/home/skogix/lore/integration/persona-mapping.conf`

### CLI Interface
- **Argc CLI:** `/home/skogix/lore/Argcfile.sh` (argc-powered)
- **Main Tool:** `/home/skogix/lore/tools/manage-lore.sh` (800+ lines)

### Documentation
- **Main Doc:** `/home/skogix/lore/CLAUDE.md` (CANONICAL)
- **Current State:** `/home/skogix/lore/docs/CURRENT_UNDERSTANDING.md`
- **API Docs:** `/home/skogix/lore/docs/api/{entry,book,persona}.md`
- **Tool Reference:** `/home/skogix/lore/docs/api/generation-tools.md` (1078 lines)

### Session Memories
- **Location:** `/home/skogix/lore/.serena/memories/`
- **Files:** 5 session memory files documenting learnings across sessions

## File Naming Conventions

### JSON Data Files
- **Entry files:** `entry_<unix_timestamp>.json`
  - Example: `entry_1743758088.json`
  - Batch entries: `entry_<timestamp>_<hex_hash>.json` (quantum entanglement pattern)
- **Book files:** `book_<unix_timestamp>.json` or `book_<timestamp>_<hex_hash>.json`
  - Example: `book_1743774022_e2298400.json`
- **Persona files:** `persona_<unix_timestamp>.json` or `<name>.json`
  - Example: `persona_1743758088.json`, `amy.json`

### Context Files
- **Format:** `context-<session_id>.json`
- **Session ID:** Unix timestamp (e.g., `context-1764990069.json`)

### Knowledge Files
- **Numbered:** `XXNN.md` (e.g., `0000.md`, `0010.md`)
- **Ranges:**
  - 00-09: Core/Emergency
  - 10-19: Navigation
  - 20-29: Identity
  - 30-99: Operational
  - 100-199: Standards
  - 200-299: Project-specific
  - 300-399: Tools/Docs
  - 1000+: Frameworks

## Current Data Volume

As of 2026-01-05:
- **368 lore entries** (`knowledge/expanded/lore/entries/`)
- **88 lore books** (`knowledge/expanded/lore/books/`)
- **53 active personas** (`knowledge/expanded/personas/`)
- **61+ archived personas** (`knowledge/archived/`)
- **13 active session contexts** (`context/current/`)
- **5 archived session contexts** (`context/archive/`)
- **5 session memories** (`.serena/memories/`)

## Special Directories

### `.skogai/` - SkogAI Workflow State
- Created by `/skogai:*` commands
- Contains project planning and state
- `plan/codebase/` - This codebase map

### `.serena/` - Claude Code Session Memories
- Maintains session learnings across conversations
- Documents what worked vs what didn't
- Key mistakes to avoid
- Cross-session continuity

### `.github/workflows/` - CI/CD Automation
- `claude.yml` - Claude Code integration
- `lore-growth.yml` - Growth monitoring (every 6 hours)
- `doc-updater.yml` - Documentation consistency
- `claude-code-review.yml` - Code review automation

### `lorefiles/` - Legacy Knowledge
- Historical knowledge from previous system
- `skogai/current/goose-memory-backup/` - Goose agent memory backup
- Not actively used but preserved for historical reference
