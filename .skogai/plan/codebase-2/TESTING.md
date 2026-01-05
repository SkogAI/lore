# Testing Practices

*Generated: 2026-01-05*
*Focus: Lore generation and connections created with context and lore-integrator*

## Test Infrastructure

### Current Testing Status

**Comprehensive Testing:**
- ✅ Shell scripts (jq transformations) - 100+ test cases
- ⚠️  Python API - Manual testing only (no framework)
- ⚠️  Integration - Manual end-to-end verification
- ❌ Unit tests - Not implemented
- ❌ Coverage metrics - Not tracked

### Test Directory Structure

```
scripts/jq/
├── crud-get/
│   ├── transform.jq
│   ├── test.sh                # 20+ test cases
│   └── test-input-*.json      # Deterministic fixtures
├── crud-set/
│   ├── transform.jq
│   ├── test.sh                # 20+ test cases
│   └── test-input-*.json
├── crud-delete/
│   ├── transform.jq
│   ├── test.sh                # 15+ test cases
│   └── test-input-*.json
└── schema-validation/
    ├── transform.jq
    ├── test.sh                # 62 test cases
    └── test-input-*.json

agents/api/
├── lore_api.py                # Manual test in __main__
└── agent_api.py               # Manual test in __main__

# Missing: tests/ directory for pytest
```

## Shell Script Testing

### Pattern: Comprehensive jq Transformation Testing

**File:** `scripts/jq/schema-validation/test.sh`

**Test Structure:**
```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing schema-validation transformation..."

# Helper function
test_case() {
  local name=$1
  local input=$2
  local expected=$3

  echo -n "Test: $name... "
  result=$(jq -c -f "$TRANSFORM" <<< "$input")

  if [[ "$result" == "$expected" ]]; then
    echo "PASS"
  else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
  fi
}
```

### Test Coverage Categories

**From schema-validation/test.sh (62 test cases):**

1. **Happy Path Tests (5 tests)**
   - Valid objects passing all checks
   - Nested fields with valid values
   - All JSON types (string, number, boolean, array, object)

2. **Falsy Value Tests (6 tests)**
   - null values (should pass - null is valid)
   - false boolean (should pass - false is valid)
   - Zero number (should pass - 0 is valid)
   - Empty string (should pass - "" is valid)
   - Empty array (should pass - [] is valid)
   - Empty object (should pass - {} is valid)

3. **Type Safety Tests (3 tests)**
   - Wrong type (string instead of number)
   - Missing required fields
   - Multiple validation errors

4. **Boundary Conditions (4 tests)**
   - Empty schema (all inputs valid)
   - Empty input object
   - Nested missing fields
   - Deep nesting validation

5. **Error Handling (2 tests)**
   - Malformed schema
   - Null vs null type distinction

6. **Complete Coverage (2 tests)**
   - Only required fields defined
   - Only types defined (no required)

**Key Insight:** Explicitly tests falsy values that break naive implementations

### Test Principles

1. **Deterministic Input**
   - No random data generation
   - All inputs in version control (test-input-*.json)
   - Reproducible across runs

2. **Exact Expected Output**
   - Tests compare exact JSON strings
   - No fuzzy matching
   - Clear pass/fail criteria

3. **Fail Fast**
   - `set -euo pipefail` - Exit on any error
   - First failure stops test run
   - Detailed error messages

4. **Test Fixtures**
   ```bash
   # Example fixture: test-input-1.json
   {
     "name": "test",
     "age": 30,
     "active": true
   }

   # Example fixture: test-input-falsy.json
   {
     "name": null,
     "age": 0,
     "active": false,
     "tags": [],
     "meta": {}
   }
   ```

5. **Edge Cases First**
   - Test boundaries before happy path
   - Focus on what could break
   - Falsy values, empty collections, nulls

### Running Shell Tests

```bash
# Run all jq transformation tests
for test in scripts/jq/*/test.sh; do
  echo "Running $test..."
  bash "$test"
done

# Run specific test suite
bash scripts/jq/schema-validation/test.sh

# Expected output:
# Testing schema-validation transformation...
# Test: Valid object passing all checks... PASS
# Test: Missing required field... PASS
# Test: Falsy value null... PASS
# ...
# All 62 tests passed!
```

## Python API Testing

### Current Pattern: Manual Testing

**File:** `agents/api/lore_api.py:525-558`

```python
if __name__ == "__main__":
    # Manual integration test
    api = LoreAPI()

    # Create test persona
    persona = api.create_persona(
        name="Test Forest Guardian",
        core_description="A magical protector of the forest glade",
        personality_traits=["compassionate", "protective", "wise", "gentle"],
        voice_tone="serene and comforting",
    )

    print(f"Created test persona: {persona['id']}")

    # Create test entry
    entry = api.create_lore_entry(
        title="Test Chronicle",
        content="In the depths of the digital realm...",
        category="lore",
        tags=["test", "chronicle"]
    )

    print(f"Created test entry: {entry['id']}")

    # Create test book
    book = api.create_lore_book(
        title="Test Chronicles",
        description="A collection of test entries"
    )

    print(f"Created test book: {book['id']}")

    # Link entry to book
    api.add_entry_to_book(entry['id'], book['id'])

    print("✅ Manual test complete")
```

**Issues with Current Pattern:**
- ❌ No assertions - just prints output
- ❌ No cleanup - leaves test data in filesystem
- ❌ No isolation - tests affect real data
- ❌ No coverage tracking
- ❌ Can't run automatically in CI/CD

### Recommended Pattern: pytest Framework

**Proposed Structure:**
```
tests/
├── __init__.py
├── conftest.py                   # Shared fixtures
├── unit/
│   ├── test_lore_api.py         # Unit tests for lore_api
│   ├── test_agent_api.py        # Unit tests for agent_api
│   └── test_persona_manager.py  # Unit tests for persona manager
├── integration/
│   ├── test_lore_flow.py        # End-to-end pipeline tests
│   ├── test_relationship_builder.py
│   └── test_context_manager.py
└── fixtures/
    ├── test_persona.json
    ├── test_entry.json
    └── test_book.json
```

**Example Unit Test:**
```python
import pytest
import tempfile
from pathlib import Path
from agents.api.lore_api import LoreAPI

@pytest.fixture
def temp_lore_dir(tmp_path):
    """Create temporary lore directory structure."""
    lore_dir = tmp_path / "knowledge" / "expanded" / "lore"
    lore_dir.mkdir(parents=True)
    (lore_dir / "entries").mkdir()
    (lore_dir / "books").mkdir()
    (tmp_path / "knowledge" / "expanded" / "personas").mkdir(parents=True)
    return tmp_path

@pytest.fixture
def api(temp_lore_dir, monkeypatch):
    """Create LoreAPI instance with temp directory."""
    monkeypatch.setattr("agents.api.lore_api.REPO_ROOT", temp_lore_dir)
    return LoreAPI()

def test_create_persona(api):
    """Test persona creation."""
    persona = api.create_persona(
        name="Test Guardian",
        core_description="Test description",
        personality_traits=["wise", "kind", "patient", "gentle"],
        voice_tone="serene"
    )

    # Assertions
    assert persona is not None
    assert persona["name"] == "Test Guardian"
    assert "persona_" in persona["id"]
    assert len(persona["core_traits"]["values"]) == 2
    assert persona["core_traits"]["values"] == ["wise", "kind"]
    assert len(persona["core_traits"]["motivations"]) == 2
    assert persona["core_traits"]["motivations"] == ["patient", "gentle"]
    assert persona["voice"]["tone"] == "serene"

def test_create_entry(api):
    """Test entry creation."""
    entry = api.create_lore_entry(
        title="Test Entry",
        content="Test content",
        category="lore",
        tags=["test"]
    )

    assert entry is not None
    assert entry["title"] == "Test Entry"
    assert entry["content"] == "Test content"
    assert entry["category"] == "lore"
    assert "test" in entry["tags"]
    assert "entry_" in entry["id"]

def test_add_entry_to_book(api):
    """Test bidirectional entry-book linking."""
    # Create entry and book
    entry = api.create_lore_entry("Test Entry", "Content", "lore")
    book = api.create_lore_book("Test Book", "Description")

    # Link them
    result = api.add_entry_to_book(entry["id"], book["id"])
    assert result is True

    # Verify bidirectional link
    updated_entry = api.get_lore_entry(entry["id"])
    updated_book = api.get_lore_book(book["id"])

    assert updated_entry["book_id"] == book["id"]
    assert entry["id"] in updated_book["entries"]

def test_link_book_to_persona(api):
    """Test book-persona linking."""
    persona = api.create_persona("Test", "Desc", ["trait1", "trait2", "trait3", "trait4"], "tone")
    book = api.create_lore_book("Test Book", "Description")

    result = api.link_book_to_persona(book["id"], persona["id"])
    assert result is True

    # Verify bidirectional link
    updated_book = api.get_lore_book(book["id"])
    updated_persona = api.get_persona(persona["id"])

    assert persona["id"] in updated_book["readers"]
    assert book["id"] in updated_persona["knowledge"]["lore_books"]
```

**Running Tests:**
```bash
# Install pytest
pip install pytest pytest-cov

# Run all tests
pytest tests/

# Run with coverage
pytest --cov=agents --cov-report=html tests/

# Run specific test
pytest tests/unit/test_lore_api.py::test_create_persona

# Run tests matching pattern
pytest -k "test_create"
```

## Integration Testing

### Current Practice: Manual Verification

**End-to-End Pipeline Test:**
```bash
# 1. Create entry with pipeline
./integration/lore-flow.sh manual "Fixed critical bug in quantum mojito mixer"

# 2. Verify entry created
ls knowledge/expanded/lore/entries/ | tail -1

# 3. Verify content populated
jq '.content' knowledge/expanded/lore/entries/entry_*.json | tail -1

# 4. Verify book linked
jq '.book_id' knowledge/expanded/lore/entries/entry_*.json | tail -1
```

**Issues:**
- ❌ Manual - requires human to verify
- ❌ Creates real data - no cleanup
- ❌ Can't run in CI/CD
- ❌ No assertions

### Recommended Integration Tests

**Proposed File:** `tests/integration/test_lore_flow.py`

```python
import pytest
import subprocess
import json
from pathlib import Path

@pytest.fixture
def isolated_repo(tmp_path, monkeypatch):
    """Create isolated repository for testing."""
    repo = tmp_path / "lore"
    repo.mkdir()

    # Copy scripts
    subprocess.run(["cp", "-r", "integration", str(repo)])
    subprocess.run(["cp", "-r", "tools", str(repo)])

    # Create data directories
    (repo / "knowledge" / "expanded" / "lore" / "entries").mkdir(parents=True)
    (repo / "knowledge" / "expanded" / "lore" / "books").mkdir(parents=True)
    (repo / "knowledge" / "expanded" / "personas").mkdir(parents=True)

    monkeypatch.chdir(repo)
    return repo

def test_lore_flow_manual_input(isolated_repo):
    """Test manual input pipeline."""
    # Run pipeline
    result = subprocess.run(
        ["./integration/lore-flow.sh", "manual", "Test content for entry"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0

    # Verify entry created
    entries_dir = isolated_repo / "knowledge" / "expanded" / "lore" / "entries"
    entries = list(entries_dir.glob("entry_*.json"))
    assert len(entries) == 1

    # Verify content populated
    with open(entries[0]) as f:
        entry = json.load(f)

    assert entry["content"] != ""  # Not empty (Issue #6 test)
    assert "test" in entry["content"].lower()  # Contains input

def test_lore_flow_git_diff(isolated_repo):
    """Test git diff input pipeline."""
    # Setup git repo
    subprocess.run(["git", "init"], cwd=isolated_repo)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=isolated_repo)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=isolated_repo)

    # Create test file and commit
    test_file = isolated_repo / "test.txt"
    test_file.write_text("Initial content")
    subprocess.run(["git", "add", "test.txt"], cwd=isolated_repo)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=isolated_repo)

    # Make change
    test_file.write_text("Updated content")

    # Run pipeline
    result = subprocess.run(
        ["./integration/lore-flow.sh", "git-diff", "HEAD"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0

    # Verify entry created from git diff
    entries_dir = isolated_repo / "knowledge" / "expanded" / "lore" / "entries"
    entries = list(entries_dir.glob("entry_*.json"))
    assert len(entries) == 1

    with open(entries[0]) as f:
        entry = json.load(f)

    assert entry["content"] != ""
    assert entry["metadata"]["created_by"] == "Test"  # From git author
```

## Provider Testing

### Documented Status (CLAUDE.md)

```
**Provider Status:**

- ✅ **Claude** - Tested and working via OpenRouter API
- ✅ **OpenAI** - Tested and working via OpenRouter API
- ✅ **Ollama** - Tested with local models (llama3.2:3b)
```

### Manual Provider Verification

**Test Script:**
```bash
#!/bin/bash
# Test all three LLM providers

echo "Testing LLM providers..."

# Test Ollama
echo "1. Testing Ollama..."
LLM_PROVIDER=ollama ./tools/llama-lore-creator.sh - entry "Test Ollama" "place"
if [ $? -eq 0 ]; then
  echo "✅ Ollama: PASS"
else
  echo "❌ Ollama: FAIL"
fi

# Test Claude
echo "2. Testing Claude..."
LLM_PROVIDER=claude ./tools/llama-lore-creator.sh - entry "Test Claude" "place"
if [ $? -eq 0 ]; then
  echo "✅ Claude: PASS"
else
  echo "❌ Claude: FAIL"
fi

# Test OpenAI
echo "3. Testing OpenAI..."
LLM_PROVIDER=openai ./tools/llama-lore-creator.sh openai entry "Test OpenAI" "place"
if [ $? -eq 0 ]; then
  echo "✅ OpenAI: PASS"
else
  echo "❌ OpenAI: FAIL"
fi
```

### Recommended Provider Tests

**Proposed File:** `tests/integration/test_llm_providers.py`

```python
import pytest
import os

@pytest.mark.skipif(
    not os.environ.get("OPENROUTER_API_KEY"),
    reason="No OpenRouter API key"
)
def test_claude_provider():
    """Test Claude provider via OpenRouter."""
    # Implementation

@pytest.mark.skipif(
    not os.environ.get("OPENROUTER_API_KEY"),
    reason="No OpenRouter API key"
)
def test_openai_provider():
    """Test OpenAI provider via OpenRouter."""
    # Implementation

@pytest.mark.skipif(
    not os.environ.get("OLLAMA_HOST"),
    reason="No Ollama host configured"
)
def test_ollama_provider():
    """Test Ollama local provider."""
    # Implementation
```

## Known Issues Testing

### Issue #5: Meta-Commentary Detection

**Current Validation (llama-lore-creator.sh:43-67):**
```bash
validate_lore_output() {
  local content="$1"

  # Check for meta-commentary patterns
  if echo "$content" | head -n 1 | grep -qiE '^[[:space:]]*(I will|Let me|Here is)'; then
    return 1  # Validation failed
  fi

  return 0
}
```

**Test Case:**
```bash
# Input with meta-commentary
content="I will create a lore entry about the dark tower.

The dark tower stands..."

# Should fail validation
if validate_lore_output "$content"; then
  echo "❌ FAIL: Should detect meta-commentary"
else
  echo "✅ PASS: Meta-commentary detected"
fi

# Input without meta-commentary
content="The dark tower stands tall in the misty highlands..."

# Should pass validation
if validate_lore_output "$content"; then
  echo "✅ PASS: Clean narrative accepted"
else
  echo "❌ FAIL: Should accept clean narrative"
fi
```

### Issue #6: Empty Content Field

**Test to Reproduce:**
```bash
# Run pipeline
./integration/lore-flow.sh manual "Test content"

# Get entry ID
entry_id=$(ls -t knowledge/expanded/lore/entries/ | head -1 | sed 's/\.json//')

# Check content field
content=$(jq -r '.content' "knowledge/expanded/lore/entries/${entry_id}.json")

if [ "$content" = "" ] || [ "$content" = "null" ]; then
  echo "❌ FAIL: Content is empty (Issue #6 reproduced)"
  exit 1
else
  echo "✅ PASS: Content populated"
fi
```

**Root Cause:** Variable name typo in lore-flow.sh line 263 (`entry_file` vs `$ENTRY_FILE`)

## Test Coverage Goals

### Current Coverage (Estimated)
```
Shell scripts (jq):       ~90% (comprehensive test suites)
Python API:               ~10% (manual tests only)
Integration:              ~20% (manual verification)
Provider integration:     ~30% (manual testing)
```

### Target Coverage
```
Shell scripts:            100% (maintain current)
Python API:               80%+ (add pytest)
Integration:              70%+ (automated tests)
Provider integration:     80%+ (mock + real tests)
```

## Continuous Integration

### Recommended CI/CD Pipeline

**File:** `.github/workflows/test.yml` (proposed)

```yaml
name: Test Suite

on: [push, pull_request]

jobs:
  test-shell:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run shell tests
        run: |
          for test in scripts/jq/*/test.sh; do
            bash "$test"
          done

  test-python:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      - name: Run pytest
        run: pytest --cov=agents --cov-report=xml tests/
      - name: Upload coverage
        uses: codecov/codecov-action@v2

  test-integration:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup test environment
        run: |
          # Install ollama for local testing
          # Setup test data
      - name: Run integration tests
        run: pytest tests/integration/
```

## Test Execution

### Running All Tests

```bash
# Shell tests
for test in scripts/jq/*/test.sh; do
  echo "Running $test..."
  bash "$test" || exit 1
done

# Python tests (when implemented)
pytest tests/

# Integration tests (when implemented)
pytest tests/integration/

# Provider tests (requires API keys)
OPENROUTER_API_KEY=$KEY pytest tests/integration/test_llm_providers.py
```

### Test Fixtures

**Location:** `tests/fixtures/`

```json
// tests/fixtures/test_persona.json
{
  "id": "persona_test",
  "name": "Test Persona",
  "core_traits": {
    "temperament": "balanced",
    "values": ["wise", "kind"],
    "motivations": ["patient", "gentle"]
  },
  "voice": {
    "tone": "serene",
    "patterns": [],
    "vocabulary": "standard"
  }
}

// tests/fixtures/test_entry.json
{
  "id": "entry_test",
  "title": "Test Entry",
  "content": "Test content",
  "category": "lore",
  "tags": ["test"],
  "metadata": {
    "created_by": "test",
    "created_at": "2025-01-01T00:00:00Z"
  }
}
```

## Summary

**Strengths:**
- ✅ Comprehensive jq transformation testing (100+ tests)
- ✅ Deterministic test fixtures
- ✅ Clear pass/fail criteria
- ✅ Edge case coverage (falsy values, boundaries)

**Gaps:**
- ❌ No Python test framework (pytest needed)
- ❌ No integration test automation
- ❌ No coverage tracking
- ❌ Manual provider verification only
- ❌ No CI/CD pipeline

**Immediate Actions:**
1. Add pytest framework for Python API
2. Create integration test suite
3. Setup CI/CD pipeline
4. Add coverage reporting
5. Automate provider testing

**Long-term Goals:**
- 80%+ code coverage across Python modules
- Automated regression testing for known issues
- Performance testing for large datasets (10k+ entries)
- Stress testing for concurrent operations
