# Integration Layer

Automated mythology generation from codebase activity - transforms technical changes into narrative lore told through agent personas.

## Architecture

See [INTEGRATION_ARCHITECTURE.md](./INTEGRATION_ARCHITECTURE.md) for the complete vision and design.

## Current Status

✅ **Working** - lore-flow.sh (manual/git-diff mode)
🚧 **In Progress** - Git author → persona mapping
📋 **Planned** - Automated workflow triggers

## Quick Start

### Manual Lore Generation

```bash
# Generate lore from a message
./integration/lore-flow.sh manual "Amy implemented quantum mojito generator"

# Generate from git commit
./integration/lore-flow.sh git-diff HEAD

# Generate from previous commits
./integration/lore-flow.sh git-diff HEAD~3
```

## What It Does

```
Input (git diff/log/message)
  ↓
Extract content
  ↓
Select persona (Amy Ravenwolf by default)
  ↓
Load persona context → persona-manager.py
  ↓
Generate narrative → llama-lore-integrator.sh (LLM call)
  ↓
Create lore entry → manage-lore.sh
  ↓
Add to persona's chronicle book
  ↓
Done!
```

## Components

### lore-flow.sh

Main workflow orchestrator - handles input → persona → LLM → storage pipeline.

**Usage:**
```bash
./integration/lore-flow.sh [input-type] [content]
```

**Input Types:**
- `git-diff` - Extract from git commit
- `log` - Read from log file
- `manual` - Direct message input

### persona-bridge/

Contains persona-manager.py for loading persona context and rendering prompts.

**Direct Usage:**
```bash
# List all personas
python3 integration/persona-bridge/persona-manager.py

# Render specific persona prompt
python3 integration/persona-bridge/persona-manager.py --persona persona_1744992765 --render-prompt
```

### workflows/

Future automation:
- Git hooks (post-commit)
- Scheduled batch processing
- Test workflows

## Configuration

### Persona Selection

Currently hardcoded to Amy Ravenwolf (`persona_1744992765`).

**TODO:** Add git author → persona mapping:
```bash
# In lore-flow.sh, around line 80:
case $GIT_AUTHOR in
  "skogix")
    PERSONA_ID="persona_1744992765"  # Amy
    ;;
  "other-author")
    PERSONA_ID="persona_XXXXX"       # Other persona
    ;;
  *)
    PERSONA_ID="persona_1763820091"  # Village Elder (default narrator)
    ;;
esac
```

### LLM Provider

Uses existing llama-lore-integrator.sh which expects:
- `LLM_PROVIDER` environment variable (claude, gpt-4, llama3)
- Appropriate API keys configured

## Examples

### Basic Usage

```bash
$ ./integration/lore-flow.sh manual "Fixed critical bug in quantum mojito mixer"

=== Lore Generation Flow ===
Session: 1764315234
Input Type: manual

[1/5] Extracting content...
Content extracted: 47 characters

[2/5] Selecting persona...
Selected persona: Amy Ravenwolf (persona_1744992765)

[3/5] Loading persona context...
Persona context loaded

[4/5] Generating narrative...
Using llama-lore-integrator.sh to generate narrative...
Narrative generated: 342 characters

[5/5] Creating lore entry...
Creating lore entry: Amy Ravenwolf's Tale - Session 1764315234
Category: event
Entry created: entry_1764315234_a4b3c2d1
Entry updated with narrative
Adding entry to chronicle: book_1764315000

=== Lore Generation Complete ===
Entry ID: entry_1764315234_a4b3c2d1
Persona: Amy Ravenwolf (persona_1744992765)
Chronicle: book_1764315000
Session: 1764315234

View entry: ./tools/manage-lore.sh show-entry entry_1764315234_a4b3c2d1
```

### Git Integration

```bash
# After committing code
git commit -m "feat: add quantum superposition to mojito mixer"

# Generate lore for that commit
./integration/lore-flow.sh git-diff HEAD

# The lore entry will:
# - Use commit message as title
# - Extract git author as persona
# - Include full diff in narrative context
# - Save to persona's chronicle
```

## Future Automation

### Git Hook

Add to `.git/hooks/post-commit`:
```bash
#!/bin/bash
./integration/lore-flow.sh git-diff HEAD &
```

### Daily Digest

Cron job to process all activity:
```bash
# Run at midnight
0 0 * * * cd /path/to/lore && ./integration/workflows/daily-digest.sh
```

## Dependencies

- `orchestrator/orchestrator.py` - Context creation, knowledge loading
- `agents/api/lore_api.py` - Python API for lore management
- `tools/llama-lore-integrator.sh` - LLM narrative generation
- `tools/manage-lore.sh` - Lore CRUD operations
- `tools/create-persona.sh` - Persona management
- `integration/persona-bridge/persona-manager.py` - Persona context loading

## Troubleshooting

### No narrative generated

Check that `llama-lore-integrator.sh` can access LLM:
```bash
export LLM_PROVIDER=claude
./tools/llama-lore-integrator.sh - extract-lore test.txt
```

### Persona not found

List available personas:
```bash
./tools/create-persona.sh list
```

Update `PERSONA_ID` in lore-flow.sh to a valid ID.

### Entry not created

Check lore directory permissions:
```bash
ls -la knowledge/expanded/lore/entries/
ls -la knowledge/expanded/lore/books/
```

## Next Steps

1. ✅ Basic manual lore generation - **DONE**
2. 🚧 Git author → persona mapping - **IN PROGRESS**
3. 📋 Automated git hook integration - PLANNED
4. 📋 Batch processing workflow - PLANNED
5. 📋 Lore relationship auto-linking - PLANNED
