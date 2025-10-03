# Issue 11: Migrate agents/api/agent_api.py to use configuration system

## Title
Migrate agents/api/agent_api.py to use configuration system

## Body
## Description
Update `agents/api/agent_api.py` to use the new configuration system from issue #5 instead of hardcoded `/home/skogix/skogai/` paths.

## Current Issues
- Line 20: Hardcoded config path `/home/skogix/skogai/config/llm_config.json`
- Line 90: Hardcoded demo directory path `/home/skogix/skogai/demo/content_creation_{session_id}`
- Line 123: Hardcoded demo directory path `/home/skogix/skogai/demo/content_creation_{session_id}`
- Line 145: Hardcoded agent implementations path `/home/skogix/skogai/agents/implementations/content/{agent_type}-agent.md`

## Requirements
- Import and use the configuration system: `from config import paths`
- Replace hardcoded config path with `paths.get_config_file("llm_config.json")`
- Replace demo directory paths with `paths.get_demo_output_dir(session_id, "content_creation")`
- Replace agent implementations path with proper path resolution
- Maintain exact same functionality
- Ensure all API methods work correctly

## Example Transformation
**Before:**
```python
def __init__(self, config_path: str = "/home/skogix/skogai/config/llm_config.json"):
    self.config_path = config_path
```

**After:**
```python
from config import paths

def __init__(self, config_path: str = None):
    self.config_path = config_path or paths.get_config_file("llm_config.json")
```

## Testing
- Verify all AgentAPI methods work correctly
- Test with custom config paths
- Test with and without environment variables set
- Ensure backward compatibility with existing callers

Related to #5 (Configuration system implementation)
