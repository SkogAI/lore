# Issue 10: Refactor demo/content-workflow.sh to use SKOGAI_* environment variables

## Title
Refactor demo/content-workflow.sh to use SKOGAI_* environment variables

## Body
## Description
Update \`demo/content-workflow.sh\` to use SKOGAI_* environment variables instead of hardcoded paths.

## Current Issues
- Likely contains hardcoded \`/home/skogix/skogai/\` paths

## Requirements
- Use \`SKOGAI_HOME\` and related environment variables
- Maintain exact same functionality
- Ensure demo workflow works properly

## Environment Variables to Use
- \`SKOGAI_HOME\` - Base directory (default: \`\$HOME/skogai\` or \`\$(pwd)\`)
- Other relevant SKOGAI_* variables as needed

## Testing
- Verify demo workflow works correctly
- Test with and without environment variables set

Related to #41
