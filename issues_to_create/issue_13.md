# Issue 13: Migrate agents/implementations/small_model_agents.py to use configuration system

## Title
Migrate agents/implementations/small_model_agents.py to use configuration system

## Body
## Description
Update `agents/implementations/small_model_agents.py` to use the new configuration system from issue #5 instead of hardcoded `/home/skogix/skogai/` paths.

## Current Issues
- Line 18: Hardcoded prompt directory `/home/skogix/skogai/agents/templates/small_models`

## Requirements
- Import and use the configuration system: `from config import paths`
- Replace hardcoded prompt_dir with proper path resolution
- Use appropriate path resolution method for agents templates
- Maintain exact same functionality
- Ensure all small model agent methods work correctly

## Example Transformation
**Before:**
```python
prompt_dir: str = "/home/skogix/skogai/agents/templates/small_models"
```

**After:**
```python
from config import paths

prompt_dir: str = None
# In __init__ or method:
self.prompt_dir = prompt_dir or paths.get_agents_dir() / "templates" / "small_models"
```

## Testing
- Verify all small model agent functionality works
- Test prompt loading and generation
- Test with and without environment variables set
- Ensure backward compatibility with existing callers

Related to #5 (Configuration system implementation)
