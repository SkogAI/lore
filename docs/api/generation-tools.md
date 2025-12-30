# Generation Tools API

Complete reference for all lore generation endpoints and tools in the Lore system.

## Overview

The Lore system provides multiple tools for generating content with LLM assistance:

- **generate-agent-lore.py** - Python script for specialized agent lorebooks
- **llama-lore-creator.sh** - Shell script for creating individual lore components
- **llama-lore-integrator.sh** - Shell script for extracting lore from existing content
- **create-persona.sh** - Shell script for persona CRUD operations
- **context-manager.sh** - Shell script for session context lifecycle
- **manage-lore.sh** - Shell script for basic lore CRUD operations (deprecated)

All LLM-powered tools support three providers:
- **ollama** - Local models (default)
- **claude** - Claude CLI
- **openai** - OpenAI API (includes OpenRouter)

---

## generate-agent-lore.py

Python tool that creates specialized lorebooks for agent types using LLM analysis.

### Purpose

Generates a complete lorebook tailored to a specific agent type by:
1. Analyzing agent needs via LLM
2. Generating 0-3 entries per category (character, place, object, event, concept)
3. Creating narrative content for each entry
4. Optionally creating/linking a persona

### Location

`generate-agent-lore.py` (repository root)

### Usage

```bash
python generate-agent-lore.py --agent-type TYPE --provider PROVIDER [OPTIONS]
```

### Parameters

**Required:**
- `--agent-type TYPE` - Agent type (e.g., orchestrator, researcher, writer)

**Optional:**
- `--description DESC` - Agent purpose description
- `--model MODEL` - LLM model name (default: llama3)
- `--provider {ollama,claude,openai}` - LLM provider (default: ollama)
- `--persona PERSONA_ID` - Link to existing persona
- `--create-persona` - Create new persona for agent type
- `--export PATH` - Export as SillyTavern lorebook

### Environment Variables

**For OpenAI provider:**
- `OPENAI_API_KEY` or `OPENROUTER_API_KEY` - API key
- `OPENAI_BASE_URL` - API endpoint (default: https://openrouter.ai/api/v1)

**For Claude provider:**
- Requires `$SKOGAI_LORE/orchestrator/lore-writer.md` system prompt

### Examples

```bash
# Basic usage with local model
python generate-agent-lore.py --agent-type orchestrator --provider ollama

# Use Claude with custom description
python generate-agent-lore.py \
  --agent-type "medieval-storyteller" \
  --description "A village elder who narrates code changes as fantasy tales" \
  --provider claude

# Create persona and link
python generate-agent-lore.py \
  --agent-type researcher \
  --provider openai \
  --model gpt-4 \
  --create-persona

# Link to existing persona
python generate-agent-lore.py \
  --agent-type writer \
  --provider claude \
  --persona persona_1234567890

# Export to SillyTavern
python generate-agent-lore.py \
  --agent-type narrator \
  --provider claude \
  --export ./exports/
```

### Output

Creates:
- **Lorebook**: `knowledge/expanded/lore/books/book_<timestamp>.json`
- **Entries**: 4-10 entries across categories in `knowledge/expanded/lore/entries/`
- **Persona** (optional): `knowledge/expanded/personas/persona_<timestamp>.json`

### Core Functions

#### determine_agent_needs(agent_type, agent_description, model, provider)

Analyzes agent requirements and suggests lore entries.

**Returns:** Dict with categories (character/place/object/event/concept) containing entry suggestions

```python
{
  "character": [
    {"title": "Character Name", "reason": "Brief explanation"}
  ],
  "place": [...],
  ...
}
```

#### generate_lore_entry(title, category, agent_type, model, provider)

Generates narrative content for a specific entry.

**Returns:** String with 2-3 paragraphs of narrative prose

Includes meta-commentary stripping to ensure clean output.

#### create_specialized_lorebook(api, agent_type, agent_description, model, provider)

Complete workflow to create lorebook with all entries.

**Returns:**
```python
{
  "success": True,
  "book_id": "book_1234567890",
  "categories": {"character": [...], "place": [...]},
  "entry_count": 8
}
```

#### create_persona_with_lore(api, agent_type, model, book_id, provider)

Creates persona with LLM-generated traits and links to lorebook.

**Returns:**
```python
{
  "success": True,
  "persona_id": "persona_1234567890",
  "name": "Generated Name",
  "description": "..."
}
```

### Known Issues

⚠️ **Issue #5**: LLM may generate meta-commentary instead of direct narrative
- **Workaround**: Script includes stripping logic, but may not catch all cases
- **Status**: Prompt engineering improvements needed

---

## llama-lore-creator.sh

Shell script for creating individual lore components with LLM-generated content.

### Purpose

Generate lore content from scratch using LLM assistance for:
- Individual entries with rich narrative
- Personas with generated traits
- Complete lorebooks with multiple entries
- Linking personas to lore books

### Location

`tools/llama-lore-creator.sh`

### Usage

```bash
[LLM_PROVIDER=provider] ./tools/llama-lore-creator.sh [model] [command] [args]
```

### Commands

#### entry

Generate a single lore entry with LLM content.

```bash
LLM_PROVIDER=claude ./tools/llama-lore-creator.sh - entry "The Crystal Forest" "place"
```

**Arguments:**
1. Title (string)
2. Category (character|place|object|event|concept|custom)

**Process:**
1. Creates empty entry via manage-lore.sh
2. LLM generates 2-3 paragraphs of content
3. Updates entry with content and summary
4. Validates output for meta-commentary

**Output:** Entry ID (e.g., entry_1234567890_abc123)

#### persona

Generate a persona with LLM-determined traits.

```bash
LLM_PROVIDER=claude ./tools/llama-lore-creator.sh - persona "Elara" "An elven sorceress"
```

**Arguments:**
1. Name (string)
2. Description (string)

**Process:**
1. LLM generates TRAITS (comma-separated) and VOICE description
2. Creates persona via create-persona.sh
3. Falls back to defaults if parsing fails

**Output:** Persona ID (e.g., persona_1234567890)

#### lorebook

Generate a complete lorebook with multiple entries.

```bash
LLM_PROVIDER=claude ./tools/llama-lore-creator.sh - lorebook "Eldoria" "A magical realm" 5
```

**Arguments:**
1. Title (string)
2. Description (string)
3. Entry count (number, default: 3)

**Process:**
1. Creates empty book via manage-lore.sh
2. LLM generates entry titles with categories
3. For each title, calls `entry` command to generate content
4. Adds all entries to book

**Output:** Book ID (e.g., book_1234567890)

#### link

Link a persona to lore books.

```bash
LLM_PROVIDER=claude ./tools/llama-lore-creator.sh - link persona_1234567890 2
```

**Arguments:**
1. Persona ID (string)
2. Book count (number, default: 1)

**Process:**
1. Gets existing books (up to count)
2. If not enough, generates new book titled "{Persona}'s Chronicles"
3. Links each book to persona via manage-lore.sh

### Environment Variables

- `LLM_PROVIDER` - Provider to use: ollama (default), claude, openai
- `OPENAI_API_KEY` / `OPENROUTER_API_KEY` - For openai provider
- `OPENAI_BASE_URL` - API endpoint (default: https://openrouter.ai/api/v1)

### Provider Setup

**Ollama:**
```bash
# Auto-pulls model if not found
LLM_PROVIDER=ollama ./tools/llama-lore-creator.sh llama3.2:3b entry "Title" "place"
```

**Claude:**
```bash
# Requires Claude CLI installed
npm install -g @anthropic-ai/claude-code
LLM_PROVIDER=claude ./tools/llama-lore-creator.sh - entry "Title" "place"
```

**OpenAI/OpenRouter:**
```bash
# Requires API key
export OPENROUTER_API_KEY="sk-or-v1-..."
LLM_PROVIDER=openai ./tools/llama-lore-creator.sh gpt-4 entry "Title" "place"
```

### Output Validation

The script includes validation functions:

**validate_lore_output(content):**
- Checks for meta-commentary patterns
- Validates minimum word count (100+)
- Returns 0 on success, 1 on failure

**strip_meta_commentary(content):**
- Removes first line if it contains meta-commentary
- Patterns: "I will", "Let me", "Here is", "This entry", etc.

### Examples

```bash
# Create entry with local model
LLM_PROVIDER=ollama ./tools/llama-lore-creator.sh llama3 entry "The Void" "place"

# Create persona with Claude
LLM_PROVIDER=claude ./tools/llama-lore-creator.sh - persona "Amy" "Bold researcher"

# Generate lorebook with OpenAI
export OPENROUTER_API_KEY="sk-or-v1-..."
LLM_PROVIDER=openai ./tools/llama-lore-creator.sh gpt-4 lorebook "My World" "Fantasy setting" 10

# Link persona to books
LLM_PROVIDER=claude ./tools/llama-lore-creator.sh - link persona_1743770116 3
```

---

## llama-lore-integrator.sh

Shell script for extracting and integrating existing content into the lore system.

### Purpose

Transform existing documents, files, and directories into lore entries by:
- Extracting narrative elements from text
- Creating personas from character descriptions
- Building lorebooks from document directories
- Analyzing relationships between entries

### Location

`tools/llama-lore-integrator.sh`

### Usage

```bash
[LLM_PROVIDER=provider] ./tools/llama-lore-integrator.sh [model] [command] [args]
```

### Commands

#### extract-lore

Extract lore entities from a text file.

```bash
# Output as markdown
LLM_PROVIDER=claude ./tools/llama-lore-integrator.sh - extract-lore story.txt

# Output as JSON
LLM_PROVIDER=claude ./tools/llama-lore-integrator.sh - extract-lore story.txt json
```

**Arguments:**
1. File path (string)
2. Output format (lore|json, default: lore)

**Process:**
1. Reads first 8000 chars of file
2. LLM identifies 3-5 key entities (characters, places, objects, events, concepts)
3. Returns formatted output with title, category, summary, content, tags

**Output formats:**

**Markdown (lore):**
```markdown
---
## [CATEGORY] Title

**Summary**: One sentence essence

**Content**:
[Narrative prose]

**Tags**: tag1, tag2, tag3
---
```

**JSON:**
```json
{
  "entries": [
    {
      "title": "Entity Name",
      "category": "character",
      "summary": "...",
      "content": "...",
      "tags": ["tag1", "tag2"]
    }
  ]
}
```

#### create-entries

Create lore entries from LLM analysis output.

```bash
# From JSON analysis
ANALYSIS=$(LLM_PROVIDER=claude ./tools/llama-lore-integrator.sh - extract-lore story.txt json)
./tools/llama-lore-integrator.sh - create-entries "$ANALYSIS" book_1234567890

# From markdown analysis
ANALYSIS=$(LLM_PROVIDER=claude ./tools/llama-lore-integrator.sh - extract-lore story.txt lore)
./tools/llama-lore-integrator.sh - create-entries "$ANALYSIS"
```

**Arguments:**
1. Analysis text (JSON or markdown string)
2. Book ID (optional) - adds all entries to specified book

**Process:**
1. Parses JSON or markdown analysis
2. Creates entry for each entity via manage-lore.sh
3. Updates entries with content, summary, tags
4. Optionally adds to specified book

#### create-persona

Create a persona from a character description file.

```bash
LLM_PROVIDER=claude ./tools/llama-lore-integrator.sh - create-persona character.txt
```

**Arguments:**
1. File path (string)

**Process:**
1. Reads first 8000 chars of file
2. LLM extracts: NAME, DESCRIPTION, TRAITS, VOICE, BACKGROUND, EXPERTISE, LIMITATIONS
3. Creates persona via create-persona.sh
4. Updates with background/expertise/limitations

**Output:** Persona ID

#### analyze-connections

Find and create relationships between entries in a book.

```bash
LLM_PROVIDER=claude ./tools/llama-lore-integrator.sh - analyze-connections book_1744512793
```

**Arguments:**
1. Book ID (string)

**Process:**
1. Gets all entries from book
2. Sends entry titles/summaries/categories to LLM
3. LLM identifies meaningful connections (3-5 minimum)
4. Updates each entry's `relationships` array

**Relationship types:**
- `part_of` - Component relationship
- `located_in` - Spatial relationship
- `created_by` - Creation relationship
- `opposes` - Opposition relationship
- `allies_with` - Alliance relationship

**Example relationship:**
```json
{
  "target_id": "entry_1744513046",
  "relationship_type": "located_in",
  "description": "The Village Elder resides in Greenhaven"
}
```

#### import-directory

Create a complete lorebook from a directory of files.

```bash
LLM_PROVIDER=claude ./tools/llama-lore-integrator.sh - import-directory ./docs "Documentation Lore" "Lore extracted from project docs"
```

**Arguments:**
1. Directory path (string)
2. Book title (string)
3. Book description (string)

**Process:**
1. Creates empty lorebook
2. For each text file in directory:
   - Extracts lore via `extract-lore`
   - Creates entries via `create-entries`
   - Adds to book
3. Analyzes connections via `analyze-connections`

**This is the primary workflow for importing existing content.**

### Examples

```bash
# Extract from document
LLM_PROVIDER=claude ./tools/llama-lore-integrator.sh - extract-lore worldbuilding.txt json

# Create entries and add to book
ANALYSIS=$(LLM_PROVIDER=claude ./tools/llama-lore-integrator.sh - extract-lore story.txt json)
./tools/llama-lore-integrator.sh - create-entries "$ANALYSIS" book_1234567890

# Create persona from character bio
LLM_PROVIDER=claude ./tools/llama-lore-integrator.sh - create-persona character-bio.txt

# Import entire documentation directory
LLM_PROVIDER=openai ./tools/llama-lore-integrator.sh gpt-4 import-directory ./world "World Lore" "Complete world documentation"

# Analyze connections in existing book
LLM_PROVIDER=claude ./tools/llama-lore-integrator.sh - analyze-connections book_1744512793
```

### Environment Variables

Same as llama-lore-creator.sh:
- `LLM_PROVIDER` - ollama (default), claude, openai
- `OPENAI_API_KEY` / `OPENROUTER_API_KEY`
- `OPENAI_BASE_URL`

---

## create-persona.sh

Shell script for persona CRUD operations without LLM assistance.

### Purpose

Direct manipulation of persona JSON files for:
- Creating personas with specified traits
- Listing all personas
- Viewing persona details
- Editing persona fields
- Deleting personas

### Location

`tools/create-persona.sh`

### Usage

```bash
./tools/create-persona.sh [command] [args]
```

### Commands

#### create

Create a new persona.

```bash
./tools/create-persona.sh create "Forest Guardian" "A magical protector" "compassionate,wise,gentle" "serene"
```

**Arguments:**
1. Name (string)
2. Description (string)
3. Traits (comma-separated)
4. Voice tone (string)

**Creates:** `knowledge/expanded/personas/persona_<timestamp>.json`

**Structure:**
```json
{
  "id": "persona_<timestamp>",
  "name": "...",
  "core_traits": {
    "temperament": "balanced",
    "values": ["trait1", "trait2", ...],
    "motivations": []
  },
  "voice": {
    "tone": "...",
    "patterns": [],
    "vocabulary": "standard"
  },
  "background": {...},
  "knowledge": {
    "expertise": [],
    "limitations": [],
    "lore_books": []
  },
  "interaction_style": {...},
  "meta": {
    "version": "1.0",
    "created": "...",
    "modified": "..."
  }
}
```

#### list

List all personas with summary.

```bash
./tools/create-persona.sh list
```

**Output:**
```
persona_1743795839 - Amy (bold, sassy, confident, witty) - 2 lore books
persona_1744992765 - Forest Guardian (compassionate, wise, gentle) - 0 lore books
```

#### show

Display detailed persona information.

```bash
./tools/create-persona.sh show persona_1763812641
```

**Output:**
```
=== Persona: Forest Guardian ===
ID: persona_1763812641

Core Traits:
  Temperament: balanced
  Values: compassionate, wise, gentle

Voice:
  Tone: serene

Background:
  Origin:

Knowledge:
  Expertise:
  Limitations:

Lore Books:
  None
```

#### edit

Edit a persona field.

```bash
./tools/create-persona.sh edit persona_1763812641 name "New Name"
./tools/create-persona.sh edit persona_1763812641 tone "mysterious and cryptic"
./tools/create-persona.sh edit persona_1763812641 temperament "fiery"
```

**Arguments:**
1. Persona ID (string)
2. Field (name|description|tone|temperament)
3. Value (string)

**Note:** Updates `meta.modified` timestamp automatically

#### delete

Delete a persona with confirmation.

```bash
./tools/create-persona.sh delete persona_1763812641
```

**Prompts:** `Are you sure you want to delete persona: ... (ID)? [y/N]`

### Examples

```bash
# Create new persona
./tools/create-persona.sh create "Amy Ravenwolf" "Bold researcher" "fiery,sassy,confident,witty" "sharp and direct"

# List all personas
./tools/create-persona.sh list

# View details
./tools/create-persona.sh show persona_1743795839

# Edit voice tone
./tools/create-persona.sh edit persona_1743795839 tone "bold and analytical"

# Delete persona
./tools/create-persona.sh delete persona_1763812641
```

---

## context-manager.sh

Shell script for session context lifecycle management.

### Purpose

Manage session contexts for tracking:
- Session state across workflows
- Active knowledge and personas
- Orchestrator mode and configuration
- Session history and timeline

### Location

`tools/context-manager.sh`

### Usage

```bash
./tools/context-manager.sh [command] [args]
```

### Commands

#### create

Create new context from template.

```bash
session_id=$(./tools/context-manager.sh create base)
echo $session_id
# Output: 1764990069
```

**Arguments:**
1. Template name (string) - loads from `context/templates/<name>-context.json`
2. Context type (string, optional, default: "base")

**Process:**
1. Copies template file
2. Sets `session_id` to current timestamp
3. Sets `created` and `last_updated` to current ISO timestamp
4. Sets `context_type` to specified type

**Creates:** `context/current/context-<session_id>.json`

**Returns:** Session ID (timestamp)

#### update

Update a field in existing context.

```bash
./tools/context-manager.sh update 1764990069 "system_state.orchestrator_mode" "lore"
```

**Arguments:**
1. Session ID (string)
2. Key (string) - jq path notation
3. Value (string)

**Process:**
1. Updates specified field using jq
2. Updates `last_updated` timestamp

#### archive

Move context from current to archive.

```bash
./tools/context-manager.sh archive 1764990069
```

**Arguments:**
1. Session ID (string)

**Process:**
- Moves file from `context/current/` to `context/archive/`

### Context Structure

**Base template** (`context/templates/base-context.json`):
```json
{
  "session_id": "",
  "created": "",
  "last_updated": "",
  "context_type": "base",
  "system_state": {
    "orchestrator_mode": "",
    "memory_priority": "core"
  },
  "active_knowledge": [],
  "prepared": {}
}
```

**Persona template** (`context/templates/persona-context.json`):
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

### Integration

**With orchestrator:**
```bash
# Create context for lore generation
session_id=$(./tools/context-manager.sh create base)
./tools/context-manager.sh update $session_id "system_state.orchestrator_mode" "lore"
./tools/context-manager.sh update $session_id "prepared.topic" "quantum computing"

# ... perform work ...

# Archive when complete
./tools/context-manager.sh archive $session_id
```

### Examples

```bash
# Create base context
session_id=$(./tools/context-manager.sh create base)

# Update orchestrator mode
./tools/context-manager.sh update $session_id "system_state.orchestrator_mode" "lore"

# Update active persona
./tools/context-manager.sh update $session_id "prepared.persona_id" "persona_1744992765"

# Archive session
./tools/context-manager.sh archive $session_id

# Create persona-specific context
session_id=$(./tools/context-manager.sh create persona "persona")
```

---

## manage-lore.sh

Shell script for basic lore CRUD operations.

### ⚠️ Deprecation Notice

This bash tool is deprecated in favor of the Python API (`agents/api/lore_api.py`).

See `docs/guides/migration/MIGRATION_GUIDE.md` for migration instructions.

### Purpose

Provides basic file operations for:
- Creating empty entries and books
- Listing and viewing lore
- Adding entries to books
- Linking books to personas
- Searching lore
- Schema validation

### Location

`tools/manage-lore.sh`

### Usage

```bash
./tools/manage-lore.sh [command] [args]
```

### Commands

#### create-entry

Create an empty lore entry.

```bash
./tools/manage-lore.sh create-entry "The Dark Tower" "place"
```

**Arguments:**
1. Title (string)
2. Category (character|place|event|object|concept|custom)

**Creates:** `knowledge/expanded/lore/entries/entry_<timestamp>_<hash>.json`

**Output:** Entry ID

#### create-book

Create an empty lore book.

```bash
./tools/manage-lore.sh create-book "Eldoria Chronicles" "A collection of tales from the realm"
```

**Arguments:**
1. Title (string)
2. Description (string)

**Creates:** `knowledge/expanded/lore/books/book_<timestamp>_<hash>.json`

**Output:** Book ID

#### list-entries

List all lore entries.

```bash
# List all
./tools/manage-lore.sh list-entries

# Filter by category
./tools/manage-lore.sh list-entries place
```

**Arguments:**
1. Category (optional) - filter by category

#### list-books

List all lore books.

```bash
./tools/manage-lore.sh list-books
```

**Output:**
```
book_1744512793 - Specialized Lore for Orchestrator Agent (8 entries) [draft]
```

#### show-entry

Display a specific lore entry.

```bash
./tools/manage-lore.sh show-entry entry_1744512859
```

**Output:**
```
Lore Entry: The Village Elder
ID: entry_1744512859
Category: character
---
Summary: ...
---
Content:
[narrative content]
---
Tags: character, lore
Created: 2025-01-15T10:30:00Z by skogix
```

#### show-book

Display a specific lore book.

```bash
./tools/manage-lore.sh show-book book_1744512793
```

**Output:**
```
Lore Book: Specialized Lore for Orchestrator Agent
ID: book_1744512793
Description: ...
Status: draft
---
Structure:
• Introduction: Overview of this lore book
---
Entries (8):
• The Village Elder (entry_1744512859)
• Greenhaven (entry_1744512860)
...
```

#### add-to-book

Add an entry to a book.

```bash
# Add to book's entry list
./tools/manage-lore.sh add-to-book entry_1763812594 book_1763812594

# Add to specific section
./tools/manage-lore.sh add-to-book entry_1763812594 book_1763812594 "Introduction"
```

**Arguments:**
1. Entry ID (string)
2. Book ID (string)
3. Section name (optional)

**Process:**
1. Adds entry ID to book's `entries` array
2. Optionally adds to specified section
3. Updates book's `updated_at` timestamp
4. Sets entry's `book_id` field

#### link-to-persona

Associate a lore book with a persona.

```bash
./tools/manage-lore.sh link-to-persona book_1763812594 persona_1763812641
```

**Arguments:**
1. Book ID (string)
2. Persona ID (string)

**Process:**
1. Adds persona to book's `readers` array
2. Adds book to persona's `knowledge.lore_books` array

#### search

Search lore entries by keyword.

```bash
./tools/manage-lore.sh search "forest"
./tools/manage-lore.sh search "quantum mojito"
```

**Arguments:**
1. Query (string)

**Searches:** title, content, summary, tags (case-insensitive)

#### validate-entry

Validate an entry JSON file against schema.

```bash
./tools/manage-lore.sh validate-entry knowledge/expanded/lore/entries/entry_1234567890.json
```

#### validate-book

Validate a book JSON file against schema.

```bash
./tools/manage-lore.sh validate-book knowledge/expanded/lore/books/book_1234567890.json
```

### Features

- **Schema validation** using jq
- **Input sanitization** for safe file operations
- **Atomic updates** (write to temp, then move)
- **Error handling** with cleanup
- **Duplicate detection** with warnings

### Migration to Python API

**Old (bash):**
```bash
./tools/manage-lore.sh create-entry "Title" "place"
```

**New (Python):**
```python
from agents.api.lore_api import LoreAPI

lore = LoreAPI()
entry = lore.create_lore_entry(
    title="Title",
    content="...",
    category="place"
)
```

---

## Provider Comparison

| Feature | Ollama | Claude | OpenAI |
|---------|--------|--------|--------|
| **Cost** | Free | Paid | Paid |
| **Speed** | Fast (local) | Medium | Medium |
| **Quality** | Model-dependent | High | High |
| **Setup** | `ollama pull model` | `npm install -g @anthropic-ai/claude-code` | API key only |
| **Offline** | Yes | No | No |
| **API Key** | Not required | Not required (CLI) | Required |

### Provider Selection Guide

**Use Ollama when:**
- Working offline
- Need fast iteration
- Cost is a concern
- Have local GPU resources

**Use Claude when:**
- Need highest quality narrative
- Working with complex lore
- Budget allows for API calls
- Have Claude CLI installed

**Use OpenAI when:**
- Need GPT-4 capabilities
- Using OpenRouter for model access
- Want multiple model options
- Need reliable API access

---

## Common Workflows

### 1. Create Specialized Agent Lorebook

```bash
# With Python
python generate-agent-lore.py \
  --agent-type orchestrator \
  --provider claude \
  --create-persona

# With shell script
LLM_PROVIDER=claude ./tools/llama-lore-creator.sh - lorebook \
  "Orchestrator Lore" \
  "Knowledge for orchestrator agents" \
  8
```

### 2. Import Existing Documentation

```bash
# Extract and create lorebook from directory
LLM_PROVIDER=openai ./tools/llama-lore-integrator.sh gpt-4 import-directory \
  ./docs \
  "Project Documentation Lore" \
  "Lore extracted from project documentation"
```

### 3. Create Persona with Chronicles

```bash
# Create persona
./tools/create-persona.sh create \
  "Amy Ravenwolf" \
  "Bold quantum researcher" \
  "fiery,analytical,curious,witty" \
  "sharp and direct"

# Link to lore books
persona_id=$(ls -t knowledge/expanded/personas/ | head -n 1 | sed 's/\.json//')
LLM_PROVIDER=claude ./tools/llama-lore-creator.sh - link $persona_id 2
```

### 4. Extract Lore from Story File

```bash
# Extract entities
ANALYSIS=$(LLM_PROVIDER=claude ./tools/llama-lore-integrator.sh - extract-lore story.txt json)

# Create book
./tools/manage-lore.sh create-book "Story Lore" "Entities from story.txt"
book_id=$(ls -t knowledge/expanded/lore/books/ | head -n 1 | sed 's/\.json//')

# Create entries and add to book
./tools/llama-lore-integrator.sh - create-entries "$ANALYSIS" $book_id

# Analyze connections
LLM_PROVIDER=claude ./tools/llama-lore-integrator.sh - analyze-connections $book_id
```

### 5. Session Context Management

```bash
# Create session context
session_id=$(./tools/context-manager.sh create base)

# Configure for lore generation
./tools/context-manager.sh update $session_id "system_state.orchestrator_mode" "lore"
./tools/context-manager.sh update $session_id "prepared.persona_id" "persona_1744992765"
./tools/context-manager.sh update $session_id "prepared.topic" "quantum computing"

# ... perform work ...

# Archive when done
./tools/context-manager.sh archive $session_id
```

---

## Error Handling

### Common Issues

**Issue #5: Meta-commentary in content**
```
Content: "I will create a narrative about..."
```
**Solution:** Both llama-lore-creator.sh and generate-agent-lore.py include stripping logic

**Issue #6: Empty content field**
```json
{"content": ""}
```
**Solution:** Use llama-lore-creator.sh directly instead of integration pipeline

**Provider errors:**
```
Error: No API key found
```
**Solution:** Set `OPENAI_API_KEY` or `OPENROUTER_API_KEY` environment variable

**Model not found:**
```
Model 'llama3' not found
```
**Solution:** Run `ollama pull llama3` or specify correct model name

---

## Testing Status

✅ **Verified Working:**
- All shell script tools with all three providers
- Python generate-agent-lore.py with all providers
- Integration pipeline (lore-flow.sh) end-to-end

⚠️ **Known Issues:**
- Issue #5: LLM meta-commentary (prompt engineering needed)
- Issue #6: Pipeline content update bug (timing/paths)

**Last tested:** 2025-12-12

---

## See Also

- **[Entry API](./entry.md)** - Lore entry operations
- **[Book API](./book.md)** - Lore book operations
- **[Persona API](./persona.md)** - Persona operations
- **[Integration Pipeline](../CLAUDE.md#integration-pipeline)** - Automated lore generation
