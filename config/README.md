# LORE Configuration System

This directory contains the centralized configuration system for the LORE project, providing a single source of truth for all file system paths.

## Overview

The configuration system supports:

- **Environment variable overrides** for flexible deployment
- **Git-aware path resolution** (auto-detects repository root)
- **Backward compatibility** (defaults to `/home/skogix/skogai`)
- **Multiple deployment scenarios** (development, production, testing)
- **Consistent API** across Python and Shell

## Quick Start

### Python

```python
from config.paths import get_agents_dir, get_log_file, get_path

# Get standard directories
agents_dir = get_agents_dir()
logs_dir = get_logs_dir()

# Get custom paths
config_file = get_path("config", "settings.json")
log_file = get_log_file("agent.log")  # Auto-creates logs dir
```

### Shell/Bash

```bash
# Source the configuration
source "$(dirname "$0")/config/paths.sh"

# Use exported variables
echo "Agents: $SKOGAI_AGENTS_DIR"
echo "Logs: $SKOGAI_LOGS_DIR"

# Use helper functions
log_file=$(skogai_get_log_file "agent.log")
custom_path=$(skogai_get_path "demo" "workflow.py")
```

## Environment Variables

### Primary Configuration

- **`SKOGAI_BASE_DIR`**: Override the base directory for the entire project
  - Default: Git repository root, or `/home/skogix/skogai`
  - Example: `export SKOGAI_BASE_DIR=/opt/lore`

- **`SKOGAI_LOGS_DIR`**: Override the logs directory location
  - Default: `$SKOGAI_BASE_DIR/logs`
  - Example: `export SKOGAI_LOGS_DIR=/var/log/lore`

### Exported Variables (Shell)

When you source `paths.sh`, these variables are automatically exported:

- `SKOGAI_BASE_DIR` - Base directory
- `SKOGAI_AGENTS_DIR` - Agents directory
- `SKOGAI_CONFIG_DIR` - Config directory
- `SKOGAI_DEMO_DIR` - Demo directory
- `SKOGAI_DOCS_DIR` - Docs directory
- `SKOGAI_LOGS_DIR` - Logs directory
- `SKOGAI_LOREFILES_DIR` - Lorefiles directory
- `SKOGAI_TOOLS_DIR` - Tools directory

## Python API Reference

### Path Resolution Functions

#### `get_repo_root() -> Path`

Get the repository root directory using git.

```python
from config.paths import get_repo_root

repo_root = get_repo_root()
# Returns: PosixPath('/path/to/lore')
```

**Raises:**
- `RuntimeError`: If not in a git repository or git is not installed

---

#### `get_base_dir() -> Path`

Get the base directory for the LORE project.

**Resolution order:**
1. `SKOGAI_BASE_DIR` environment variable
2. Git repository root (if available)
3. Default: `/home/skogix/skogai`

```python
from config.paths import get_base_dir

base = get_base_dir()
# Returns: PosixPath('/home/skogix/skogai')
```

---

#### `get_agents_dir() -> Path`

Get the agents directory path.

```python
from config.paths import get_agents_dir

agents = get_agents_dir()
# Returns: PosixPath('/home/skogix/skogai/agents')
```

---

#### `get_config_dir() -> Path`

Get the config directory path.

---

#### `get_demo_dir() -> Path`

Get the demo directory path.

---

#### `get_docs_dir() -> Path`

Get the docs directory path.

---

#### `get_logs_dir() -> Path`

Get the logs directory path. Can be overridden with `SKOGAI_LOGS_DIR`.

```python
from config.paths import get_logs_dir

logs = get_logs_dir()
# Returns: PosixPath('/home/skogix/skogai/logs')

# With override:
import os
os.environ['SKOGAI_LOGS_DIR'] = '/var/log/lore'
logs = get_logs_dir()
# Returns: PosixPath('/var/log/lore')
```

---

#### `get_lorefiles_dir() -> Path`

Get the lorefiles directory path.

---

#### `get_tools_dir() -> Path`

Get the tools directory path.

---

#### `get_path(*parts: str) -> Path`

Get a path relative to the base directory.

**Args:**
- `*parts`: Path components to join

**Returns:**
- Absolute path constructed from `base_dir` + `parts`

```python
from config.paths import get_path

# Simple path
log_file = get_path("logs", "agent.log")
# Returns: PosixPath('/home/skogix/skogai/logs/agent.log')

# Nested path
api_file = get_path("agents", "api", "agent_api.py")
# Returns: PosixPath('/home/skogix/skogai/agents/api/agent_api.py')
```

---

#### `ensure_dir(path: Path) -> Path`

Ensure a directory exists, creating it if necessary.

**Args:**
- `path`: Directory path to ensure exists

**Returns:**
- The same path (for chaining)

```python
from config.paths import ensure_dir, get_logs_dir

# Ensure logs directory exists
logs_dir = ensure_dir(get_logs_dir())

# Chaining example
log_file = ensure_dir(get_logs_dir()) / "agent.log"
```

---

#### `get_log_file(filename: str) -> Path`

Get a log file path, ensuring the logs directory exists.

**Args:**
- `filename`: Name of the log file

**Returns:**
- Full path to the log file

```python
from config.paths import get_log_file

log_file = get_log_file("agent.log")
# Returns: PosixPath('/home/skogix/skogai/logs/agent.log')
# Also creates /home/skogix/skogai/logs/ if it doesn't exist
```

---

## Shell API Reference

### Setup

Source the configuration script at the beginning of your shell script:

```bash
#!/bin/bash

# Get the script's directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source paths configuration
source "$SCRIPT_DIR/config/paths.sh"

# Now you can use the configuration
echo "Working in: $SKOGAI_BASE_DIR"
```

### Functions

#### `skogai_get_repo_root`

Get the repository root directory using git.

```bash
repo_root=$(skogai_get_repo_root)
echo "Repo root: $repo_root"
```

---

#### `skogai_get_base_dir`

Get the base directory for the LORE project.

**Resolution order:**
1. `SKOGAI_BASE_DIR` environment variable
2. Git repository root (if available)
3. Default: `/home/skogix/skogai`

```bash
base_dir=$(skogai_get_base_dir)
echo "Base: $base_dir"
```

---

#### `skogai_get_path <part1> [part2] [...]`

Get a path relative to the base directory.

```bash
# Simple path
log_file=$(skogai_get_path "logs" "agent.log")
echo "$log_file"
# Output: /home/skogix/skogai/logs/agent.log

# Nested path
api_file=$(skogai_get_path "agents" "api" "agent_api.py")
echo "$api_file"
# Output: /home/skogix/skogai/agents/api/agent_api.py
```

---

#### `skogai_ensure_dir <directory>`

Ensure a directory exists, creating it if necessary.

```bash
skogai_ensure_dir "$SKOGAI_LOGS_DIR"
skogai_ensure_dir "/tmp/custom/path"
```

---

#### `skogai_get_log_file <filename>`

Get a log file path, ensuring the logs directory exists.

```bash
log_file=$(skogai_get_log_file "agent.log")
echo "Logging to: $log_file"
# Output: Logging to: /home/skogix/skogai/logs/agent.log
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
  Base Directory:      /home/skogix/skogai
  Agents Directory:    /home/skogix/skogai/agents
  Config Directory:    /home/skogix/skogai/config
  Demo Directory:      /home/skogix/skogai/demo
  Docs Directory:      /home/skogix/skogai/docs
  Logs Directory:      /home/skogix/skogai/logs
  Lorefiles Directory: /home/skogix/skogai/lorefiles
  Tools Directory:     /home/skogix/skogai/tools
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
log_file = "/home/skogix/skogai/logs/agent.log"
```

**After:**
```python
from config.paths import get_agents_dir, get_log_file

AGENTS_DIR = str(get_agents_dir())
log_file = str(get_log_file("agent.log"))
```

### Shell Migration

**Before:**
```bash
BASE_DIR="/home/skogix/skogai"
AGENTS_DIR="$BASE_DIR/agents"
log_file="/home/skogix/skogai/logs/agent.log"
```

**After:**
```bash
source "$(dirname "$0")/config/paths.sh"

AGENTS_DIR="$SKOGAI_AGENTS_DIR"
log_file=$(skogai_get_log_file "agent.log")
```

---

## Deployment Scenarios

### Development (Git Repository)

```bash
# No configuration needed - auto-detects git repo root
cd /home/dev/lore
python demo/small_model_workflow.py
```

### Production (Custom Location)

```bash
# Set base directory via environment variable
export SKOGAI_BASE_DIR=/opt/lore
export SKOGAI_LOGS_DIR=/var/log/lore

systemctl start lore-service
```

### Testing (Temporary Directory)

```bash
# Use custom directory for testing
export SKOGAI_BASE_DIR=/tmp/lore-test
python -m pytest tests/
```

### Docker Container

```dockerfile
ENV SKOGAI_BASE_DIR=/app
ENV SKOGAI_LOGS_DIR=/var/log/lore

WORKDIR /app
COPY . .
CMD ["python", "streamlit_chat.py"]
```

---

## Testing the Configuration

### Test Python API

```bash
python3 -c "
from config.paths import get_base_dir, get_agents_dir, get_log_file
print(f'Base: {get_base_dir()}')
print(f'Agents: {get_agents_dir()}')
print(f'Log: {get_log_file(\"test.log\")}')
"
```

### Test Shell API

```bash
source config/paths.sh --print
```

### Test with Custom Base Directory

```bash
# Python
SKOGAI_BASE_DIR=/tmp/test python3 -c "from config.paths import get_base_dir; print(get_base_dir())"

# Shell
SKOGAI_BASE_DIR=/tmp/test source config/paths.sh --print
```

---

## Validation Tools

See `config/validate.py` and `config/validate.sh` for validation scripts that:

- Check for hardcoded paths in Python and Shell files
- Verify all files use the configuration system
- Report files that need migration

```bash
# Validate Python files
python config/validate.py

# Validate Shell files
./config/validate.sh
```

---

## Pre-commit Hook

Install the pre-commit hook to prevent hardcoded paths:

```bash
# Copy hook to .git/hooks/
cp config/pre-commit-hook.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

The hook will:
- Check staged files for hardcoded `/home/skogix/skogai` paths
- Block commits that introduce hardcoded paths
- Suggest using the configuration API

---

## Troubleshooting

### Issue: "Failed to determine git repository root"

**Cause:** Not in a git repository or git is not installed.

**Solution:**
- Set `SKOGAI_BASE_DIR` environment variable
- Or ensure you're in a git repository
- Or install git

### Issue: Paths point to wrong directory

**Cause:** Environment variable override or not in expected location.

**Solution:**
```bash
# Check current configuration
source config/paths.sh --print

# Or in Python
python3 -c "from config.paths import get_base_dir; print(get_base_dir())"

# Override if needed
export SKOGAI_BASE_DIR=/correct/path
```

### Issue: Module not found when importing config.paths

**Cause:** Not running from repository root or Python path issue.

**Solution:**
```bash
# Run from repository root
cd /path/to/lore
python your_script.py

# Or add to PYTHONPATH
export PYTHONPATH=/path/to/lore:$PYTHONPATH
```

---

## Files in This Directory

- **`__init__.py`** - Python package initialization
- **`paths.py`** - Python path configuration API
- **`paths.sh`** - Shell path configuration API
- **`README.md`** - This documentation
- **`validate.py`** - Python validation script (to be created)
- **`validate.sh`** - Shell validation script (to be created)
- **`pre-commit-hook.sh`** - Git pre-commit hook (to be created)

---

## Contributing

When adding new directories or paths to the project:

1. Add getter functions to `paths.py` and `paths.sh`
2. Export new variables in `paths.sh`
3. Update this README with documentation
4. Update `__init__.py` exports if needed

---

## License

Part of the LORE project. See repository LICENSE for details.
