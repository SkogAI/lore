# Python API Deprecation Notice

**Status**: DEPRECATED as of 2026-01-05  
**Affects**: `agents/api/lore_api.py`, `agents/api/agent_api.py`

## Summary

The Python API layer for lore management is deprecated due to known reliability issues. Shell tools are now the canonical, supported interface for all lore operations.

## Background

During development and real-world usage, the Python API demonstrated several reliability issues:

- Inconsistent behavior ("broken as fudge" per session memories)
- Complex dependency chain making debugging difficult
- Shell tools proved more reliable and easier to maintain
- Better integration with existing Unix toolchain

## What This Means

### ✅ Use These (Recommended)

**Shell Tools** - PRIMARY, actively maintained:
- `tools/manage-lore.sh` - CRUD operations for entries and books
- `tools/create-persona.sh` - CRUD operations for personas  
- `tools/llama-lore-creator.sh` - LLM-powered content generation
- `tools/llama-lore-integrator.sh` - Extract lore from documents
- `integration/lore-flow.sh` - Complete automation pipeline

**CLI** - argc-based interface:
- `argc create-entry` - Create entries
- `argc create-book` - Create books
- `argc create-persona` - Create personas
- `argc list-books` - List all books
- `argc show-book <id>` - Display book details

**jq Transforms** - Direct JSON manipulation:
- `scripts/jq/crud-get/` - Get values from JSON
- `scripts/jq/crud-set/` - Set values in JSON
- `scripts/jq/crud-delete/` - Delete values from JSON

### ⚠️ Avoid These (Deprecated)

**Python API** - Has known issues, deprecated:
- `agents/api/lore_api.py` - LoreAPI class
- `agents/api/agent_api.py` - AgentAPI class

### 🔧 Still Using Python API

Some tools still use the Python API internally and will be migrated over time:
- `integration/persona-bridge/persona-manager.py` - Persona context management
- `generate-agent-lore.py` - Agent lorebook generation
- `tools/lore_tui.py` - Terminal UI

These tools work but may exhibit the same reliability issues. Prefer shell-based alternatives when available.

## Migration Guide

### Before (Python API)

```python
from agents.api.lore_api import LoreAPI

lore = LoreAPI()

# Create entry
entry = lore.create_lore_entry(
    title="The Discovery",
    content="In the twilight hours...",
    category="lore",
    tags=["discovery"]
)

# Create book
book = lore.create_lore_book(
    title="Chronicles",
    description="A collection"
)

# Link entry to book
lore.add_entry_to_book(entry['id'], book['id'])
```

### After (Shell Tools)

```bash
# Create entry
entry_id=$(./tools/manage-lore.sh create-entry "The Discovery" "lore")

# Update entry with content
jq -f scripts/jq/crud-set/transform.jq \
  --arg path "content" \
  --arg value "In the twilight hours..." \
  "knowledge/expanded/lore/entries/${entry_id}.json" > tmp.json
mv tmp.json "knowledge/expanded/lore/entries/${entry_id}.json"

# Create book
book_id=$(./tools/manage-lore.sh create-book "Chronicles" "A collection")

# Link entry to book
./tools/manage-lore.sh add-to-book "$entry_id" "$book_id"
```

### Or Use Argc CLI

```bash
# Create entry with all fields
argc create-entry \
  --title "The Discovery" \
  --content "In the twilight hours..." \
  --category lore \
  --tags discovery research

# Create book
argc create-book \
  --title "Chronicles" \
  --description "A collection"

# Link using manage-lore.sh
./tools/manage-lore.sh add-to-book "$entry_id" "$book_id"
```

## LLM-Powered Generation

### Before (Python API)

```python
from agents.api.agent_api import AgentAPI

agent = AgentAPI()
result = agent.process_agent_request(
    agent_type="research",
    input_data={"topic": "quantum computing"},
    session_id="1234"
)
```

### After (Shell Tools)

```bash
# Generate lore entry with LLM
LLM_PROVIDER=claude ./tools/llama-lore-creator.sh - entry "Quantum Discovery" "concept"

# Extract lore from document
LLM_PROVIDER=claude ./tools/llama-lore-integrator.sh - extract-lore document.txt json

# Full automation pipeline
./integration/lore-flow.sh git-diff HEAD
./integration/lore-flow.sh manual "Amy implemented quantum mojito generator"
```

## Why Shell Tools are Better

### Reliability
- Battle-tested in production use
- Simpler implementation = fewer failure modes
- Direct file operations with clear error messages

### Maintainability
- No complex dependency chain
- Easy to debug with standard Unix tools
- Self-documenting with clear command structure

### Integration
- Works seamlessly with git hooks
- Composable with other shell scripts
- Standard Unix pipeline patterns

### Performance
- No Python interpreter overhead
- Direct jq operations on JSON
- Parallel execution with shell job control

## Timeline

- **2025-12**: Python API developed and documented
- **2025-12-30**: Issues discovered in production use
- **2026-01-05**: Python API formally deprecated
- **Future**: Python-dependent tools will be migrated to shell

## Support

### Python API
- ❌ No active maintenance
- ❌ No new features
- ❌ No bug fixes
- ⚠️ May be removed in future release

### Shell Tools
- ✅ Actively maintained
- ✅ New features added
- ✅ Bug fixes prioritized
- ✅ Long-term support

## Questions?

See the tool documentation:
- `tools/AGENTS.md` - Shell tool reference
- `docs/api/entry.md` - Entry operations
- `docs/api/book.md` - Book operations
- `docs/api/persona.md` - Persona operations

Or review session memories in `.serena/memories/` for historical context.
