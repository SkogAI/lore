# Directory Structure

**Generated:** 2026-01-05

## Repository Root

```
/home/skogix/lore/
├── agents/                        # Python API layer
│   ├── api/
│   │   ├── lore_api.py           # Lore CRUD operations (558 lines)
│   │   └── agent_api.py          # LLM provider wrapper (322 lines)
│   ├── implementations/          # Agent implementations
│   ├── prompts/                  # Prompt templates
│   └── templates/                # Persona templates
│
├── context/                       # Session state management
│   ├── templates/                # Context schemas
│   │   ├── base-context.json     # Session template
│   │   └── persona-context.json  # Persona-specific fields
│   ├── current/                  # Active sessions (13 contexts)
│   └── archive/                  # Completed sessions (5 contexts)
│
├── docs/                          # Documentation
│   ├── CONCEPT.md                # Core vision
│   ├── CURRENT_UNDERSTANDING.md  # System state (~800 lines)
│   ├── SYSTEM_MAP.md             # Architecture overview
│   ├── ARCHITECTURE.md           # Technical architecture
│   ├── api/                      # API Reference
│   │   ├── entry.md              # Entry API docs
│   │   ├── book.md               # Book API docs
│   │   ├── persona.md            # Persona API docs
│   │   └── generation-tools.md   # Tool reference (1078 lines)
│   └── project/
│       └── handover.md           # Session handover notes
│
├── integration/                   # Pipeline & orchestration
│   ├── lore-flow.sh              # Main 5-step pipeline (293 lines)
│   ├── orchestrator-flow.sh      # TODO stub for orchestration
│   ├── persona-bridge/
│   │   └── persona-manager.py    # Load & render personas (120+ lines)
│   ├── persona-mapping.conf      # Git author -> Persona mapping
│   ├── workflows/                # Automation scripts
│   └── services/                 # Systemd service definitions
│
├── knowledge/                     # Data storage (core + generated)
│   ├── core/                     # Schema definitions
│   │   ├── lore/
│   │   │   └── schema.json       # Entry schema (Draft 07)
│   │   ├── book-schema.json      # Book schema
│   │   └── persona/
│   │       └── schema.json       # Persona schema
│   ├── expanded/                 # Generated data
│   │   ├── lore/
│   │   │   ├── entries/          # 1,202 entry JSON files
│   │   │   └── books/            # 107 book JSON files
│   │   └── personas/             # 92 persona JSON files
│   └── archived/                 # Historical preservation
│
├── orchestrator/                  # Session context creation
│   ├── orchestrator.py           # Session + knowledge orchestration (~150 lines)
│   ├── identity/                 # Orchestrator identity configs
│   ├── lore-writer.md            # Lore writing specs
│   └── variants/                 # Mode-specific configurations
│
├── scripts/                       # Utility scripts
│   ├── jq/                       # JSON CRUD operations (60+ transforms)
│   │   ├── crud-get/             # Get values from JSON
│   │   ├── crud-set/             # Set values in JSON
│   │   ├── crud-delete/          # Delete values from JSON
│   │   ├── crud-merge/           # Merge JSON values
│   │   └── schema-validation/    # Validate JSON (62 test cases)
│   └── pre-commit/
│       ├── validate.sh           # Shell script path validation
│       └── validate.py           # Python pre-commit validation
│
├── tools/                         # Lore management CLI
│   ├── manage-lore.sh            # CRUD: entries, books, personas (~500 lines)
│   ├── create-persona.sh         # Persona creation
│   ├── context-manager.sh        # Session lifecycle (120+ lines)
│   ├── llama-lore-integrator.sh  # Content extraction (~200 lines)
│   ├── llama-lore-creator.sh     # LLM entry generation (150 lines)
│   └── index-knowledge.sh        # Generate INDEX.md
│
├── .skogai/                       # SkogAI workflow state
│   └── plan/
│       └── codebase/             # This codebase map
│
├── .serena/                       # Claude Code session memories
│   └── memories/                 # Session learnings (5 files)
│
├── .github/                       # GitHub configuration
│   └── workflows/                # CI/CD workflows
│
├── Argcfile.sh                    # argc-powered CLI interface
├── generate-agent-lore.py         # Specialized lorebook generation
├── CLAUDE.md                      # Project instructions (~2000 lines)
├── pyproject.toml                 # Python project config
└── uv.lock                        # Python dependencies lock
```

## Key Locations

### Data Storage
| Type | Location | Count |
|------|----------|-------|
| Lore Entries | `knowledge/expanded/lore/entries/` | 1,202 files |
| Lore Books | `knowledge/expanded/lore/books/` | 107 files |
| Personas | `knowledge/expanded/personas/` | 92 files |
| Active Contexts | `context/current/` | 13 files |
| Archived Contexts | `context/archive/` | 5 files |

### Schemas (Contracts)
| Type | Location |
|------|----------|
| Entry Schema | `knowledge/core/lore/schema.json` |
| Book Schema | `knowledge/core/book-schema.json` |
| Persona Schema | `knowledge/core/persona/schema.json` |

### Pipeline
| Component | Location |
|-----------|----------|
| Main Pipeline | `integration/lore-flow.sh` |
| Persona Manager | `integration/persona-bridge/persona-manager.py` |
| Author Mapping | `integration/persona-mapping.conf` |

### CLI Interface
| Tool | Location |
|------|----------|
| Argc CLI | `Argcfile.sh` |
| Main CRUD Tool | `tools/manage-lore.sh` |
| LLM Creator | `tools/llama-lore-creator.sh` |
| LLM Integrator | `tools/llama-lore-integrator.sh` |

### Documentation
| Document | Location |
|----------|----------|
| Main Doc (CANONICAL) | `CLAUDE.md` |
| Current State | `docs/CURRENT_UNDERSTANDING.md` |
| API Docs | `docs/api/{entry,book,persona}.md` |
| Tool Reference | `docs/api/generation-tools.md` |

## Module Organization

### Tool Hierarchy
```
Level 4: orchestrator.py          (session context + knowledge loading)
    ↓
Level 3: lore-flow.sh             (orchestrates all tools)
    ↓
Level 2: llama-lore-creator.sh    (LLM-powered generation)
         llama-lore-integrator.sh (extraction + analysis)
    ↓
Level 1: manage-lore.sh           (CRUD, no LLM)
```

### Data Layer
- **Location:** `knowledge/`, `agents/api/`
- **Purpose:** JSON schemas and storage
- **Pattern:** Simple JSON file I/O with schema loading

### API Layer
- **Location:** `agents/api/`
- **Purpose:** CRUD operations
- **Files:**
  - `lore_api.py` (558 lines) - JSON file CRUD
  - `agent_api.py` (322 lines) - LLM provider integration

### Tool Layer
- **Location:** `tools/`
- **Purpose:** Primary CLI interface (shell + Python)
- **Pattern:** Shell scripts with jq for JSON manipulation

### Integration Layer
- **Location:** `integration/`
- **Purpose:** Pipeline orchestration
- **Pattern:** 5-step lore generation flow

### Orchestration Layer
- **Location:** `orchestrator/`
- **Purpose:** Session coordination and context management
- **Pattern:** Knowledge categorization by ID prefix

## File Naming Conventions

### JSON Data Files
| Type | Pattern | Example |
|------|---------|---------|
| Entry (Python) | `entry_<timestamp>.json` | `entry_1764992601.json` |
| Entry (Shell) | `entry_<timestamp>_<hash>.json` | `entry_1764992601_a4b3c2d1.json` |
| Book | `book_<timestamp>.json` | `book_1764992601.json` |
| Persona | `persona_<timestamp>.json` | `persona_1764992753.json` |
| Context | `context-<session_id>.json` | `context-1764990069.json` |

### Knowledge Files
| Range | Category |
|-------|----------|
| 00-09 | Core/Emergency (load FIRST) |
| 10-19 | Navigation |
| 20-29 | Identity |
| 30-99 | Operational |
| 100-199 | Standards |
| 200-299 | Project-specific |
| 300-399 | Tools/Docs |
| 1000+ | Frameworks |

## Integration Points

### Entry Points by Use Case

**Manual Lore Creation:**
```
User -> tools/manage-lore.sh create-entry -> knowledge/expanded/lore/entries/
```

**LLM-Generated Lore:**
```
User -> tools/llama-lore-creator.sh -> tools/manage-lore.sh -> entries/
```

**Pipeline Auto-Generation:**
```
Git commit -> integration/lore-flow.sh -> [5 steps] -> entries/ + books/ + personas/
```

**Relationship Analysis:**
```
Book -> tools/llama-lore-integrator.sh analyze-connections -> LLM -> entries/ (updated)
```

**Context Management:**
```
Session start -> tools/context-manager.sh create -> context/current/
Session end -> context-manager.sh archive -> context/archive/
```

## Module Patterns

### Shell Tools Pattern
```bash
#!/bin/bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$SCRIPT_DIR"
DATA_DIR="$REPO_ROOT/knowledge/expanded"

function_name() {
  local param=$1
  # Implementation with atomic file operations
}

case "$1" in
  command) function_name "$2" ;;
  *) usage ;;
esac
```

### Python API Pattern
```python
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class LoreAPI:
    def __init__(self):
        self.repo_root = Path(__file__).parent.parent
        self.data_dir = self.repo_root / "knowledge" / "expanded"
        self.schemas = {}
        self.load_schemas()

    def method_name(self, param: str) -> Optional[Dict[str, Any]]:
        """Docstring with type hints."""
        try:
            # Implementation with JSON file I/O
            pass
        except Exception as e:
            logger.error(f"Error: {e}")
            return None
```

### jq Transformation Pattern
```
scripts/jq/operation-name/
├── transform.jq           # Transformation logic
├── test.sh                # Test cases
├── test-input-*.json      # Test fixtures
└── README.md              # Usage documentation
```

## Key Observations

### 1. Atomic Operations
- All JSON updates use temp file + move pattern
- Prevents corruption on write failures
- Validation happens before atomicity

### 2. Bidirectional Linking
- Entry <-> Book: via `book_id` + `entries` array
- Book <-> Persona: via `readers` + `lore_books` arrays
- Entry <-> Entry: via `relationships` array

### 3. Storage is Source of Truth
- All data persists as JSON files
- APIs are thin wrappers around file I/O
- Schema validation ensures data integrity

### 4. Context as Glue
- Session ID (timestamp) ties all artifacts
- Context files preserve session state
- Enables cross-session continuity
