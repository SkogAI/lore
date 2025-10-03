# Configuration System Summary

## What This Configuration System Does

The lore repository uses a centralized configuration system for path management based on a **single primary environment variable**: `SKOGAI_LORE`.

## Key Architecture

```
skogcli config (skogai namespace)
    ↓
  Sets: SKOGAI, SKOGAI_LORE, SKOGAI_LOGS_DIR
    ↓
.envrc (loads config via direnv)
    ↓
config/paths.sh (sources automatically)
    ↓
  Exports: SKOGAI_*_DIR variables
    ↓
Scripts and applications use the exported variables
```

## Environment Variable Ownership

### Managed by `skogcli config` (skogai namespace)

These are set externally and should NEVER be managed by this repository:

- **`SKOGAI`** - Base workspace directory for all SkogAI projects
- **`SKOGAI_LORE`** - Path to this repository (the PRIMARY variable)
- **`SKOGAI_LOGS_DIR`** - System-wide logs directory

### Managed by `config/paths.sh` (this repository)

These are automatically derived from `SKOGAI_LORE` when sourcing `config/paths.sh`:

- **`SKOGAI_BASE_DIR`** - Alias for `SKOGAI_LORE`
- **`SKOGAI_AGENTS_DIR`** - `$SKOGAI_LORE/agents`
- **`SKOGAI_CONFIG_DIR`** - `$SKOGAI_LORE/config`
- **`SKOGAI_CONTEXT_DIR`** - `$SKOGAI_LORE/context`
- **`SKOGAI_DEMO_DIR`** - `$SKOGAI_LORE/demo`
- **`SKOGAI_DOCS_DIR`** - `$SKOGAI_LORE/docs`
- **`SKOGAI_KNOWLEDGE_DIR`** - `$SKOGAI_LORE/knowledge`
- **`SKOGAI_LOREFILES_DIR`** - `$SKOGAI_LORE/lorefiles`

### Not Environment Variables

These are provided as commands by `skogcli`:

- **Tools** - Use `skogcli tool-name` commands directly, not env vars

## Usage

### For Shell Scripts

```bash
#!/bin/bash

# Source the configuration
source "$(dirname "$0")/config/paths.sh"

# Now use the exported variables
echo "Agents: $SKOGAI_AGENTS_DIR"
config_file=$(skogai_get_path "config" "settings.json")
```

### For Python Scripts

```python
from config.paths import get_agents_dir, get_path

# Use the path functions
agents_dir = get_agents_dir()
config_file = get_path("config", "settings.json")
```

## Testing

Both Python and Shell configurations have test suites:

```bash
# Set the required environment variable
export SKOGAI_LORE=$(pwd)

# Run Python tests
python config/test_config.py

# Run Shell tests
bash config/test_config.sh
```

## What Was Fixed

1. **Removed deprecated functions** that referenced removed features (get_logs_dir, get_tools_dir, get_log_file)
2. **Fixed imports** in `config/__init__.py` to only export existing functions
3. **Updated tests** to test only available functionality
4. **Enhanced documentation** with detailed purpose and usage for each variable
5. **Fixed shell script** to handle edge cases with `set -euo pipefail`
6. **Clarified ownership** of each environment variable in the documentation

## Current Status

✅ Configuration system is fully functional and tested
✅ All tests passing (Python and Shell)
✅ Documentation is comprehensive and clear
✅ Separation of concerns is well-defined
✅ Ready for migration of hardcoded paths throughout the codebase
