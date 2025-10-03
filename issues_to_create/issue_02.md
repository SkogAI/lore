# Issue 2: Refactor tools/index-knowledge.sh to use jq instead of sed

## Title
Refactor tools/index-knowledge.sh to use jq instead of sed

## Body
## Description
Rewrite \`tools/index-knowledge.sh\` to eliminate sed usage for extracting metadata. Replace hardcoded paths with SKOGAI_* environment variables.

## Current Issues
- Uses \`sed\` for extracting ID and tags from markdown files (lines 12, 14)
- Hardcoded paths: \`/home/skogix/skogai/knowledge/\`
- Could use more robust metadata extraction

## Requirements
- Use proper markdown/YAML frontmatter parsing or grep patterns instead of sed
- Use \`SKOGAI_HOME\` and \`SKOGAI_KNOWLEDGE_DIR\` environment variables
- Maintain exact same functionality
- Make metadata extraction more robust

## Environment Variables to Use
- \`SKOGAI_HOME\` - Base directory (default: \`\$HOME/skogai\` or \`\$(pwd)\`)
- \`SKOGAI_KNOWLEDGE_DIR\` - Knowledge directory (default: \`\$SKOGAI_HOME/knowledge\`)

## Testing
- Verify INDEX.md is generated correctly
- Test with various markdown file formats
- Test with and without environment variables set

Related to #41
