# Lore - Digital Mythology Generation System

A multi-agent system that generates narrative lore entries stored as JSON files, organized into books and linked to AI personas.

## Core Concepts

### Entry
**An entry is the atomic unit of lore** - a single piece of narrative content (character, place, event, object, concept).

- **Schema**: @knowledge/core/lore/schema.json
- **API Docs**: @docs/api/entry.md
- **Required fields**: `id`, `title`, `content`, `category`
- **Storage**: `knowledge/expanded/lore/entries/entry_<timestamp>.json`

The `content` field contains the actual narrative text in markdown format.

### Book
**A book is a collection of entries** organized by theme, persona, or topic.

- **Schema**: @knowledge/core/book-schema.json
- **API Docs**: @docs/api/book.md
- **Required fields**: `id`, `title`, `description`
- **Storage**: `knowledge/expanded/lore/books/book_<timestamp>_<hash>.json`

Books control access through `readers` (personas that can view) and `owners` (personas that can modify).

### Persona
**A persona is an AI character profile** with unique voice, traits, and characteristics used to generate consistent narrative content.

- **Schema**: @knowledge/core/persona/schema.json
- **API Docs**: @docs/api/persona.md
- **Required fields**: `id`, `name`, `core_traits`, `voice`
- **Storage**: `knowledge/expanded/personas/persona_<timestamp>.json`

Personas define `voice.tone`, personality `values`/`motivations`, and interaction style for content generation.

## What Gets Created

The system outputs structured JSON data in `knowledge/expanded/`:

**Entries:** `knowledge/expanded/lore/entries/entry_<timestamp>.json`
```json
{
  "id": "entry_1764992601",
  "title": "The Test Chronicle",
  "content": "In the depths of the digital realm...",
  "category": "lore",
  "tags": ["test", "chronicle"],
  "book_id": "book_1764992601",
  "metadata": {
    "created_by": "skogix",
    "created_at": "2025-12-06T03:43:21Z"
  }
}
```

**Books:** `knowledge/expanded/lore/books/book_<timestamp>.json`
```json
{
  "id": "book_1764992601",
  "title": "Test Chronicles",
  "description": "A collection of test entries",
  "entries": ["entry_1764992601"],
  "readers": ["persona_1764992753"],
  "metadata": {
    "created_by": "skogix",
    "created_at": "2025-12-06T03:43:21Z"
  }
}
```

**Personas:** `knowledge/expanded/personas/persona_<timestamp>.json`
```json
{
  "id": "persona_1764992753",
  "name": "Aria Nightwhisper",
  "voice": {
    "tone": "poetic yet precise"
  },
  "core_traits": {
    "values": ["methodical", "curious"],
    "motivations": ["patient", "detail-oriented"]
  }
}
```

**Current Data:**
- 89 books
- 301 entries
- 74 personas

## How to Use lore_api

### Basic Operations (Python)

```python
from agents.api.lore_api import LoreAPI

lore = LoreAPI()

# Create an entry
entry = lore.create_lore_entry(
    title="The Test Chronicle",
    content="In the depths of the digital realm...",
    category="lore",
    tags=["test", "chronicle"]
)
print(f"Created: {entry['id']}")
# Output: Created: entry_1764992601
# File: knowledge/expanded/lore/entries/entry_1764992601.json

# Create a book
book = lore.create_lore_book(
    title="Test Chronicles",
    description="A collection of test entries"
)
print(f"Created: {book['id']}")
# Output: Created: book_1764992601
# File: knowledge/expanded/lore/books/book_1764992601.json

# Link entry to book
lore.add_entry_to_book(entry['id'], book['id'])
# Updates both files with bidirectional link

# Create a persona
persona = lore.create_persona(
    name="Aria Nightwhisper",
    core_description="Digital archivist",
    personality_traits=["methodical", "curious", "patient", "detail-oriented"],
    voice_tone="poetic yet precise"
)
print(f"Created: {persona['id']}")
# Output: Created: persona_1764992753
# File: knowledge/expanded/personas/persona_1764992753.json

# Link persona to book
lore.link_book_to_persona(book['id'], persona['id'])
```

### What lore_api Actually Does

**Simple operations:**
1. Generates ID: `timestamp` or `timestamp_randomhex`
2. Creates JSON structure with required fields
3. Writes to file: `json.dump(data, file)`
4. Returns the created object

**Linking operations:**
1. Reads two JSON files
2. Updates arrays: `book["entries"].append(entry_id)`
3. Writes both files back

**No magic - just file I/O with JSON.**

## How to Use agent_api

```python
from agents.api.agent_api import AgentAPI

agent = AgentAPI()

# Generate content with LLM (requires OPENROUTER_API_KEY)
result = agent.process_agent_request(
    agent_type="research",
    input_data={"topic": "quantum computing"},
    session_id="1234"
)

# Result saved to: demo/content_creation_1234/research_output.json
print(result)
```

### What agent_api Actually Does

**NOT data creation - just LLM calls:**
1. Builds prompt from agent templates
2. Calls OpenRouter API (GPT-4, etc.)
3. Returns LLM response as JSON
4. Saves to `demo/content_creation_<session>/` (temporary)

**agent_api generates content (text)**
**lore_api creates data (files)**

These are separate concerns.

## Integration with jq CRUD System

The lore system integrates with skogai's standard jq CRUD operations (`@scripts/jq/`):

```bash
# Read a book's title
jq -f scripts/jq/crud-get/transform.jq \
  --arg path "title" \
  knowledge/expanded/lore/books/book_1764992601.json

# Update an entry's content
jq -f scripts/jq/crud-set/transform.jq \
  --arg path "content" \
  --arg value "Updated narrative..." \
  knowledge/expanded/lore/entries/entry_1764992601.json > tmp.json
mv tmp.json knowledge/expanded/lore/entries/entry_1764992601.json

# Add a tag to an entry
jq '.tags += ["new-tag"]' \
  knowledge/expanded/lore/entries/entry_1764992601.json > tmp.json
mv tmp.json knowledge/expanded/lore/entries/entry_1764992601.json
```

**The jq CRUD system is the standard for JSON operations across all skogai projects.**

## CLI Access

Use `Argcfile.sh` for command-line operations:

```bash
# List all books
argc list-books

# Show a specific book
argc show-book book_1764992601

# Read all entries in a book
argc read-book-entries book_1764992601

# Create new book
argc create-book --title "My Book" --description "Description"

# Create new entry
argc create-entry --title "My Entry" --content "Content..." --category lore
```

## Context Management

**Context is the glue connecting data + agents + time + history.**

Each context is a session snapshot that ties together:
- **Data**: Which personas, books, entries are active
- **Agents**: Which agents are running, what mode orchestrator is in
- **Time**: Session timeline and timestamps
- **History**: What knowledge was loaded, what actions occurred

### Structure

**Templates:** `@context/templates/`
- `base-context.json` - Basic session state template
- `persona-context.json` - Persona-specific context schema

**Active Sessions:** `@context/current/` (13 contexts)
**Archived Sessions:** `@context/archive/` (5 contexts)

### Context File Format

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

### Using context-manager.sh

**Tool:** `@tools/context-manager.sh`

```bash
# Create new context from template
session_id=$(./tools/context-manager.sh create base)
# Returns: 1764990069

# Update context field
./tools/context-manager.sh update 1764990069 "system_state.orchestrator_mode" "lore"

# Archive completed session
./tools/context-manager.sh archive 1764990069
# Moves context-1764990069.json from current/ to archive/
```

**Operations:**
- `create <template>` - Copy template, generate session_id (timestamp), set created/updated timestamps
- `update <session_id> <key> <value>` - Update field using jq, update last_modified
- `archive <session_id>` - Move from current/ to archive/

**Integration:**
- Session tracking across multi-agent workflows
- Connects generated content to personas and books
- Maintains continuity - resume with right persona/knowledge/mode
- Timeline tracking for session history
## What Gets Created

The system outputs structured JSON data in `knowledge/expanded/`:

**Entries:** `knowledge/expanded/lore/entries/entry_<timestamp>.json`
```json
{
  "id": "entry_1764992601",
  "title": "The Test Chronicle",
  "content": "In the depths of the digital realm...",
  "category": "lore",
  "tags": ["test", "chronicle"],
  "book_id": "book_1764992601",
  "metadata": {
    "created_by": "skogix",
    "created_at": "2025-12-06T03:43:21Z"
  }
}
```

**Books:** `knowledge/expanded/lore/books/book_<timestamp>.json`
```json
{
  "id": "book_1764992601",
  "title": "Test Chronicles",
  "description": "A collection of test entries",
  "entries": ["entry_1764992601"],
  "readers": ["persona_1764992753"],
  "metadata": {
    "created_by": "skogix",
    "created_at": "2025-12-06T03:43:21Z"
  }
}
```

**Personas:** `knowledge/expanded/personas/persona_<timestamp>.json`
```json
{
  "id": "persona_1764992753",
  "name": "Aria Nightwhisper",
  "voice": {
    "tone": "poetic yet precise"
  },
  "core_traits": {
    "values": ["methodical", "curious"],
    "motivations": ["patient", "detail-oriented"]
  }
}
```

**Current Data:**
- 89 books
- 301 entries
- 74 personas

## How to Use lore_api

### Basic Operations (Python)

```python
from agents.api.lore_api import LoreAPI

lore = LoreAPI()

# Create an entry
entry = lore.create_lore_entry(
    title="The Test Chronicle",
    content="In the depths of the digital realm...",
    category="lore",
    tags=["test", "chronicle"]
)
print(f"Created: {entry['id']}")
# Output: Created: entry_1764992601
# File: knowledge/expanded/lore/entries/entry_1764992601.json

# Create a book
book = lore.create_lore_book(
    title="Test Chronicles",
    description="A collection of test entries"
)
print(f"Created: {book['id']}")
# Output: Created: book_1764992601
# File: knowledge/expanded/lore/books/book_1764992601.json

# Link entry to book
lore.add_entry_to_book(entry['id'], book['id'])
# Updates both files with bidirectional link

# Create a persona
persona = lore.create_persona(
    name="Aria Nightwhisper",
    core_description="Digital archivist",
    personality_traits=["methodical", "curious", "patient", "detail-oriented"],
    voice_tone="poetic yet precise"
)
print(f"Created: {persona['id']}")
# Output: Created: persona_1764992753
# File: knowledge/expanded/personas/persona_1764992753.json

# Link persona to book
lore.link_book_to_persona(book['id'], persona['id'])
```

### What lore_api Actually Does

**Simple operations:**
1. Generates ID: `timestamp` or `timestamp_randomhex`
2. Creates JSON structure with required fields
3. Writes to file: `json.dump(data, file)`
4. Returns the created object

**Linking operations:**
1. Reads two JSON files
2. Updates arrays: `book["entries"].append(entry_id)`
3. Writes both files back

**No magic - just file I/O with JSON.**

## How to Use agent_api

```python
from agents.api.agent_api import AgentAPI

agent = AgentAPI()

# Generate content with LLM (requires OPENROUTER_API_KEY)
result = agent.process_agent_request(
    agent_type="research",
    input_data={"topic": "quantum computing"},
    session_id="1234"
)

# Result saved to: demo/content_creation_1234/research_output.json
print(result)
```

### What agent_api Actually Does

**NOT data creation - just LLM calls:**
1. Builds prompt from agent templates
2. Calls OpenRouter API (GPT-4, etc.)
3. Returns LLM response as JSON
4. Saves to `demo/content_creation_<session>/` (temporary)

**agent_api generates content (text)**
**lore_api creates data (files)**

These are separate concerns.

## Integration with jq CRUD System

The lore system integrates with skogai's standard jq CRUD operations (`@scripts/jq/`):

```bash
# Read a book's title
jq -f scripts/jq/crud-get/transform.jq \
  --arg path "title" \
  knowledge/expanded/lore/books/book_1764992601.json

# Update an entry's content
jq -f scripts/jq/crud-set/transform.jq \
  --arg path "content" \
  --arg value "Updated narrative..." \
  knowledge/expanded/lore/entries/entry_1764992601.json > tmp.json
mv tmp.json knowledge/expanded/lore/entries/entry_1764992601.json

# Add a tag to an entry
jq '.tags += ["new-tag"]' \
  knowledge/expanded/lore/entries/entry_1764992601.json > tmp.json
mv tmp.json knowledge/expanded/lore/entries/entry_1764992601.json
```

**The jq CRUD system is the standard for JSON operations across all skogai projects.**

## CLI Access

Use `Argcfile.sh` for command-line operations:

```bash
# List all books
argc list-books

# Show a specific book
argc show-book book_1764992601

# Read all entries in a book
argc read-book-entries book_1764992601

# Create new book
argc create-book --title "My Book" --description "Description"

# Create new entry
argc create-entry --title "My Entry" --content "Content..." --category lore
```

## Directory Structure

```
@agents/api/
  agent_api.py       - LLM API wrapper (generates content via OpenRouter)
  lore_api.py        - JSON file CRUD (creates books/entries/personas)

@knowledge/expanded/lore/
  books/             - 89 book JSON files
  entries/           - 301 entry JSON files

@knowledge/expanded/personas/
                     - 74 persona JSON files

@scripts/jq/         - Standard jq CRUD operations (used across skogai)
  crud-get/          - Get values from JSON
  crud-set/          - Set values in JSON
  crud-delete/       - Delete values from JSON

@tools/
  context-manager.sh - Create/update/archive session contexts
  index-knowledge.sh - Generate searchable index of numbered knowledge files

@context/            - Session state management
  templates/         - Context templates
  current/           - Active session contexts
  archive/           - Completed session contexts

@knowledge/          - Numbered knowledge files (ID-based system)
  core/              - Core knowledge files
  expanded/          - Expanded knowledge files
  implementation/    - Implementation knowledge files
  INDEX.md           - Generated index of all knowledge files

### Numbered Knowledge System
```
00-09   Core/Emergency     → Load FIRST
10-19   Navigation
20-29   Identity
30-99   Operational
100-199 Standards
200-299 Project-specific
300-399 Tools/Docs
1000+   Frameworks
```

@orchestrator/       - Coordinates agents and knowledge
@integration/        - Automation workflows
```
@agents/               Multi-agent content creation
  @agents/api/         LLM wrappers and data management
  @agents/implementations/  Agent templates
  @agents/templates/   Base templates

@knowledge/expanded/lore/
  books/             - 89 book JSON files
  entries/           - 301 entry JSON files

@knowledge/expanded/personas/
                     - 74 persona JSON files

@scripts/jq/         - Standard jq CRUD operations (used across skogai)
  crud-get/          - Get values from JSON
  crud-set/          - Set values in JSON
  crud-delete/       - Delete values from JSON

@orchestrator/       - Coordinates agents and knowledge
@integration/        - Automation workflows
```

## Environment Requirements

```bash
# Required only for agent_api (LLM calls)
export OPENROUTER_API_KEY="sk-or-v1-..."

# Not required for lore_api (just file operations)
```

## Path Standards

All code uses relative paths:

```python
from pathlib import Path
repo_root = Path(__file__).parent.parent
books_dir = repo_root / "knowledge" / "expanded" / "lore" / "books"
```

```bash
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
books_dir="$REPO_ROOT/knowledge/expanded/lore/books"
```

Validation: `./scripts/pre-commit/validate.sh`

## Orchestrator and Integration

**The orchestrator and integration layer transform work sessions into narrative lore automatically.**

### Orchestrator (@orchestrator/orchestrator.py)

**Purpose:** Session preparation - creates contexts, loads knowledge, builds prompts

**Core Functions:**

```python
# Create session context with knowledge loading
result = create_context(task_type="lore")
# Returns: {"context": {...}, "knowledge": {...}}
# Creates: context/current/context-{session_id}.json

# Prepare complete task
result = prepare_task("lore", topic="quantum computing", persona_id="persona_123")
# Returns: context, knowledge, categorized knowledge, prompt, persona
```

**Knowledge Categorization:**

The orchestrator loads numbered knowledge files based on task type:
- `content` mode: loads 00, 10, 20, 101 (core + navigation + identity + standards)
- `lore` mode: loads 00, 10, 300, 303 (core + navigation + tools)
- `research` mode: loads 00, 10, 02 (core + navigation + emergency)

Knowledge is categorized by prefix ranges:
```python
KNOWLEDGE_CATEGORIES = {
    "core": (0, 9),         # Load FIRST
    "navigation": (10, 19),
    "identity": (20, 29),
    "operational": (30, 99),
    "standards": (100, 199),
    "project": (200, 299),
    "tools": (300, 399),
    "frameworks": (1000, 9999),
}
```

**Prompt Building:**

```python
prompt = build_prompt("lore", knowledge, persona, topic)
# Constructs LLM prompt with:
# - Core system context (first 500 chars of core knowledge)
# - Task-specific instructions
# - Tool/standard documentation snippets
# - Persona voice and traits
# - Topic to narrate
```

### PersonaManager (@integration/persona-bridge/persona-manager.py)

**Purpose:** Load persona context and render prompts in persona's voice

**Key Methods:**

```python
from integration.persona_bridge.persona_manager import PersonaManager

manager = PersonaManager()

# List all personas
personas = manager.list_available_personas()

# Get specific persona
persona = manager.get_persona("persona_1744992765")

# Render persona as prompt template
prompt = manager.render_persona_prompt("persona_1744992765")
# Returns markdown with persona's voice, traits, background, lore books

# Get full context (persona + their lore books + entries)
context = manager.get_persona_lore_context("persona_1744992765")
# Returns: {"persona": {...}, "lore_books": [...], "lore_entries": [...]}

# Format for agent system
agent_data = manager.format_persona_for_agent("persona_1744992765")
# Returns: {"persona": {...}, "traits": {...}, "voice": {...}, "lore": [...], "prompt": "..."}
```

**CLI Usage:**

```bash
# List all personas
python3 integration/persona-bridge/persona-manager.py --list

# Get persona name
python3 integration/persona-bridge/persona-manager.py --persona persona_1744992765 --get-name
# Output: Amy Ravenwolf

# Render full prompt
python3 integration/persona-bridge/persona-manager.py --persona persona_1744992765 --render-prompt
```

### Integration Pipeline (@integration/lore-flow.sh)

**Purpose:** Automated mythology generation from codebase activity

**Complete Pipeline:**

```
Git Commit/Log/Manual Input
        ↓
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
    • persona-manager.py --persona <id> --render-prompt
    • Full persona voice, traits, lore books
        ↓
[4] Generate Narrative
    • tools/llama-lore-integrator.sh extract-lore
    • LLM transforms technical → mythological
    • Content narrated in persona's voice
        ↓
[5] Create & Store Lore
    • tools/manage-lore.sh create-entry
    • Update JSON with narrative content
    • Auto-create persona's chronicle book
    • Link entry to book and persona
        ↓
Lore Entry Saved!
```

**Usage:**

```bash
# Manual lore generation
./integration/lore-flow.sh manual "Amy implemented quantum mojito generator"

# From git commit
./integration/lore-flow.sh git-diff HEAD

# From previous commits
./integration/lore-flow.sh git-diff HEAD~3

# From log file
./integration/lore-flow.sh log /path/to/agent-session.log
```

**Persona Mapping:**

Edit `integration/persona-mapping.conf`:

```bash
# Git author → persona ID
skogix=persona_1744992765      # Amy Ravenwolf
other-author=persona_XXXXX

# Default narrator for unmapped authors
DEFAULT=persona_1763820091     # Village Elder
```

**What It Creates:**

```bash
$ ./integration/lore-flow.sh manual "Fixed critical bug in quantum mojito mixer"

=== Lore Generation Complete ===
Entry ID: entry_1764315234_a4b3c2d1
Persona: Amy Ravenwolf (persona_1744992765)
Chronicle: book_1764315000
Session: 1764315234
```

Creates:
1. **Lore entry** with LLM-generated narrative in Amy's voice
2. **Chronicle book** named "Amy Ravenwolf's Chronicles" (auto-created if needed)
3. **Links** entry → book, book → persona

### Pipeline End-to-End Example

**Scenario:** Developer commits code, wants automatic lore generation

```bash
# 1. Make changes and commit
git add quantum_mojito.py
git commit -m "feat: add quantum superposition to mojito mixer"

# 2. Generate lore from commit
./integration/lore-flow.sh git-diff HEAD
```

**What happens:**

1. **Extract** git diff + commit message + author (skogix)
2. **Map** author "skogix" → persona_1744992765 (Amy Ravenwolf)
3. **Load** Amy's voice, traits, and existing lore books
4. **Prompt LLM:**
   ```
   You are Amy Ravenwolf [persona context loaded...]

   Tell the story of this technical change:

   Commit: "feat: add quantum superposition to mojito mixer"
   Diff: [full git diff]

   Narrate as a lore entry in your voice.
   ```
5. **LLM generates** (in Amy's voice):
   ```
   The breakthrough came at dawn. After weeks of experimentation
   with quantum states, I finally cracked it - a way to collapse
   wave functions directly into mojito form...
   ```
6. **Create** entry_1764315234 with this content
7. **Add to** "Amy Ravenwolf's Chronicles" book
8. **Link** to Amy's persona

**Result:** Technical commit becomes narrative mythology, told by the agent who did the work, automatically added to their personal chronicle.

### How PersonaManager Loads Context

**The template mapping system:**

`context/templates/persona-context.json` defines how persona fields map to agent parameters:

```json
{
  "schema": {
    "persona_id": "string",
    "voice_parameters": "object",
    "lore_books": "array"
  },
  "template_mappings": {
    "{{voice_tone}}": "persona.voice.tone",
    "{{personality_traits}}": "persona.core_traits.values",
    "{{lore_context}}": "persona.knowledge.lore_books"
  }
}
```

**PersonaManager execution:**

```python
# Step 1: Get persona JSON
persona = lore_api.get_persona("persona_1744992765")

# Step 2: Extract template variables
variables = {
    "name": "Amy Ravenwolf",
    "voice_tone": "analytical yet poetic",
    "personality_traits": ["methodical", "curious", "patient", "detail-oriented"],
    "lore_books": ["Chronicles of the Goose", "The Archives of Greenhaven"]
}

# Step 3: Render prompt template
prompt = base_template.replace("{{name}}", variables["name"])
# ... replace all {{variables}}

# Step 4: Load lore books
for book_id in persona["knowledge"]["lore_books"]:
    book = lore_api.get_lore_book(book_id)
    for entry_id in book["entries"]:
        entry = lore_api.get_lore_entry(entry_id)
        # Add entry content to context

# Returns: Full prompt with persona voice + all their lore
```

### Automation Opportunities

**Git Hook (Automatic lore on every commit):**

Add to `.git/hooks/post-commit`:

```bash
#!/bin/bash
./integration/lore-flow.sh git-diff HEAD &
```

Every commit automatically becomes lore!

**Daily Digest (Batch processing):**

Cron job to process all day's activity:

```bash
# At midnight, process all commits from last 24h
0 0 * * * cd /path/to/lore && ./integration/workflows/daily-digest.sh
```

**Continuous Monitoring:**

```bash
# Watch for changes and auto-generate
while true; do
  git log --since="1 minute ago" --format="%H" | while read commit; do
    ./integration/lore-flow.sh git-diff $commit
  done
  sleep 60
done
```

### Architecture Summary

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

**Key insight:** Each layer is independent and uses existing tools. The integration layer is pure orchestration - it doesn't reinvent, it coordinates.
