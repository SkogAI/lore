# Plan 1-1: Fix Pipeline and Verify End-to-End

## Objective

Fix the known Issue #6 (empty content bug) and verify the lore-flow.sh pipeline produces a complete lore entry with actual content using Claude Code as the LLM provider.

## Context

**From CONCERNS.md - Issue #6 Root Cause:**
- Variable typo on line 263 of `integration/lore-flow.sh`
- Python code uses `entry_file` instead of `$ENTRY_FILE`
- Shell variable not expanded into embedded Python script

**Provider:** Using `LLM_PROVIDER=claude` for simplicity/speed (per user decision)

**Success criteria from roadmap:**
- Entry JSON written with actual content (Issue #6 fixed)
- Book and persona linking works

## Tasks

### Task 1: Fix Variable Typo in lore-flow.sh

**File:** `integration/lore-flow.sh`
**Line:** 263

Read the file and fix the Python embedded code where `entry_file` should be `$ENTRY_FILE`.

The fix is documented in CONCERNS.md:
```python
# WRONG (current):
with open(entry_file, 'w') as f:

# CORRECT:
with open('$ENTRY_FILE', 'w') as f:
```

Also check line 256-257 for similar issues - the read operation may have the same problem.

**Verification:** After fix, grep for `entry_file` (without $) to confirm no unresolved references remain in Python blocks.

### Task 2: Run Pipeline with Test Input

Execute the pipeline with manual input:

```bash
LLM_PROVIDER=claude ./integration/lore-flow.sh manual "Testing the lore pipeline with Claude - a brave adventurer debugged the ancient scripts"
```

Capture:
- Exit code
- Entry ID created
- Any error messages

**Expected:** Script completes without error, prints entry ID.

### Task 3: Verify Entry Has Content

Read the created entry JSON file and verify:

1. `content` field is NOT empty
2. `content` contains actual narrative text (not error messages)
3. `title` is set
4. `category` is set to "event"
5. `tags` array includes expected values

**Command:**
```bash
cat knowledge/expanded/lore/entries/<entry_id>.json | jq '{title, content, category, tags}'
```

**Checkpoint:** `checkpoint:human-verify`
Show the entry content to user for quality confirmation.

### Task 4: Verify Book and Persona Linking

Check that the entry was properly linked:

1. Entry's `book_id` field is set
2. Chronicle book exists and contains the entry ID in its `entries` array
3. Chronicle book is linked to a persona via `readers` array

**Commands:**
```bash
# Get book_id from entry
BOOK_ID=$(jq -r '.book_id' knowledge/expanded/lore/entries/<entry_id>.json)

# Verify entry is in book
jq '.entries' knowledge/expanded/lore/books/${BOOK_ID}.json

# Verify persona linked
jq '.readers' knowledge/expanded/lore/books/${BOOK_ID}.json
```

### Task 5: Document Results

Update STATE.md with:
- Phase 1 marked as complete
- Issue #6 resolution noted
- Entry ID created during verification

## Verification

- [ ] `entry_file` typo fixed → `$ENTRY_FILE`
- [ ] Pipeline runs without error
- [ ] Entry content field has actual narrative
- [ ] Entry linked to book
- [ ] Book linked to persona

## Success Criteria

1. **Issue #6 Fixed:** The variable typo is corrected
2. **Pipeline Runs:** `lore-flow.sh manual "..."` completes successfully
3. **Content Populated:** Entry JSON has non-empty `content` field with LLM-generated narrative
4. **Linking Works:** Entry → Book → Persona chain is intact

## Output

- Fixed `integration/lore-flow.sh`
- One new lore entry (test entry for verification)
- Updated STATE.md marking phase complete
