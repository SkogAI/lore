---
phase: 02-quality-prompts
type: execute
---

<objective>
Extract 4 embedded prompts from llama-lore-integrator.sh into external files following agents/prompts/ repository standards.

Purpose: Complete prompt externalization for all lore generation tools. Enable iteration without shell code edits.
Output: 4 prompt files in agents/prompts/ + updated llama-lore-integrator.sh that reads from files
</objective>

<execution_context>
~/.claude/.skogai/skogai/workflows/execute-phase.md
./summary.md
</execution_context>

<context>
@.skogai/plan/PROJECT.md
@.skogai/plan/ROADMAP.md
@.skogai/plan/phases/02-quality-prompts/phase-2-CONTEXT.md
@.skogai/plan/phases/02-quality-prompts/2-1-SUMMARY.md
@tools/llama-lore-integrator.sh
@agents/prompts/README.md
</context>

<tasks>

<task type="auto">
  <name>Task 1: Create 4 prompt files with YAML frontmatter</name>
  <files>agents/prompts/lore/extract-json.md, agents/prompts/lore/extract-markdown.md, agents/prompts/personas/character-analysis.md, agents/prompts/lore/analyze-connections.md</files>
  <action>
Extract prompts from llama-lore-integrator.sh at lines 85, 116, 295, and 388. For each prompt:

1. Create files in appropriate directories (agents/prompts/lore/, agents/prompts/personas/)
2. Add YAML frontmatter:
   ```yaml
   ---
   title: extract-json (or extract-markdown, character-analysis, analyze-connections)
   type: prompt
   category: lore (or persona for character-analysis)
   tags: [extraction, analysis] (appropriate tags)
   ---
   ```
3. Add structured sections:
   - # Objective
   - # Inputs
   - # Expected Output
   - # Prompt: (actual prompt content)

Copy exact prompt text from PROMPT variables. Preserve all instructions, format specifications, and examples.

**extract-json.md**: From extract_lore_from_file() line 85 - JSON format extraction with "You are a lore archaeologist..." (json branch)
**extract-markdown.md**: From extract_lore_from_file() line 116 - Markdown format extraction (lore branch)
**character-analysis.md**: From create_persona_from_description() line 295 - Character/persona analysis prompt
**analyze-connections.md**: From analyze_connections() line 388 - Relationship detection between lore entries
  </action>
  <verify>ls agents/prompts/lore/extract-json.md agents/prompts/lore/extract-markdown.md agents/prompts/personas/character-analysis.md agents/prompts/lore/analyze-connections.md confirms files exist. Each has YAML frontmatter and prompt content.</verify>
  <done>4 files created with proper structure, YAML validates, prompt content matches original</done>
</task>

<task type="auto">
  <name>Task 2: Update llama-lore-integrator.sh to read from external files</name>
  <files>tools/llama-lore-integrator.sh</files>
  <action>
Add REPO_ROOT variable at top of script (if not already present from Plan 2-1 pattern):
```bash
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
```

Replace the 4 PROMPT assignments with file reads:

**In extract_lore_from_file() JSON branch (line ~85):**
Replace `PROMPT="You are a lore archaeologist...` with:
```bash
PROMPT=$(cat "$REPO_ROOT/agents/prompts/lore/extract-json.md" | sed '1,/^---$/d; 1,/^---$/d; /^# /d')
```

**In extract_lore_from_file() lore branch (line ~116):**
Replace `PROMPT="You are a lore archaeologist...` with:
```bash
PROMPT=$(cat "$REPO_ROOT/agents/prompts/lore/extract-markdown.md" | sed '1,/^---$/d; 1,/^---$/d; /^# /d')
```

**In create_persona_from_description() (line ~295):**
Replace `PROMPT="Analyze the following text...` with:
```bash
PROMPT=$(cat "$REPO_ROOT/agents/prompts/personas/character-analysis.md" | sed '1,/^---$/d; 1,/^---$/d; /^# /d')
```

**In analyze_connections() (line ~388):**
Replace `PROMPT="Analyze these lore entries...` with:
```bash
PROMPT=$(cat "$REPO_ROOT/agents/prompts/lore/analyze-connections.md" | sed '1,/^---$/d; 1,/^---$/d; /^# /d')
```

Ensure variable substitution works ($content, $file_path, etc. are still expanded in prompts).
  </action>
  <verify>grep -n "cat.*agents/prompts" tools/llama-lore-integrator.sh shows 4 file reads. No embedded multi-line PROMPT=" strings remain.</verify>
  <done>Script reads from external files, no embedded prompts, variables expand correctly</done>
</task>

<task type="auto">
  <name>Task 3: Verify llama-lore-integrator.sh still works</name>
  <files>N/A (testing only)</files>
  <action>
Test each extraction function to ensure refactoring works:

1. Test JSON extraction:
   Create test file: `echo "The wizard controls time and space using ancient algorithms" > /tmp/test-lore.txt`
   ```bash
   LLM_PROVIDER=ollama ./tools/llama-lore-integrator.sh llama3.2 extract-lore /tmp/test-lore.txt json
   ```
   Should return JSON with entries array (no errors).

2. Test markdown extraction:
   ```bash
   LLM_PROVIDER=ollama ./tools/llama-lore-integrator.sh llama3.2 extract-lore /tmp/test-lore.txt lore
   ```
   Should return markdown formatted lore entries (no errors).

3. Test connection analysis (requires existing entries):
   ```bash
   # Find a book with multiple entries
   book_id=$(ls knowledge/expanded/lore/books/*.json | head -1 | xargs basename | cut -d. -f1)
   LLM_PROVIDER=ollama ./tools/llama-lore-integrator.sh llama3.2 analyze-connections "$book_id"
   ```
   Should analyze and show connections (no errors).

If tests fail: debug file paths, sed syntax, variable expansion. Fix before completing.
  </action>
  <verify>All test commands complete without errors. Output format matches pre-refactoring behavior (JSON structure, markdown formatting, connection analysis).</verify>
  <done>llama-lore-integrator.sh works identically to before. All extraction and analysis functions produce expected output.</done>
</task>

</tasks>

<verification>
Before declaring plan complete:
- [ ] 4 prompt files exist in agents/prompts/ with proper structure
- [ ] YAML frontmatter validates for all 4 files
- [ ] llama-lore-integrator.sh reads from files (no embedded prompts)
- [ ] All extraction/analysis functions work correctly
- [ ] No errors or regressions introduced
- [ ] Phase 2 complete: All 7 prompts externalized (3 from Plan 2-1, 4 from Plan 2-2)
</verification>

<success_criteria>

- All tasks completed
- 4 prompt files created following README.md standards
- llama-lore-integrator.sh refactored to read external files
- Functionality unchanged (verified via testing)
- No embedded prompts remain in script
- **Phase 2 complete**: All 7 target prompts externalized and working
</success_criteria>

<output>
After completion, create `.skogai/plan/phases/02-quality-prompts/2-2-SUMMARY.md`:

# Plan 2-2 Summary: Extract llama-lore-integrator.sh Prompts

**[One-liner summary of what was accomplished]**

## Accomplishments

- Created 4 prompt files in agents/prompts/
- Refactored llama-lore-integrator.sh to read from external files
- Verified all extraction and analysis functions still work
- **Phase 2 complete**: All 7 prompts successfully externalized

## Files Created/Modified

- `agents/prompts/lore/extract-json.md` - JSON format lore extraction
- `agents/prompts/lore/extract-markdown.md` - Markdown format lore extraction
- `agents/prompts/personas/character-analysis.md` - Character/persona analysis
- `agents/prompts/lore/analyze-connections.md` - Lore entry relationship detection
- `tools/llama-lore-integrator.sh` - Updated to read from external files

## Decisions Made

[Any implementation choices, or "None"]

## Issues Encountered

[Problems and resolutions, or "None"]

## Next Phase Readiness

**Phase 2 Goals Achieved:**
- ✅ All 7 prompts extracted from shell scripts
- ✅ Prompts follow agents/prompts/README.md standards
- ✅ Scripts updated to read external files
- ✅ Functionality verified unchanged

**Ready for Phase 3**: Auto-trigger (git hooks)

Prompts can now be iterated without touching shell code. Future prompt quality improvements (Issue #5 fixes) can be done purely by editing markdown files in agents/prompts/.
</output>
