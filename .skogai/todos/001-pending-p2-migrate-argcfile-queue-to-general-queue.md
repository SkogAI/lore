---
status: pending
priority: p2
issue_id: "001"
tags: [queue, argcfile, refactor, infrastructure]
dependencies: []
---

# Migrate Argcfile Queue to General Queue Solution

## Problem Statement

The lore project currently has a queue implementation in `Argcfile.sh` (lines 470-642) that duplicates functionality from the general queue solution at `/home/skogix/.local/bin/queue`.

This creates:
- Code duplication and maintenance overhead
- Two different queue implementations with potentially divergent behavior
- Confusion about which queue system to use

**Current state:**
- Argcfile queue is a placeholder for testing LLM generation workflows
- It's currently OK to keep for development/testing purposes
- General queue (`/home/skogix/.local/bin/queue`) is production-ready infrastructure

**When to migrate:**
- After LLM generation queue patterns are validated
- When Argcfile queue is no longer needed for testing
- Before considering the feature "production-ready"

## Findings

### Argcfile Queue (lore/Argcfile.sh)
- **Lines:** 470-642 (173 lines)
- **Commands:** `queue-add`, `queue-list`, `queue-process`, `queue-clear`
- **Storage:** `.lore-queue/` directory
- **Features:** Type validation, status tracking, dry-run support

### General Queue (/home/skogix/.local/bin/queue)
- **Type:** Bash script (production-ready)
- **Storage:** `~/.cache/skogai/queue.json`
- **Commands:** `add`, `list`, `status`, `run`, `remove`, `clear`, `retry`
- **Features:** Atomic operations (flock), retry logic, parallel jobs, daemon mode
- **Pattern:** KISS - 252 lines, minimal, reliable

### Key Differences
1. General queue has retry logic and max_attempts tracking
2. General queue uses atomic flock operations
3. General queue has daemon mode capability
4. Argcfile queue has more validation but less resilience

## Proposed Solutions

### Option 1: Complete Migration (Recommended)
**Replace Argcfile queue commands with calls to general queue**

```bash
# Before:
argc queue-add --type doc --input "path/to/file.md"

# After:
queue add "argc generate-from-docs --path path/to/file.md"
```

**Pros:**
- Single source of truth
- Leverage production-ready retry logic
- Reduce maintenance burden
- Consistent queue behavior across all tools

**Cons:**
- Requires refactoring generate-* commands to work with queue
- Need to test integration thoroughly
- Breaking change for any existing workflows

**Effort:** Medium (4-6 hours)
**Risk:** Low - general queue is proven infrastructure

---

### Option 2: Wrapper Approach
**Keep Argcfile commands as high-level wrappers around general queue**

```bash
# Argcfile.sh
queue-add() {
  # Validate inputs (keep existing validation)
  # Transform to general queue format
  queue add "argc generate-from-${argc_type} ..."
}
```

**Pros:**
- Preserve Argcfile interface
- Add validation layer on top of queue
- Gradual migration path

**Cons:**
- Still maintaining wrapper code
- Extra layer of indirection
- Not true KISS

**Effort:** Low (2-3 hours)
**Risk:** Very low

---

### Option 3: Keep Both (Status Quo)
**Maintain separate queue for lore-specific operations**

**Pros:**
- No immediate work required
- Useful for testing patterns
- Domain-specific queue behavior

**Cons:**
- Code duplication
- Two systems to maintain
- Confusing for future developers

**Effort:** None
**Risk:** Technical debt accumulation

## Recommended Action

**DEFERRED - Keep Argcfile queue as testing placeholder**

The current Argcfile queue implementation should remain until:
1. LLM generation patterns are validated and stable
2. Resource-aware scheduling requirements are clear
3. Integration between argc commands and queue is tested

**When ready to migrate, follow Option 1 (Complete Migration):**

1. **Phase 1: Prepare general queue**
   - Add any missing features from Argcfile queue (if needed)
   - Test daemon mode with LLM generation commands
   - Verify retry logic works for LLM failures

2. **Phase 2: Update generate-* commands**
   - Ensure `generate-from-docs`, `generate-from-git`, `generate-from-stdin` work as standalone commands
   - Add proper exit codes for queue retry logic
   - Test error handling

3. **Phase 3: Remove Argcfile queue**
   - Delete queue namespace (lines 470-642)
   - Update documentation to use `queue add "argc generate-..."`
   - Archive `.lore-queue/` directory

4. **Phase 4: Verify integration**
   - Test end-to-end: queue add → run → verify lore entry created
   - Test daemon mode during idle hours
   - Confirm retry logic for failed LLM calls

## Acceptance Criteria

- [ ] General queue successfully processes `argc generate-*` commands
- [ ] Retry logic handles LLM failures (API errors, rate limits)
- [ ] Daemon mode runs during specified time windows
- [ ] No functionality lost from removing Argcfile queue
- [ ] Documentation updated with new queue usage patterns
- [ ] All existing queue items migrated (if any)
- [ ] `.lore-queue/` directory cleaned up

## Technical Details

**Files affected:**
- `Argcfile.sh` (remove lines 470-642)
- Documentation mentioning queue commands
- Any scripts calling `argc queue-*` commands

**Testing checklist:**
- [ ] `queue add "argc generate-from-git HEAD"` creates entry
- [ ] `queue add "argc generate-from-docs docs/README.md"` works
- [ ] Failed LLM calls get retried (test with bad API key)
- [ ] Daemon mode respects time windows
- [ ] Multiple parallel jobs don't corrupt queue.json

## Work Log

### 2026-01-05 - Todo Created

**By:** Claude Code

**Actions:**
- Analyzed both queue implementations
- Compared Argcfile queue (173 lines) vs general queue (252 lines)
- Identified general queue as production-ready infrastructure
- Created migration plan with 3 options

**Decision:**
- Keep Argcfile queue as testing placeholder for now
- Status set to `pending` - will triage when testing phase complete
- Priority p2 - important refactor but not blocking current work

**Notes:**
- General queue pattern (KISS, 252 lines) aligns better with SkogAI values
- Argcfile queue useful for validating LLM generation patterns
- Migration should happen before considering feature production-ready
