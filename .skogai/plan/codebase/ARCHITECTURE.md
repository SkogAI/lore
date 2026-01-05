# System Architecture

**Generated:** 2026-01-05

## Overview

Lore is an **agent memory system using narrative as storage format**. It transforms work sessions (code changes, commits, chat logs) into mythological narrative entries stored as JSON, creating persistent memory for AI agents across sessions.

**Core Philosophy:** "Automate EVERYTHING so we can drink mojitos on a beach"

## High-Level Architecture

```
Raw Input (git diff/logs/manual)
    |
[1] Extract Content
    |
[2] Select Persona
    |
[3] Load Persona Context
    |
[4] Generate Narrative via LLM
    |
[5] Create & Store Lore
```

## Core Components

### 1. Pipeline Orchestrator
**File:** `integration/lore-flow.sh` (293 lines)

**Responsibilities:**
- Extract content from git diffs, logs, or manual input
- Map git authors to personas via configuration
- Load persona context including voice and lore books
- Coordinate LLM generation with persona voice
- Create entries and establish bidirectional links

### 2. Persona Manager
**File:** `integration/persona-bridge/persona-manager.py` (120+ lines)

**Operations:**
- Parse persona JSON from file system
- Load associated lore books
- Apply template mappings (JSON fields -> prompt variables)
- Render complete persona prompts with voice/traits/lore

### 3. Orchestrator Engine
**File:** `orchestrator/orchestrator.py` (~150 lines)

**Key Functions:**
- `create_context()` - Generate session JSON
- `load_numbered_knowledge()` - Load task-specific knowledge
- `categorize_knowledge()` - Sort by ID prefix
- `build_prompt()` - Construct LLM prompt
- `prepare_task()` - Complete task setup

**Knowledge Routing:**
```python
knowledge_map = {
    "content": ["00", "10", "20", "101"],  # Core + navigation + identity + standards
    "lore": ["00", "10", "300", "303"],    # Core + navigation + tools
    "research": ["00", "10", "02"],        # Core + navigation + emergency
}
```

### 4. Context Manager
**File:** `tools/context-manager.sh` (120+ lines)

**Operations:**
- `create <template>` - Create new session
- `update <session_id> <key> <value>` - Modify state
- `archive <session_id>` - Store completed session

### 5. Storage Layer
**Files:** `tools/manage-lore.sh`, `agents/api/lore_api.py`

**Operations:**
- CRUD for entries, books, personas
- Bidirectional linking
- Atomic file operations (temp + move)
- Schema validation (shell only)

### 6. Relationship Builder
**File:** `tools/llama-lore-integrator.sh`

**Key Function:** `analyze_lore_connections()`
1. Get all entries in a book
2. Extract title/summary/category
3. Prompt LLM to identify connections
4. Parse output: SOURCE / TARGET / RELATIONSHIP / DESCRIPTION
5. Update entries' relationships arrays

---

## Data Flow: Step by Step

### Step 1: Content Extraction
**Source:** `integration/lore-flow.sh:38-72`

```bash
git-diff)
  RAW_CONTENT=$(git diff "$INPUT_CONTENT" || git show "$INPUT_CONTENT")
  GIT_AUTHOR=$(git log -1 --format='%an' "$INPUT_CONTENT")

log)
  RAW_CONTENT=$(cat "$INPUT_CONTENT")

manual)
  RAW_CONTENT="$INPUT_CONTENT"
```

### Step 2: Persona Selection
**Source:** `integration/lore-flow.sh:76-133`

```bash
lookup_persona() {
  # Try exact match: skogix=persona_1744992765
  # Try case-insensitive match
  # Fall back to DEFAULT=persona_id
  # Final fallback: hardcoded Village Elder
}

PERSONA_ID=$(lookup_persona "$GIT_AUTHOR" "$PERSONA_MAPPING")
```

### Step 3: Load Persona Context
**Source:** `integration/lore-flow.sh:135-147`

```bash
PERSONA_PROMPT=$(python3 "$PERSONA_MANAGER" --persona "$PERSONA_ID" --render-prompt)
```

**PersonaManager loads:**
- Persona JSON with voice, traits, background
- Referenced books (from persona.knowledge.lore_books)
- Entry content from each book

### Step 4: Generate Narrative via LLM
**Source:** `integration/lore-flow.sh:149-208`

```bash
TEMP_CONTENT="/tmp/lore-content-$SESSION_ID.txt"
cat > "$TEMP_CONTENT" <<EOF
# Technical Change - Session $SESSION_ID

$RAW_CONTENT

---
Narrated by: $PERSONA_NAME ($PERSONA_ID)
EOF

EXTRACTED_LORE=$("$LORE_INTEGRATOR" "$LORE_MODEL" extract-lore "$TEMP_CONTENT" json)
```

### Step 5: Create & Store Lore
**Source:** `integration/lore-flow.sh:210-293`

```bash
# Generate ID
ENTRY_ID=$(manage-lore.sh create-entry "$ENTRY_TITLE" "event")

# Update content
python3 -c "
entry['content'] = narrative
entry['tags'] = ['generated', 'automated', '$PERSONA_NAME']
"

# Link to book (bidirectional)
add_to_book "$ENTRY_ID" "$BOOK_ID"
```

---

## Connection Mechanisms

### Entry <-> Book
```json
// In book_1764992601.json:
{
  "entries": ["entry_1764992601", "entry_1764992602"]
}

// In entry_1764992601.json:
{
  "book_id": "book_1764992601"
}
```

### Book <-> Persona
```json
// In book.json:
{
  "readers": ["persona_1764992753"]
}

// In persona.json:
{
  "knowledge": {
    "lore_books": ["book_1764992601"]
  }
}
```

### Entry <-> Entry (Relationships)
```json
// In entry.json:
{
  "relationships": [
    {
      "target_id": "entry_1764992602",
      "relationship_type": "part_of",
      "description": "This event led to..."
    }
  ]
}
```

---

## Context Structure

```json
{
  "session_id": "1764992601",
  "created": "2025-12-06T03:43:21Z",
  "system_state": {
    "orchestrator_mode": "lore",
    "memory_priority": "core",
    "active_agents": []
  },
  "active_knowledge": ["00", "10", "300"],
  "interaction_state": {
    "current_task": "",
    "task_progress": 0,
    "pending_actions": []
  }
}
```

---

## Integration Architecture

```
+------------------------------------------------------------------+
|                    Work Session Activity                          |
|              (git commits, logs, manual events)                   |
+--------------------------------+---------------------------------+
                                 |
+--------------------------------v---------------------------------+
|                    Orchestrator Layer                             |
|  - orchestrator.py: Create session context, load knowledge        |
|  - context-manager.sh: Track session state                        |
+--------------------------------+---------------------------------+
                                 |
+--------------------------------v---------------------------------+
|                    Integration Layer                              |
|  - lore-flow.sh: Extract content, map author -> persona           |
|  - persona-manager.py: Load persona context + lore books          |
|  - llama-lore-integrator.sh: LLM narrative generation             |
+--------------------------------+---------------------------------+
                                 |
+--------------------------------v---------------------------------+
|                      Storage Layer                                |
|  - lore_api.py: JSON file CRUD operations                         |
|  - manage-lore.sh: CLI lore management                            |
+--------------------------------+---------------------------------+
                                 |
+--------------------------------v---------------------------------+
|                    Lore System Storage                            |
|  - knowledge/expanded/lore/entries/: Narrative entries            |
|  - knowledge/expanded/lore/books/: Chronicle collections          |
|  - knowledge/expanded/personas/: Agent profiles                   |
+------------------------------------------------------------------+
```

---

## Design Patterns

### JSON File Storage
- All data as JSON in `knowledge/expanded/`
- No database - simple file I/O
- Schema validation via JSON Schema

### Timestamp-Based IDs
- `entry_<timestamp>` or `entry_<timestamp>_<hash>`
- Same timestamp = conceptually related (batch)

### Persona Voice System
- Template mapping: `{{voice_tone}}` -> `persona.voice.tone`
- Consistent narrative in persona's voice

### Access Control
- Books have `readers` (view) and `owners` (modify)
- Personas linked to books via `knowledge.lore_books`

### Knowledge Categorization
```python
KNOWLEDGE_CATEGORIES = {
    "core": (0, 9),           # Load FIRST
    "navigation": (10, 19),
    "identity": (20, 29),
    "operational": (30, 99),
    "standards": (100, 199),
    "project": (200, 299),
    "tools": (300, 399),
    "frameworks": (1000, 9999),
}
```

---

## Why Narrative Format?

1. **Compressed Context:** "vanquished the auth daemon" loads more meaning than "fixed bug #123"
2. **Consistent Persona:** Agents maintain voice across sessions
3. **Memorable:** Stories stick, bullet points don't
4. **Relational:** Entries link, building knowledge graph

### Example: Mythology as Documentation

**"Quantum Birds"**
- Content: "Chirp in programming languages, nest in directory trees"
- Meaning: Directory navigation and git workflow as metaphor

**"The PATCH TOOL"**
- Content: "Creator: Dot. Uses: Rewrite history, Fix timeline paradoxes"
- Meaning: Git operations (rebase, amend)

---

## Key Insights

### 1. Context as Narrative Continuity
- `session_id` ties all artifacts from one session
- Context files persist state across sessions
- Agents resume with complete context

### 2. Bidirectional Linking
- Entry <-> Book via `book_id` + `entries`
- Book <-> Persona via `readers` + `lore_books`
- Entry <-> Entry via `relationships`

### 3. Atomic Operations
- All updates use temp file + move
- Prevents corruption on failures
- Validation before atomicity

### 4. Persona as Context Injection
- PersonaManager loads JSON + referenced books
- Templates transform JSON to prompt variables
- All content in persona's voice

### 5. Storage is Truth
- JSON files are source of truth
- APIs are thin wrappers
- Schema validation ensures integrity

---

## Current State Metrics

- **1,202 lore entries** across 107 books
- **92 personas** with voice/trait definitions
- **13 active sessions** in context/current/
- **5 archived sessions** in context/archive/
- **Relationships graph** partially populated
