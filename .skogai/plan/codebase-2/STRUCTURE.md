# Directory Structure

*Generated: 2026-01-05*
*Focus: Lore generation and connections created with context and lore-integrator*

## Repository Root

```
/home/skogix/lore/
├── .planning/                     # GSD workflow artifacts (this document)
├── .serena/                       # Serena memory system
│   └── memories/                  # Session memories
├── agents/                        # Python API layer
├── context/                       # Session state management
├── docs/                          # Documentation
├── integration/                   # Pipeline & orchestration
├── knowledge/                     # Data storage (core + generated)
├── orchestrator/                  # Session context creation
├── scripts/                       # Utility scripts (jq, etc.)
├── tools/                         # Lore management CLI
├── Argcfile.sh                    # argc-powered CLI interface
├── generate-agent-lore.py         # Specialized lorebook generation
├── pyproject.toml                 # Python dependencies
└── requirements.txt               # Simplified dependency list
```

## Core Directories

### integration/ - Pipeline & Orchestration

```
integration/
├── lore-flow.sh                   # Main 5-step pipeline (8.8 KB)
│   ├── Step 1: Extract content from git/logs/manual
│   ├── Step 2: Select persona via mapping
│   ├── Step 3: Load persona context
│   ├── Step 4: Generate narrative via LLM
│   └── Step 5: Create & store lore
├── persona-bridge/
│   └── persona-manager.py         # Load & render personas (120+ lines)
│       ├── _parse_persona_from_json_file()
│       ├── _parse_lore_book_from_json_file()
│       └── _parse_lore_entry_from_json_file()
├── persona-mapping.conf           # Author → Persona mapping
│   # Format: author=persona_id
│   # Example: skogix=persona_1744992765
├── orchestrator-flow.sh           # TODO stub for orchestration
├── workflows/                     # Automation scripts
├── services/                      # Systemd service definitions
├── INTEGRATION_ARCHITECTURE.md    # Design docs
└── IMPLEMENTATION_SUMMARY.md      # Implementation status
```

**Key Files:**
- `lore-flow.sh` (293 lines) - Complete pipeline from input to stored lore
- `persona-manager.py` - Bridges Python API with persona context loading

### orchestrator/ - Session Context Creation

```
orchestrator/
├── orchestrator.py                # Session + knowledge orchestration (150+ lines)
│   ├── create_context()          # Generate session JSON
│   ├── load_numbered_knowledge() # Load task-specific knowledge files
│   ├── categorize_knowledge()    # Sort by ID prefix ranges
│   ├── build_prompt()            # Assemble LLM prompt
│   └── prepare_task()            # Complete task setup
└── variants/                      # Mode-specific configurations
    ├── implementation-mode.md     # Code execution phase
    ├── planning-mode.md           # Design and architecture phase
    └── lore-writer.md             # Documentation tasks
```

**Knowledge Categories:**
```python
KNOWLEDGE_CATEGORIES = {
    "core": (0, 9),           # Load FIRST - Emergency/critical
    "navigation": (10, 19),   # Navigation guides
    "identity": (20, 29),     # Agent identity
    "operational": (30, 99),  # Operational procedures
    "standards": (100, 199),  # Standards and conventions
    "project": (200, 299),    # Project-specific knowledge
    "tools": (300, 399),      # Tool documentation
    "frameworks": (1000, 9999) # Framework references
}
```

### tools/ - Lore Management CLI

```
tools/
├── manage-lore.sh                 # CRUD: entries, books, personas (500+ lines)
│   ├── create-entry <title> <category>
│   ├── create-book <title> <description>
│   ├── create-persona <name> <traits> <tone>
│   ├── list-entries [category]
│   ├── list-books
│   ├── show-entry <entry_id>
│   ├── show-book <book_id>
│   ├── add-to-book <entry_id> <book_id> [section]
│   ├── link-to-persona <book_id> <persona_id>
│   └── search <query>
├── create-persona.sh              # Persona creation
│   ├── create <name> <desc> <traits> <tone>
│   ├── list
│   ├── show <persona_id>
│   ├── edit <persona_id> <field> <value>
│   └── delete <persona_id>
├── context-manager.sh             # Session lifecycle (120+ lines)
│   ├── create <template>         # Generate session with timestamp ID
│   ├── update <session_id> <key> <value>
│   └── archive <session_id>      # Move to archive/
├── llama-lore-integrator.sh       # Content extraction (200+ lines)
│   ├── extract-lore <file> [json|lore]
│   ├── create-entries <analysis> <book_id>
│   ├── create-persona <character.txt>
│   ├── import-directory <dir> <book_title> <desc>
│   └── analyze-connections <book_id>  # LLM relationship analysis
├── llama-lore-creator.sh          # LLM entry generation (150 lines)
│   ├── entry <title> <category>   # Generate single entry
│   ├── persona <name> <desc>      # Generate persona
│   ├── lorebook <title> <desc> <count>
│   └── link <persona_id> <book_count>
└── index-knowledge.sh             # Generate INDEX.md for numbered files
```

**Tool Hierarchy:**
- **manage-lore.sh** - Low-level CRUD, no LLM
- **llama-lore-creator.sh** - LLM-powered generation
- **llama-lore-integrator.sh** - Extraction + relationship analysis
- **lore-flow.sh** - High-level pipeline orchestrating all tools

### agents/ - Python API Layer

```
agents/
├── api/
│   ├── lore_api.py                # Lore CRUD operations (550+ lines)
│   │   ├── create_lore_entry()
│   │   ├── create_lore_book()
│   │   ├── create_persona()
│   │   ├── get_lore_entry()
│   │   ├── get_lore_book()
│   │   ├── get_persona()
│   │   ├── list_lore_entries()
│   │   ├── list_lore_books()
│   │   ├── list_personas()
│   │   ├── add_entry_to_book()
│   │   ├── link_book_to_persona()
│   │   ├── search_lore()
│   │   └── get_persona_lore_context()
│   ├── agent_api.py               # LLM API wrapper (320+ lines)
│   │   ├── process_agent_request()
│   │   ├── build_agent_prompt()
│   │   ├── retrieve_context()
│   │   ├── store_context()
│   │   └── _call_llm_api()
│   └── mcp-servers.json           # Model config
├── implementations/               # Agent implementations
├── prompts/                       # Prompt templates
└── templates/                     # Persona templates
    └── personas/
```

**API Pattern:**
- **lore_api.py** - Simple JSON file I/O with schema loading (but no validation)
- **agent_api.py** - OpenRouter API abstraction with request/response handling

### knowledge/ - Data Storage

```
knowledge/
├── core/                          # Schema definitions
│   ├── lore/
│   │   └── schema.json            # Entry schema (Draft 07)
│   │       ├── Required: id, title, content, category
│   │       ├── Category enum: character|place|event|object|concept|custom
│   │       └── Relationships: array with target_id, relationship_type, description
│   ├── book-schema.json           # Book schema
│   │   ├── Required: id, title, description
│   │   ├── Readers/owners: persona-based access control
│   │   └── Status enum: draft|active|archived|deprecated
│   └── persona/
│       └── schema.json            # Persona schema
│           ├── Required: id, name, core_traits, voice
│           ├── Core traits: temperament, values, motivations
│           └── Voice: tone, patterns, vocabulary
│
├── expanded/                      # Generated data
│   ├── lore/
│   │   ├── entries/               # 1,202 entry JSON files
│   │   │   └── entry_{timestamp}[_{hash}].json
│   │   │       ├── Simple: entry_1764992601
│   │   │       └── Hashed: entry_1764992601_a4b3c2d1
│   │   └── books/                 # 107 book JSON files
│   │       └── book_{timestamp}.json
│   │           └── book_1764992601
│   └── personas/                  # 92 persona JSON files
│       └── persona_{timestamp}.json
│           └── persona_1764992753
│
└── numbered/                      # Task-specific knowledge
    ├── 00-09/                     # Core (load FIRST)
    ├── 10-19/                     # Navigation
    ├── 20-29/                     # Identity
    ├── 30-99/                     # Operational
    ├── 100-199/                   # Standards
    ├── 200-299/                   # Project-specific
    ├── 300-399/                   # Tools/Docs
    └── INDEX.md                   # Generated index (via index-knowledge.sh)
```

**ID Formats:**
- **Timestamp only:** `entry_1764992601` (Python lore_api.py)
- **Timestamp + hash:** `entry_1764992601_a4b3c2d1` (Shell manage-lore.sh)
- **Batch marker:** `entry_1759487978_*` (12 entries) - Same timestamp = quantum entangled batch

### context/ - Session State Management

```
context/
├── templates/                     # Context templates
│   ├── base-context.json          # Session template
│   │   ├── session_id (timestamp)
│   │   ├── created (ISO datetime)
│   │   ├── system_state (orchestrator_mode, memory_priority)
│   │   ├── active_knowledge (loaded files)
│   │   └── interaction_state (current_task, progress, pending_actions)
│   └── persona-context.json       # Persona-specific fields
│       └── template_mappings (JSON paths → prompt variables)
├── current/                       # Active sessions (13 contexts)
│   └── context-{session_id}.json
└── archive/                       # Completed sessions (5 contexts)
    └── context-{session_id}.json
```

**Context Lifecycle:**
1. **Create:** `context-manager.sh create base` → `context/current/context-{timestamp}.json`
2. **Update:** `context-manager.sh update <id> <key> <value>` → Modify via jq
3. **Archive:** `context-manager.sh archive <id>` → Move to `context/archive/`

### scripts/ - Utility Scripts

```
scripts/
├── jq/                            # JSON CRUD operations
│   ├── crud-get/                  # Get values from JSON
│   │   ├── transform.jq           # jq transformation
│   │   └── test.sh                # Test cases
│   ├── crud-set/                  # Set values in JSON
│   │   ├── transform.jq
│   │   └── test.sh
│   ├── crud-delete/               # Delete values from JSON
│   │   ├── transform.jq
│   │   └── test.sh
│   ├── schema-validation/         # Validate JSON against schema
│   │   ├── transform.jq
│   │   └── test.sh                # 62 test cases
│   ├── type-conversion/           # to-array, to-object, etc.
│   ├── data-extraction/           # extract-urls, group-by-field
│   └── IMPLEMENTATION_SPEC.md     # jq implementation guide
└── pre-commit/                    # Git hooks
    └── validate.sh                # Path validation
```

**Test Coverage:**
- schema-validation: 62 test cases (happy path, falsy values, boundaries, errors)
- crud-get/set/delete: 20+ test cases each
- All tests use deterministic fixtures (test-input-*.json)

### docs/ - Documentation

```
docs/
├── CONCEPT.md                     # Core vision: narrative memory system
├── CURRENT_UNDERSTANDING.md       # Current state and system understanding
├── SYSTEM_MAP.md                  # Architecture and component relationships
├── ARCHITECTURE.md                # Technical architecture overview
├── INFRASTRUCTURE_ASSESSMENT.md   # Technical debt and work orders
├── project/
│   └── handover.md                # Session handover notes
└── api/                           # API Reference
    ├── entry.md                   # Entry API docs
    ├── book.md                    # Book API docs
    ├── persona.md                 # Persona API docs
    └── generation-tools.md        # Complete tool reference (1078 lines)
```

**Documentation Status:**
- ✅ Complete: Entry, Book, Persona schemas
- ✅ Complete: Tool reference documentation
- ⚠️  Known issues documented: #5 (meta-commentary), #6 (empty content)
- ❌ Missing: Orchestrator implementation guide

## File Sizes & Line Counts

### Key Shell Scripts
```
integration/lore-flow.sh           293 lines (8.8 KB)
tools/manage-lore.sh               ~500 lines
tools/llama-lore-integrator.sh     ~200 lines
tools/llama-lore-creator.sh        150 lines
tools/context-manager.sh           120 lines
```

### Python Modules
```
agents/api/lore_api.py             558 lines
agents/api/agent_api.py            322 lines
orchestrator/orchestrator.py       ~150 lines
integration/persona-bridge/persona-manager.py  120 lines
```

### Documentation
```
docs/api/generation-tools.md       1,078 lines
docs/CURRENT_UNDERSTANDING.md      ~800 lines
CLAUDE.md                          ~2,000 lines (project instructions)
```

## Data Volume

**As of 2026-01-05:**
```
knowledge/expanded/lore/entries/   1,202 files (~2.4 MB)
knowledge/expanded/lore/books/     107 files (~214 KB)
knowledge/expanded/personas/       92 files (~184 KB)
context/current/                   13 files
context/archive/                   5 files
.serena/memories/                  5 session memories
```

## Module Organization Patterns

### Shell Tools Pattern
```bash
#!/bin/bash
set -e                                  # Fail-fast execution
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Configuration
REPO_ROOT="$SCRIPT_DIR"
DATA_DIR="$REPO_ROOT/knowledge/expanded"

# Functions
function_name() {
  local param=$1
  # Implementation with atomic file operations
}

# Main execution
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

## Integration Points

### Entry Points by Use Case

**Manual Lore Creation:**
```
User → tools/manage-lore.sh create-entry → knowledge/expanded/lore/entries/
```

**LLM-Generated Lore:**
```
User → tools/llama-lore-creator.sh → tools/manage-lore.sh → entries/
```

**Pipeline Auto-Generation:**
```
Git commit → integration/lore-flow.sh → [5 steps] → entries/ + books/ + personas/
```

**Relationship Analysis:**
```
Book → tools/llama-lore-integrator.sh analyze-connections → LLM → entries/ (updated relationships)
```

**Context Management:**
```
Session start → tools/context-manager.sh create → context/current/
Session end → context-manager.sh archive → context/archive/
```

## Key Observations

### 1. Tool Hierarchy
- **Level 1:** manage-lore.sh (CRUD, no LLM)
- **Level 2:** llama-lore-creator.sh, llama-lore-integrator.sh (LLM-powered)
- **Level 3:** lore-flow.sh (orchestrates all tools)
- **Level 4:** orchestrator.py (session context + knowledge loading)

### 2. Atomic Operations
- All JSON updates use temp file + move pattern
- Prevents corruption on write failures
- Validation happens before atomicity

### 3. Bidirectional Linking
- Entry ↔ Book: via book_id + entries array
- Book ↔ Persona: via readers + lore_books arrays
- Entry ↔ Entry: via relationships array

### 4. Storage is Source of Truth
- All data persists as JSON files
- APIs are thin wrappers around file I/O
- Schema validation ensures data integrity

### 5. Context as Glue
- Session ID (timestamp) ties all artifacts
- Context files preserve session state
- Enables cross-session continuity

This structure demonstrates **clear separation of concerns**: shell tools handle orchestration, Python provides API abstractions, jq standardizes JSON operations, and context binds everything together across sessions.
