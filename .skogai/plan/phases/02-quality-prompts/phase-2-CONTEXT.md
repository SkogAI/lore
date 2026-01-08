# Phase 2 Context: Quality Prompts

## What We're Actually Doing

Extract embedded LLM prompts from shell scripts and externalize them into the `agents/prompts/` repository following existing standards. This enables prompt iteration without touching shell code.

## The Real Scope

**Simple refactoring:**
1. Find the 7 prompts embedded in shell scripts
2. Extract them → save as `agents/prompts/category/descriptive-name.md`
3. Update scripts to read from those files instead

**NOT doing:**
- ❌ Prompt tuning/optimization (that comes after extraction)
- ❌ Testing frameworks or validation systems
- ❌ Model selection changes
- ❌ Multi-shot prompting strategies
- ❌ Quality scoring systems

Just: Get prompts out of scripts → into files → enable iteration.

## Target Prompts (7 total)

### tools/llama-lore-creator.sh (3 prompts)
1. **Line 126**: `generate_lore_entry()` - Main lore entry generation
   - Target: `agents/prompts/lore/entry-generation.md`
2. **Line 222**: `generate_persona()` - Persona trait generation
   - Target: `agents/prompts/personas/trait-generation.md`
3. **Line 284**: `generate_lorebook()` - Entry title generation
   - Target: `agents/prompts/lore/title-generation.md`

### tools/llama-lore-integrator.sh (4 prompts)
1. **Line 85**: `extract_lore_from_file()` - JSON format extraction
   - Target: `agents/prompts/lore/extract-json.md`
2. **Line 116**: `extract_lore_from_file()` - Markdown format extraction
   - Target: `agents/prompts/lore/extract-markdown.md`
3. **Line 295**: `create_persona_from_description()` - Character analysis
   - Target: `agents/prompts/personas/character-analysis.md`
4. **Line 388**: `analyze_connections()` - Relationship detection
   - Target: `agents/prompts/lore/analyze-connections.md`

## Standards (from agents/prompts/README.md)

Each extracted prompt file must have:

### 1. YAML Frontmatter
```yaml
---
title: descriptive-name
type: prompt
category: lore|persona|tool|workflow
tags: [relevant, tags, here]
---
```

### 2. Structure
- **Objective**: Clear statement of what this prompt does
- **Inputs**: Required variables/parameters
- **Expected Output**: Format and content description
- **Examples**: Real examples where applicable

### 3. File Organization
- Use category directories: `lore/`, `personas/`
- Kebab-case filenames: `entry-generation.md`
- Follow existing patterns in the repository

## Implementation Pattern

**Before:**
```bash
PROMPT="You are a master lore writer...
[300 lines of embedded prompt]
..."
result=$(run_llm "$PROMPT")
```

**After:**
```bash
PROMPT=$(cat "$REPO_ROOT/agents/prompts/lore/entry-generation.md" | sed '1,/^---$/d; 1,/^---$/d')
result=$(run_llm "$PROMPT")
```

The `sed` command strips YAML frontmatter, leaving just the prompt content.

## Success Criteria

1. ✅ All 7 prompts extracted to `agents/prompts/` following standards
2. ✅ Shell scripts updated to read from external files
3. ✅ Scripts still work (no functionality broken)
4. ✅ Prompts can be edited without touching shell code
5. ✅ YAML frontmatter validates against README.md standards

## Why This Matters

**Current state:** Prompts buried in shell scripts
- Hard to find and compare
- Require shell editing to iterate
- No metadata or documentation
- Can't version or track changes separately

**After extraction:**
- Prompts visible in dedicated directory
- Edit markdown, test immediately
- Metadata tracks purpose and usage
- Git history shows prompt evolution
- Future: Can A/B test different prompts

## What Comes After

Once prompts are external, **Phase 3** can focus on:
- Prompt quality iteration (using Village Elder as standard)
- Issue #5 fixes (meta-commentary reduction)
- Provider-specific optimizations
- Few-shot example integration

But that's future work. Phase 2 is just: **Extract → Externalize → Verify still works**.

---

*Context gathered: 2026-01-08*
*Based on: `/dot:skogai:list-phase-assumptions 2` discussion*
