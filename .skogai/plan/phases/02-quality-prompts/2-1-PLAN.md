---
phase: 02-quality-prompts
type: execute
---

<objective>
Extract 3 embedded prompts from llama-lore-creator.sh into external files following agents/prompts/ repository standards.

Purpose: Enable prompt iteration without editing shell code. First step toward externalizing all LLM prompts.
Output: 3 prompt files in agents/prompts/ + updated llama-lore-creator.sh that reads from files
</objective>

<execution_context>
~/.claude/.skogai/skogai/workflows/execute-phase.md
./summary.md
</execution_context>

<context>
@.skogai/plan/PROJECT.md
@.skogai/plan/ROADMAP.md
@.skogai/plan/phases/02-quality-prompts/phase-2-CONTEXT.md
@.skogai/plan/phases/01-verify-pipeline/phase-1-1-SUMMARY.md
@tools/llama-lore-creator.sh
@agents/prompts/README.md
</context>

<tasks>

<task type="auto">
  <name>Task 1: Create 3 prompt files with YAML frontmatter</name>
  <files>agents/prompts/lore/entry-generation.md, agents/prompts/personas/trait-generation.md, agents/prompts/lore/title-generation.md</files>
  <action>
Extract prompts from llama-lore-creator.sh at lines 126, 222, and 284. For each prompt:

1. Create directory if needed (agents/prompts/lore/, agents/prompts/personas/)
2. Add YAML frontmatter following README.md standards:
   ```yaml
   ---
   title: entry-generation (or trait-generation, title-generation)
   type: prompt
   category: lore (or persona for trait-generation)
   tags: [generation, narrative] (appropriate tags)
   ---
   ```
3. Add structured sections:
   - # Objective: What this prompt does
   - # Inputs: Required variables (title, category, etc.)
   - # Expected Output: Format description
   - # Prompt: (the actual prompt content from the script)

Copy the exact prompt text from the PROMPT variable in each function. Preserve all instructions, examples, and formatting.

**entry-generation.md**: From generate_lore_entry() line 126 - the main lore generation prompt with "You are a master lore writer..."
**trait-generation.md**: From generate_persona() line 222 - persona trait extraction prompt
**title-generation.md**: From generate_lorebook() line 284 - lorebook title generation prompt
  </action>
  <verify>ls agents/prompts/lore/entry-generation.md agents/prompts/personas/trait-generation.md agents/prompts/lore/title-generation.md confirms files exist. Each file has YAML frontmatter and prompt content.</verify>
  <done>3 files created with proper structure, YAML frontmatter validates, prompt content matches original</done>
</task>

<task type="auto">
  <name>Task 2: Update llama-lore-creator.sh to read from external files</name>
  <files>tools/llama-lore-creator.sh</files>
  <action>
Add REPO_ROOT variable at top of script (after shebang):
```bash
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
```

Replace the 3 PROMPT assignments with file reads that strip YAML frontmatter:

**In generate_lore_entry() (line ~126):**
Replace `PROMPT="You are a master lore writer...` with:
```bash
PROMPT=$(cat "$REPO_ROOT/agents/prompts/lore/entry-generation.md" | sed '1,/^---$/d; 1,/^---$/d; /^# /d')
```

**In generate_persona() (line ~222):**
Replace `PROMPT="Generate personality traits...` with:
```bash
PROMPT=$(cat "$REPO_ROOT/agents/prompts/personas/trait-generation.md" | sed '1,/^---$/d; 1,/^---$/d; /^# /d')
```

**In generate_lorebook() (line ~284):**
Replace `PROMPT="Generate $entry_count...` with:
```bash
PROMPT=$(cat "$REPO_ROOT/agents/prompts/lore/title-generation.md" | sed '1,/^---$/d; 1,/^---$/d; /^# /d')
```

The sed command: strips first YAML block (lines 1 to first ---), strips second block (content to second ---), removes markdown headers (# Objective, etc.), leaving just prompt content.

**Variable substitution:** Ensure prompt files use placeholder syntax if needed, or keep variable expansion working ($title, $category, $entry_count, etc.).
  </action>
  <verify>grep -n "cat.*agents/prompts" tools/llama-lore-creator.sh shows 3 file reads. No more embedded PROMPT=" multi-line strings in the script.</verify>
  <done>Script reads from external files, no embedded prompts remain, variable substitution works</done>
</task>

<task type="auto">
  <name>Task 3: Verify llama-lore-creator.sh still works</name>
  <files>N/A (testing only)</files>
  <action>
Test each generation function to ensure refactoring didn't break functionality:

1. Test entry generation:
   ```bash
   LLM_PROVIDER=ollama ./tools/llama-lore-creator.sh llama3.2 entry "Test Entry" "concept"
   ```
   Should generate entry with narrative content (no errors).

2. Test persona generation:
   ```bash
   LLM_PROVIDER=ollama ./tools/llama-lore-creator.sh llama3.2 persona "Test Persona" "A test character"
   ```
   Should generate persona with traits (no errors).

3. Test lorebook generation:
   ```bash
   LLM_PROVIDER=ollama ./tools/llama-lore-creator.sh llama3.2 lorebook "Test Book" "Test description" 3
   ```
   Should generate book with 3 entry titles (no errors).

If any test fails: check file paths, sed command, variable substitution. Fix before marking done.
  </action>
  <verify>All 3 test commands complete without errors. Generated output matches pre-refactoring behavior (narrative content, proper formatting).</verify>
  <done>llama-lore-creator.sh works identically to before refactoring. All 3 functions generate expected output.</done>
</task>

</tasks>

<verification>
Before declaring plan complete:
- [ ] 3 prompt files exist in agents/prompts/ with proper structure
- [ ] YAML frontmatter validates (title, type, category, tags)
- [ ] llama-lore-creator.sh reads from files (no embedded prompts)
- [ ] All 3 generation functions work (entry, persona, lorebook)
- [ ] No errors or regressions introduced
</verification>

<success_criteria>

- All tasks completed
- 3 prompt files created following README.md standards
- llama-lore-creator.sh refactored to read external files
- Functionality unchanged (verified via testing)
- No embedded prompts remain in script
</success_criteria>

<output>
After completion, create `.skogai/plan/phases/02-quality-prompts/2-1-SUMMARY.md`:

# Plan 2-1 Summary: Extract llama-lore-creator.sh Prompts

**[One-liner summary of what was accomplished]**

## Accomplishments

- Created 3 prompt files in agents/prompts/
- Refactored llama-lore-creator.sh to read from external files
- Verified all generation functions still work

## Files Created/Modified

- `agents/prompts/lore/entry-generation.md` - Main lore entry generation prompt
- `agents/prompts/personas/trait-generation.md` - Persona trait extraction prompt
- `agents/prompts/lore/title-generation.md` - Lorebook title generation prompt
- `tools/llama-lore-creator.sh` - Updated to read from external files

## Decisions Made

[Any implementation choices, or "None"]

## Issues Encountered

[Problems and resolutions, or "None"]

## Next Step

Ready for 2-2-PLAN.md (extract llama-lore-integrator.sh prompts)
</output>
