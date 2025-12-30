# Project Index: SkogAI Lore System

**Generated:** 2025-12-30
**Version:** 0.1.0
**Repository:** https://github.com/SkogAI/lore

## 📊 Project Overview

Digital mythology generation system that transforms work sessions (git commits, code changes, chat logs) into narrative lore entries. Acts as persistent memory for AI agents using narrative compression.

**Current Scale:**
- 1,182 lore entries
- 104 lore books
- 91 personas
- 65 jq transforms

## 📁 Project Structure

```
lore/
├── agents/              # Python APIs and agent implementations
│   ├── api/            # lore_api.py, agent_api.py (core CRUD)
│   └── implementations/ # Agent templates and personas
├── knowledge/          # Knowledge base and lore storage
│   ├── core/           # JSON schemas (entry, book, persona)
│   └── expanded/       # Actual lore data (entries/, books/, personas/)
├── orchestrator/       # Session orchestrator (Python)
├── integration/        # Pipeline automation (bash)
│   ├── lore-flow.sh   # 5-step pipeline: git→lore
│   ├── persona-bridge/ # Persona→agent context mapper
│   └── services/      # System services (agent-small, lore-service)
├── tools/              # Lore management scripts (bash)
├── scripts/jq/         # 65 jq transforms for JSON CRUD
├── context/            # Session state management
│   ├── templates/     # Context templates
│   ├── current/       # Active sessions (19 files)
│   └── archive/       # Completed sessions (5 files)
└── docs/              # System documentation
```

## 🚀 Entry Points

### CLI
- **Argcfile.sh** - Main CLI interface (argc-based)
  - `argc list-books` - List all lore books
  - `argc show-book <id>` - Display book details
  - `argc validate-entry <id>` - Validate entry schema

### Python APIs
- **agents/api/lore_api.py** - Core CRUD for entries/books/personas
  - `LoreAPI.create_lore_entry()` - Create new entry
  - `LoreAPI.create_lore_book()` - Create new book
  - `LoreAPI.create_persona()` - Create new persona
  - `LoreAPI.add_entry_to_book()` - Link entry to book

- **agents/api/agent_api.py** - LLM API wrapper
  - `AgentAPI.process_agent_request()` - Call OpenRouter API

### Integration Pipelines
- **integration/lore-flow.sh** - Full automation pipeline
  - `./integration/lore-flow.sh manual "content"` - Manual lore creation
  - `./integration/lore-flow.sh git-diff HEAD` - Generate from commit

### Tools
- **tools/manage-lore.sh** - Direct lore management
- **tools/llama-lore-creator.sh** - LLM-powered generation
- **tools/llama-lore-integrator.sh** - Extract lore from documents
- **tools/context-manager.sh** - Session lifecycle

## 📦 Core Modules

### agents/api/lore_api.py
- **Exports:** `LoreAPI` class
- **Purpose:** JSON file CRUD for entries/books/personas
- **Storage:** `knowledge/expanded/lore/`, `knowledge/expanded/personas/`
- **Operations:** create, read, update, link entities

### agents/api/agent_api.py
- **Exports:** `AgentAPI` class
- **Purpose:** LLM API wrapper (OpenRouter)
- **Providers:** Claude, OpenAI, Ollama
- **Output:** Narrative content generation

### orchestrator/orchestrator.py
- **Exports:** `create_context()`, `prepare_task()`, `build_prompt()`
- **Purpose:** Session preparation, knowledge loading, prompt building
- **Knowledge Categories:** core (00-09), navigation (10-19), tools (300-399)

### integration/persona-bridge/persona-manager.py
- **Exports:** `PersonaManager` class
- **Purpose:** Load persona context, render prompts
- **Methods:** `get_persona()`, `render_persona_prompt()`, `get_persona_lore_context()`

### tools/manage-lore.sh
- **Commands:** create-entry, create-book, add-to-book, link-to-persona, search
- **Purpose:** Basic CRUD without LLM requirement

### tools/llama-lore-creator.sh
- **Commands:** entry, persona, lorebook, link
- **Purpose:** LLM-powered content generation

### tools/llama-lore-integrator.sh
- **Commands:** extract-lore, create-entries, import-directory, analyze-connections
- **Purpose:** Extract lore from existing documents

## 🔧 Configuration

- **pyproject.toml** - Python package config, dependencies, metadata
- **Argcfile.sh** - CLI command definitions and argc configuration
- **.config/wt.toml** - Git worktree configuration

## 📚 Core Schemas

### knowledge/core/lore/schema.json
Entry schema - atomic unit of lore
- Required: `id`, `title`, `content`, `category`
- Categories: character, place, event, object, concept, custom
- Relationships: Links to other entries

### knowledge/core/book-schema.json
Book schema - collection of entries
- Required: `id`, `title`, `description`
- Access: `readers`, `owners` (persona-based)
- Status: draft, active, archived, deprecated

### knowledge/core/persona/schema.json
Persona schema - AI character profile
- Required: `id`, `name`, `core_traits`, `voice`
- Voice: `tone`, `patterns`, `vocabulary`
- Knowledge: `expertise`, `limitations`, `lore_books`

## 🧪 jq Transform Library

**Location:** `scripts/jq/`
**Count:** 65 transforms

### CRUD Operations
- `crud-get/` - Get values from JSON
- `crud-set/` - Set values in JSON
- `crud-delete/` - Delete values from JSON
- `crud-merge/` - Merge JSON objects
- `crud-query/` - Query JSON structures

### Array Operations
- `array-append/`, `array-prepend/` - Add elements
- `array-filter/`, `array-map/` - Transform arrays
- `array-unique/` - Deduplicate
- `array-chunk/`, `array-flatten/` - Reshape

### Validation
- `schema-validation/` - Validate against schemas
- `validate-types/`, `validate-required/` - Field validation
- `validate-format/`, `validate-range/` - Value validation

### String Operations
- `string-split/`, `string-join/` - Tokenization
- `string-replace/`, `string-match/` - Pattern matching
- `string-trim/`, `string-truncate/` - Formatting

### Specialized
- `extract-code-blocks/` - Parse markdown code
- `extract-urls/`, `extract-mentions/` - Pattern extraction
- `normalize-timestamp/` - Date formatting
- `generate-stats/` - Analytics

## 🔗 Key Dependencies

- **anthropic** >=0.68.0 - Claude API access
- **openai** >=1.109.1 - OpenAI API access
- **click** >=8.1.0 - CLI framework
- **pyyaml** >=6.0 - YAML parsing
- **requests** >=2.31.0 - HTTP client
- **textual** >=1.0.0 - TUI framework
- **gradio** >=5.48.0 - Web UI framework
- **rich** >=13.7.0 - Terminal formatting

## 📝 Quick Start

### 1. Setup
```bash
# Install dependencies
pip install -e .

# Or with uv
uv sync
```

### 2. Configure Environment
```bash
# Required for LLM features
export OPENROUTER_API_KEY="sk-or-v1-..."

# Optional - set custom paths
export LORE_DIR="/path/to/lore/knowledge/expanded/lore"
```

### 3. Create Your First Entry
```bash
# Using Python API
python -c "
from agents.api.lore_api import LoreAPI
lore = LoreAPI()
entry = lore.create_lore_entry(
    title='My First Entry',
    content='In the beginning...',
    category='lore'
)
print(f'Created: {entry[\"id\"]}')
"

# Using CLI
argc create-entry --title "My First Entry" \
                  --content "In the beginning..." \
                  --category lore
```

### 4. Generate From Git Commit
```bash
# Generate lore from latest commit
./integration/lore-flow.sh git-diff HEAD
```

### 5. Explore Data
```bash
# List all books
argc list-books

# Show specific book
argc show-book book_1759486042

# Search entries
tools/manage-lore.sh search "quantum"
```

## 🏗️ Architecture Patterns

### Data Model
- **Entry** - Atomic narrative unit (JSON file)
- **Book** - Collection of entries (JSON file)
- **Persona** - AI character profile (JSON file)

### Pipeline Flow
```
Git Commit/Log/Manual Input
    ↓
Extract Content (git-diff/log/manual)
    ↓
Select Persona (author→persona mapping)
    ↓
Load Persona Context (voice, traits, lore books)
    ↓
Generate Narrative (LLM transformation)
    ↓
Create & Store Lore (JSON files + links)
```

### Context System
- **Session ID** - Timestamp binds data+agent+time+history
- **Entry ID Patterns:**
  - `entry_<timestamp>` - Individual entry
  - `entry_<timestamp>_<hash>` - Quantum entangled batch
- **Template Mappings** - Transform persona JSON → agent prompts

### Knowledge Numbering
```
00-09   Core/Emergency (load FIRST)
10-19   Navigation
20-29   Identity
30-99   Operational
100-199 Standards
200-299 Project-specific
300-399 Tools/Docs
1000+   Frameworks
```

## 🔍 Key Concepts

### Narrative as Memory
Technical changes compressed into mythological stories:
- Bug fix → "vanquished the auth daemon"
- New feature → "discovered spell in forest glade"
- Refactor → "restructured realm's foundations"

### Quantum Entanglement
Same timestamp = conceptually linked entries:
- `entry_1759487978_*` (12 entries) = system architecture mythology batch

### Multiverse Mythology
Same concepts across different agent books with different narrative interpretations:
- Orchestrator view: "Greenhaven - medieval village"
- Lore-Collector view: "The Village (Goose's Domain)"

## 📊 Statistics

- **Python files:** 9 modules
- **Shell scripts:** 80+ tools and transforms
- **Documentation:** 50+ markdown files
- **JSON schemas:** 3 core schemas
- **Lore entries:** 1,182 narrative units
- **Lore books:** 104 collections
- **Personas:** 91 AI characters
- **Context sessions:** 19 active, 5 archived
- **jq transforms:** 65 operations

## 🎯 Use Cases

1. **Agent Memory** - Persistent knowledge across sessions
2. **Code Documentation** - Technical changes as narrative
3. **Team History** - Shared mythology of project evolution
4. **Knowledge Base** - Searchable lore with relationships
5. **Context Loading** - Efficient token usage (3K vs 58K)

## ⚙️ Environment Variables

```bash
OPENROUTER_API_KEY    # Required for LLM features
SKOGAI_DIR           # Path to skogai folder (default: /home/skogix/)
LORE_DIR             # Path to lore data (default: knowledge/expanded/lore)
BOOKS_DIR            # Path to books (default: lore/books)
ENTRIES_DIR          # Path to entries (default: lore/entries)
PERSONA_DIR          # Path to personas (default: expanded/personas)
```

## 🧭 Navigation Tips

- **Start with:** `CLAUDE.md` - Complete system documentation
- **API Reference:** `docs/api/` - Entry, Book, Persona APIs
- **Architecture:** `docs/ARCHITECTURE.md`, `docs/SYSTEM_MAP.md`
- **Examples:** `integration/QUICK_START.md`
- **Current State:** `docs/CURRENT_UNDERSTANDING.md`

## 📈 Token Efficiency

**Traditional approach:**
- Read all files every session → ~58,000 tokens

**With this index:**
- Read PROJECT_INDEX.md → ~3,000 tokens (94% reduction)

**ROI:**
- 10 sessions: 550,000 tokens saved
- 100 sessions: 5,500,000 tokens saved

---

**Note:** This is a living index. Update when structure changes significantly.
