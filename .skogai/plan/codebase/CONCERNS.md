# Technical Concerns & Issues

**Generated:** 2026-01-05

## Production Readiness Summary

| Scenario | Status | Notes |
|----------|--------|-------|
| **Single-user manual workflows** | Ready | Direct tool usage works well |
| **Automated pipelines** | Not ready | Issue #6 blocks auto-generation |
| **Multi-user scenarios** | At risk | No file locking, race conditions |
| **Current scale (1.2k entries)** | Ready | Performance acceptable |
| **Future scale (10k+ entries)** | Not ready | Need pagination, indexing |

## Issue Summary

| Category | Count | Severity |
|----------|-------|----------|
| Critical Issues | 3 | Production blocker |
| High Severity | 8 | Must fix before scale |
| Medium Severity | 4 | Quality issues |
| Architectural Debt | 4 | Maintenance burden |
| Known Bugs | 2 | Blocks auto-generation |
| Security | 3 | Exploit risk |
| Scalability | 3 | Blocks 10k+ entries |
| Missing Features | 5 | Incomplete system |
| Code Quality | 3 | Hard to debug |
| Documentation | 3 | Operational risk |
| **TOTAL** | **38** | |

---

## Critical Issues (Production Blockers)

### 1. Variable Name Typo in lore-flow.sh - Data Loss Risk

**File:** `integration/lore-flow.sh:263`

**Issue:** Python code inside shell script uses undefined variable `entry_file` instead of `$ENTRY_FILE`

**Code:**
```python
# Line 263 (WRONG)
with open(entry_file, 'w') as f:  # Should be '$ENTRY_FILE'
    json.dump(entry, f, indent=2)
```

**Impact:**
- Entry content never gets written to disk
- Silent failure - no error message
- Directly causes Issue #6 (empty content field)

**Fix:**
```python
with open('$ENTRY_FILE', 'w') as f:
    json.dump(entry, f, indent=2)
```

**Priority:** CRITICAL | **Effort:** 1 line fix

---

### 2. Command Substitution Regex Fragility

**File:** `integration/lore-flow.sh:230, 276, 280`

**Issue:** Parsing IDs from command output using brittle regex patterns

**Code:**
```bash
# Line 230
ENTRY_ID=$("$LORE_DIR/tools/manage-lore.sh" create-entry "$ENTRY_TITLE" "$LORE_CATEGORY" \
    | grep -oP 'entry_\d+_[a-f0-9]+' | head -1 || echo "")
```

**Problems:**
- If output format changes, regex fails silently
- `|| echo ""` suppresses errors
- Empty ID causes downstream failures

**Fix:**
```bash
ENTRY_ID=$("$LORE_DIR/tools/manage-lore.sh" create-entry "$ENTRY_TITLE" "$LORE_CATEGORY")
if [ -z "$ENTRY_ID" ] || ! [[ "$ENTRY_ID" =~ ^entry_[0-9]+(_[a-f0-9]+)?$ ]]; then
    echo "ERROR: Failed to extract valid entry ID: '$ENTRY_ID'" >&2
    exit 1
fi
```

**Priority:** CRITICAL | **Effort:** 10 lines

---

### 3. Python Variable Interpolation in Shell Here-doc - Injection Risk

**File:** `integration/lore-flow.sh:248-265`

**Issue:** Raw shell variables interpolated into Python code without escaping

**Code:**
```bash
python3 -c "
...
entry['summary'] = 'Auto-generated lore from $INPUT_TYPE'
entry['tags'] = ['generated', 'automated', '$PERSONA_NAME', '$INPUT_TYPE']
"
```

**Risks:**
- If `$PERSONA_NAME` contains quotes, JSON syntax breaks
- Potential injection attack: `PERSONA_NAME="Evil', 'injected_tag"`

**Fix:**
```bash
jq --arg summary "Auto-generated lore from $INPUT_TYPE" \
   --arg persona "$PERSONA_NAME" \
   --arg input_type "$INPUT_TYPE" \
   '.summary = $summary | .tags += ["generated", "automated", $persona, $input_type]' \
   "$ENTRY_FILE" > tmp.json
mv tmp.json "$ENTRY_FILE"
```

**Priority:** CRITICAL | **Effort:** 15 lines

---

## High Severity Issues

### 4. No Schema Validation in Pipeline

**File:** `integration/lore-flow.sh`

**Issue:** Entries created by pipeline have no schema validation

**Unlike:** `manage-lore.sh` validates via jq, but `lore-flow.sh` doesn't

**Fix:**
```bash
if ! validate_against_schema "$ENTRY_FILE" "entry"; then
    echo "ERROR: Generated entry failed schema validation" >&2
    exit 1
fi
```

**Priority:** HIGH | **Effort:** 5 lines

---

### 5. Unquoted Variables in Shell Commands

**File:** `integration/lore-flow.sh:275, 261`

**Issue:** Persona names with spaces break grep patterns

**Example:**
```bash
PERSONA_NAME="Amy Raven wolf"
CHRONICLE_NAME="${PERSONA_NAME}'s Chronicles"
# grep -F "$CHRONICLE_NAME" will fail with unquoted space
```

**Priority:** HIGH | **Effort:** 10 lines

---

### 6. Temporary File Race Conditions

**File:** `integration/lore-flow.sh:154, 244`

**Issue:** Uses predictable temp file names without mktemp

**Code:**
```bash
TEMP_CONTENT="/tmp/lore-content-$SESSION_ID.txt"
```

**Problems:**
- Session ID is just `date +%s` - collides if multiple runs in same second
- Symlink attack vulnerability

**Fix:**
```bash
TEMP_CONTENT=$(mktemp -t lore-content-XXXXXX.txt)
trap "rm -f $TEMP_CONTENT" EXIT INT TERM
```

**Priority:** HIGH | **Effort:** 5 lines

---

### 7. No File Locking in Multi-User Scenario

**Issue:** No mutual exclusion when multiple lore-flow instances modify the same book

**Scenario:**
1. Process A reads book_ID
2. Process B reads book_ID
3. Process A adds entry, writes book_ID
4. Process B adds entry, writes book_ID (overwrites A's changes)

**Fix:**
```bash
(
  flock -x 200  # Exclusive lock
  jq '.entries += ["'$entry_id'"]' "$book_file" > tmp.json
  mv tmp.json "$book_file"
) 200>"$book_file.lock"
```

**Priority:** HIGH | **Effort:** 20 lines

---

### 8. Error Handling Gaps - Silent Failures

**Examples:**

**lore-flow.sh:184:**
```bash
EXTRACTED_LORE=$("$LORE_INTEGRATOR" ... || echo "")
# If LLM extraction fails, creates empty entry instead of failing
```

**llama-lore-integrator.sh:185-186:**
```bash
ENTRY_ID=$(ls -t $SKOGAI_DIR/knowledge/expanded/lore/entries/ | head -n 1 | sed 's/\.json//')
# Race condition if another process also created one
```

**Fix:**
```bash
EXTRACTED_LORE=$("$LORE_INTEGRATOR" ...)
if [ $? -ne 0 ] || [ -z "$EXTRACTED_LORE" ]; then
    echo "ERROR: LLM extraction failed" >&2
    exit 1
fi
```

**Priority:** HIGH | **Effort:** 30 lines

---

## Medium Severity Issues

### 9. No Validation that Persona Actually Exists

**File:** `integration/lore-flow.sh:127-131`

**Issue:** Only checks if name lookup succeeded, not if persona JSON is valid

**Fix:**
```bash
if [ ! -f "$PERSONAS_DIR/$PERSONA_ID.json" ]; then
    echo "ERROR: Persona file not found: $PERSONA_ID" >&2
    exit 1
fi

if ! jq empty "$PERSONAS_DIR/$PERSONA_ID.json" 2>/dev/null; then
    echo "ERROR: Invalid persona JSON: $PERSONA_ID" >&2
    exit 1
fi
```

**Priority:** MEDIUM | **Effort:** 10 lines

---

### 10. Fragile Persona Mapping Configuration

**File:** `integration/persona-mapping.conf`

**Issues:**
- No validation of persona IDs
- No caching - reads file every time
- No error if mapping file missing

**Priority:** MEDIUM | **Effort:** 15 lines

---

### 11. LLM Model Parameter Inconsistency

**File:** `integration/lore-flow.sh:179-184`

**Issue:** Model set twice with same default, no validation that model exists

**Fix:**
```bash
if [ "$LLM_PROVIDER" = "ollama" ]; then
    if ! ollama list | grep -q "$LLM_MODEL"; then
        echo "ERROR: Model $LLM_MODEL not available in Ollama" >&2
        exit 1
    fi
fi
```

**Priority:** MEDIUM | **Effort:** 10 lines

---

## Architectural Debt

### 12. Orchestrator Layer Contains TODO Stubs

**File:** `integration/orchestrator-flow.sh`

**Issues:**
- Lines 26, 34, 42: "This would be replaced with actual LLM call in production"
- Script just echoes static messages
- No actual orchestration logic implemented

**Priority:** LOW | **Effort:** Unknown

---

### 13. Duplicate run_llm() Implementations

**Count:** 6 separate implementations

**Locations:**
- llama-lore-creator.sh
- llama-lore-integrator.sh
- generate-agent-lore.py
- agent_api.py
- llama-lore-creator.py
- llama-lore-integrator.py

**Problems:**
- Each has different error handling
- Bug fix in one place doesn't propagate

**Priority:** MEDIUM | **Effort:** 200 lines (new llm-service.sh)

---

### 14. Shell Tools vs Python API Inconsistency

**Issue:** CLAUDE.md states "Shell tools are canonical" but lore_api.py loads schemas never used for validation

**Evidence:**
- lore_api.py: Loads schemas but never validates
- manage-lore.sh: Validates via jq

**Priority:** MEDIUM | **Effort:** 50 lines

---

## Known Bugs (Documented)

### 15. Issue #5: LLM Meta-Commentary in Generated Content

**Documented in:** CLAUDE.md

**Symptom:** Generated entries contain "I need your approval to..." instead of narrative

**Mitigation:** Validation + stripping in llama-lore-creator.sh

**Limitation:** Only removes first-line meta-commentary, not internal

**Priority:** MEDIUM | **Effort:** 20 lines (prompt engineering)

---

### 16. Issue #6: Empty Content Field in Pipeline

**Documented in:** CLAUDE.md

**Symptom:** `lore-flow.sh` creates entries but content field stays empty

**Root Cause:** Variable typo in line 263 (see Issue #1)

**Workaround:** Use llama-lore-creator.sh directly

**Priority:** CRITICAL | **Effort:** 1 line fix

---

## Security Concerns

### 17. Temp Files in /tmp Without Protection

**Issue:** Predictable temp file names can be symlink-attacked

**Example Attack:**
```bash
ln -s /etc/passwd /tmp/narrative-$SESSION_ID.txt
# Script overwrites /etc/passwd
```

**Fix:** Use mktemp (see Issue #6)

**Priority:** MEDIUM | **Effort:** 5 lines

---

### 18. API Key Exposure Risk

**File:** `tools/llama-lore-integrator.sh:22-23`

**Issue:** API key visible in curl command and process list (`ps aux`)

**Fix:**
```bash
curl ... -H "Authorization: Bearer $OPENAI_API_KEY" ...
# curl reads from environment, doesn't expose in ps
```

**Priority:** LOW | **Effort:** 2 lines

---

### 19. Git Author Input Not Sanitized

**File:** `integration/lore-flow.sh:45`

**Risk:** Special characters could break grep patterns

**Fix:**
```bash
GIT_AUTHOR=$(echo "$GIT_AUTHOR" | tr -cd '[:alnum:] _-')
```

**Priority:** LOW | **Effort:** 2 lines

---

## Scalability & Performance Concerns

### 20. Naive List Operations for ID Lookups

**File:** `integration/lore-flow.sh:276`

**Issue:** Lists ALL books, greps for one; O(n) instead of O(1)

**Current Scale:** 107 books - acceptable
**Future Issue:** At 10k books, will be slow

**Priority:** LOW | **Effort:** 10 lines

---

### 21. Inefficient File Discovery

**Pattern:**
```bash
ENTRY_ID=$(ls -t ... | head -n 1 | sed 's/\.json//')
```

**Issue:** O(n log n) when O(1) possible with predictable ID format

**Priority:** LOW | **Effort:** 5 lines

---

### 22. No Pagination/Streaming for Large Datasets

**File:** `agents/api/lore_api.py:250-267`

**Issue:** `list_lore_entries()` loads ALL into memory

**Current:** ~1,202 entries x ~2KB = ~2.4MB
**Scale:** At 100k entries = 200MB+ operation

**Priority:** LOW | **Effort:** 30 lines

---

## Missing Features

### 23. No Entry Deduplication

**Priority:** LOW | **Effort:** 20 lines

### 24. No Relationship Validation

**Issue:** Relationships can point to non-existent entries

**Priority:** LOW | **Effort:** 10 lines

### 25. No Content Type Validation

**Issue:** Content not validated as markdown

**Priority:** LOW | **Effort:** Unknown

### 26. Missing Async/Batch Processing

**Issue:** Sequential 5-stage pipeline, slow for bulk

**Priority:** LOW | **Effort:** 200+ lines

### 27. No Knowledge Graph Queries

**Issue:** Can't query "all entries related to X"

**Priority:** LOW | **Effort:** 100+ lines

---

## Code Quality Issues

### 28. Inconsistent Error Handling Patterns

**Examples:**
- manage-lore.sh: Uses `set -e` (aggressive)
- lore-flow.sh: Uses `set -e` but then `|| echo ""` to suppress

**Priority:** LOW | **Effort:** 50 lines

### 29. No Input Validation Framework

**Missing:** Central validation for title length, category enum, ID format

**Priority:** LOW | **Effort:** 100 lines

### 30. Logging Insufficient for Debugging

**Missing:** Timestamps, severity levels, file-based logs, debug mode

**Priority:** LOW | **Effort:** 50 lines

---

## Documentation Gaps

### 31. No Integration Tests for Pipeline

**Would catch:** Issue #6 immediately

**Priority:** MEDIUM | **Effort:** 50 lines

### 32. Critical Bug Not Documented in Runbook

**Missing:** Troubleshooting guide with debugging steps

**Priority:** LOW | **Effort:** 30 minutes

### 33. No Operational Guide for Multi-User Setup

**Missing:** File locking, concurrency documentation

**Priority:** MEDIUM | **Effort:** 1 hour

---

## Immediate Action Items

### Priority 0 (Fix Now)
1. Fix variable typo in `integration/lore-flow.sh:263` -> Blocks Issue #6
2. Add explicit error checking after ID extraction
3. Use `mktemp` for temp files (security)

### Priority 1 (This Week)
4. Add schema validation in pipeline
5. Implement file locking for concurrent writes
6. Fix variable escaping in Python interpolation
7. Consolidate duplicate `run_llm()` implementations

### Priority 2 (This Month)
8. Add input validation framework
9. Implement Python API schema validation
10. Create integration tests for pipeline
11. Implement structured logging
12. Create operational runbook

### Priority 3 (Long-term)
13. Implement knowledge graph queries
14. Add async/batch processing
15. Add pagination to list operations
16. Performance optimization for large scale

---

## Files Requiring Immediate Attention

**Critical:**
- `integration/lore-flow.sh` (lines 263, 230, 248-265, 154, 244, 276, 280)

**High Priority:**
- `integration/orchestrator-flow.sh` (lines 12, 26, 34, 42, 47)
- `agents/api/lore_api.py` (add validation)
- `tools/llama-lore-integrator.sh` (API key exposure)

**Documentation:**
- Create: `docs/operations/TROUBLESHOOTING.md`
- Create: `docs/operations/MULTI_USER_SETUP.md`
- Update: `CLAUDE.md` with Issue #6 root cause
