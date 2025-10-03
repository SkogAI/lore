# Issue 1: Refactor tools/context-manager.sh to use jq instead of sed

## Title
Refactor tools/context-manager.sh to use jq instead of sed

## Body
## Description
Rewrite \`tools/context-manager.sh\` to eliminate sed/awk usage and use jq for JSON manipulation. Replace hardcoded paths with SKOGAI_* environment variables.

## Current Issues
- Uses \`sed -i\` extensively for JSON field updates (lines 13-16, 41-42)
- Hardcoded paths: \`/home/skogix/skogai/context/\`
- Brittle string replacement for JSON manipulation

## Requirements
- Replace all \`sed\` commands with \`jq\` for JSON manipulation
- Use \`SKOGAI_HOME\` environment variable with sane defaults
- Use \`SKOGAI_CONTEXT_DIR\` for context directory paths
- Maintain exact same functionality
- Ensure proper error handling

## Example Transformation
**Before:**
\`\`\`bash
sed -i "s/\"created\": \"\"/\"created\": \"\$(date -Iseconds)\"/" "/home/skogix/skogai/context/current/context-\${session_id}.json"
\`\`\`

**After:**
\`\`\`bash
CONTEXT_DIR="\${SKOGAI_CONTEXT_DIR:-\${SKOGAI_HOME:-\$HOME/skogai}/context}"
jq ".created = \"\$(date -Iseconds)\"" "\${CONTEXT_DIR}/current/context-\${session_id}.json" > tmp.json && mv tmp.json "\${CONTEXT_DIR}/current/context-\${session_id}.json"
\`\`\`

## Environment Variables to Use
- \`SKOGAI_HOME\` - Base directory (default: \`\$HOME/skogai\` or \`\$(pwd)\`)
- \`SKOGAI_CONTEXT_DIR\` - Context directory (default: \`\$SKOGAI_HOME/context\`)

## Testing
- Verify all functions work: create, archive, update
- Test with and without environment variables set
- Ensure JSON output is valid

Related to #41
