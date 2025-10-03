# Issue 14: Migrate demo/small_model_workflow.py to use configuration system

## Title
Migrate demo/small_model_workflow.py to use configuration system

## Body
## Description
Update `demo/small_model_workflow.py` to use the new configuration system from issue #5 instead of hardcoded `/home/skogix/skogai/` paths.

## Current Issues
- Line 33: Hardcoded output directory `/home/skogix/skogai/demo/small_model_content_{timestamp}`

## Requirements
- Import and use the configuration system: `from config import paths`
- Replace hardcoded output path with `paths.get_demo_output_dir()`
- Maintain exact same functionality
- Ensure demo workflow executes correctly

## Example Transformation
**Before:**
```python
output_dir = f"/home/skogix/skogai/demo/small_model_content_{timestamp}"
```

**After:**
```python
from config import paths

output_dir = paths.get_demo_output_dir(timestamp, "small_model_content")
paths.ensure_dir(output_dir)
```

## Testing
- Run the demo workflow end-to-end
- Verify output files are created in correct location
- Test with and without environment variables set
- Ensure demo produces expected results

Related to #5 (Configuration system implementation)
