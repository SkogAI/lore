# Issue 12: Migrate agents/api/lore_api.py to use configuration system

## Title
Migrate agents/api/lore_api.py to use configuration system

## Body
## Description
Update `agents/api/lore_api.py` to use the new configuration system from issue #5 instead of hardcoded `/home/skogix/skogai/` paths.

## Current Issues
- Line 17: Hardcoded base directory `/home/skogix/skogai`
- Line 497: Hardcoded example path `/home/skogix/skogai/example-lorebook.json`

## Requirements
- Import and use the configuration system: `from config import paths`
- Replace hardcoded base_dir with environment variable support
- Use `paths.get_base_dir()` or similar method for base directory
- Replace example path with proper path resolution
- Maintain exact same functionality
- Ensure all LoreAPI methods work correctly

## Example Transformation
**Before:**
```python
def __init__(self, base_dir: str = "/home/skogix/skogai"):
    self.base_dir = base_dir
```

**After:**
```python
from config import paths

def __init__(self, base_dir: str = None):
    self.base_dir = base_dir or paths.get_base_dir()
```

## Testing
- Verify all LoreAPI methods work correctly
- Test lore creation, retrieval, and updates
- Test with and without environment variables set
- Ensure backward compatibility with existing callers

Related to #5 (Configuration system implementation)
