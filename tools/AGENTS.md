# TOOLS

CLI utilities for lore management and LLM-powered content generation.

## OVERVIEW

Shell scripts + Python tools for CRUD operations and narrative generation. Some require `LLM_PROVIDER` env var for LLM calls.

## STRUCTURE

```
tools/
├── manage-lore.sh           # Core CRUD (deprecated, use Python API)
├── create-persona.sh        # Persona CRUD
├── llama-lore-creator.sh    # LLM content generation
├── llama-lore-integrator.sh # Extract lore from existing content
├── context-manager.sh       # Session state management
├── index-knowledge.sh       # Generate knowledge index
├── lore_tui.py              # Terminal UI (Textual-based)
└── check_hardcoded_paths.sh # Validation helper
```

## WHERE TO LOOK

| Task | Tool | Notes |
|------|------|-------|
| Create entry | `manage-lore.sh create-entry "Title" "category"` | No LLM |
| Create book | `manage-lore.sh create-book "Title" "Description"` | No LLM |
| Create persona | `create-persona.sh create "Name" "Desc" "traits" "tone"` | No LLM |
| Generate lore entry | `llama-lore-creator.sh - entry "Title" "category"` | Requires LLM |
| Generate persona | `llama-lore-creator.sh - persona "Name" "Desc"` | Requires LLM |
| Generate lorebook | `llama-lore-creator.sh - lorebook "Theme" "Desc" 5` | Requires LLM |
| Extract from file | `llama-lore-integrator.sh - extract-lore file.txt` | Requires LLM |
| Import directory | `llama-lore-integrator.sh - import-directory ./docs "Title" "Desc"` | Requires LLM |
| Browse lore | `python lore_tui.py` | Interactive TUI |

## CONVENTIONS

**LLM Provider Setup:**
```bash
export LLM_PROVIDER=claude    # or openai, ollama
export OPENROUTER_API_KEY="sk-or-v1-..."
```

**Categories:** `character`, `place`, `event`, `object`, `concept`, `custom`

**Output Format:**
```
Created lore entry: entry_1763812594_160d22f7
```

## ANTI-PATTERNS

| DO NOT | Why |
|--------|-----|
| Use `manage-lore.sh` for new code | Deprecated - use `LoreAPI` Python class |
| Hardcode absolute paths | Pre-commit blocks them |
| Generate without persona context | LLM needs voice/traits for consistency |

## COMMANDS

```bash
# No LLM Required
./manage-lore.sh list-entries
./manage-lore.sh list-books
./manage-lore.sh show-entry entry_123
./manage-lore.sh search "quantum"
./create-persona.sh list

# LLM Required
LLM_PROVIDER=claude ./llama-lore-creator.sh - entry "Dark Tower" "place"
LLM_PROVIDER=claude ./llama-lore-integrator.sh - extract-lore story.txt json

# Interactive
python lore_tui.py --base-dir ./knowledge/expanded
```

## NOTES

**Deprecation:** `manage-lore.sh` works but Python API (`agents/api/lore_api.py`) is preferred.

**Known Issue:** LLM sometimes outputs "I need your approval..." - fix prompt in `llama-lore-creator.sh`.
