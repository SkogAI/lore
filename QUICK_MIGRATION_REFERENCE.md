# Quick Migration Reference

## TL;DR

Replace hardcoded `/home/skogix/skogai` paths with configuration system calls.

## Python Files

### Before
```python
config_path = "/home/skogix/skogai/config/llm_config.json"
output_dir = f"/home/skogix/skogai/demo/output_{timestamp}"
context_file = "/home/skogix/skogai/context/current/context.json"
```

### After
```python
from config import paths

config_path = paths.get_config_file("llm_config.json")
output_dir = paths.get_demo_output_dir(session_id, "agent_type")
paths.ensure_dir(output_dir)
context_file = paths.get_context_file("context.json")
```

## Shell Scripts

### Before
```bash
CONFIG_DIR="/home/skogix/skogai/config"
OUTPUT_DIR="/home/skogix/skogai/demo/output"
CONTEXT_FILE="/home/skogix/skogai/context/current/context.json"
```

### After
```bash
# Source the configuration library (adjust path as needed)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config/paths.sh"

CONFIG_DIR=$(get_config_dir)
OUTPUT_DIR=$(get_demo_output_dir "$session_id" "agent_type")
ensure_dir "$OUTPUT_DIR"
CONTEXT_FILE=$(get_context_file "context.json")
```

## Common Patterns

### Pattern 1: Config Files
```python
# Before
with open("/home/skogix/skogai/config/llm_config.json") as f:
    config = json.load(f)

# After
from config import paths
with open(paths.get_config_file("llm_config.json")) as f:
    config = json.load(f)
```

### Pattern 2: Output Directories
```python
# Before
timestamp = int(time.time())
output_dir = f"/home/skogix/skogai/demo/output_{timestamp}"
os.makedirs(output_dir, exist_ok=True)

# After
from config import paths
output_dir = paths.get_demo_output_dir(session_id, "content_creation")
paths.ensure_dir(output_dir)
```

### Pattern 3: Sys.path Manipulation
```python
# Before
sys.path.append("/home/skogix/skogai")
sys.path.append("/home/skogix/skogai/agents")

# After
from config import paths
# Usually not needed if running from repo, but if required:
sys.path.insert(0, str(paths.get_base_dir()))
sys.path.insert(0, str(paths.get_agents_dir()))
```

### Pattern 4: Context Files
```bash
# Before
CONTEXT_DIR="/home/skogix/skogai/context"
TEMPLATE="$CONTEXT_DIR/templates/base-context.json"
CURRENT="$CONTEXT_DIR/current/context-${session_id}.json"

# After
source "$(dirname "$0")/config/paths.sh"
CONTEXT_DIR=$(get_context_dir)
TEMPLATE="$CONTEXT_DIR/templates/base-context.json"
CURRENT="$CONTEXT_DIR/current/context-${session_id}.json"
```

### Pattern 5: Service Scripts
```bash
# Before
INSTALL_DIR="/home/skogix/skogai"
SERVICE_SCRIPT="$INSTALL_DIR/service.sh"

# After
source "$(dirname "$0")/config/paths.sh"
INSTALL_DIR=$(get_base_dir)
SERVICE_SCRIPT="$INSTALL_DIR/service.sh"
```

## Available Functions

### Python API (`config/paths.py`)

```python
from config import paths

# Base paths
paths.get_base_dir()                    # Base directory
paths.get_config_dir()                  # Config directory
paths.get_agents_dir()                  # Agents directory
paths.get_demo_dir()                    # Demo directory
paths.get_context_dir()                 # Context directory
paths.get_knowledge_dir()               # Knowledge base directory

# Specific files/dirs
paths.get_config_file(filename)         # Config file path
paths.get_demo_output_dir(session_id, agent_type)  # Demo output
paths.get_context_file(filename)        # Context file path
paths.get_agent_file(agent_name)        # Agent implementation

# Utilities
paths.ensure_dir(path)                  # Create directory if needed
```

### Shell API (`config/paths.sh`)

```bash
source "path/to/config/paths.sh"

# Base paths
get_base_dir
get_config_dir
get_agents_dir
get_demo_dir
get_context_dir
get_knowledge_dir

# Specific files/dirs
get_config_file "filename"
get_demo_output_dir "$session_id" "$agent_type"
get_context_file "filename"
get_agent_file "agent_name"

# Utilities
ensure_dir "$path"
```

## Environment Variables

Set these to customize paths:

```bash
export SKOGAI_BASE_DIR="/custom/path"           # Override base directory
export SKOGAI_CONFIG_DIR="/custom/config"       # Override config directory
export SKOGAI_AGENTS_DIR="/custom/agents"       # Override agents directory
export SKOGAI_DEMO_DIR="/custom/demo"           # Override demo directory
export SKOGAI_CONTEXT_DIR="/custom/context"     # Override context directory
export SKOGAI_KNOWLEDGE_DIR="/custom/knowledge" # Override knowledge directory
```

### Path Resolution Priority

1. **Environment variable** (if set)
2. **Git repository root** (auto-detected if in git repo)
3. **Legacy default** (`/home/skogix/skogai`)

## Migration Checklist

For each file you migrate:

- [ ] Import/source configuration library
- [ ] Replace all hardcoded paths
- [ ] Use `ensure_dir()` for directory creation
- [ ] Test with default configuration
- [ ] Test with custom environment variables
- [ ] Run validation tool
- [ ] Update file documentation if needed

## Validation

### Check a Python file
```bash
python tools/check_hardcoded_paths.py path/to/file.py
```

### Check a Shell script
```bash
bash tools/check_hardcoded_paths.sh path/to/script.sh
```

### Check before commit
Pre-commit hooks automatically check new changes:
```bash
# Install hooks
pip install pre-commit
pre-commit install

# Manually run
pre-commit run --all-files
```

## Testing Your Migration

1. **Default configuration:**
   ```bash
   # Run your script normally
   python your_script.py
   ```

2. **Custom base directory:**
   ```bash
   export SKOGAI_BASE_DIR="/tmp/test-skogai"
   python your_script.py
   ```

3. **Individual overrides:**
   ```bash
   export SKOGAI_CONFIG_DIR="/custom/config"
   export SKOGAI_DEMO_DIR="/custom/demo"
   python your_script.py
   ```

4. **Verify paths:**
   Add debug output:
   ```python
   from config import paths
   print(f"Base dir: {paths.get_base_dir()}")
   print(f"Config dir: {paths.get_config_dir()}")
   ```

## Common Mistakes

### ❌ Don't: Hard-code in imports
```python
sys.path.append("/home/skogix/skogai/agents")
from agents.implementations import MyAgent
```

### ✅ Do: Use relative imports or configuration
```python
# Best: Use relative imports if in same package
from .implementations import MyAgent

# Or: Use configuration for sys.path if needed
from config import paths
sys.path.insert(0, str(paths.get_agents_dir()))
from implementations import MyAgent
```

### ❌ Don't: Hard-code directory creation
```python
os.makedirs("/home/skogix/skogai/output", exist_ok=True)
```

### ✅ Do: Use ensure_dir
```python
from config import paths
output_dir = paths.get_demo_output_dir(session_id, "type")
paths.ensure_dir(output_dir)
```

### ❌ Don't: String concatenation with base path
```python
base = paths.get_base_dir()
config = base + "/config/llm.json"  # Wrong!
```

### ✅ Do: Use proper path joining
```python
from config import paths
config = paths.get_config_file("llm.json")
# Or if you need custom joining:
from pathlib import Path
config = paths.get_base_dir() / "config" / "llm.json"
```

## Need Help?

1. Check `MIGRATION_ROADMAP.md` for overall strategy
2. Read `config/README.md` for complete API reference
3. See `MIGRATION_GUIDE.md` for detailed examples (when available)
4. Look at already-migrated files for examples
5. Run validation tools to catch issues

## Quick Start Example

**Migrate a simple Python script:**

```python
# Before (hardcoded_script.py)
import json

with open("/home/skogix/skogai/config/llm_config.json") as f:
    config = json.load(f)

output_dir = "/home/skogix/skogai/demo/output"

# After (migrated_script.py)
import json
from config import paths

with open(paths.get_config_file("llm_config.json")) as f:
    config = json.load(f)

output_dir = paths.get_demo_dir() / "output"
paths.ensure_dir(output_dir)
```

**Migrate a simple Shell script:**

```bash
# Before (hardcoded_script.sh)
#!/bin/bash
CONFIG_DIR="/home/skogix/skogai/config"
echo "Config: $CONFIG_DIR"

# After (migrated_script.sh)
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config/paths.sh"

CONFIG_DIR=$(get_config_dir)
echo "Config: $CONFIG_DIR"
```

That's it! You're ready to migrate files. Start with the configuration system foundation issue, then work through the others systematically.
