# Issue 3: Refactor tools/llama-lore-creator.sh to use jq instead of sed

## Title
Refactor tools/llama-lore-creator.sh to use jq instead of sed

## Body
## Description
Rewrite \`tools/llama-lore-creator.sh\` to eliminate sed usage for parsing and JSON manipulation.

## Current Issues
- Uses \`sed\` for extracting entry IDs from filenames (lines 52, 105, 129, 187)
- Uses \`sed\` for parsing model output (lines 92-93, 119, 146-147, 179)
- Relies on SKOGAI_DIR but could be more robust

## Requirements
- Replace sed commands with jq for JSON parsing
- Use proper string manipulation for parsing model output
- Maintain exact same functionality
- Improve error handling for parsing failures

## Example Transformation
**Before:**
\`\`\`bash
ENTRY_ID=\$(ls -t \$SKOGAI_DIR/knowledge/expanded/lore/entries/ | head -n 1 | sed 's/\.json//')
TRAITS=\$(echo "\$RESPONSE" | grep -i "TRAITS:" | head -n 1 | sed 's/TRAITS://i' | xargs)
\`\`\`

**After:**
\`\`\`bash
ENTRY_ID=\$(ls -t \$SKOGAI_DIR/knowledge/expanded/lore/entries/*.json | head -n 1 | xargs basename | cut -d. -f1)
TRAITS=\$(echo "\$RESPONSE" | grep -i "TRAITS:" | head -n 1 | cut -d: -f2- | xargs)
\`\`\`

## Testing
- Verify all functions work: entry generation, persona creation, lorebook creation
- Test parsing of various model outputs
- Ensure JSON files are valid

Related to #41
