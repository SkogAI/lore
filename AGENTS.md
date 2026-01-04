# LORE - DIGITAL MYTHOLOGY GENERATION SYSTEM

**Generated:** 2026-01-04
**Commit:** a404060
**Branch:** master

## OVERVIEW

Multi-agent system transforming technical changes into narrative lore. Git commits become mythology told through AI personas with distinct voices. JSON files as database, jq as transformation engine.

## STRUCTURE

```
lore/
├── agents/api/           # LoreAPI + AgentAPI (Python CRUD + LLM calls)
├── integration/          # Automated lore pipeline (git → persona → narrative)
├── knowledge/            # JSON data store (728 entries, 102 books, 89 personas)
│   ├── core/             # Schemas + numbered knowledge (00-09 core)
│   ├── expanded/         # Active lore (entries/, books/, personas/)
│   └── archived/         # Historical preservation (NEVER delete)
├── orchestrator/         # Session context + knowledge loading
├── scripts/jq/           # 50+ schema-driven jq transformations
├── tools/                # CLI tools (manage-lore.sh, llama-*.sh)
└── context/              # Session state JSON files
```

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| Create lore entry | `tools/manage-lore.sh create-entry` | Or `LoreAPI.create_lore_entry()` |
| Create book | `tools/manage-lore.sh create-book` | Or `LoreAPI.create_lore_book()` |
| Create persona | `tools/create-persona.sh create` | Or `LoreAPI.create_persona()` |
| Auto-generate from git | `integration/lore-flow.sh git-diff HEAD` | Maps author → persona |
| LLM content generation | `tools/llama-lore-creator.sh` | Requires `LLM_PROVIDER` env |
| JSON transforms | `scripts/jq/<transform>/transform.jq` | Schema in `schema.json` |
| Entry schema | `knowledge/core/lore/schema.json` | Required: id, title, content, category |
| Persona schema | `knowledge/core/persona/schema.json` | Required: id, name, core_traits, voice |
| CLI commands | `./Argcfile.sh --help` | argc-based CLI |

## CONVENTIONS

**ID Format:** `{type}_{timestamp}[_{hash}].json`
- `entry_1767098607_fb5f66fe.json`
- `book_1764992601.json`
- `persona_1764992753.json`

**Path Standards:** ALL code uses relative paths from repo root
```python
repo_root = Path(__file__).parent.parent
```
```bash
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
```

**Knowledge Numbering:**
- 00-09: Core/Emergency (load FIRST)
- 10-19: Navigation
- 20-29: Identity
- 30-99: Operational
- 100-199: Standards
- 200-299: Project-specific
- 300-399: Tools/Docs

**Import Order:** stdlib → third-party → local

**Type Hints:** Always use `Dict`, `List`, `Optional`, `Any` from typing

## ANTI-PATTERNS (THIS PROJECT)

| DO NOT | Why |
|--------|-----|
| Use hardcoded absolute paths | Pre-commit hook blocks `/home/skogix/*` |
| Delete archived lore | Historical preservation is CRITICAL |
| Use `// fallback` in jq for falsy values | Breaks on null/false - use `try-catch` |
| Generate meta-commentary in lore | "I will now..." is forbidden in output |
| Refactor while fixing bugs | Fix minimally, refactor separately |
| Switch to mega-prompts | Architectural decision - constraints drive creativity |
| Suppress types with `as any` | Project requires type safety |

## COMMANDS

```bash
# Development
python orchestrator/orchestrator.py init [content|lore|research]  # Start session
./Argcfile.sh list-books                                          # List all books
./Argcfile.sh create-entry --title "X" --category lore            # Create entry

# Lore Generation
./integration/lore-flow.sh manual "description"      # Manual input
./integration/lore-flow.sh git-diff HEAD             # From git commit
LLM_PROVIDER=claude ./tools/llama-lore-creator.sh - entry "Title" "category"

# Testing
./scripts/jq/test-all.sh                             # Run all jq tests (139 tests)
./scripts/jq/crud-get/test.sh                        # Single transform test

# Validation
./scripts/pre-commit/validate.sh                     # Check paths
python agents/api/lore_api.py                        # Test API
```

## NOTES

**Default Branch:** `master` (not main)

**Package Manager:** `uv` with `pyproject.toml` - Python 3.12+ required

**LLM Providers:** Claude, OpenAI, Ollama via OpenRouter API (`OPENROUTER_API_KEY`)

**Known Issues:**
- Issue #5: LLM generates meta-commentary instead of lore
- Issue #6: Pipeline creates entries with empty content

**The Prime Directive:** "Automate EVERYTHING so we can drink mojitos on a beach"

**Key Personas:**
- Amy Ravenwolf 🔥 - Fiery template
- Claude 🌊 - Anti-Goose, analytical
- Dot 💻 - Minimalist (4000 token max)
- Goose 🦢 - Chaos agent (HATES MINT)

## SESSION MEMORIES

**Location:** `.serena/memories/`

Claude Code session memories documenting key learnings:

1. **session-2025-12-30-lore-pipeline-discussion.md**
   - Actual system: `lore-flow.sh` working 5-step pipeline
   - Context = narrative continuity (data + time + persona + flow)
   - Mistakes: Over-designing before understanding, treating local LLMs wrong

2. **lore-generation-tools-documentation-session.md**
   - Created `docs/api/generation-tools.md` (1078 lines)
   - Corrected: Shell tools are primary, Python API is broken
   - Removed incorrect deprecation notices

3. **session-2025-12-31-prompts-repository-and-skill-patterns.md**
   - Skill pattern: SKILL.md router + progressive disclosure
   - Agent-prompting philosophy: Features = prompts, tools = primitives
   - Three-layer: Claude Code → Subagents → End Agents (ollama, lore)

4. **session-2025-12-31-docs-analysis.md**
   - Created PROJECT_INDEX.md (204 files, ~30K lines → 3KB index)
   - Discovered TODO-AICHAT-BASED-SKOGAI legacy docs (63 files)
   - Prompts repository setup at `agents/prompts/`

5. **session-2025-12-31-argc-sanity-check.md**
   - Verified argc provides 100% lore API coverage
   - Critical: `LLM_OUTPUT` env var required
   - End-to-end flow tested and working

## SUBDIRECTORY AGENTS

- `scripts/jq/AGENTS.md` - jq transformation conventions
- `tools/AGENTS.md` - CLI tool documentation
- `integration/AGENTS.md` - Pipeline workflows
