# Lore Integration: Wire It All Together

**Goal:** Local LLMs doing actual work, producing lore we can be proud of.

## Vision

The pieces exist. The 5-step pipeline exists. 1200+ entries exist. What's missing is the wiring - making Ollama continuously generate quality lore from real activity, hands-free.

**End state:** Git commits, session logs, and manual events flow automatically through local LLMs into rich narrative entries that grow the mythology.

## Requirements

### Validated

Existing capabilities (inferred from codebase):

- ✓ CRUD operations for entries/books/personas — `manage-lore.sh`, `create-persona.sh`
- ✓ LLM content generation — `llama-lore-creator.sh`, `llama-lore-integrator.sh`
- ✓ 5-step pipeline skeleton — `lore-flow.sh` (extract → persona → context → generate → store)
- ✓ Context/session management — `context-manager.sh`
- ✓ Persona rendering — `persona-manager.py`
- ✓ Quality exemplars — Village Elder, Greenhaven entries demonstrate the target quality
- ✓ 1200+ entries, 107 books, 92 personas — existing mythology to build on
- ✓ All 3 LLM providers supported — claude, openai, ollama

### Active

What needs to be built/wired:

- [ ] Ollama integration verified end-to-end — confirm local models work through full pipeline
- [ ] Pipeline produces quality content — entries match Village Elder/Greenhaven standard
- [ ] Automatic trigger mechanism — git hooks or continuous monitoring kicks off generation
- [ ] Session continuity — context flows between runs, personas remember their work
- [ ] Relationship building — new entries connect to existing lore graph

### Out of Scope

- Cloud LLM dependency — must work purely with local Ollama, no API costs
- UI/visualization — CLI only, no web interface
- Multi-repo support — this lore repo only, not a general tool
- Python API changes — shell tools are canonical, don't touch lore_api.py
- Data migration — preserve all existing entries/books/personas exactly as they are
- Complex before simple — wire existing tools first, optimize later

## Context

### What Good Lore Looks Like

From SHOWCASE.md and exploration, quality entries have:

1. **Rich narrative** (2-3 paragraphs) — atmospheric, literary, immersive
2. **Agent context** — "For our [agent type], this means..." practical guidance
3. **World-building connections** — references to other lore elements
4. **Practical applications** — actionable information embedded in narrative

**Exemplar:** Village Elder (entry_1744512859)
```
"The Village Elder: A Beacon of Wisdom and Guidance

As the oldest and wisest resident of the village, the Village Elder is a revered
figure whose counsel is sought by all. With eyes that have seen the rise and fall
of generations, they possess an innate understanding of the intricate web of
relationships that bind the community together..."
```

### The Pipeline (lore-flow.sh)

```
Git Commit/Log/Manual Input
    ↓
[1] Extract Content — git-diff, log, or manual input
    ↓
[2] Select Persona — author → persona mapping
    ↓
[3] Load Persona Context — voice, traits, lore books
    ↓
[4] Generate Narrative — LLM transforms technical → mythological
    ↓
[5] Create & Store Lore — entry created, linked to book and persona
```

### Constraints

- **Preserve existing data** — 1200+ entries are historical artifacts
- **Shell tools canonical** — build on manage-lore.sh, not Python
- **Ollama model limits** — work within context window constraints
- **Keep it simple** — wire existing pieces, don't reinvent

### Known Issues (treated as resolved)

- Issue #5: LLM meta-commentary — PRs pending, assume fixed
- Issue #6: Empty content in pipeline — PRs pending, assume fixed

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Ollama only, no cloud | Free, runs 24/7, no API costs | — Pending |
| Shell tools canonical | Documented standard, better error handling | — Established |
| Conservative integration | Wire existing tools, don't rebuild | — Pending |
| Quality over quantity | Match Village Elder standard | — Pending |

## Success Criteria

1. `./integration/lore-flow.sh git-diff HEAD` produces quality narrative entry using Ollama
2. Entry content matches Village Elder quality standard (rich, practical, connected)
3. New entries automatically link to relevant books and personas
4. Pipeline runs without manual intervention after trigger
5. Local LLM does the actual generation work (no cloud dependency)

---
*Last updated: 2026-01-05 after initialization*
