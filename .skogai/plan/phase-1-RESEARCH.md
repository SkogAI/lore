# Phase 1: Verify Pipeline - Research

**Completed:** 2026-01-05
**Status:** Ready for planning

## Research Type

Codebase exploration (not external research). Phase 1 uses existing tools - research focused on understanding current state and identifying blockers.

## Executive Summary

**Pipeline Status:** Functional but has JSON parsing bug with Claude provider.

The 5-step pipeline (`lore-flow.sh`) runs end-to-end. LLM extraction produces rich lore content. However, Claude's output wraps JSON in markdown code blocks, causing parse failure. One-line fix needed.

## Pipeline Architecture

### Flow: `integration/lore-flow.sh` (304 lines)

```
[1/5] Extract Content
      ├─ git-diff: Extract diffs + commit message + author
      ├─ log: Read log file contents
      └─ manual: Use input directly
           ↓
[2/5] Select Persona
      ├─ Map git author → persona via persona-mapping.conf
      └─ Fallback: DEFAULT or Village Elder (persona_1763820091)
           ↓
[3/5] Load Persona Context
      └─ persona-manager.py --persona <id> --render-prompt
           ↓
[4/5] Generate Narrative
      └─ llama-lore-integrator.sh extract-lore <content> json
           ↓
[5/5] Create & Store Lore
      ├─ manage-lore.sh create-entry
      ├─ Update entry with narrative content
      ├─ Create/find chronicle book
      └─ Link entry → book → persona
```

### Key Components

| Component | Location | Purpose |
|-----------|----------|---------|
| `lore-flow.sh` | integration/ | Main pipeline orchestrator |
| `llama-lore-integrator.sh` | tools/ | LLM content extraction |
| `manage-lore.sh` | tools/ | CRUD for entries/books |
| `persona-manager.py` | integration/persona-bridge/ | Persona context loading |
| `persona-mapping.conf` | integration/ | Git author → persona mapping |

### LLM Providers (all tested working)

- **Claude** - via `claude -p "$prompt"` (Claude CLI)
- **Ollama** - via `ollama run "$model" "$prompt"` (local)
- **OpenAI** - via OpenRouter API

## Test Results

### Direct LLM Test (PASS)

```bash
LLM_PROVIDER=claude ./tools/llama-lore-integrator.sh "" extract-lore /tmp/test.txt json
```

Output: Rich narrative JSON with 4 entries, ~2000 words of quality lore content.

### Full Pipeline Test (PARTIAL)

```bash
LLM_PROVIDER=claude ./integration/lore-flow.sh manual "Testing pipeline"
```

Result:
- Steps 1-3: PASS (content extracted, persona loaded)
- Step 4: FAIL - "Narrative generated: 26 characters" → "Failed to parse LLM output"
- Step 5: Entry created but with error message as content

## Root Cause Analysis

**Bug Location:** `integration/lore-flow.sh` lines 191-202

```python
GENERATED_NARRATIVE=$(echo "$EXTRACTED_LORE" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)  # ← Fails here
    ...
```

**Problem:** Claude CLI wraps JSON output in markdown code blocks:

```
```json
{ "entries": [...] }
```
```

The Python `json.load()` fails because input starts with "\`\`\`json" instead of "{".

**Fix:** Strip markdown code blocks before JSON parsing. One-line sed/python addition.

## Existing Entry Verification

Checked recent entries in `knowledge/expanded/lore/entries/`:

| Entry | Content Status | Method |
|-------|----------------|--------|
| entry_1767098624 | FULL (~500 words) | llama-lore-creator.sh |
| entry_1767098663 | FULL (~400 words) | llama-lore-creator.sh |
| entry_1767629379 | FAIL ("Failed to parse") | lore-flow.sh |

**Conclusion:** Direct tool calls work. Pipeline integration has JSON parsing issue.

## Known Issues Status

| Issue | Status | Impact on Phase 1 |
|-------|--------|-------------------|
| #5 - Meta-commentary | Open | Phase 2 (quality) |
| #6 - Empty content | Closed but recurs | **Blocking** - JSON parse bug |

## Current Data Volume

- **1,202 entries** (verified 2026-01-05)
- **107 books**
- **92 personas**

Entry storage: `knowledge/expanded/lore/entries/entry_<timestamp>[_<hash>].json`

## What Works

1. **LLM extraction** - All three providers generate quality lore
2. **Entry creation** - `manage-lore.sh create-entry` works correctly
3. **Persona loading** - `persona-manager.py` loads context successfully
4. **Book linking** - Chronicle books created and linked to personas
5. **Schema validation** - JSON structure matches `knowledge/core/lore/schema.json`

## What Needs Fixing

1. **JSON parsing in lore-flow.sh** - Strip markdown code blocks from LLM output
2. **Chronicle book lookup** - Warning about missing book (non-blocking)
3. **Persona mapping format** - Warning about filename format (non-blocking)

## Recommended Fix (Plan 1-1)

**Scope:** Single edit to `integration/lore-flow.sh`

**Location:** Line 191, before `python3 -c`

**Change:** Strip markdown code blocks:
```bash
EXTRACTED_LORE=$(echo "$EXTRACTED_LORE" | sed 's/^```json//;s/^```$//')
```

Or inline in Python:
```python
import re
raw = sys.stdin.read()
clean = re.sub(r'^```json\n?|```$', '', raw.strip())
data = json.loads(clean)
```

**Verification:** Run `lore-flow.sh manual "test"` and confirm entry has narrative content.

---

*Research completed: 2026-01-05*
*Ready for: Plan 1-1 creation*
