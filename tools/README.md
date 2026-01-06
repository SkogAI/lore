# Lore Tools

CLI utilities for lore management and LLM-powered content generation.

## Quick Start

```bash
# List existing lore
./manage-lore.sh list-books
./manage-lore.sh list-entries

# Create entry (no LLM required)
./manage-lore.sh create-entry "The Dark Tower" "place"

# Generate entry with LLM content
LLM_PROVIDER=claude ./llama-lore-creator.sh - entry "Crystal Forest" "place"

# Extract lore from existing document
LLM_PROVIDER=claude ./llama-lore-integrator.sh - extract-lore story.txt
```

## Available Tools

### Core CRUD (No LLM Required)

| Tool | Purpose |
|------|---------|
| `manage-lore.sh` | Create, list, show, search entries and books |
| `create-persona.sh` | Create, list, show, edit personas |
| `context-manager.sh` | Session state management |
| `index-knowledge.sh` | Generate searchable knowledge index |

### LLM-Powered Generation

| Tool | Purpose |
|------|---------|
| `llama-lore-creator.sh` | Generate entries, personas, lorebooks |
| `llama-lore-integrator.sh` | Extract lore from documents, analyze connections |

### Utilities

| Tool | Purpose |
|------|---------|
| `lore_tui.py` | Interactive terminal UI (Textual-based) |
| `check_hardcoded_paths.sh` | Validation for pre-commit hook |

## Configuration

### LLM Provider Setup

Required for `llama-lore-*.sh` tools:

```bash
export LLM_PROVIDER=claude    # Options: claude, openai, ollama
export OPENROUTER_API_KEY="sk-or-v1-..."  # For cloud providers
```

### Categories

Valid lore categories: `character`, `place`, `event`, `object`, `concept`, `custom`

## Common Workflows

### Create a Complete Lorebook

```bash
# Generate a themed lorebook with 5 entries
LLM_PROVIDER=claude ./llama-lore-creator.sh - lorebook "Eldoria" "A magical realm" 5
```

### Import Existing Documentation

```bash
# Extract lore from a directory of files
LLM_PROVIDER=claude ./llama-lore-integrator.sh - import-directory ./docs "Documentation Lore" "Lore from project docs"
```

### Link Persona to Books

```bash
# Link a persona to their chronicles
./manage-lore.sh link-to-persona book_123 persona_456
```

## Documentation

- **[AGENTS.md](./AGENTS.md)** - Developer reference with conventions and anti-patterns
- **[../docs/api/generation-tools.md](../docs/api/generation-tools.md)** - Complete API reference
- **[../CLAUDE.md](../CLAUDE.md)** - System documentation

## Known Issues

- **[Issue #5](https://github.com/SkogAI/lore/issues/5)**: LLM generates meta-commentary instead of lore
- **[Issue #6](https://github.com/SkogAI/lore/issues/6)**: Pipeline creates entries with empty content

---

*The beach awaits. The mojitos are quantum.*
