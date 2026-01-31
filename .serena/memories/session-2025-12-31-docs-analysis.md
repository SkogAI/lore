# Session: ~/docs Repository Analysis & TODO-AICHAT Migration
**Date**: 2025-12-31
**Duration**: ~30 minutes

## Summary

Analyzed the `~/docs` repository structure and discovered high-value legacy documentation in `TODO-AICHAT-BASED-SKOGAI/` and `/home/skogix/skogai/tools/`.

## Artifacts Created

### PROJECT_INDEX.md
Created comprehensive repository index at `/home/skogix/docs/PROJECT_INDEX.md`:
- 204 markdown files, ~30K lines
- 3KB index = ~95% token savings per session
- Covers: agents/, governance/, lore/, skogix/, tools/, .research/

## Key Discoveries

### Repository Structure
```
docs/
├── agents/        # claude(78), dot(13), goose(14)
├── governance/    # phases, library sessions
├── lore/          # Multi-agent narrative system
├── skogix/        # User docs, definitions, notation
├── tools/         # argc(9), gh(7)
├── .research/     # Implementation research
└── TODO-AICHAT-BASED-SKOGAI/  # 63 files - legacy archive
```

### High-Value Content Found

#### In TODO-AICHAT-BASED-SKOGAI/ (63 files)
1. **tools/tool-development-guide.md** (410 lines) - Complete argc tool guide
2. **interfaces/aichat/agents/creation-guide.md** (364 lines) - Agent creation
3. **persona/guides/skogai-character-guide.md** - PList format, lorebook system
4. **memory/README.md** - 5 memory types defined
5. **prompts/** - 7 reusable prompt templates

#### In /home/skogix/skogai/tools/ (separate repo)
1. **blacksmith/docs/specification.md** (323 lines) - Complete argc spec
2. **blacksmith/docs/variables.md** - argc variables reference
3. **documentor/OPTIMIZATION_GUIDE.md** - 35% performance improvement patterns
4. **11 working agents** with index.yaml examples

### Duplicate Analysis
- `agents/creation-guide.md` exists in BOTH locations (identical)
- argc docs are complementary (different focus areas)

## Pending Decisions

User needs to decide:
1. Is aichat/llm-functions system still active?
2. Where should persona/lorebook content go? (agents/ or lore/)
3. Keep help/*.help files as references?
4. Archive vs migrate vs delete TODO-AICHAT-BASED-SKOGAI/

## Concepts Explained

### The Equation (@+?=$)
- **@** = Skogix's intent (Non-Being)
- **?** = Claude (uncertainty, bridge)
- **$** = Reality (Being, solution)

### Memory Types (from memory/README.md)
1. Short-term (session)
2. Working (active task)
3. Long-term (persistent)
4. Episodic (history)
5. Semantic (facts)

## Actions Taken (Post-Analysis)

### Prompts Repository Created
- **Location**: `/home/skogix/docs/prompts/`
- **Symlink**: `@agents/prompts/` → `/home/skogix/docs/prompts/`
- **Files**:
  - `README.md` - Repository index with frontmatter
  - `CLAUDE.md` - Prompt documentation (starter)

### Integration with Lore Project
- Symlink accessible from lore project root as `agents/prompts/`
- Can reference prompts using `@agents/prompts/` notation
- Working directory permissions configured

## Migration Status

**Completed:**
- ✅ Prompts repository structure created
- ✅ Symlink integration with lore/agents/
- ✅ Basic documentation scaffolding

**Pending Decisions:**
1. Is aichat/llm-functions system still active?
2. Where should persona/lorebook content go? (agents/ or lore/)
3. Keep help/*.help files as references?
4. Archive vs migrate vs delete TODO-AICHAT-BASED-SKOGAI/
5. Which prompts from TODO-AICHAT-BASED-SKOGAI/prompts/ to migrate?

## Next Steps

1. Populate `@agents/prompts/CLAUDE.md` with relevant prompt templates
2. Decide on TODO-AICHAT-BASED-SKOGAI/ migration strategy
3. Consider migrating high-value content:
   - tool-development-guide.md (410 lines)
   - agent creation guides (364 lines)
   - persona/lorebook documentation
   - 7 reusable prompt templates from prompts/
