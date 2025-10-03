# Issue 7: Refactor openrouter/openrouter-models-new.sh to use SKOGAI_* environment variables

## Title
Refactor openrouter/openrouter-models-new.sh to use SKOGAI_* environment variables

## Body
## Description
Update \`openrouter/openrouter-models-new.sh\` to use SKOGAI_* environment variables instead of hardcoded paths.

## Current Issues
- Hardcoded path: \`/home/skogix/skogai/.venv\`

## Requirements
- Use \`SKOGAI_VENV\` environment variable for virtual environment path
- Maintain exact same functionality
- Handle case when venv doesn't exist

## Environment Variables to Use
- \`SKOGAI_VENV\` - Virtual environment path (default: \`\$SKOGAI_HOME/.venv\` or \`\$(pwd)/.venv\`)

## Testing
- Verify script works with and without venv
- Test with and without environment variables set
- Ensure API calls work correctly

Related to #41
