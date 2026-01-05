# Testing Practices

## Testing Philosophy

The Lore project follows a **validation-first, schema-driven testing philosophy** rather than traditional unit testing.

**Key Principles:**
1. **Schema validation** - JSON schemas are the source of truth
2. **Pre-commit validation** - Prevent bad data at commit time
3. **Integration testing** - Workflow-based testing via GitHub Actions
4. **Real-world usage** - Production testing through actual operations

## Test Framework & Structure

### Test Location
- **Primary:** `/home/skogix/lore/tests/`
- **Current structure:** Minimal - single subdirectory `tests/basic-flow/`
- **Test format:** Simple JSON definitions (not pytest/unittest)

### Test Definition Format
```json
{
  "test_name": "basic-flow",
  "description": "Basic workflow test for SkogAI orchestration",
  "input": "Test input",
  "expected_outcome": {
    "response_type": "implementation",
    "contains": ["expected", "strings"]
  },
  "tracking": {
    "orchestrator_version": "v0",
    "agents": ["agent_list"],
    "knowledge_modules": ["core"]
  }
}
```

### Test Coverage
**Current state:** Minimal explicit test suite

**What's tested:**
- ✅ Schema validation (JSON schemas)
- ✅ Path conventions (no hardcoded paths)
- ✅ File structure and naming
- ✅ Git workflow integrity
- ✅ Growth metrics and patterns
- ✅ Document updates
- ❌ Unit tests (no pytest/unittest framework)
- ❌ Code coverage (no coverage tools)

## Validation & Pre-Commit

### Pre-Commit Framework
**Configuration:** `.pre-commit-config.yaml` (v6.0.0)

**Local Validation Hooks:**
```yaml
- id: validate-shell-paths
  name: Validate Shell Paths
  entry: bash scripts/pre-commit/validate.sh
  language: system
  types: [shell]

- id: validate-python-paths
  name: Validate Python Paths
  entry: python3 scripts/pre-commit/validate.py --strict
  language: system
  types: [python]
```

**Standard Hooks:**
- `check-case-conflict` - Files that conflict in case-insensitive filesystems
- `check-merge-conflict` - Merge conflict markers
- `check-yaml` - YAML syntax validation
- `check-json` - JSON syntax validation
- `mixed-line-ending` - Line ending consistency (LF)
- `trailing-whitespace` - Trailing whitespace removal
- `end-of-file-fixer` - Ensure files end with newline

### Validation Scripts

**`scripts/pre-commit/validate.sh`** - Shell script path checking:
- Detects hardcoded absolute paths in `.sh` files
- Ensures relative path usage
- Supports `--strict` mode for CI

**`scripts/pre-commit/validate.py`** - Python hardcoded path detection:
- Scans Python files for absolute paths
- Validates path construction patterns
- Strict mode enforces all checks

**Execution:**
```bash
# Pre-commit validation
bash scripts/pre-commit/validate.sh
python3 scripts/pre-commit/validate.py --strict

# Manual validation
pre-commit run --all-files
```

## Integration Testing

### GitHub Actions Workflows
**Location:** `.github/workflows/`

**Active Workflows:**

1. **`claude.yml`** - Claude Code integration
   - **Trigger:** On comment, issue, PR review
   - **Purpose:** Claude Code automation
   - **Tests:** Integration with Claude Code CLI

2. **`lore-growth.yml`** - Growth monitoring
   - **Trigger:** Scheduled (every 6 hours)
   - **Purpose:** Monitor lore system health
   - **Tests:** Entry/book/persona counts, pattern detection

3. **`doc-updater.yml`** - Documentation updates
   - **Trigger:** On push to master
   - **Purpose:** Keep documentation synchronized
   - **Tests:** Documentation consistency

4. **`lore-keeper-bot.yml`** - Lore maintenance
   - **Trigger:** Various events
   - **Purpose:** Automated lore management
   - **Tests:** Lore data integrity

5. **`claude-code-review.yml`** - Code review automation
   - **Trigger:** Pull requests
   - **Purpose:** Automated code review
   - **Tests:** Code quality checks

6. **`release.yml`** - Release automation
   - **Trigger:** Tagged releases
   - **Purpose:** Automated releases
   - **Tests:** Build and package verification

### CI/CD Configuration
**Workflow toggle:** `.github/workflow-config.yml`
**Archived workflows:** `.github/workflows-old/`

## Testing Practices

### 1. Schema Validation Testing
**Purpose:** Ensure all data conforms to JSON Schema contracts

**Schemas:**
- Entry: `knowledge/core/lore/schema.json`
- Book: `knowledge/core/book-schema.json`
- Persona: `knowledge/core/persona/schema.json`

**Validation methods:**
- `argc validate-entry <entry_id>` - CLI validation
- `argc validate-book <book_id>` - Book validation
- `argc validate-persona <persona_id>` - Persona validation
- jq transformations in `scripts/jq/` - Field validation

**Example:**
```bash
# Validate entry against schema
argc validate-entry entry_1743758088

# Check required fields
jq 'has("id", "title", "content", "category")' entry.json
```

### 2. Path Validation Testing
**Purpose:** Prevent hardcoded paths, ensure portability

**Methods:**
- Pre-commit hooks scan for absolute paths
- Validation scripts check Python and Shell files
- CI enforces strict mode

**Example:**
```bash
# Check shell scripts
bash scripts/pre-commit/validate.sh

# Check Python files
python3 scripts/pre-commit/validate.py --strict
```

### 3. Workflow Integration Testing
**Purpose:** Test end-to-end pipeline functionality

**Test approach:**
- Real-world usage through GitHub Actions
- Workflow definitions track orchestrator versions
- Agent and knowledge module tracking

**Example test flow:**
```bash
# Manual pipeline test
./integration/lore-flow.sh manual "Test content"

# Verify entry created
argc list-entries | grep -i "test"

# Validate created entry
entry_id=$(argc list-entries | head -1 | cut -d: -f1)
argc validate-entry "$entry_id"
```

### 4. Git Workflow Testing
**Purpose:** Ensure git integration works correctly

**Tests:**
- Merge conflict detection
- Case conflict detection
- Line ending consistency
- YAML/JSON syntax validation

**Automated via:**
- Pre-commit hooks
- GitHub Actions workflows

### 5. Growth Monitoring Testing
**Purpose:** Track system health and patterns

**Metrics tracked:**
- Entry count growth rate
- Book creation patterns
- Persona utilization
- Context session lifecycle

**Monitoring:**
- `lore-growth.yml` workflow (every 6 hours)
- Pattern detection for anomalies
- Automated alerts on issues

## Manual Testing

### Entry CRUD Testing
```bash
# Create entry
./tools/manage-lore.sh create-entry "Test Entry" "lore"
entry_id=$(./tools/manage-lore.sh list-entries | head -1 | cut -d: -f1)

# Read entry
./tools/manage-lore.sh show-entry "$entry_id"

# Update entry (via jq)
jq '.content = "Updated content"' \
  "knowledge/expanded/lore/entries/${entry_id}.json" > tmp.json
mv tmp.json "knowledge/expanded/lore/entries/${entry_id}.json"

# Validate entry
argc validate-entry "$entry_id"

# Delete entry (manual - no delete command)
rm "knowledge/expanded/lore/entries/${entry_id}.json"
```

### Book CRUD Testing
```bash
# Create book
./tools/manage-lore.sh create-book "Test Book" "Description"
book_id=$(./tools/manage-lore.sh list-books | head -1 | cut -d: -f1)

# Link entry to book
./tools/manage-lore.sh add-to-book "$entry_id" "$book_id"

# Read book
./tools/manage-lore.sh show-book "$book_id"

# Validate book
argc validate-book "$book_id"
```

### Pipeline Testing
```bash
# Test manual input
./integration/lore-flow.sh manual "Fixed quantum mojito bug"

# Test git diff extraction
git add .
git commit -m "test: pipeline testing"
./integration/lore-flow.sh git-diff HEAD

# Verify entry created with content
entry_id=$(./tools/manage-lore.sh list-entries | head -1 | cut -d: -f1)
./tools/manage-lore.sh show-entry "$entry_id" | grep -q "content"
```

### LLM Provider Testing
```bash
# Test Ollama (local)
LLM_PROVIDER=ollama ./tools/llama-lore-creator.sh - entry "Test" "lore"

# Test Claude (via OpenRouter)
LLM_PROVIDER=claude ./tools/llama-lore-creator.sh - entry "Test" "lore"

# Test OpenAI (via OpenRouter)
LLM_PROVIDER=openai ./tools/llama-lore-creator.sh gpt-4 entry "Test" "lore"
```

## Test Execution

### Local Testing
```bash
# Run pre-commit hooks
pre-commit run --all-files

# Run validation scripts
bash scripts/pre-commit/validate.sh
python3 scripts/pre-commit/validate.py --strict

# Test orchestrator
python orchestrator/orchestrator.py init lore

# Test argc commands
argc list-entries
argc list-books
argc list-personas
```

### CI Testing
- Push to master triggers workflows
- Pull requests trigger code review
- Scheduled workflows run every 6 hours
- Manual workflow dispatch available

## Known Testing Gaps

### Missing Test Infrastructure
- ❌ No pytest/unittest framework configured
- ❌ No test discovery automation
- ❌ No code coverage measurement tools
- ❌ No mocking/stubbing infrastructure
- ❌ No integration test suite
- ❌ No performance/load testing

### Compensating Factors
- ✅ Strict pre-commit validation prevents bad data
- ✅ Schema validation enforces data integrity
- ✅ GitHub Actions provide workflow testing
- ✅ Real-world usage validates functionality
- ✅ Manual testing procedures documented

### What Should Be Added
1. **Pytest framework** - Unit tests for Python modules
2. **Shell test framework** - bats or shunit2 for shell scripts
3. **Code coverage** - pytest-cov for Python coverage
4. **Integration tests** - End-to-end pipeline tests
5. **Mock LLM responses** - Test without API calls
6. **Load testing** - Test with 10k+ entries
7. **Concurrent testing** - Multi-user scenarios

## Testing Recommendations

### Priority 1 (Critical)
1. Add integration tests for `lore-flow.sh` pipeline
2. Add unit tests for `lore_api.py` CRUD operations
3. Add schema validation tests for all JSON files
4. Add concurrent access tests (file locking)

### Priority 2 (High)
5. Add mock LLM tests (avoid API calls)
6. Add shell script tests (bats framework)
7. Add error handling tests
8. Add edge case tests (empty fields, special characters)

### Priority 3 (Nice-to-have)
9. Add performance tests (large datasets)
10. Add code coverage reporting
11. Add mutation testing
12. Add property-based testing

## Test Data

### Test Fixtures
**Location:** Not currently organized
**Recommendation:** Create `tests/fixtures/` with:
- Sample entries, books, personas
- Valid and invalid JSON samples
- Edge case test data

### Test Cleanup
**Current:** Manual cleanup required
**Recommendation:** Add teardown scripts to remove test data after runs

## Debugging Tests

### Enable Debug Logging
```bash
# Python
export LOG_LEVEL=DEBUG
python agents/api/lore_api.py

# Shell (set -x)
bash -x tools/manage-lore.sh list-entries
```

### Inspect Test Failures
```bash
# Check pre-commit output
pre-commit run --all-files --verbose

# Check GitHub Actions logs
gh run list
gh run view <run_id>
```

### Validate JSON Manually
```bash
# Check JSON syntax
jq empty knowledge/expanded/lore/entries/entry_*.json

# Validate against schema
ajv validate -s knowledge/core/lore/schema.json \
  -d knowledge/expanded/lore/entries/entry_1743758088.json
```

## Test Documentation

### Test Coverage Documentation
**Current:** Not maintained
**Recommendation:** Document what's tested in each area

### Test Plan Documentation
**Current:** This document
**Future:** Create detailed test plans per component

### Bug Report Process
**Location:** GitHub Issues
**Known Issues:**
- Issue #5: LLM meta-commentary in generated content
- Issue #6: Pipeline creates entries with empty content

## Summary

The Lore project prioritizes **data integrity through schema validation and pre-commit hooks** over traditional unit testing. This approach works well for:
- Ensuring valid JSON data
- Preventing hardcoded paths
- Validating workflows through automation

However, gaps exist in:
- Unit test coverage
- Integration test automation
- Performance testing
- Concurrent access testing

The system compensates through:
- Real-world usage testing
- GitHub Actions automation
- Manual testing procedures
- Schema-driven validation
