# Migration Guide: Hardcoded Paths to Configuration System

This guide provides step-by-step instructions for migrating from hardcoded paths to the new configuration system.

## Overview

**Status:** Partially implemented (Issue #5)

The configuration system has been implemented and the most critical files have been migrated. However, **87+ Python files and 15+ shell scripts** still contain hardcoded paths that need migration.

## What Has Been Done

### ✅ Implemented

1. **Configuration System** (`config/` directory):
   - `config/paths.py` - Python path resolution
   - `config/settings.py` - Configuration management
   - `config/paths.sh` - Shell script path resolution
   - `config/__init__.py` - Module initialization
   - `config/README.md` - Complete documentation

2. **Validation Tools**:
   - `tools/check_hardcoded_paths.py` - Python file validator
   - `tools/check_hardcoded_paths.sh` - Shell script validator
   - `.pre-commit-config.yaml` - Pre-commit hook configuration

3. **Migrated Files** (examples):
   - `agents/api/agent_api.py` - All 6 hardcoded paths replaced
   - `demo/small_model_workflow.py` - Updated to use paths API
   - `tools/context-manager.sh` - Updated to source paths.sh

### ❌ Still To Do

Files that still need migration (partial list):

**Python Files:**
- `agents/api/lore_api.py`
- `agents/implementations/small_model_agents.py`
- `demo/chat_ui_demo.py`
- `demo/issue_creator_demo.py`
- `demo/lore_demo.py`
- `generate-agent-lore.py`
- `integration/persona-bridge/persona-manager.py`
- `main.py`
- `openrouter/or_free_helper.py`
- `openrouter/or-free.py`
- `streamlit_chat.py`
- `skogai-chat.py`
- `st-lore-export.py`
- Plus 70+ more files

**Shell Scripts:**
- `tools/index-knowledge.sh`
- `openrouter/openrouter-models.sh.bak`
- `openrouter/openrouter-models-new.sh`
- `openrouter/orfree`
- `skogai-agent-small-service.sh`
- `skogai-lore-service.sh`
- `setup-skogai-agent-small.sh`
- Plus 8+ more scripts

**Service/Config Files:**
- `skogai-chat.desktop`
- `skogai-lore-service.service`
- `skogai-agent-small.service`

**Data Files:**
- `MASTER_KNOWLEDGE/MERGE_MANIFEST.json` (577+ hardcoded paths)
- `node_modules/.modules.yaml`
- Various configuration and manifest files

## Migration Steps

### For Python Files

1. **Add imports** at the top of the file:
   ```python
   import os
   import sys

   # Add project root to path
   project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
   sys.path.insert(0, project_root)

   from config import paths
   ```

2. **Replace hardcoded paths** with configuration calls:
   ```python
   # Before:
   config_file = "/home/skogix/skogai/config/llm_config.json"
   output_dir = f"/home/skogix/skogai/demo/output_{session_id}"
   os.makedirs(output_dir, exist_ok=True)

   # After:
   config_file = paths.get_config_file("llm_config.json")
   output_dir = paths.get_demo_output_dir(session_id, "output")
   paths.ensure_dir(output_dir)
   ```

3. **Test the changes**:
   ```bash
   # Test in git repository
   python your_script.py

   # Test with custom base directory
   SKOGAI_BASE_DIR=/tmp/test python your_script.py
   ```

### For Shell Scripts

1. **Source the path library** at the beginning:
   ```bash
   #!/bin/bash

   # Load path configuration
   SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
   source "$SCRIPT_DIR/../config/paths.sh"
   ```

2. **Replace hardcoded paths**:
   ```bash
   # Before:
   CONTEXT_DIR="/home/skogix/skogai/context"
   KNOWLEDGE_DIR="/home/skogix/skogai/knowledge"
   mkdir -p "$CONTEXT_DIR/current"

   # After:
   context_dir=$(get_context_dir)
   knowledge_dir=$(get_knowledge_dir)
   ensure_dir "$context_dir/current"
   ```

3. **Test the changes**:
   ```bash
   # Test in git repository
   bash your_script.sh

   # Test with custom base directory
   SKOGAI_BASE_DIR=/tmp/test bash your_script.sh
   ```

### For Service Files

1. **Update systemd service files**:
   ```ini
   # Before:
   WorkingDirectory=/home/skogix/skogai
   ExecStart=/home/skogix/skogai/script.sh

   # After:
   WorkingDirectory=%h/skogai
   ExecStart=%h/skogai/script.sh
   Environment="SKOGAI_BASE_DIR=%h/skogai"
   ```

2. **Update desktop files**:
   ```desktop
   # Before:
   Exec=/home/skogix/skogai/start-chat-ui.sh

   # After:
   Exec=/usr/local/bin/skogai-start-chat
   # (Install script to /usr/local/bin with proper path resolution)
   ```

## Automated Migration

A semi-automated migration script is available:

```bash
# Run migration script (to be created)
python tools/migrate_hardcoded_paths.py --dry-run

# Apply changes
python tools/migrate_hardcoded_paths.py --apply
```

**Note:** The migration script should be reviewed before use. Some paths may require manual intervention.

## Validation

### Pre-commit Hooks

Install pre-commit hooks to prevent new hardcoded paths:

```bash
pip install pre-commit
pre-commit install
```

### Manual Validation

Check files for hardcoded paths:

```bash
# Check Python files
python tools/check_hardcoded_paths.py $(find . -name "*.py" -not -path "./node_modules/*")

# Check shell scripts
bash tools/check_hardcoded_paths.sh $(find . -name "*.sh" -not -path "./node_modules/*")
```

## Deployment Configuration

### Development Environment

No configuration needed - automatically uses git repository root:

```bash
cd /path/to/lore
python demo/small_model_workflow.py "test topic"
```

### Production Environment

Set environment variables in your deployment:

```bash
# /etc/environment or ~/.bashrc
export SKOGAI_BASE_DIR="/opt/skogai"
export SKOGAI_KNOWLEDGE_DIR="/mnt/data/knowledge"
export SKOGAI_CONTEXT_DIR="/var/lib/skogai/context"
```

### Docker Environment

```dockerfile
ENV SKOGAI_BASE_DIR=/app
ENV SKOGAI_KNOWLEDGE_DIR=/data/knowledge
ENV SKOGAI_CONTEXT_DIR=/data/context
```

### Systemd Service

```ini
[Service]
Environment="SKOGAI_BASE_DIR=/opt/skogai"
Environment="SKOGAI_KNOWLEDGE_DIR=/mnt/data/knowledge"
```

## Testing Migration

After migrating a file:

1. **Unit test** - Ensure the file still works:
   ```bash
   python -m pytest tests/test_your_file.py
   ```

2. **Integration test** - Test in realistic environment:
   ```bash
   # Test with default paths
   python your_script.py

   # Test with custom paths
   export SKOGAI_BASE_DIR=/tmp/test_env
   python your_script.py
   ```

3. **Pre-commit check** - Ensure no hardcoded paths remain:
   ```bash
   pre-commit run --files your_script.py
   ```

## Common Migration Patterns

### Pattern 1: Config File Path
```python
# Before:
config_path = "/home/skogix/skogai/config/llm_config.json"

# After:
from config import paths
config_path = paths.get_config_file("llm_config.json")
```

### Pattern 2: Output Directory with Session ID
```python
# Before:
output_dir = f"/home/skogix/skogai/demo/content_{session_id}"
os.makedirs(output_dir, exist_ok=True)

# After:
from config import paths
output_dir = paths.get_demo_output_dir(session_id, "content")
paths.ensure_dir(output_dir)
```

### Pattern 3: Agent Implementation Path
```python
# Before:
agent_file = f"/home/skogix/skogai/agents/implementations/{agent_type}.py"

# After:
from config import paths
agent_file = paths.get_agent_path(f"implementations/{agent_type}.py")
```

### Pattern 4: Context Management (Shell)
```bash
# Before:
CONTEXT_DIR="/home/skogix/skogai/context"
cp "$CONTEXT_DIR/templates/base.json" "$CONTEXT_DIR/current/session.json"

# After:
source "$SCRIPT_DIR/../config/paths.sh"
context_dir=$(get_context_dir)
cp "$(get_context_path 'templates/base.json')" "$(get_context_path 'current/session.json')"
```

### Pattern 5: Virtual Environment
```bash
# Before:
VENV="/home/skogix/skogai/.venv"
source "$VENV/bin/activate"

# After:
source "$(dirname "$0")/../config/paths.sh"
venv_dir=$(get_venv_dir)
source "$venv_dir/bin/activate"
```

## Known Issues

1. **Node modules** - Some generated files in `node_modules/` have hardcoded paths. These are auto-generated and should be excluded from migration.

2. **Legacy documentation** - `MASTER_KNOWLEDGE/` contains historical documentation with hardcoded paths. These are archives and don't need migration.

3. **External dependencies** - Some paths reference external systems (`/mnt/warez/`, etc.). These may need special handling or configuration.

## Rollback Plan

If migration causes issues:

1. **Git revert** - Revert specific commits:
   ```bash
   git revert <commit-hash>
   ```

2. **Temporary bypass** - Set environment variable to legacy path:
   ```bash
   export SKOGAI_BASE_DIR="/home/skogix/skogai"
   ```

3. **File-specific rollback** - Restore individual files:
   ```bash
   git checkout HEAD~1 -- path/to/file.py
   ```

## Next Steps

1. **Create migration script** - Automate bulk file migration
2. **Migrate remaining Python files** - Systematic file-by-file migration
3. **Migrate shell scripts** - Update all shell scripts
4. **Update service files** - Systemd and desktop files
5. **Document edge cases** - Document any special cases discovered
6. **Add tests** - Ensure configuration system works correctly
7. **Update CI/CD** - Ensure deployment pipelines use new system

## Questions?

See `config/README.md` for detailed API documentation and examples.

Report issues at: https://github.com/SkogAI/lore/issues/5
