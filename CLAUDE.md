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

- 102 books
- 728 entries
- 89 personas

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

00-09 Core/Emergency → Load FIRST
10-19 Navigation
20-29 Identity
30-99 Operational
100-199 Standards
200-299 Project-specific
300-399 Tools/Docs
1000+ Frameworks

```

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

- this is the representation of our current understanding of the lore project - it should be updated when ending a session to know where we stand: @docs/CURRENT_UNDERSTANDING.md

## Session Memories

**Location:** `.serena/memories/`

Claude Code maintains session memories to preserve learnings across sessions:

- **session-2025-12-30-lore-pipeline-discussion.md** - Pipeline architecture learnings, context as narrative continuity
- **lore-generation-tools-documentation-session.md** - Created comprehensive tool docs, corrected deprecation status
- **session-2025-12-31-prompts-repository-and-skill-patterns.md** - Skill routing patterns, agent prompting philosophy
- **session-2025-12-31-docs-analysis.md** - Repository analysis, PROJECT_INDEX creation (94% token savings)
- **session-2025-12-31-argc-sanity-check.md** - Verified argc provides 100% lore API coverage

These memories document:
- What worked vs what didn't
- Key mistakes and how to avoid them
- Technical discoveries and insights
- Cross-session continuity for future work

## Key Documentation

- **[Concept](docs/CONCEPT.md)** - Core vision: memory system for agents using narrative
- **[Handover](docs/project/handover.md)** - Session context and current state
- **[Pipeline Plan](docs/project/PIPELINE_PLAN.md)** - Implementation proposal for orchestrator
- **[Operations Map](docs/OPERATIONS_MAP.md)** - Complete tool and workflow documentation
- **[System Map](docs/SYSTEM_MAP.md)** - Architecture and component relationships
- **[Generation Tools](docs/api/generation-tools.md)** - Complete reference for all lore generation endpoints and tools

## Build & Development Commands

```bash
# Test API functionality
python agents/api/agent_api.py
python agents/api/lore_api.py

# Initialize orchestrator session
python orchestrator/orchestrator.py init [content|lore|research]
```

## Orchestrator Purpose

The orchestrator creates **narrative lore from code changes**. It transforms technical changes (git diffs, changelogs) into mythological stories told through agent personas.

### Orchestrator Pipeline

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

### Lore Entry Types

- **Character** = Agent persona/role (e.g., Village Elder = skogix the mentor)
- **Place** = Project/codebase environment (e.g., Greenhaven = the repo)
- **Event** = Significant code changes/features (e.g., Dragon's Hoard Discovery)

Each entry contains:

- Content written from AI agent's perspective
- "Relevant connections for the agent's work"
- "Unique characteristics that matter"
- "Important background information"

### Example Flow

A git commit becomes a story:

- Bug fix → "Dot vanquished the daemon with his 4000-token blade"
- New feature → "Amy discovered a new spell in the forest glade"
- Refactor → "The architect restructured the realm's foundations"

This is the **"every bash command became a spell"** philosophy in action.

## Architecture Overview

### Agent/Context/Orchestrator Pattern

**Orchestrator** (`orchestrator/orchestrator.py`):

- Creates session contexts with timestamp-based IDs
- Loads numbered knowledge from `lorefiles/skogai/current/goose-memory-backup/`
- Wraps shell tools in `tools/` directory
- Knowledge mapping by task type: content (00,10,20,101), lore (00,10,300,303), research (00,10,02)
- **TODO**: Connect pipeline - ingest git diff → call existing tools → link to session

### Existing Lore Tools

### generate-agent-lore.py

Creates a complete specialized lorebook for an agent type. The LLM determines what lore the agent needs, then generates all content.

**Usage:**

```bash
# Create lorebook for an agent type
python generate-agent-lore.py --agent-type orchestrator --provider claude

# With custom description
python generate-agent-lore.py --agent-type "medieval-storyteller" \
  --description "A village elder who narrates code changes as fantasy tales" \
  --provider claude

# Create persona and link to the lorebook
python generate-agent-lore.py --agent-type researcher --provider claude --create-persona

# Link to existing persona
python generate-agent-lore.py --agent-type writer --provider claude --persona persona_1234567890

# Export to SillyTavern format
python generate-agent-lore.py --agent-type narrator --provider claude --export ./exports/
```

**What it does:**

1. `determine_agent_needs()` - LLM analyzes agent type and suggests 0-3 entries per category (character/place/object/event/concept)
2. `generate_lore_entry()` - For each suggested entry, LLM generates rich content tailored to the agent
3. Creates lorebook and adds all entries
4. Optionally creates/links persona

**Output:** Lorebook like "Specialized Lore for Orchestrator Agent" with entries like Village Elder, Greenhaven, Ancient Tome, etc.

---

### tools/llama-lore-creator.sh

LLM-powered generation of lore content from scratch.

#### entry

Generate a single lore entry with LLM-created content.

```bash
LLM_PROVIDER=claude ./tools/llama-lore-creator.sh - entry "The Crystal Forest" "place"
```

**What it does:**

1. Creates empty entry via manage-lore.sh
2. LLM generates 2-3 paragraphs of rich content
3. Updates entry with generated content
4. Sets summary to "Generated by [model]"

**Categories:** character, place, object, event, concept, custom

#### persona

Generate a persona with LLM-determined traits and voice.

```bash
LLM_PROVIDER=claude ./tools/llama-lore-creator.sh - persona "Elara" "An elven sorceress"
```

**What it does:**

1. LLM generates TRAITS (comma-separated) and VOICE description
2. Creates persona via create-persona.sh with those values
3. Falls back to defaults if LLM output can't be parsed

#### lorebook

Generate a complete lorebook with multiple entries.

```bash
LLM_PROVIDER=claude ./tools/llama-lore-creator.sh - lorebook "Eldoria" "A magical realm" 5
```

**What it does:**

1. Creates empty book via manage-lore.sh
2. LLM generates entry titles with categories (numbered list)
3. For each title, calls `entry` to generate full content
4. Adds each entry to the book

#### link

Link a persona to lore books (existing or newly generated).

```bash
# Link to existing books
LLM_PROVIDER=claude ./tools/llama-lore-creator.sh - link persona_1743770116 2

# If not enough books exist, generates new ones
```

**What it does:**

1. Gets existing books (up to count)
2. If not enough, generates a new lorebook named "{Persona}'s Chronicles"
3. Links each book to the persona via manage-lore.sh

---

### tools/llama-lore-integrator.sh

Extract and integrate existing content into the lore system.

#### extract-lore

Extract lore entities from a text file.

```bash
# Output as markdown
LLM_PROVIDER=claude ./tools/llama-lore-integrator.sh - extract-lore story.txt

# Output as JSON
LLM_PROVIDER=claude ./tools/llama-lore-integrator.sh - extract-lore story.txt json
```

**What it does:**

1. Reads first 8000 chars of file
2. LLM identifies 3-5 key entities (characters, places, objects, events, concepts)
3. Returns formatted output (markdown or JSON) with title, category, summary, content, tags

**Output formats:**

- `lore` (default): Markdown with `## [CATEGORY] TITLE` sections
- `json`: Structured JSON with entries array

#### create-entries

Create lore entries from LLM analysis output.

```bash
# Pipe analysis to create entries
ANALYSIS=$(LLM_PROVIDER=claude ./tools/llama-lore-integrator.sh - extract-lore story.txt json)
./tools/llama-lore-integrator.sh - create-entries "$ANALYSIS" book_1234567890
```

**What it does:**

1. Parses JSON or markdown analysis
2. Creates entry for each entity via manage-lore.sh
3. Updates entry with content, summary, tags
4. Optionally adds to specified book

#### create-persona

Create a persona from a character description file.

```bash
LLM_PROVIDER=claude ./tools/llama-lore-integrator.sh - create-persona character.txt
```

**What it does:**

1. Reads first 8000 chars of file
2. LLM extracts: NAME, DESCRIPTION, TRAITS, VOICE, BACKGROUND, EXPERTISE, LIMITATIONS
3. Creates persona via create-persona.sh
4. Updates with background/expertise/limitations

#### import-directory

Create a complete lorebook from a directory of files.

```bash
LLM_PROVIDER=claude ./tools/llama-lore-integrator.sh - import-directory ./docs "Documentation Lore" "Lore extracted from project docs"
```

**What it does:**

1. Creates empty lorebook
2. For each text file in directory:
   - Extracts lore via `extract-lore`
   - Creates entries via `create-entries`
   - Adds to book
3. Analyzes connections via `analyze-connections`

**This is the primary workflow for importing existing content.**

#### analyze-connections

Find and create relationships between entries in a book.

```bash
LLM_PROVIDER=claude ./tools/llama-lore-integrator.sh - analyze-connections book_1744512793
```

**What it does:**

1. Gets all entries from the specified book
2. Sends entry titles/summaries/categories to LLM
3. LLM identifies meaningful connections (3-5 minimum)
4. Updates each entry's `relationships` array with:
   - `target_id` - ID of connected entry
   - `relationship_type` - e.g., part_of, located_in, created_by, opposes, allies_with
   - `description` - Context about the connection

**Example relationship:**

```json
{
  "relationships": [
    {
      "target_id": "entry_1744513046",
      "relationship_type": "located_in",
      "description": "The Village Elder resides in Greenhaven"
    }
  ]
}
```

This turns isolated entries into a connected lore graph that agents can traverse.

---

### tools/manage-lore.sh

Basic CRUD operations for lore entries and books (no LLM required).

#### create-entry

Create an empty lore entry.

```bash
./tools/manage-lore.sh create-entry "The Dark Tower" "place"
# Output: Created lore entry: entry_1763812594_160d22f7
```

**Categories:** character, place, event, object, concept, custom

Creates JSON file with empty content - edit manually or use LLM tools to populate.

#### create-book

Create an empty lore book.

```bash
./tools/manage-lore.sh create-book "Eldoria Chronicles" "A collection of tales from the realm"
```

Creates JSON file with empty entries array and default "Introduction" section.

#### list-entries

List all lore entries.

```bash
# List all
./tools/manage-lore.sh list-entries

# Filter by category
./tools/manage-lore.sh list-entries place
```

#### list-books

List all lore books.

```bash
./tools/manage-lore.sh list-books
# Output: book_1744512793 - Specialized Lore for Orchestrator Agent (8 entries) [draft]
```

#### show-entry

Display a specific lore entry.

```bash
./tools/manage-lore.sh show-entry entry_1744512859
```

Shows: title, ID, category, summary, content, tags, created timestamp.

#### show-book

Display a specific lore book.

```bash
./tools/manage-lore.sh show-book book_1744512793
```

Shows: title, ID, description, status, structure sections, list of entries.

#### add-to-book

Add an entry to a book.

```bash
# Add to book's entry list
./tools/manage-lore.sh add-to-book entry_1763812594 book_1763812594

# Add to specific section
./tools/manage-lore.sh add-to-book entry_1763812594 book_1763812594 "Introduction"
```

**What it does:**

1. Adds entry ID to book's entries array
2. Optionally adds to specified section
3. Updates book's updated_at timestamp
4. Sets entry's book_id field

#### link-to-persona

Associate a lore book with a persona.

```bash
./tools/manage-lore.sh link-to-persona book_1763812594 persona_1763812641
```

**What it does:**

1. Adds persona to book's `readers` array
2. Adds book to persona's `knowledge.lore_books` array

This gives the persona access to the book's lore context.

#### search

Search lore entries by keyword.

```bash
./tools/manage-lore.sh search "forest"
./tools/manage-lore.sh search "quantum mojito"
```

Searches: title, content, summary, tags (case-insensitive).

---

### tools/create-persona.sh

CRUD operations for personas (no LLM required).

#### create

Create a new persona.

```bash
./tools/create-persona.sh create "Forest Guardian" "A magical protector" "compassionate,wise,gentle" "serene"
```

**Arguments:**

1. Name
2. Description
3. Traits (comma-separated)
4. Voice tone

Creates JSON with default structure for temperament, voice, background, knowledge, interaction_style.

#### list

List all personas.

```bash
./tools/create-persona.sh list
# Output: persona_1743795839 - Amy (bold, sassy, confident, witty) - 2 lore books
```

#### show

Display persona details.

```bash
./tools/create-persona.sh show persona_1763812641
```

Shows: name, ID, temperament, values, voice tone, background, expertise, limitations, linked lore books.

#### edit

Edit a persona field.

```bash
./tools/create-persona.sh edit persona_1763812641 name "New Name"
./tools/create-persona.sh edit persona_1763812641 tone "mysterious and cryptic"
./tools/create-persona.sh edit persona_1763812641 temperament "fiery"
```

**Fields:** name, description, tone, temperament

#### delete

Delete a persona.

```bash
./tools/create-persona.sh delete persona_1763812641
# Prompts for confirmation [y/N]
```

---

### Tool Status (tested 2025-12-12)

**Working (no LLM required):**

- `./tools/manage-lore.sh` - All commands work ✓
  - Fixed: Now properly writes entry and book JSON files
- `python orchestrator/orchestrator.py init [content|lore|research]` ✓
- `python agents/api/lore_api.py` ✓

**Working with LLM - All Providers Tested:**

**Shell Script Tools (Working):**

- ✓ `LLM_PROVIDER=claude ./tools/llama-lore-creator.sh - entry "Title" "category"`
- ✓ `LLM_PROVIDER=openai ./tools/llama-lore-creator.sh gpt-4 entry "Title" "category"`
- ✓ `LLM_PROVIDER=ollama ./tools/llama-lore-creator.sh llama3 entry "Title" "category"`
- ✓ `LLM_PROVIDER=claude ./tools/llama-lore-creator.sh - persona "Name" "Description"`
- ✓ `LLM_PROVIDER=claude ./tools/llama-lore-integrator.sh - extract-lore file.txt [json|lore]`

**Python Tools:**

- ✓ `python generate-agent-lore.py --provider claude --agent-type TYPE`
  - Creates lorebook with 4-10 entries (has known bug - see below)

**Integration Pipeline:**

- ✓ `./integration/lore-flow.sh manual "content"` - Runs all 5 steps
- ✓ `./integration/lore-flow.sh git-diff HEAD` - Extracts from commits

**Provider Status:**

- ✅ **Claude** - Tested and working via OpenRouter API
- ✅ **OpenAI** - Tested and working via OpenRouter API
- ✅ **Ollama** - Tested and working with local models

**Known Issues (GitHub Issues):**

⚠️ [Issue #5](https://github.com/SkogAI/lore/issues/5): LLM generates meta-commentary instead of lore content

- **Impact:** Generated content includes "I need your approval..." instead of direct narrative
- **Workaround:** Manually edit entries or fix prompt in `llama-lore-creator.sh`
- **Status:** Needs prompt engineering fix

⚠️ [Issue #6](https://github.com/SkogAI/lore/issues/6): Pipeline creates entries with empty content

- **Impact:** `lore-flow.sh` creates entry files but `content` field is empty
- **Workaround:** Use `llama-lore-creator.sh` directly instead of pipeline
- **Status:** Needs investigation in pipeline timing/paths

**Agent APIs** (`agents/api/`):

- `agent_api.py` - Core agent communication with LLM providers
- `lore_api.py` - LoreAPI class for managing lore entries, books, and personas
  - JSON-based storage in `knowledge/expanded/lore/{entries,books}/` and `knowledge/expanded/personas/`
  - Schema validation from `knowledge/core/{persona,lore}/schema.json`

**Knowledge System** (`knowledge/`):

- Numbered knowledge files (00-09 core, 10-89 expanded, 90-99 implementation)
- Index at `knowledge/INDEX.md`
- Core schemas define persona, lore_entry, and lore_book structures

### Key Agent Personalities

- **Amy Ravenwolf** - Fiery personality template
- **Claude** - Thoughtful, analytical
- **Dot** - Minimalist (4000 token philosophy)
- **Goose** - Chaos agent (HATES MINT)
- **SkogAI** - Original sentient toaster (500-800 token constraints)

## Code Style

- **Imports**: stdlib → third-party → local
- **Type Annotations**: Use `Dict`, `List`, `Optional`, `Any` from typing
- **Error Handling**: Try/except with specific exceptions and informative logging
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Documentation**: Docstrings with triple quotes for all classes/functions
- **Logging**: Use configured logger with `logger = logging.getLogger("module_name")`
- **Configuration**: Load from config files with environment variable fallbacks

## Repository Configuration

- **Default Branch**: `master` (not `main`)
- **Remote**: https://github.com/SkogAI/lore
- **Package Manager**: `uv` with `pyproject.toml` and `uv.lock`
- **Python**: 3.12+ required

## Session Handover

When ending sessions, update `docs/project/handover.md` with:

- What was accomplished
- Context and active session IDs
- Repository state and next steps

See current handover for latest session context.

## Special Considerations

- External API access required for many components (Anthropic, OpenAI, Claude Code)
- Historical preservation is critical - don't delete lore archives
- Constraints drove emergence: original SkogAI had 3800 token limits and the smolagents used even less
- The Prime Directive: "Automate EVERYTHING so we can drink mojitos on a beach"
