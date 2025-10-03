# Issue 5: Refactor docs/generators/knowledge-docs.sh to use jq and SKOGAI_* vars

## Title
Refactor docs/generators/knowledge-docs.sh to use jq and SKOGAI_* vars

## Body
## Description
Rewrite \`docs/generators/knowledge-docs.sh\` to eliminate sed usage and use SKOGAI_* environment variables instead of hardcoded paths.

## Current Issues
- Uses \`sed\` for extracting metadata from markdown (lines 28-29)
- Hardcoded paths: \`/home/skogix/skogai/\`
- Uses \`tr\` for case conversion (could be simplified)

## Requirements
- Replace sed with proper metadata extraction
- Use \`SKOGAI_HOME\` and \`SKOGAI_DOCS_DIR\` environment variables
- Maintain exact same functionality
- Ensure generated documentation is correct

## Environment Variables to Use
- \`SKOGAI_HOME\` - Base directory (default: \`\$HOME/skogai\` or \`\$(pwd)\`)
- \`SKOGAI_DOCS_DIR\` - Docs directory (default: \`\$SKOGAI_HOME/docs/generated\`)
- \`SKOGAI_KNOWLEDGE_DIR\` - Knowledge directory (default: \`\$SKOGAI_HOME/knowledge\`)

## Testing
- Verify generated documentation is correct
- Test with various markdown formats
- Test with and without environment variables set

Related to #41
