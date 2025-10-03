# SkogAI Configuration System

This directory contains the centralized configuration and path management system for the SkogAI ecosystem.

## Overview

The configuration system provides:
- **Centralized path resolution** - No more hardcoded paths
- **Environment variable support** - Easy customization per deployment
- **Git-aware defaults** - Automatically detects repository root
- **Backward compatibility** - Falls back to legacy paths when needed

## Quick Start

### Python Usage

```python
from config import paths, config

# Get standard directories
agents_dir = paths.agents_dir
context_dir = paths.context_dir
knowledge_dir = paths.knowledge_dir

# Build paths relative to standard directories
agent_file = paths.get_agent_path("implementations/research.py")
context_file = paths.get_context_path("current/session_123.json")
config_file = paths.get_config_file("llm_config.json")

# Get demo output directory with session ID
output_dir = paths.get_demo_output_dir("1234567890", "content_creation")

# Ensure a directory exists
paths.ensure_dir(output_dir)
```

### Shell Script Usage

```bash
#!/bin/bash

# Load path configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../config/paths.sh"

# Get standard directories
base_dir=$(get_base_dir)
agents_dir=$(get_agents_dir)
context_dir=$(get_context_dir)

# Build paths
agent_file=$(get_agent_path "implementations/research.py")
context_file=$(get_context_path "current/session_123.json")

# Ensure directory exists
output_dir=$(get_demo_output_dir "1234567890" "content_creation")
ensure_dir "$output_dir"
```

## Environment Variables

Configure paths using environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `SKOGAI_BASE_DIR` | Base directory for SkogAI | Git repo root or `/home/skogix/skogai` |
| `SKOGAI_AGENTS_DIR` | Agents directory | `$SKOGAI_BASE_DIR/agents` |
| `SKOGAI_CONTEXT_DIR` | Context directory | `$SKOGAI_BASE_DIR/context` |
| `SKOGAI_KNOWLEDGE_DIR` | Knowledge directory | `$SKOGAI_BASE_DIR/knowledge` |
| `SKOGAI_CONFIG_DIR` | Config directory | `$SKOGAI_BASE_DIR/config` |
| `SKOGAI_DEMO_DIR` | Demo output directory | `$SKOGAI_BASE_DIR/demo` |
| `SKOGAI_TOOLS_DIR` | Tools directory | `$SKOGAI_BASE_DIR/tools` |
| `SKOGAI_METRICS_DIR` | Metrics directory | `$SKOGAI_BASE_DIR/metrics` |
| `SKOGAI_VENV_DIR` | Virtual environment | `$SKOGAI_BASE_DIR/.venv` |

### Example Configuration

```bash
# In ~/.bashrc or deployment script
export SKOGAI_BASE_DIR="/opt/skogai"
export SKOGAI_KNOWLEDGE_DIR="/mnt/data/knowledge"
export SKOGAI_CONTEXT_DIR="/var/lib/skogai/context"
```

## Path Resolution Order

The system resolves paths in the following priority order:

1. **Environment variable** - Explicit override
2. **Git repository root** - Auto-detected if in a git repo
3. **Legacy path** - `/home/skogix/skogai` for backward compatibility

## API Reference

### Python API

#### SkogAIPathResolver

```python
from config import paths

# Properties
paths.base_dir        # Base directory (Path)
paths.agents_dir      # Agents directory (Path)
paths.context_dir     # Context directory (Path)
paths.knowledge_dir   # Knowledge directory (Path)
paths.config_dir      # Config directory (Path)
paths.demo_dir        # Demo directory (Path)
paths.tools_dir       # Tools directory (Path)
paths.metrics_dir     # Metrics directory (Path)
paths.venv_dir        # Virtual environment (Path)

# Methods
paths.get_agent_path(relative_path: str) -> Path
paths.get_context_path(relative_path: str) -> Path
paths.get_knowledge_path(relative_path: str) -> Path
paths.get_config_file(filename: str) -> Path
paths.get_demo_output_dir(session_id: Optional[str], prefix: str) -> Path
paths.ensure_dir(path: Path) -> Path
```

#### SkogAIConfig

```python
from config import config

# Load configuration
config.load()  # Load from default location
config.load(Path("/custom/config.json"))  # Load from specific file

# Get values
api_key = config.get("llm.api_key", default="", env_var="SKOGAI_LLM_API_KEY")
model = config.get("llm.model", default="gpt-4")

# Set values
config.set("llm.api_key", "sk-...")
config.save()  # Save to file

# Get all config
all_config = config.all
```

### Shell API

```bash
# Source the library
source "$SCRIPT_DIR/../config/paths.sh"

# Get directories
get_base_dir
get_agents_dir
get_context_dir
get_knowledge_dir
get_config_dir
get_demo_dir
get_tools_dir
get_metrics_dir
get_venv_dir

# Build paths
get_agent_path "relative/path"
get_context_path "relative/path"
get_knowledge_path "relative/path"
get_config_file "filename"
get_demo_output_dir "session_id" "prefix"

# Utilities
ensure_dir "/path/to/directory"
```

## Migration Guide

### Migrating Python Code

**Before:**
```python
config_path = "/home/skogix/skogai/config/llm_config.json"
output_dir = f"/home/skogix/skogai/demo/content_creation_{session_id}"
os.makedirs(output_dir, exist_ok=True)
```

**After:**
```python
from config import paths

config_path = paths.get_config_file("llm_config.json")
output_dir = paths.get_demo_output_dir(session_id, "content_creation")
paths.ensure_dir(output_dir)
```

### Migrating Shell Scripts

**Before:**
```bash
CONTEXT_DIR="/home/skogix/skogai/context"
mkdir -p "$CONTEXT_DIR/current"
```

**After:**
```bash
source "$SCRIPT_DIR/../config/paths.sh"

context_dir=$(get_context_dir)
ensure_dir "$context_dir/current"
```

## Pre-commit Hooks

Pre-commit hooks are configured to prevent new hardcoded paths:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## Testing

Test the configuration system:

```python
# Test Python API
python -c "from config import paths; print(f'Base: {paths.base_dir}')"

# Test with custom environment
SKOGAI_BASE_DIR=/tmp/test python -c "from config import paths; print(f'Base: {paths.base_dir}')"
```

```bash
# Test Shell API
source config/paths.sh
echo "Base: $(get_base_dir)"

# Test with custom environment
SKOGAI_BASE_DIR=/tmp/test bash -c "source config/paths.sh; echo 'Base: $(get_base_dir)'"
```

## Best Practices

1. **Always use the configuration system** - Never hardcode absolute paths
2. **Use environment variables for deployment** - Different paths per environment
3. **Test with different configurations** - Ensure code works in various setups
4. **Document custom paths** - If adding new path types, update this README
5. **Run pre-commit hooks** - Catch hardcoded paths before committing

## Troubleshooting

### "Module not found" errors in Python

Make sure to add the project root to `sys.path`:

```python
import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from config import paths
```

### Paths not resolving correctly

Check environment variables:

```bash
env | grep SKOGAI
```

### Shell scripts can't find paths.sh

Use absolute path from script location:

```bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../config/paths.sh"
```

## Contributing

When adding new path types:

1. Add property to `SkogAIPathResolver` in `paths.py`
2. Add environment variable to documentation
3. Add getter function to `paths.sh`
4. Update this README
5. Write tests

## See Also

- [CLAUDE.md](../CLAUDE.md) - Repository guidelines
- [Issue #5](https://github.com/SkogAI/lore/issues/5) - Original issue tracking this work
