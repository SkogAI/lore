# System Architecture

## Overview

Lore is an **agent memory system using narrative as storage format**. It transforms work sessions (code changes, commits, chat logs) into mythological narrative entries stored as JSON, creating persistent memory for AI agents across sessions.

**Core Philosophy:** "Automate EVERYTHING so we can drink mojitos on a beach" - automation-driven design with constraint-driven creativity (agents operate on 500-800 token limits, creating emergent complexity through narrative compression).

## Main Components

### 1. Orchestrator Layer (`orchestrator/`)

**Purpose:** Session preparation and coordination

**orchestrator.py** - Main coordinator (200+ lines):
- Creates session contexts with timestamp-based IDs
- Loads and categorizes numbered knowledge files by task type:
  - `content` mode: 00, 10, 20, 101 (core + navigation + identity + standards)
  - `lore` mode: 00, 10, 300, 303 (core + navigation + tools)
  - `research` mode: 00, 10, 02 (core + navigation + emergency)
- Builds prompts for LLM tasks with:
  - Core system context (first 500 chars)
  - Task-specific instructions
  - Tool/standard documentation snippets
  - Persona voice and traits
  - Topic to narrate
- Manages context state across agent workflows

**context-manager.sh** - Session lifecycle:
- `create <template>` - Generate session context from template
- `update <session_id> <key> <value>` - Track state changes
- `archive <session_id>` - Move completed sessions to archive

### 2. Integration Pipeline (`integration/`)

**Purpose:** Transform technical changes into narrative lore

**lore-flow.sh** - 5-step pipeline (main entry point):
```
[1] Extract Content
    • git-diff: Extract diffs + commit message + author
    • log: Read log file contents
    • manual: Use input directly
        ↓
[2] Select Persona
    • Git author → persona mapping (persona-mapping.conf)
    • Fallback to DEFAULT or Village Elder
        ↓
[3] Load Persona Context
    • persona-manager.py --render-prompt
    • Full persona voice, traits, lore books
        ↓
[4] Generate Narrative
    • LLM transforms technical → mythological
    • Content narrated in persona's voice
        ↓
[5] Create & Store Lore
    • manage-lore.sh create-entry
    • Link entry to book and persona
```

**persona-manager.py** - Persona context loading:
- Loads persona JSON with voice, traits, background
- Renders prompt templates with variable substitution
- Gets full context (persona + lore books + entries)
- Formats for agent system consumption

**persona-mapping.conf** - Git author to persona mapping:
```bash
skogix=persona_1744992765      # Amy Ravenwolf
DEFAULT=persona_1763820091     # Village Elder
```

### 3. Agent APIs (`agents/api/`)

**Purpose:** Core data operations and LLM integration

**lore_api.py** (280 lines) - CRUD operations:
- `create_lore_entry()` - Generate ID, create JSON, write to disk
- `create_lore_book()` - Generate book with structure
- `create_persona()` - Create persona with traits/voice
- `add_entry_to_book()` - Bidirectional linking
- `link_book_to_persona()` - Access control setup
- Schema validation from JSON Schema files
- Timestamp-based ID generation

**agent_api.py** - LLM provider wrapper:
- Calls OpenRouter API via HTTP
- Manages session context and phase orchestration
- Supports research, outline, writing agents
- Configurable temperature, max_tokens per agent type

### 4. Shell Tools (`tools/`)

**Purpose:** Primary, canonical interface (recommended over Python API)

**manage-lore.sh** (800+ lines) - Complete CRUD:
- `create-entry`, `create-book`, `create-persona`
- `list-entries`, `list-books`, `list-personas`
- `show-entry`, `show-book`, `show-persona`
- `add-to-book`, `link-to-persona`
- `search` - Keyword search in titles/content/tags

**llama-lore-creator.sh** - LLM-powered generation:
- `entry <title> <category>` - Generate single entry
- `persona <name> <description>` - Generate persona
- `lorebook <title> <description> <count>` - Generate book with entries
- `link <persona_id> <count>` - Link persona to books

**llama-lore-integrator.sh** - Extract and integrate:
- `extract-lore <file> [json|lore]` - Extract entities from documents
- `create-entries <analysis> <book_id>` - Create from analysis
- `create-persona <file>` - Create from character description
- `import-directory <dir> <title> <desc>` - Bulk import
- `analyze-connections <book_id>` - Find relationships

**create-persona.sh** - Persona management:
- `create <name> <desc> <traits> <tone>`
- `list`, `show`, `edit`, `delete`

### 5. Knowledge System (`knowledge/`)

**Purpose:** Numbered organization by priority

**Structure:**
- `core/` - Schemas and templates (00-09, 100-199)
- `expanded/` - Generated content:
  - `lore/entries/` - 368 entry JSON files
  - `lore/books/` - 88 book JSON files
  - `personas/` - 53 persona JSON files
- `archived/` - Historical knowledge

**Numbering System:**
```
00-09   Core/Emergency → Load FIRST
10-19   Navigation
20-29   Identity
30-99   Operational
100-199 Standards
200-299 Project-specific
300-399 Tools/Docs
1000+   Frameworks
```

**INDEX.md** - Generated by `tools/index-knowledge.sh`

### 6. Context Management (`context/`)

**Purpose:** Session binding (data + agent + time + history)

**Structure:**
- `templates/` - Context schemas (base-context.json, persona-context.json)
- `current/` - Active session contexts (13 contexts)
- `archive/` - Completed sessions (5 contexts)

**Context File Format:**
```json
{
  "session_id": "1764990069",
  "created": "2025-12-06T04:01:09Z",
  "system_state": {
    "orchestrator_mode": "lore",
    "memory_priority": "core"
  },
  "active_knowledge": ["file1.txt", "file2.txt"],
  "prepared": {
    "topic": "quantum",
    "persona_id": "persona_1764992753",
    "categories": {
      "core": [...],
      "navigation": [...]
    }
  }
}
```

## Design Patterns

### JSON File Storage Pattern
- All data stored as JSON in `knowledge/expanded/`
- No database - simple file I/O with `json.dump()`
- Schema validation via JSON Schema contracts

### Timestamp-Based ID Pattern
- `entry_<timestamp>` - Individual entries
- `book_<timestamp>` - Books
- `persona_<timestamp>` - Personas
- `entry_<timestamp>_<hash>` - Batch entry "quantum entanglement" (same timestamp = conceptually related)

### Persona Voice System
- Personas define: `voice.tone`, `core_traits.values`, `core_traits.motivations`
- Template mapping: `{{voice_tone}}` → `persona.voice.tone`
- Consistent narrative generation in persona's voice

### Access Control Pattern
- Books have `readers` (view) and `owners` (modify) arrays
- Personas linked to books via `knowledge.lore_books`
- Bidirectional linking: entry ↔ book ↔ persona

### Knowledge Categorization
- Files numbered by priority (00=core emergency, 1000+=frameworks)
- Task-specific loading (orchestrator selects by task type)
- Progressive disclosure (load only what's needed)

### Template Mapping System
Context templates map persona fields to agent parameters:
```json
{
  "template_mappings": {
    "{{name}}": "persona.name",
    "{{voice_tone}}": "persona.voice.tone",
    "{{personality_traits}}": "persona.core_traits.values",
    "{{lore_books}}": "persona.knowledge.lore_books"
  }
}
```

## Data Flow

```
Git Commits / Code Changes
        ↓
[1] Extract Content (manage-lore.sh)
    • git diff, commit message, author
        ↓
[2] Select Persona (persona-mapping.conf)
    • Git author → persona ID
    • Fallback to DEFAULT
        ↓
[3] Load Persona Context (persona-manager.py)
    • Persona voice, traits, lore books
    • Template variable substitution
        ↓
[4] Generate Narrative (agent_api.py → LLM)
    • Technical change → mythological story
    • Narrated in persona's voice
        ↓
[5] Store Lore (manage-lore.sh)
    • Create entry JSON
    • Link to book (entry_id in book['entries'])
    • Link to persona (book_id in persona['knowledge.lore_books'])
        ↓
Persistent Lore Entry + Chronicle Book + Persona Memory
```

## Why Narrative Format?

1. **Compressed Context:** "vanquished the auth daemon" loads more meaning than "fixed bug #123"
2. **Consistent Persona:** Agents maintain voice/perspective across sessions
3. **Memorable:** Stories stick, bullet points don't
4. **Relational:** Entries link to each other, building a knowledge graph

### Example: Mythology as Technical Documentation

From `book_1759486042`:

**"Quantum Birds"**
- Content: "Chirp in programming languages, nest in directory trees. Migration patterns follow git branches."
- Meaning: Directory navigation and git workflow compressed into metaphor

**"The PATCH TOOL"**
- Content: "Creator: Dot. Uses: Rewrite history, Fix timeline paradoxes."
- Meaning: Git operations (rebase, amend, etc.)

**"Two-Number Entry Bridges"**
- Content: "Allow quantum entanglement of ideas across universes."
- Summary: "Pattern: entry_[timestamp1][hash1] ↔ entry[timestamp2]_[hash2]"
- Meaning: The entry describes its own ID format - meta-documentation

## Integration Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Work Session Activity                       │
│              (git commits, logs, manual events)                  │
└────────────────────────────┬────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Orchestrator Layer                            │
│  • orchestrator.py - Create session context, load knowledge      │
│  • context-manager.sh - Track session state                      │
└────────────────────────────┬────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Integration Layer                             │
│  • lore-flow.sh - Extract content, map author → persona          │
│  • persona-manager.py - Load persona context + lore books        │
│  • llama-lore-integrator.sh - LLM narrative generation           │
└────────────────────────────┬────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                      Storage Layer                               │
│  • lore_api.py - JSON file CRUD operations                       │
│  • manage-lore.sh - CLI lore management                          │
└────────────────────────────┬────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Lore System Storage                           │
│  • knowledge/expanded/lore/entries/ - Narrative entries          │
│  • knowledge/expanded/lore/books/ - Chronicle collections        │
│  • knowledge/expanded/personas/ - Agent profiles                 │
└─────────────────────────────────────────────────────────────────┘
```

**Key Insight:** Each layer is independent and uses existing tools. The integration layer is pure orchestration - it doesn't reinvent, it coordinates.

## Current State

**Data Volume (2026-01-05):**
- 368 lore entries
- 88 lore books
- 53 active personas
- 13 active session contexts
- 5 archived session contexts

**Verified Working:**
- ✅ lore-flow.sh pipeline (all 5 steps)
- ✅ All 3 LLM providers (claude, openai, ollama)
- ✅ Shell tool CRUD operations
- ✅ argc CLI coverage
- ✅ Session context tracking

**Known Issues:**
- ⚠️ Issue #5: LLM generates meta-commentary instead of lore content
- ⚠️ Issue #6: Pipeline creates entries with empty content field
