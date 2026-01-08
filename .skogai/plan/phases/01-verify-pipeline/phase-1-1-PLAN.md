# Plan 1-1: Fix JSON Parsing Bug

**Phase:** 1 - Verify Pipeline
**Plan:** 1 of 1
**Created:** 2026-01-05

## Objective

Fix the JSON parsing bug in `lore-flow.sh` that causes "Failed to parse LLM output" when using Claude provider. Verify pipeline produces entries with actual narrative content.

## Prerequisites

- Research completed (phase-1-RESEARCH.md)
- Root cause identified: Claude wraps JSON in markdown code blocks
- Fix location known: `integration/lore-flow.sh` line 191

## Tasks

### Task 1: Fix JSON Parsing

**File:** `integration/lore-flow.sh`
**Location:** Lines 190-202

**Current code:**
```python
GENERATED_NARRATIVE=$(echo "$EXTRACTED_LORE" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    entries = data.get('entries', [])
    ...
```

**Fix:** Strip markdown code blocks before parsing:
```python
GENERATED_NARRATIVE=$(echo "$EXTRACTED_LORE" | python3 -c "
import json, sys, re
try:
    raw = sys.stdin.read()
    # Strip markdown code blocks (```json ... ```)
    clean = re.sub(r'^\`\`\`json\n?|\`\`\`$', '', raw.strip(), flags=re.MULTILINE)
    data = json.loads(clean)
    entries = data.get('entries', [])
    ...
```

**Checkpoint:** Code compiles (no syntax errors when sourced)

### Task 2: Verify with Claude Provider

**Command:**
```bash
LLM_PROVIDER=claude ./integration/lore-flow.sh manual "Phase 1 verification test"
```

**Expected output:**
- All 5 steps complete without error
- "Narrative generated: X characters" where X > 100
- Entry created with actual content (not "Failed to parse")

**Checkpoint:** Pipeline completes, entry created

### Task 3: Verify Entry Content

**Check created entry:**
```bash
# Get latest entry
LATEST=$(ls -t knowledge/expanded/lore/entries/*.json | head -1)
# Check content field
jq '.content' "$LATEST" | head -5
```

**Expected:** Rich narrative content (multiple sentences, story-like text)

**Checkpoint:** Content is narrative, not error message

### Task 4: Verify Book + Persona Linking

**Check linkages:**
```bash
# Get entry's book_id
ENTRY_ID=$(jq -r '.id' "$LATEST")
BOOK_ID=$(jq -r '.book_id // empty' "$LATEST")

# Verify book exists and contains entry
jq ".entries | contains([\"$ENTRY_ID\"])" "knowledge/expanded/lore/books/${BOOK_ID}*.json" 2>/dev/null || echo "Book linkage needs verification"
```

**Expected:** Entry is linked to a chronicle book

**Checkpoint:** MVP complete - book contains entry, linked to persona

## Verification

Run full verification:
```bash
# Clean test
LLM_PROVIDER=claude ./integration/lore-flow.sh manual "Final Phase 1 verification"

# Check results
LATEST=$(ls -t knowledge/expanded/lore/entries/*.json | head -1)
echo "=== Entry Content Preview ==="
jq -r '.title, .content[:200]' "$LATEST"
echo ""
echo "=== Linkage Check ==="
jq -r '.book_id // "NO BOOK LINK"' "$LATEST"
```

## Success Criteria

- [ ] `lore-flow.sh` completes all 5 steps without errors
- [ ] Generated entry has narrative content (not empty, not error message)
- [ ] Entry is linked to a chronicle book
- [ ] Chronicle book is linked to a persona
- [ ] Works with Claude provider (primary) and Ollama (secondary)

## Output

**Files modified:**
- `integration/lore-flow.sh` (JSON parsing fix)

**Files created:**
- New lore entry in `knowledge/expanded/lore/entries/`
- Possibly new chronicle book (if first for persona)

## Rollback

If fix causes issues:
```bash
git checkout integration/lore-flow.sh
```

## Notes

- Keep the fix minimal - one regex substitution
- Don't over-engineer (honor the 3800-token heritage)
- Issue #5 (meta-commentary) is Phase 2 scope, ignore for now

---

*Plan ready for execution*
*Estimated scope: Small (15-30 min)*
