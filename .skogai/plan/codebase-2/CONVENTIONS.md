# Code Conventions

*Generated: 2026-01-05*
*Focus: Lore generation and connections created with context and lore-integrator*

## Shell Script Conventions

### Standard Header Pattern
```bash
#!/bin/bash
set -e                      # Fail-fast execution (exit on error)
set -u                      # Fail on undefined variables (optional)

# Path resolution - consistent across all scripts
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$SCRIPT_DIR"
```

### Variable Naming
- **UPPERCASE:** Constants, environment variables, global configuration
  ```bash
  LORE_DIR="/home/skogix/lore"
  ENTRIES_DIR="$LORE_DIR/knowledge/expanded/lore/entries"
  LLM_PROVIDER="${LLM_PROVIDER:-ollama}"
  ```

- **lowercase:** Function variables, local scope
  ```bash
  function process_entry() {
    local entry_id=$1
    local content=$2
  }
  ```

### Error Handling Pattern

**Pattern 1: File Existence Checks**
```bash
if [ ! -f "$file" ]; then
    echo "ERROR: File not found: $file" >&2
    return 1
fi
```

**Pattern 2: Command Validation**
```bash
if ! command -v ollama &>/dev/null; then
    echo "ERROR: Ollama not found. Please install it first:" >&2
    echo "  curl https://ollama.ai/install.sh | sh" >&2
    exit 1
fi
```

**Pattern 3: jq Error Handling**
```bash
if ! jq "$jq_expression" "$file" > "$temp_file" 2>/dev/null; then
    echo "ERROR: jq transformation failed" >&2
    rm -f "$temp_file"
    return 1
fi
```

**Pattern 4: Error Output to stderr**
```bash
echo "ERROR: message" >&2  # Always redirect errors to stderr
echo "Warning: message" >&2  # Warnings too
# Regular output to stdout (implicit)
```

### Atomic File Operations

**Standard Pattern (manage-lore.sh:80-107):**
```bash
atomic_update() {
  local file="$1"
  local jq_expression="$2"
  local validate_type="$3"  # Optional schema validation

  # 1. Check file exists
  if [ ! -f "$file" ]; then
    echo "ERROR: File not found: $file" >&2
    return 1
  fi

  # 2. Create temp file
  local temp_file="${file}.tmp.$$"

  # 3. Apply jq transformation
  if ! jq "$jq_expression" "$file" > "$temp_file" 2>/dev/null; then
    echo "ERROR: jq transformation failed" >&2
    rm -f "$temp_file"
    return 1
  fi

  # 4. Optional: Validate against schema
  if [ -n "$validate_type" ]; then
    if ! validate_against_schema "$temp_file" "$validate_type"; then
      echo "ERROR: Schema validation failed" >&2
      rm -f "$temp_file"
      return 1
    fi
  fi

  # 5. Move temp file (atomic)
  if ! mv "$temp_file" "$file"; then
    echo "ERROR: Failed to update file" >&2
    rm -f "$temp_file"
    return 1
  fi
}
```

**Why Atomic:**
- Crash during write → Original file unchanged
- Validation failure → Original file unchanged
- Process killed → Original file unchanged

### Function Naming

**Command-style (kebab-case):**
```bash
# Used for user-facing commands
create-entry()
add-to-book()
link-to-persona()
```

**Internal functions (snake_case):**
```bash
# Used for internal helpers
create_entry()
add_to_book()
generate_id()
atomic_update()
```

### JSON Construction Pattern

**NEVER use string concatenation:**
```bash
# ❌ WRONG - Injection risk
content="{\"title\": \"$title\", \"content\": \"$content\"}"
```

**ALWAYS use jq:**
```bash
# ✅ CORRECT - Safe JSON construction
jq -n \
  --arg title "$title" \
  --arg content "$content" \
  '{title: $title, content: $content}'
```

### ID Generation Patterns

**Two Formats Coexist:**

**Format 1: Timestamp only (Python)**
```bash
# Python lore_api.py
entry_id = f"entry_{int(time.time())}"
# Example: entry_1764992601
```

**Format 2: Timestamp + hash (Shell)**
```bash
# Shell manage-lore.sh
entry_id="entry_$(date +%s)_$(openssl rand -hex 4)"
# Example: entry_1764992601_a4b3c2d1
```

**Recommendation:** Use timestamp+hash for collision avoidance

### Provider Switching Pattern

**Standard across LLM integration scripts:**
```bash
case "$PROVIDER" in
  ollama)
    ollama run "$MODEL_NAME" "$prompt"
    ;;
  claude)
    claude -p "$prompt"
    ;;
  openai)
    curl -s "$base_url/chat/completions" \
      -H "Authorization: Bearer $api_key" \
      -H "Content-Type: application/json" \
      -d "{\"model\":\"$MODEL_NAME\",\"messages\":[...]}" | \
      jq -r '.choices[0].message.content'
    ;;
  *)
    echo "ERROR: Unknown provider: $PROVIDER" >&2
    exit 1
    ;;
esac
```

### Temp File Handling

**Current Pattern (needs improvement):**
```bash
# ⚠️  Predictable paths - race condition risk
TEMP_CONTENT="/tmp/lore-content-$SESSION_ID.txt"
```

**Recommended Pattern:**
```bash
# ✅ Use mktemp for unique, secure temp files
TEMP_CONTENT=$(mktemp -t lore-content-XXXXXX.txt)
trap "rm -f $TEMP_CONTENT" EXIT  # Cleanup on exit
```

## Python Conventions

### Import Order
```python
# 1. Standard library
import json
import logging
import os
from pathlib import Path
from typing import Dict, Any, Optional, List

# 2. Third-party
import requests
import click
import yaml

# 3. Local
from agents.api import lore_api
```

### Type Annotations
```python
# Use typing module for all function signatures
def create_lore_entry(
    self,
    title: str,
    content: str,
    category: str,
    tags: Optional[List[str]] = None,
    summary: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """Create a new lore entry.

    Args:
        title: Entry title
        content: Entry content in markdown
        category: Entry category (character, place, event, object, concept, custom)
        tags: Optional list of tags
        summary: Optional brief summary

    Returns:
        Entry dictionary or None on failure
    """
    pass
```

### Error Handling

**Current Pattern (overly broad):**
```python
# ⚠️ Catches all exceptions without distinction
try:
    with open(entry_path, "r") as f:
        return json.load(f)
except Exception as e:
    logger.error(f"Failed to load lore entry {entry_id}: {e}")
    return None  # Silent failure
```

**Recommended Pattern:**
```python
# ✅ Specific exception handling
try:
    with open(entry_path, "r") as f:
        return json.load(f)
except FileNotFoundError:
    logger.warning(f"Lore entry not found: {entry_id}")
    return None
except json.JSONDecodeError as e:
    logger.error(f"Invalid JSON in {entry_id}: {e}")
    raise  # Re-raise for caller to handle
except IOError as e:
    logger.error(f"Failed to read {entry_id}: {e}")
    raise
```

### Logging Pattern
```python
import logging

# Module-level logger
logger = logging.getLogger(__name__)

# Usage
logger.info(f"Created lore entry: {entry_id}")
logger.warning(f"Persona not found, using default")
logger.error(f"Failed to load persona: {e}")
logger.debug(f"Entry content: {content[:100]}")
```

### Path Management
```python
from pathlib import Path

# Prefer Path objects
self.repo_root = Path(__file__).parent.parent
self.entries_dir = self.repo_root / "knowledge" / "expanded" / "lore" / "entries"

# Convert to string only when needed
entry_path = str(self.entries_dir / f"{entry_id}.json")
```

### Docstring Convention
```python
def method_name(self, param: str) -> Optional[Dict[str, Any]]:
    """One-line summary.

    Longer description if needed. Explain the purpose and any important
    behavior or side effects.

    Args:
        param: Description of param

    Returns:
        Description of return value

    Raises:
        ValueError: When param is invalid
        FileNotFoundError: When file doesn't exist
    """
    pass
```

### ID Generation Pattern

**Current (lore_api.py:68-71):**
```python
def generate_id(self, prefix: str = "") -> str:
    """Generate a unique identifier for a new entity."""
    timestamp = int(time.time())
    return f"{prefix}{timestamp}"
```

**Recommendation (add collision avoidance):**
```python
import secrets

def generate_id(self, prefix: str = "") -> str:
    """Generate a unique identifier with collision avoidance."""
    timestamp = int(time.time())
    random_hex = secrets.token_hex(4)  # 8 hex chars
    return f"{prefix}{timestamp}_{random_hex}"
```

## LLM Prompt Engineering Patterns

### Multi-Part Structure
```
## CRITICAL INSTRUCTION
Direct output instructions to prevent meta-commentary

## Task
What the LLM should do

## Format Requirements
Output format specifications

## Quality Checklist (Internal - DO NOT OUTPUT)
Validation criteria for LLM to self-check

## Examples
Correct output examples to guide LLM

## Your Task
Specific instructions with context
```

### Example from llama-lore-creator.sh (lines 116-148):
```bash
PROMPT="You are a master lore writer crafting narrative mythology.

## CRITICAL INSTRUCTION
Write the lore entry content DIRECTLY. No meta-commentary, no explanations, no approval requests.

## Task
Create a $category entry titled \"$title\"

## Format Requirements
- 2-3 paragraphs of rich narrative prose
- Present tense, immersive storytelling
- Mythological/fantastical tone
- NO phrases like: \"I will\", \"Let me\", \"I need\", \"Here is\", \"This entry\"

## Quality Checklist (Internal - DO NOT OUTPUT)
✓ Directly starts with narrative
✓ No meta-commentary
✓ 150-300 words
✓ Establishes atmosphere and significance

## Examples of CORRECT Output
[Examples provided...]

## Your Task
Write the $category entry for \"$title\" NOW. Begin directly with narrative prose:"
```

### Validation Pattern

**Pattern from llama-lore-creator.sh (lines 43-67):**
```bash
validate_lore_output() {
  local content="$1"
  local errors=()

  # Check for meta-commentary patterns at start
  if echo "$content" | head -n 1 | grep -qiE '^[[:space:]]*(I will|Let me|Here is)'; then
    errors+=("⚠️  Contains meta-commentary in first line")
  fi

  # Check minimum length
  word_count=$(echo "$content" | wc -w)
  if [ "$word_count" -lt 100 ]; then
    errors+=("⚠️  Too short ($word_count words, recommended 100+)")
  fi

  # Report
  if [ ${#errors[@]} -gt 0 ]; then
    printf '%s\n' "${errors[@]}" >&2
    return 1
  fi

  echo "✅ Lore content validated" >&2
  return 0
}
```

### Stripping Pattern

**Pattern from llama-lore-creator.sh (lines 69-79):**
```bash
strip_meta_commentary() {
  local content="$1"

  # Remove first line if it's meta-commentary
  if echo "$content" | head -n 1 | grep -qiE '^[[:space:]]*(I will|Let me|Here is)'; then
    echo "$content" | tail -n +2  # Skip first line
  else
    echo "$content"  # Return unchanged
  fi
}
```

## JSON Schema Validation

### Schema Location Convention
```
knowledge/core/
├── lore/
│   └── schema.json           # Entry schema
├── book-schema.json          # Book schema
└── persona/
    └── schema.json           # Persona schema
```

### Validation via jq

**Pattern:**
```bash
validate_against_schema() {
  local file=$1
  local schema_type=$2  # "entry", "book", or "persona"

  local schema_file="knowledge/core/${schema_type}/schema.json"

  # Use jq to validate
  jq -f scripts/jq/schema-validation/transform.jq \
    --argfile schema "$schema_file" \
    "$file"
}
```

### Required Fields by Type

**Entry:**
```json
{
  "required": ["id", "title", "content", "category"],
  "category": "enum[character|place|event|object|concept|custom]"
}
```

**Book:**
```json
{
  "required": ["id", "title", "description"],
  "status": "enum[draft|active|archived|deprecated]"
}
```

**Persona:**
```json
{
  "required": ["id", "name", "core_traits", "voice"],
  "interaction_style.formality": "enum[very_formal|formal|neutral|casual|very_casual]",
  "interaction_style.humor": "enum[none|subtle|occasional|frequent|constant]",
  "interaction_style.directness": "enum[very_direct|direct|balanced|indirect|very_indirect]"
}
```

## Context Management Patterns

### Session ID Generation
```bash
# Simple timestamp
session_id=$(date +%s)

# Used consistently:
TEMP_FILE="/tmp/content-$session_id.txt"
ENTRY_ID="entry_$session_id"
CONTEXT_FILE="context/current/context-$session_id.json"
```

### Context Update Pattern

**Via context-manager.sh:**
```bash
# Update single field
context-manager.sh update "$session_id" "system_state.orchestrator_mode" "lore"

# Internally uses jq
jq ".system_state.orchestrator_mode = \"lore\"" "$context_file" > tmp.json
mv tmp.json "$context_file"
```

## Relationship Patterns

### Bidirectional Linking

**Entry ↔ Book:**
```bash
add_to_book() {
  local entry_id=$1
  local book_id=$2

  # 1. Add entry_id to book.entries array
  jq ".entries += [\"$entry_id\"]" "$book_file" > tmp.json
  mv tmp.json "$book_file"

  # 2. Set entry.book_id
  jq ".book_id = \"$book_id\"" "$entry_file" > tmp.json
  mv tmp.json "$entry_file"

  # 3. Update timestamps
  timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  jq ".metadata.updated_at = \"$timestamp\"" "$book_file" > tmp.json
  mv tmp.json "$book_file"
}
```

**Book ↔ Persona:**
```bash
link_to_persona() {
  local book_id=$1
  local persona_id=$2

  # 1. Add persona to book.readers
  jq ".readers += [\"$persona_id\"]" "$book_file" > tmp.json
  mv tmp.json "$book_file"

  # 2. Add book to persona.knowledge.lore_books
  jq ".knowledge.lore_books += [\"$book_id\"]" "$persona_file" > tmp.json
  mv tmp.json "$persona_file"
}
```

### Relationship Analysis Pattern

**Via llama-lore-integrator.sh analyze-connections:**
```bash
# 1. Get all entries in book
entries=$(jq -r '.entries[]' "$book_file")

# 2. Build catalog (title, summary, category for each)
catalog=""
for entry_id in $entries; do
  title=$(jq -r '.title' "entries/${entry_id}.json")
  summary=$(jq -r '.summary' "entries/${entry_id}.json")
  catalog+="$entry_id: $title - $summary\n"
done

# 3. Prompt LLM
prompt="Analyze these entries and identify connections:
$catalog

Format: ## CONNECTION / SOURCE / TARGET / RELATIONSHIP / DESCRIPTION"

connections=$(run_llm "$prompt")

# 4. Parse and apply
for line in $connections; do
  source=$(echo "$line" | cut -d'/' -f2)
  target=$(echo "$line" | cut -d'/' -f3)
  relationship=$(echo "$line" | cut -d'/' -f4)
  description=$(echo "$line" | cut -d'/' -f5)

  # Add relationship to source entry
  jq ".relationships += [{
    \"target_id\": \"$target\",
    \"relationship_type\": \"$relationship\",
    \"description\": \"$description\"
  }]" "entries/${source}.json" > tmp.json
  mv tmp.json "entries/${source}.json"
done
```

## Testing Patterns

### Shell Script Testing (jq transformations)

**Pattern from scripts/jq/schema-validation/test.sh:**
```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing schema-validation transformation..."

# Test with deterministic fixtures
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

**Key Principles:**
- Deterministic input (no randomness)
- Exact expected output
- Fail immediately with detailed error
- Test fixtures in git (test-input-*.json)
- Focus on edge cases (falsy values, boundaries)

### Python Testing (manual, needs improvement)

**Current Pattern (lore_api.py:525-558):**
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

**Recommended Pattern:**
```python
import pytest
from agents.api.lore_api import LoreAPI

@pytest.fixture
def api():
    return LoreAPI()

def test_create_persona(api):
    persona = api.create_persona(
        name="Test Guardian",
        core_description="Test description",
        personality_traits=["wise", "kind"],
        voice_tone="serene"
    )

    assert persona is not None
    assert persona["name"] == "Test Guardian"
    assert "persona_" in persona["id"]
    assert len(persona["core_traits"]["values"]) == 2
```

## Documentation Patterns

### Function Documentation

**Shell:**
```bash
# create_lore_entry - Create a new lore entry
#
# Arguments:
#   $1 - title (required)
#   $2 - category (required): character, place, event, object, concept, custom
#   $3 - content (optional)
#
# Returns:
#   Entry ID on success, exits with 1 on failure
#
# Example:
#   entry_id=$(create_lore_entry "The Dark Tower" "place")
```

**Python:**
```python
def create_lore_entry(
    self,
    title: str,
    content: str,
    category: str,
    tags: Optional[List[str]] = None
) -> Optional[Dict[str, Any]]:
    """Create a new lore entry.

    Args:
        title: Entry title
        content: Entry content in markdown format
        category: Entry category (character, place, event, object, concept, custom)
        tags: Optional list of searchable tags

    Returns:
        Entry dictionary with generated ID and metadata, or None on failure

    Example:
        >>> api = LoreAPI()
        >>> entry = api.create_lore_entry("The Dark Tower", "A mysterious fortress...", "place")
        >>> print(entry['id'])
        entry_1764992601
    """
    pass
```

## Security Patterns

### Avoid Predictable Temp Files
```bash
# ❌ BAD - Predictable path
TEMP_FILE="/tmp/lore-$SESSION_ID.txt"

# ✅ GOOD - Unique, secure temp file
TEMP_FILE=$(mktemp -t lore-XXXXXX.txt)
trap "rm -f $TEMP_FILE" EXIT  # Cleanup on exit
```

### API Key Handling
```bash
# ✅ Use environment variables
api_key="${OPENROUTER_API_KEY}"

# ✅ Pass in headers, not in URL
curl -H "Authorization: Bearer $api_key" ...

# ❌ Avoid exposing in process list
# curl "https://api.com?key=$api_key" ...  # Visible in ps
```

### Input Sanitization
```bash
# ❌ Direct interpolation - injection risk
title="$1"
jq ".title = \"$title\"" entry.json

# ✅ Use jq arguments - safe
title="$1"
jq --arg title "$title" '.title = $title' entry.json
```

## Summary of Key Conventions

| Aspect | Convention | Example |
|--------|-----------|---------|
| **Shell variables** | UPPERCASE for constants, lowercase for locals | `REPO_ROOT`, `local file=$1` |
| **Python imports** | stdlib → third-party → local | See Python section |
| **Error output** | Always to stderr | `echo "ERROR" >&2` |
| **File operations** | Atomic (temp + move) | `mv tmp.json file.json` |
| **JSON construction** | Always use jq | `jq --arg x "$x" '{x: $x}'` |
| **ID generation** | Timestamp or timestamp+hash | `entry_1764992601_a4b3c2d1` |
| **LLM prompts** | Multi-part with examples | See LLM section |
| **Validation** | jq-based schema validation | See Schema section |
| **Testing** | Deterministic fixtures | test-input-*.json |
| **Temp files** | Use mktemp | `$(mktemp -t lore-XXXXXX)` |
| **Logging** | Module-level logger | `logger.error(...)` |

These conventions ensure consistency, safety, and maintainability across the lore generation system.
