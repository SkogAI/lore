# Testing Practices

**Generated:** 2026-01-05

## Current Testing Status

| Area | Coverage | Framework |
|------|----------|-----------|
| Shell scripts (jq) | ~90% | Custom test.sh (100+ tests) |
| Python API | ~10% | Manual only (no pytest) |
| Integration | ~20% | Manual verification |
| Provider integration | ~30% | Manual testing |

## Test Directory Structure

```
scripts/jq/
├── crud-get/
│   ├── transform.jq
│   ├── test.sh                # 20+ test cases
│   └── test-input-*.json
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

---

## Shell Script Testing

### Pattern: jq Transformation Testing

**File:** `scripts/jq/schema-validation/test.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing schema-validation transformation..."

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

# Test cases
test_case "Valid object" '{"name":"test","age":30}' '{"valid":true,"errors":[]}'
test_case "Missing field" '{"name":"test"}' '{"valid":false,"errors":["missing required field: age"]}'
test_case "Falsy value null" '{"name":"test","age":null}' '{"valid":true,"errors":[]}'
```

### Test Coverage Categories (schema-validation)

| Category | Tests | Purpose |
|----------|-------|---------|
| Happy Path | 5 | Valid objects, all JSON types |
| Falsy Values | 6 | null, false, 0, "", [], {} |
| Type Safety | 3 | Wrong types, missing fields |
| Boundary Conditions | 4 | Empty schema, deep nesting |
| Error Handling | 2 | Malformed schema |
| **Total** | **62** | |

### Test Principles

1. **Deterministic Input** - No random data, fixtures in git
2. **Exact Expected Output** - Compare exact JSON strings
3. **Fail Fast** - `set -euo pipefail`, first failure stops
4. **Edge Cases First** - Test boundaries before happy path

### Running Shell Tests

```bash
# Run all jq tests
for test in scripts/jq/*/test.sh; do
  echo "Running $test..."
  bash "$test"
done

# Run specific test suite
bash scripts/jq/schema-validation/test.sh
```

---

## Python API Testing

### Current Pattern: Manual Testing

**File:** `agents/api/lore_api.py:525-558`

```python
if __name__ == "__main__":
    api = LoreAPI()

    # Manual integration test
    persona = api.create_persona(
        name="Test Forest Guardian",
        core_description="A magical protector",
        personality_traits=["compassionate", "wise"],
        voice_tone="serene"
    )
    print(f"Created test persona: {persona['id']}")  # No assertion
```

**Issues:**
- No assertions
- No cleanup (leaves test data)
- No isolation
- Can't run in CI/CD

### Recommended Pattern: pytest

**Proposed Structure:**
```
tests/
├── __init__.py
├── conftest.py                   # Shared fixtures
├── unit/
│   ├── test_lore_api.py
│   ├── test_agent_api.py
│   └── test_persona_manager.py
├── integration/
│   ├── test_lore_flow.py
│   └── test_context_manager.py
└── fixtures/
    ├── test_persona.json
    ├── test_entry.json
    └── test_book.json
```

**Example Unit Test:**
```python
import pytest
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

    assert persona is not None
    assert persona["name"] == "Test Guardian"
    assert "persona_" in persona["id"]

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
    assert "entry_" in entry["id"]

def test_add_entry_to_book(api):
    """Test bidirectional linking."""
    entry = api.create_lore_entry("Test Entry", "Content", "lore")
    book = api.create_lore_book("Test Book", "Description")

    result = api.add_entry_to_book(entry["id"], book["id"])
    assert result is True

    updated_entry = api.get_lore_entry(entry["id"])
    updated_book = api.get_lore_book(book["id"])

    assert updated_entry["book_id"] == book["id"]
    assert entry["id"] in updated_book["entries"]
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
```

---

## Integration Testing

### Current Practice: Manual

```bash
# 1. Create entry with pipeline
./integration/lore-flow.sh manual "Fixed quantum mojito bug"

# 2. Verify entry created
ls knowledge/expanded/lore/entries/ | tail -1

# 3. Verify content populated
jq '.content' knowledge/expanded/lore/entries/entry_*.json | tail -1

# 4. Verify book linked
jq '.book_id' knowledge/expanded/lore/entries/entry_*.json | tail -1
```

### Recommended Integration Tests

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
    subprocess.run(["cp", "-r", "integration", str(repo)])
    subprocess.run(["cp", "-r", "tools", str(repo)])
    # Create directories...
    monkeypatch.chdir(repo)
    return repo

def test_lore_flow_manual_input(isolated_repo):
    """Test manual input pipeline."""
    result = subprocess.run(
        ["./integration/lore-flow.sh", "manual", "Test content"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0

    entries_dir = isolated_repo / "knowledge" / "expanded" / "lore" / "entries"
    entries = list(entries_dir.glob("entry_*.json"))
    assert len(entries) == 1

    with open(entries[0]) as f:
        entry = json.load(f)

    assert entry["content"] != ""  # Issue #6 test
```

---

## Provider Testing

### Manual Verification Script

```bash
#!/bin/bash
echo "Testing LLM providers..."

# Test Ollama
echo "1. Testing Ollama..."
LLM_PROVIDER=ollama ./tools/llama-lore-creator.sh - entry "Test Ollama" "place"
[ $? -eq 0 ] && echo "Ollama: PASS" || echo "Ollama: FAIL"

# Test Claude
echo "2. Testing Claude..."
LLM_PROVIDER=claude ./tools/llama-lore-creator.sh - entry "Test Claude" "place"
[ $? -eq 0 ] && echo "Claude: PASS" || echo "Claude: FAIL"

# Test OpenAI
echo "3. Testing OpenAI..."
LLM_PROVIDER=openai ./tools/llama-lore-creator.sh openai entry "Test OpenAI" "place"
[ $? -eq 0 ] && echo "OpenAI: PASS" || echo "OpenAI: FAIL"
```

### pytest Skip Pattern

```python
import pytest
import os

@pytest.mark.skipif(
    not os.environ.get("OPENROUTER_API_KEY"),
    reason="No OpenRouter API key"
)
def test_claude_provider():
    """Test Claude provider via OpenRouter."""
    pass

@pytest.mark.skipif(
    not os.environ.get("OLLAMA_HOST"),
    reason="No Ollama host configured"
)
def test_ollama_provider():
    """Test Ollama local provider."""
    pass
```

---

## Known Issues Testing

### Issue #5: Meta-Commentary Detection

```bash
# Test validation function
content="I will create a lore entry..."
if validate_lore_output "$content"; then
  echo "FAIL: Should detect meta-commentary"
else
  echo "PASS: Meta-commentary detected"
fi

content="The dark tower stands tall..."
if validate_lore_output "$content"; then
  echo "PASS: Clean narrative accepted"
else
  echo "FAIL: Should accept clean narrative"
fi
```

### Issue #6: Empty Content Test

```bash
./integration/lore-flow.sh manual "Test content"
entry_id=$(ls -t knowledge/expanded/lore/entries/ | head -1 | sed 's/\.json//')
content=$(jq -r '.content' "knowledge/expanded/lore/entries/${entry_id}.json")

if [ "$content" = "" ] || [ "$content" = "null" ]; then
  echo "FAIL: Content is empty (Issue #6)"
  exit 1
else
  echo "PASS: Content populated"
fi
```

---

## Test Coverage Goals

| Area | Current | Target |
|------|---------|--------|
| Shell scripts | ~90% | 100% |
| Python API | ~10% | 80%+ |
| Integration | ~20% | 70%+ |
| Provider integration | ~30% | 80%+ |

---

## Recommended CI/CD Pipeline

**File:** `.github/workflows/test.yml`

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
```

---

## Test Fixtures

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
```

---

## Summary

**Strengths:**
- Comprehensive jq transformation testing (100+ tests)
- Deterministic test fixtures
- Clear pass/fail criteria

**Gaps:**
- No Python test framework
- No integration test automation
- No coverage tracking
- No CI/CD pipeline

**Immediate Actions:**
1. Add pytest framework
2. Create integration test suite
3. Setup CI/CD pipeline
4. Add coverage reporting
