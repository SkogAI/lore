# Code Conventions

## Naming Conventions

### Python Functions & Variables
- **Functions:** snake_case
  - `create_lore_entry()`, `load_schemas()`, `generate_id()`, `add_entry_to_book()`
- **Variables:** snake_case
  - `lore_entries_dir`, `book_id`, `persona_id`, `base_dir`
- **Classes:** PascalCase
  - `LoreAPI`, `AgentAPI`, `PersonaManager`
- **Private/Internal:** Underscore prefix
  - `_call_llm_api()`, `_parse_and_validate_response()`

### Shell Script Functions
- **CLI Commands:** kebab-case (with hyphens)
  - `create-entry`, `list-books`, `show-entry`, `validate-entry`
- **Internal Helpers:** Underscore prefix
  - `_essence_forms()`, `_time_epoch()`, `_get_category()`
- **Constants/Environment Variables:** ALL_CAPS
  - `SKOGAI_DIR`, `LORE_DIR`, `BOOKS_DIR`, `ENTRIES_DIR`, `PERSONA_DIR`

### JSON File Naming
- **Entry files:** `entry_<unix_timestamp>.json`
  - Example: `entry_1743758088.json`
  - Batch entries: `entry_<timestamp>_<hex_hash>.json`
- **Book files:** `book_<unix_timestamp>.json` or `book_<timestamp>_<hex_hash>.json`
  - Example: `book_1743774022_e2298400.json`
- **Persona files:** `persona_<unix_timestamp>.json` or `<name>.json`
  - Example: `persona_1743758088.json`, `amy.json`

### Argc CLI Commands (Argcfile.sh)
- **Command names:** kebab-case (hyphens)
  - `list-books`, `show-book`, `validate-entry`, `read-book-entries`
- **Visual identification:** Emojis for categories
  - `📚 Chronicles of the Digital Realm`
- **Aliases:** snake_case when provided

## Code Style Standards

### Python Style

**Import Ordering:**
```python
import os           # stdlib
import sys          # stdlib
import json         # stdlib
import logging      # stdlib
from typing import Dict, Any, List, Optional  # stdlib

import requests     # third-party
from pathlib import Path

# Add project root to path
sys.path.insert(0, ...)

from agents.api.lore_api import LoreAPI  # local
```

**Type Annotations:**
- Use `Dict[str, Any]`, `List[str]`, `Optional[Dict[str, Any]]`
- Import from `typing` module
- Type hints on function signatures

**Docstrings:**
- Triple-quoted strings for all classes and functions
- Module docstrings at top of file with purpose and usage
- Include Args/Returns for complex methods

**Error Handling:**
- Try/except with specific exception types
- Informative logging on errors
- Use `logger = logging.getLogger("module_name")`

**Line Length:**
- No explicit limit enforced
- Keep lines reasonable (<100 chars preferred)

**Logging:**
```python
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("module_name")

logger.info("Info message")
logger.error("Error message")
```

### Shell Script Style

**Shebang:**
```bash
#!/bin/bash
# or
#!/usr/bin/env bash
```

**Set Options:**
```bash
set -e                 # Exit on error
set -euo pipefail      # Strict mode (preferred)
```

**Function Definitions:**
- Functions defined before usage
- Clear function names describing action

**Comments:**
```bash
# Single-line comments with clear descriptions
# Multi-line comments for complex logic
```

**Variable Usage:**
- Double-quoted for safety: `"${VAR}"`
- Explicit array syntax for iteration

**Path Handling:**
```bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
```

### Documentation in Code

**Python Module Documentation:**
```python
#!/usr/bin/env python3
"""Module purpose and description.

Detailed explanation of what it does.
Usage examples if applicable.
"""

import ...

logging.basicConfig(...)
logger = logging.getLogger("module_name")

class ClassName:
    """Class purpose.

    Attributes:
        attr_name: Description
    """

    def method(self, arg: str) -> Dict[str, Any]:
        """Method purpose.

        Args:
            arg: Description

        Returns:
            Description of return value

        Raises:
            ExceptionType: When this happens
        """
```

**Shell Script Documentation:**
```bash
#!/bin/bash
# Script purpose
#
# Description of what it does
# Features/capabilities listed
#
# Usage: ./script.sh [options]

set -e

# Path setup
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Function documentation as comments
# validate_something() - Validates input
# Args: $1 - input to validate
# Returns: 0 on success, 1 on failure
validate_something() {
    # Implementation
}
```

**Argc Command Documentation:**
```bash
# @cmd Purpose of command with emoji
# @arg arg_name![`_choice_function`] Description of argument
# @option --flag Description of flag option
# @alias alternative_name
command_name() {
    # Implementation
}

# Choice function for argument validation
_choice_function() {
    # Return available choices
}
```

**README/Documentation (Markdown):**
- Hierarchical headers (#, ##, ###)
- Code blocks with language specification
- Links to related documentation (`@docs/api/entry.md`)
- Examples with context
- Last updated timestamps

## File Naming Patterns

### Knowledge/Data Structure
- **Schemas:** `knowledge/core/<domain>/schema.json`
  - `knowledge/core/lore/schema.json`
  - `knowledge/core/persona/schema.json`
- **Expanded data:** `knowledge/expanded/<type>/<domain>/file_<timestamp>.json`
- **Numbered knowledge:** `XXNN.md` (00-09 core, 10-19 navigation, etc.)

### Scripts
- **Tools:** `tools/<function>.sh`
  - `manage-lore.sh`, `context-manager.sh`
- **Pre-commit hooks:** `scripts/pre-commit/<validator>.sh` or `.py`
- **Integration:** `integration/<workflow>.sh`
- **Validation:** `validate.sh`, `validate.py`

### Tests
- **Test directory:** `tests/` (flat structure with subdirs)
- **Test definitions:** `definition.json` format

### Configuration
- **Project config:** `pyproject.toml`
- **Pre-commit:** `.pre-commit-config.yaml`
- **Environment:** `.envrc` (direnv)
- **Git ignore:** `.gitignore`

## Directory Structure Patterns

### Standard Layout
```
<module>/
├── __init__.py          # Module initialization
├── core.py              # Core functionality
├── api.py               # Public API
├── utils.py             # Utility functions
└── tests/               # Module tests
```

### Tool Layout
```
tools/
├── <tool-name>.sh       # Shell implementation
├── <tool-name>.py       # Python implementation (optional)
└── <tool-name>-tests/   # Tool-specific tests
```

### Integration Layout
```
integration/
├── <workflow>.sh        # Main workflow script
├── <component>/         # Sub-components
│   └── manager.py
├── <config>.conf        # Configuration files
└── services/            # Service daemon scripts
```

## Code Quality Standards

### Python Code Quality
- **Type annotations:** Required on public APIs
- **Docstrings:** Required on all classes and public methods
- **Error handling:** Try/except with specific exceptions
- **Logging:** Use configured logger, not print()
- **Path handling:** Use `pathlib.Path` for cross-platform compatibility
- **Configuration:** Load from config files with environment variable fallbacks

### Shell Code Quality
- **Strict mode:** Use `set -euo pipefail` at script start
- **Quoting:** Always quote variables: `"${VAR}"`
- **Error handling:** Check exit codes, use `|| exit 1` when needed
- **Portability:** Use `#!/bin/bash` (not `/bin/sh`)
- **Functions:** Declare functions before usage
- **Comments:** Document non-obvious logic

### JSON Schema Standards
- **Required fields:** Always specify in schema
- **Enums:** Use for fixed value sets
- **Descriptions:** Provide for all fields
- **Examples:** Include in schema when helpful
- **Validation:** Use JSON Schema draft-07 format

## Version Control Standards

### Git Commit Messages
- First line: Short summary (<50 chars)
- Blank line separator
- Detailed description if needed
- Reference issues: `Fixes #123`
- Auto-generated commits include:
  ```
  🤖 Generated with [Claude Code](https://claude.com/claude-code)

  Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
  ```

### Branch Strategy
- **Default branch:** `master` (not `main`)
- **Feature branches:** Descriptive names
- **Remote:** https://github.com/SkogAI/lore

### Pre-commit Hooks
- **Validation:** Check for hardcoded paths
- **Standard hooks:** Check YAML, JSON, merge conflicts
- **Line endings:** Mixed line ending check (LF)
- **Whitespace:** Trailing whitespace removal
- **End of file:** Ensure newline at EOF

## Documentation Standards

### Code Documentation
- **Module docstrings:** Every Python module
- **Function docstrings:** All public functions
- **Inline comments:** For non-obvious logic
- **TODO comments:** Format: `# TODO: Description`
- **FIXME comments:** Format: `# FIXME: Issue description`

### API Documentation
- **Location:** `docs/api/`
- **Format:** Markdown
- **Structure:**
  - Schema reference
  - Example structure
  - CRUD operations
  - Common patterns
  - Integration examples

### Project Documentation
- **CLAUDE.md:** Canonical project documentation
- **CURRENT_UNDERSTANDING.md:** System state and learnings
- **ARCHITECTURE.md:** Technical architecture
- **Last updated:** Timestamp at top of file

## Best Practices

### Path Handling
```python
# Python - Use pathlib
from pathlib import Path
repo_root = Path(__file__).parent.parent
books_dir = repo_root / "knowledge" / "expanded" / "lore" / "books"
```

```bash
# Bash - Use relative paths
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
books_dir="$REPO_ROOT/knowledge/expanded/lore/books"
```

### Environment Variables
```bash
# Required for LLM operations
export OPENROUTER_API_KEY="sk-or-v1-..."

# Optional provider configuration
export LLM_PROVIDER="ollama"  # ollama|claude|openai
export LLM_MODEL="llama3.2:3b"

# Directory mappings (via direnv/.envrc)
export SKOGAI_DIR="/path/to/lore"
export LORE_DIR="$SKOGAI_DIR/knowledge/expanded/lore"
```

### Error Messages
- **Python:** Use `logger.error()` with context
- **Shell:** Echo to stderr: `echo "ERROR: message" >&2`
- **Exit codes:** 0=success, 1=error, 2=usage error

### Validation
- **Python:** Use JSON Schema validation
- **Shell:** Use `jq` for JSON validation
- **Pre-commit:** Validate paths, syntax, formats

## Anti-Patterns to Avoid

### Hardcoded Paths
```python
# BAD - Hardcoded absolute path
entries_dir = "/home/skogix/lore/knowledge/expanded/lore/entries"

# GOOD - Relative path from project root
from pathlib import Path
repo_root = Path(__file__).parent.parent
entries_dir = repo_root / "knowledge" / "expanded" / "lore" / "entries"
```

### Unquoted Variables in Shell
```bash
# BAD - Breaks with spaces
mv $file $destination

# GOOD - Always quote
mv "${file}" "${destination}"
```

### Missing Error Handling
```python
# BAD - No error handling
with open(file_path, 'r') as f:
    data = json.load(f)

# GOOD - Handle errors
try:
    with open(file_path, 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    logger.error(f"File not found: {file_path}")
    return None
except json.JSONDecodeError:
    logger.error(f"Invalid JSON in {file_path}")
    return None
```

### Silent Failures
```bash
# BAD - Suppresses all errors
command || echo ""

# GOOD - Check and handle errors
if ! command; then
    echo "ERROR: Command failed" >&2
    exit 1
fi
```
