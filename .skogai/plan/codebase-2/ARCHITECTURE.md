# System Architecture

*Generated: 2026-01-05*
*Focus: Lore generation and connections created with context and lore-integrator*

## High-Level Architecture

The lore system implements a **5-step pipeline** that transforms work session activity into narrative lore entries through agent personas:

```
Raw Input (git diff/logs/manual)
    ↓
[1] Extract Content
    ↓
[2] Select Persona
    ↓
[3] Load Persona Context
    ↓
[4] Generate Narrative via LLM
    ↓
[5] Create & Store Lore
```

## Core Components

### 1. Pipeline Orchestrator
**File:** `integration/lore-flow.sh`

**Purpose:** Implements the 5-step flow for automatic lore generation

**Responsibilities:**
- Extract content from git diffs, logs, or manual input
- Map git authors to personas via configuration
- Load persona context including voice and lore books
- Coordinate LLM generation with persona voice
- Create entries and establish bidirectional links

### 2. Persona Manager
**File:** `integration/persona-bridge/persona-manager.py`

**Purpose:** Loads and renders persona context for LLM prompts

**Operations:**
- Parse persona JSON from file system
- Load associated lore books
- Apply template mappings (JSON fields → prompt variables)
- Render complete persona prompts with voice/traits/lore

### 3. Orchestrator Engine
**File:** `orchestrator/orchestrator.py`

**Purpose:** Creates session contexts and loads numbered knowledge

**Key Functions:**
- `create_context()` - Generate session JSON with timestamp ID
- `load_numbered_knowledge()` - Load task-specific knowledge files
- `categorize_knowledge()` - Sort by ID prefix (00-09, 10-19, etc.)
- `build_prompt()` - Construct LLM prompt with context + persona
- `prepare_task()` - Complete task setup with all components

**Knowledge Routing:**
```python
knowledge_map = {
    "content": ["00", "10", "20", "101"],     # Core + navigation + identity + standards
    "lore": ["00", "10", "300", "303"],       # Core + navigation + tools
    "research": ["00", "10", "02"],           # Core + navigation + emergency
}
```

### 4. Context Manager
**File:** `tools/context-manager.sh`

**Purpose:** Manages session lifecycle

**Operations:**
- `create <template>` - Create new session with timestamp ID
- `update <session_id> <key> <value>` - Modify session state via jq
- `archive <session_id>` - Move completed session to archive

**Lifecycle:**
```bash
session_id=$(context-manager.sh create base)      # Create
context-manager.sh update $session_id "mode" "lore"  # Update
context-manager.sh archive $session_id           # Archive
```

### 5. Storage Layer
**Files:** `tools/manage-lore.sh`, `agents/api/lore_api.py`

**Purpose:** Persists entries/books/personas to JSON files

**Operations:**
- **CRUD:** create, read, update, delete for all entity types
- **Linking:** Bidirectional entry↔book, book↔persona connections
- **Atomicity:** Temp file + move pattern prevents corruption
- **Validation:** Schema validation via jq (shell) or manual (Python)

### 6. Relationship Builder
**File:** `tools/llama-lore-integrator.sh`

**Purpose:** Creates connections between entries via LLM analysis

**Key Function:** `analyze_lore_connections()`
1. Get all entries in a book
2. Extract title/summary/category for each
3. Prompt LLM to identify meaningful connections
4. Parse LLM output (format: SOURCE / TARGET / RELATIONSHIP / DESCRIPTION)
5. Update entries' relationships arrays atomically

**Relationship Types:**
- part_of, located_in, created_by, opposes, allies_with, etc.

## Data Flow: Step by Step

### Step 1: Content Extraction
**Source:** `integration/lore-flow.sh:38-72`

**Three Input Modes:**
```bash
git-diff)
  RAW_CONTENT=$(git diff "$INPUT_CONTENT" || git show "$INPUT_CONTENT")
  GIT_AUTHOR=$(git log -1 --format='%an' "$INPUT_CONTENT")

log)
  RAW_CONTENT=$(cat "$INPUT_CONTENT")

manual)
  RAW_CONTENT="$INPUT_CONTENT"
```

**Output:** `RAW_CONTENT` variable, optional `GIT_AUTHOR`

### Step 2: Persona Selection
**Source:** `integration/lore-flow.sh:76-133`

**Mapping Flow:**
```bash
lookup_persona() {
  # Try exact match: skogix=persona_1744992765
  # Try case-insensitive match
  # Fall back to DEFAULT=persona_id
  # Final fallback: hardcoded Village Elder
}

PERSONA_ID=$(lookup_persona "$GIT_AUTHOR" "$PERSONA_MAPPING")
PERSONA_NAME=$(python3 "$PERSONA_MANAGER" --persona "$PERSONA_ID" --get-name)
```

**Data Flow:**
- Input: Git author string or explicit persona ID
- Lookup: `integration/persona-mapping.conf` (shell config format)
- Output: `PERSONA_ID` (e.g., persona_1764992753)

### Step 3: Load Persona Context
**Source:** `integration/lore-flow.sh:135-147`

**Loading Process:**
```bash
PERSONA_PROMPT=$(python3 "$PERSONA_MANAGER" --persona "$PERSONA_ID" --render-prompt)
```

**PersonaManager Operations:**
```python
# Load persona JSON: knowledge/expanded/personas/{persona_id}.json
_parse_persona_from_json_file(persona_id)

# Load associated books: knowledge/expanded/lore/books/*.json
for book_id in persona["knowledge"]["lore_books"]:
    _parse_lore_book_from_json_file(book_id)
    for entry_id in book["entries"]:
        _parse_lore_entry_from_json_file(entry_id)
```

**Context Template Mapping:**
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

**Data Loaded:**
- Persona JSON with voice, traits, background
- Referenced books (IDs from persona.knowledge.lore_books)
- Entry content from each book

### Step 4: Generate Narrative via LLM
**Source:** `integration/lore-flow.sh:149-208`

**LLM Integration:**
```bash
TEMP_CONTENT="/tmp/lore-content-$SESSION_ID.txt"
cat > "$TEMP_CONTENT" <<EOF
# Technical Change - Session $SESSION_ID

$RAW_CONTENT

---
Narrated by: $PERSONA_NAME ($PERSONA_ID)
Source: $INPUT_TYPE
EOF

EXTRACTED_LORE=$("$LORE_INTEGRATOR" "$LORE_MODEL" extract-lore "$TEMP_CONTENT" json)
GENERATED_NARRATIVE=$(echo "$EXTRACTED_LORE" | python3 -c "
  data = json.load(sys.stdin)
  print(data['entries'][0]['content'])
")
```

**LLM Call Flow:**
- Uses `$LLM_PROVIDER` environment variable
- Supports: claude (OpenRouter), openai (OpenRouter), ollama (local)
- Returns JSON with entries array containing narrative content

### Step 5: Create & Store Lore
**Source:** `integration/lore-flow.sh:210-293`

**Entry Creation:**
```bash
# Generate ID: entry_$(date +%s)_$(openssl rand -hex 4)
ENTRY_ID=$(manage-lore.sh create-entry "$ENTRY_TITLE" "event")

# Create JSON structure
{
  "id": entry_id,
  "title": ENTRY_TITLE,
  "content": "",  # Initially empty
  "category": "event",
  "tags": [],
  "metadata": {"created_by": "skogix", "created_at": timestamp},
  "visibility": {"public": true},
  "relationships": []
}
```

**Content Update:**
```python
# Read entry, update fields, write back
with open('$ENTRY_FILE', 'r') as f:
    entry = json.load(f)

entry['content'] = narrative
entry['summary'] = 'Auto-generated from $INPUT_TYPE'
entry['tags'] = ['generated', 'automated', '$PERSONA_NAME']

with open(entry_file, 'w') as f:
    json.dump(entry, f, indent=2)
```

**Book Linking (Bidirectional):**
```bash
add_to_book() {
  # 1. Add entry ID to book's entries array
  jq '.entries += ["'$entry_id'"]' "$book_file" > tmp.json
  mv tmp.json "$book_file"

  # 2. Update entry's book_id field
  jq '.book_id = "'$book_id'"' "$entry_file" > tmp.json
  mv tmp.json "$entry_file"

  # 3. Update timestamps
  jq '.metadata.updated_at = "'$timestamp'"' "$book_file" > tmp.json
  mv tmp.json "$book_file"
}
```

**Persona-to-Book Linking:**
```bash
link_to_persona() {
  # 1. Add persona to book's readers array
  jq '.readers += ["'$persona_id'"]' "$book_file" > tmp.json

  # 2. Add book to persona's lore_books array
  jq '.knowledge.lore_books += ["'$book_id'"]' "$persona_file" > tmp.json
}
```

## Context as the Binding Mechanism

**Context** ties together data + agent + time + history

**Context Structure:**
```json
{
  "session_id": "1764992601",          // Timestamp-based unique ID
  "created": "2025-12-06T03:43:21Z",   // Session start time
  "system_state": {
    "orchestrator_mode": "lore",       // content|lore|research
    "memory_priority": "core",         // What knowledge to load
    "active_agents": []                // Which agents are running
  },
  "active_knowledge": ["00", "10", "300"],  // Loaded knowledge files
  "interaction_state": {
    "current_task": "",                // What's happening now
    "task_progress": 0,                // Completion %
    "pending_actions": []              // Queued work
  }
}
```

**Session ID as Glue:**
Every lore entry created within a session captures:
```bash
SESSION_ID=$(date +%s)  # Generated at pipeline start

# Used in:
TEMP_CONTENT="/tmp/lore-content-$SESSION_ID.txt"  # Content staging
ENTRY_ID=$(entry_${SESSION_ID}...)                 # Entry generation
CHRONICLE_ID=$(book_for_$SESSION_ID)               # Book grouping
```

## Connection Mechanisms

### 1. Entry-to-Book Connection
**Mechanism:** Bidirectional linking via JSON arrays

```json
// In book_1764992601.json:
{
  "entries": ["entry_1764992601", "entry_1764992602"],
  "categories": {
    "event": ["entry_1764992601"]
  },
  "structure": [
    {
      "name": "Introduction",
      "entries": ["entry_1764992601"]
    }
  ]
}

// In entry_1764992601.json:
{
  "book_id": "book_1764992601"  // Back-reference
}
```

**Creation Flow:**
```bash
# Step 1: Create entry (standalone)
entry_id=$(manage-lore.sh create-entry "Title" "event")

# Step 2: Link to book (bidirectional update)
manage-lore.sh add-to-book "$entry_id" "$book_id"
# Atomically:
#   - Adds entry_id to book.entries array
#   - Sets entry.book_id = book_id
#   - Updates timestamps
```

### 2. Book-to-Persona Connection
**Mechanism:** Dual-direction referencing via readers/lore_books arrays

```json
// In book_1764992601.json:
{
  "readers": ["persona_1764992753"],
  "owners": []  // Who can modify
}

// In persona_1764992753.json:
{
  "knowledge": {
    "lore_books": ["book_1764992601"]
  }
}
```

### 3. Entry-to-Entry Relationships
**Mechanism:** LLM-analyzed relationship graph via relationships array

```json
// In entry_1764992601.json:
{
  "relationships": [
    {
      "target_id": "entry_1764992602",
      "relationship_type": "part_of",
      "description": "This event led to the discovery of..."
    },
    {
      "target_id": "entry_1764992603",
      "relationship_type": "located_in",
      "description": "This happened in Greenhaven"
    }
  ]
}
```

**Creation Flow (tools/llama-lore-integrator.sh:349-442):**
```bash
analyze_lore_connections() {
  # 1. Get all entries in book
  ENTRIES=$(jq -r '.entries[]' "$BOOK_FILE")

  # 2. Extract title/summary/category for each
  # Build entry catalog

  # 3. Prompt LLM to analyze connections
  PROMPT="Analyze these entries and identify connections.
           Format: ## CONNECTION / SOURCE / TARGET / RELATIONSHIP / DESCRIPTION"

  CONNECTIONS=$(run_llm "$PROMPT")

  # 4. Parse LLM output and apply atomically
  for connection in $CONNECTIONS; do
    SOURCE=$(extract SOURCE)
    TARGET=$(extract TARGET)
    RELATIONSHIP=$(extract RELATIONSHIP)
    DESCRIPTION=$(extract DESCRIPTION)

    # Add to source entry
    jq '.relationships += [{
      "target_id": $target,
      "relationship_type": $rel,
      "description": $desc
    }]' "$SOURCE_FILE" > tmp.json
    mv tmp.json "$SOURCE_FILE"
  done
}
```

## Orchestrator Knowledge Routing

**Pattern:** Load numbered knowledge files based on task type

```python
KNOWLEDGE_CATEGORIES = {
    "core": (0, 9),         # Emergency/critical - LOAD FIRST
    "navigation": (10, 19),
    "identity": (20, 29),
    "operational": (30, 99),
    "standards": (100, 199),
    "project": (200, 299),
    "tools": (300, 399),
    "frameworks": (1000, 9999),
}
```

**Task Preparation Flow:**
```python
def prepare_task(task_type: str, topic: str, persona_id: str):
    # 1. Create session context
    context = create_context(task_type)

    # 2. Load numbered knowledge for task type
    knowledge = load_numbered_knowledge(knowledge_map[task_type])

    # 3. Load persona JSON if specified
    persona = load_persona(persona_id) if persona_id else None

    # 4. Categorize knowledge by prefix
    categorized = categorize_knowledge(knowledge)

    # 5. Build LLM prompt with context + knowledge + persona voice
    prompt = build_prompt(task_type, knowledge, persona, topic)

    # 6. Save context with metadata
    return {
        "context": context,
        "knowledge": knowledge,
        "categorized": categorized,
        "prompt": prompt,
        "persona": persona
    }
```

## Atomic Operations

**Pattern:** Temp file + move for crash-safety

```bash
atomic_update() {
  local file=$1
  local jq_filter=$2

  # 1. Write to temp file first
  temp_file=$(mktemp)

  # 2. Apply jq transformation
  if ! jq "$jq_filter" "$file" > "$temp_file"; then
    rm -f "$temp_file"
    return 1
  fi

  # 3. Validate against schema (optional)
  if [ -n "$schema_type" ]; then
    validate_against_schema "$temp_file" "$schema_type"
  fi

  # 4. Move to original (atomic)
  mv "$temp_file" "$file"
}
```

## Key Insights

### 1. Context as Narrative Continuity
- `session_id` (timestamp) ties all artifacts from one session
- Context files persist session state: orchestrator mode, active agents, loaded knowledge
- Enables agents to resume with complete context across sessions

### 2. Bidirectional Linking
- Entry ↔ Book: via `book_id` field + `entries` array
- Book ↔ Persona: via `readers` array + `knowledge.lore_books` array
- Entry ↔ Entry: via `relationships` array with LLM-analyzed connection types

### 3. Atomic Operations
- All JSON updates use temp file + move pattern
- Prevents corruption on write failures
- Validation happens before atomicity

### 4. Persona as Context Injection Point
- PersonaManager loads persona JSON + referenced books
- Template mappings transform JSON → prompt variables
- All generated content narrated in persona's voice

### 5. LLM Integration Points
- `lore-flow.sh` uses `llama-lore-integrator.sh` for narrative generation
- `analyze_lore_connections()` uses LLM to find semantic relationships
- Supports 3 providers: claude, openai (OpenRouter), ollama (local)

### 6. Storage is the Source of Truth
- All data persists as JSON files in `knowledge/expanded/`
- APIs (lore_api.py, manage-lore.sh) are thin wrappers around file I/O
- Schema validation ensures data integrity

## Current State Metrics

- **1,202 lore entries** across 107 books
- **92 personas** with voice/trait definitions
- **13 active sessions** in context/current/
- **5 archived sessions** in context/archive/
- **Relationships graph** partially populated (via analyze-connections)

This architecture demonstrates a sophisticated binding mechanism where **context is the glue** connecting:
- **Data** (which entries/books/personas exist)
- **Agent** (which persona is narrating, what mode they're in)
- **Time** (when the session started, when modifications occurred)
- **History** (what knowledge was loaded, what actions occurred, archived sessions)

The system uses **narrative compression** to store technical knowledge in a form AI agents can load as context, maintaining consistent personality across sessions while building an interconnected mythology.
