# LORE Configuration System

This directory contains the centralized configuration system for the LORE project, providing a single source of truth for all file system paths.

## Overview

The configuration system:

- **Requires SKOGAI_LORE** environment variable (set by `skogcli config`)
- **Exports lore-specific** directory paths
- **Defers to external systems** for logs (skogai config) and tools (skogcli scripts)
- **Consistent API** across Python and Shell

## Quick Start

### Prerequisites

Ensure `skogcli config` is properly configured with the `skogai` namespace:

```bash
# In .envrc (automatically loaded by direnv)
eval "$(skogcli config export-env --namespace skogai,claude,openai)"
source config/paths.sh
source .venv/bin/activate
```

### Python

```python
from config.paths import get_agents_dir, get_context_dir, get_path

# Get standard directories
agents_dir = get_agents_dir()
context_dir = get_context_dir()

# Get custom paths
config_file = get_path("config", "settings.json")
session_file = get_path("context", "current", "session.json")
```

### Shell/Bash

```bash
# Source the configuration
source "$(dirname "$0")/config/paths.sh"

# Use exported variables
echo "Agents: $SKOGAI_AGENTS_DIR"
echo "Context: $SKOGAI_CONTEXT_DIR"

# Use helper functions
custom_path=$(skogai_get_path "demo" "workflow.py")
skogai_ensure_dir "$SKOGAI_CONTEXT_DIR"
```

## Environment Variables

### Required (from skogcli config)

- **`SKOGAI`**: Base workspace directory (`/home/skogix/skogai`)
- **`SKOGAI_LORE`**: This repository path (e.g., `$SKOGAI/lore`)

### Exported by config/paths.sh

When you source `config/paths.sh`, these lore-specific variables are automatically exported:

- `SKOGAI_BASE_DIR` - Base directory (same as `SKOGAI_LORE`)
- `SKOGAI_AGENTS_DIR` - Agents directory (`$SKOGAI_LORE/agents`)
- `SKOGAI_CONFIG_DIR` - Config directory (`$SKOGAI_LORE/config`)
- `SKOGAI_CONTEXT_DIR` - Context directory (`$SKOGAI_LORE/context`)
- `SKOGAI_DEMO_DIR` - Demo directory (`$SKOGAI_LORE/demo`)
- `SKOGAI_DOCS_DIR` - Docs directory (`$SKOGAI_LORE/docs`)
- `SKOGAI_KNOWLEDGE_DIR` - Knowledge directory (`$SKOGAI_LORE/knowledge`)
- `SKOGAI_LOREFILES_DIR` - Lorefiles directory (`$SKOGAI_LORE/lorefiles`)

### External (not managed by lore)

- **`SKOGAI_LOGS_DIR`**: Managed by `skogai` config namespace (system-level logs)
- **Tools**: Managed by `skogcli` scripts (not env vars)

## Python API Reference

### Path Resolution Functions

#### `get_base_dir() -> Path`

Get the base directory for the LORE repository.

**Requires:**
- `SKOGAI_LORE` environment variable (set by skogcli config)

**Raises:**
- `RuntimeError`: If `SKOGAI_LORE` is not set

```python
from config.paths import get_base_dir

base = get_base_dir()
# Returns: PosixPath('/home/skogix/skogai/lore')
```

---

#### `get_agents_dir() -> Path`

Get the agents directory path.

```python
from config.paths import get_agents_dir

agents = get_agents_dir()
# Returns: PosixPath('/home/skogix/skogai/lore/agents')
```

---

#### `get_config_dir() -> Path`

Get the config directory path.

---

#### `get_context_dir() -> Path`

Get the context directory path.

---

#### `get_demo_dir() -> Path`

Get the demo directory path.

---

#### `get_docs_dir() -> Path`

Get the docs directory path.

---

#### `get_knowledge_dir() -> Path`

Get the knowledge directory path.

---

#### `get_lorefiles_dir() -> Path`

Get the lorefiles directory path.

---

#### `get_path(*parts: str) -> Path`

Get a path relative to the base directory.

**Args:**
- `*parts`: Path components to join

**Returns:**
- Absolute path constructed from `SKOGAI_LORE` + `parts`

```python
from config.paths import get_path

# Simple path
context_file = get_path("context", "session.json")
# Returns: PosixPath('/home/skogix/skogai/lore/context/session.json')

# Nested path
api_file = get_path("agents", "api", "agent_api.py")
# Returns: PosixPath('/home/skogix/skogai/lore/agents/api/agent_api.py')
```

---

#### `ensure_dir(path: Path) -> Path`

Ensure a directory exists, creating it if necessary.

**Args:**
- `path`: Directory path to ensure exists

**Returns:**
- The same path (for chaining)

```python
from config.paths import ensure_dir, get_context_dir

# Ensure context directory exists
context_dir = ensure_dir(get_context_dir())

# Chaining example
session_file = ensure_dir(get_context_dir()) / "session.json"
```

---

## Shell API Reference

### Setup

Source the configuration script at the beginning of your shell script:

```bash
#!/bin/bash

# Get the script's directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source paths configuration (requires SKOGAI_LORE to be set)
source "$SCRIPT_DIR/config/paths.sh"

# Now you can use the configuration
echo "Working in: $SKOGAI_LORE"
```

### Functions

#### `skogai_get_path <part1> [part2] [...]`

Get a path relative to the base directory.

```bash
# Simple path
context_file=$(skogai_get_path "context" "session.json")
echo "$context_file"
# Output: /home/skogix/skogai/lore/context/session.json

# Nested path
api_file=$(skogai_get_path "agents" "api" "agent_api.py")
echo "$api_file"
# Output: /home/skogix/skogai/lore/agents/api/agent_api.py
```

---

#### `skogai_ensure_dir <directory>`

Ensure a directory exists, creating it if necessary.

```bash
skogai_ensure_dir "$SKOGAI_CONTEXT_DIR"
skogai_ensure_dir "/tmp/custom/path"
```

---

#### `skogai_print_config`

Print the current configuration (for debugging).

```bash
skogai_print_config
```

**Output:**
```
LORE Configuration:
  Base Directory (LORE): /home/skogix/skogai/lore
  Agents Directory:      /home/skogix/skogai/lore/agents
  Config Directory:      /home/skogix/skogai/lore/config
  Context Directory:     /home/skogix/skogai/lore/context
  Demo Directory:        /home/skogix/skogai/lore/demo
  Docs Directory:        /home/skogix/skogai/lore/docs
  Knowledge Directory:   /home/skogix/skogai/lore/knowledge
  Lorefiles Directory:   /home/skogix/skogai/lore/lorefiles

External (managed by skogai/skogcli):
  Logs Directory:        ${SKOGAI_LOGS_DIR} (from skogai config)
  Tools:                 via skogcli scripts
```

You can also print config directly:

```bash
source config/paths.sh --print
```

---

## Migration Patterns

### Python Migration

**Before:**
```python
import os

BASE_DIR = "/home/skogix/skogai"
AGENTS_DIR = os.path.join(BASE_DIR, "agents")
context_file = "/home/skogix/skogai/context/session.json"
```

**After:**
```python
from config.paths import get_agents_dir, get_path

AGENTS_DIR = str(get_agents_dir())
context_file = str(get_path("context", "session.json"))
```

### Shell Migration

**Before:**
```bash
BASE_DIR="/home/skogix/skogai"
AGENTS_DIR="$BASE_DIR/agents"
context_file="/home/skogix/skogai/context/session.json"
```

**After:**
```bash
source "$(dirname "$0")/config/paths.sh"

AGENTS_DIR="$SKOGAI_AGENTS_DIR"
context_file=$(skogai_get_path "context" "session.json")
```

---

## Deployment Scenarios

### Development (Local with direnv)

```bash
# .envrc loads everything automatically
cd /home/skogix/skogai/lore
python demo/small_model_workflow.py
```

### CI/CD (GitHub Actions)

```yaml
- name: Setup environment
  run: |
    export SKOGAI_LORE="${GITHUB_WORKSPACE}"
    export SKOGAI_LOGS_DIR="/tmp/logs"
    source config/paths.sh
```

### Docker Container

```dockerfile
ENV SKOGAI_LORE=/app
ENV SKOGAI_LOGS_DIR=/var/log/skogai

WORKDIR /app
COPY . .
RUN source config/paths.sh
CMD ["python", "streamlit_chat.py"]
```

---

## Testing the Configuration

### Test Python API

```bash
# Ensure SKOGAI_LORE is set first
export SKOGAI_LORE="/home/skogix/skogai/lore"

python3 -c "
from config.paths import get_base_dir, get_agents_dir, get_context_dir
print(f'Base: {get_base_dir()}')
print(f'Agents: {get_agents_dir()}')
print(f'Context: {get_context_dir()}')
"
```

### Test Shell API

```bash
# Ensure SKOGAI_LORE is set first
export SKOGAI_LORE="/home/skogix/skogai/lore"

source config/paths.sh --print
```

---

## Troubleshooting

### Issue: "SKOGAI_LORE environment variable not set"

**Cause:** `skogcli config` not loaded or `skogai` namespace not configured.

**Solution:**
```bash
# Ensure skogcli config has skogai namespace configured
skogcli config list --namespace skogai

# Load environment
eval "$(skogcli config export-env --namespace skogai)"

# Or use direnv (recommended)
direnv allow
```

### Issue: Paths point to wrong directory

**Cause:** `SKOGAI_LORE` points to incorrect location.

**Solution:**
```bash
# Check current value
echo "$SKOGAI_LORE"

# Update in skogcli config
skogcli config set lore.path /correct/path/to/lore --namespace skogai

# Or export temporarily
export SKOGAI_LORE=/correct/path/to/lore
```

### Issue: Module not found when importing config.paths

**Cause:** Not running from repository root or Python path issue.

**Solution:**
```bash
# Run from repository root
cd "$SKOGAI_LORE"
python your_script.py

# Or add to PYTHONPATH
export PYTHONPATH="$SKOGAI_LORE:$PYTHONPATH"
```

---

## Files in This Directory

- **`__init__.py`** - Python package initialization
- **`paths.py`** - Python path configuration API
- **`paths.sh`** - Shell path configuration API
- **`README.md`** - This documentation

---

## Architecture

```
skogcli config (skogai namespace)
    ↓
  Sets: SKOGAI, SKOGAI_LORE, SKOGAI_LOGS_DIR
    ↓
config/paths.sh (sources in .envrc)
    ↓
  Exports: SKOGAI_AGENTS_DIR, SKOGAI_CONFIG_DIR, etc.
    ↓
Shell scripts / Python modules use exported vars
```

**Key principle:**
- Base variables (`SKOGAI`, `SKOGAI_LORE`, `SKOGAI_LOGS_DIR`) come from `skogcli config`
- Lore-specific directories come from `config/paths.sh` / `config/paths.py`
- Tools come from `skogcli` scripts (not env vars)

---

## Contributing

When adding new directories to the project:

1. Add getter functions to `paths.py` and export variables in `paths.sh`
2. Update this README with documentation
3. Update `__init__.py` exports if needed
4. Do NOT add to `skogcli config` unless it's a system-level concern

---

## License

Part of the LORE project. See repository LICENSE for details.
