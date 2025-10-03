# Issue 15: Migrate skogai-agent-small-service.sh to use SKOGAI_* environment variables

## Title
Migrate skogai-agent-small-service.sh to use SKOGAI_* environment variables

## Body
## Description
Update `skogai-agent-small-service.sh` to use SKOGAI_* environment variables instead of hardcoded `/home/skogix/skogai/` paths.

## Current Issues
- Contains hardcoded `/home/skogix/skogai/` paths
- No environment variable support

## Requirements
- Use `SKOGAI_HOME` environment variable for base directory
- Use `SKOGAI_VENV` for virtual environment path
- Use `SKOGAI_AGENTS_DIR` for agents directory
- Maintain exact same functionality
- Ensure service starts correctly

## Environment Variables to Use
- `SKOGAI_HOME` - Base directory (default: `$HOME/skogai` or `$(pwd)`)
- `SKOGAI_VENV` - Virtual environment path (default: `$SKOGAI_HOME/.venv`)
- `SKOGAI_AGENTS_DIR` - Agents directory (default: `$SKOGAI_HOME/agents`)

## Example Transformation
**Before:**
```bash
BASE_DIR="/home/skogix/skogai"
```

**After:**
```bash
SKOGAI_HOME="${SKOGAI_HOME:-${HOME}/skogai}"
BASE_DIR="${SKOGAI_HOME}"
```

## Testing
- Start and stop the service
- Verify service runs correctly
- Test with and without environment variables set
- Ensure systemd integration works if applicable

Related to #5 (Configuration system implementation)
