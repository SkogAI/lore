# Issue 4: Refactor tools/llama-lore-integrator.sh to eliminate sed/awk usage

## Title
Refactor tools/llama-lore-integrator.sh to eliminate sed/awk usage

## Body
## Description
Rewrite \`tools/llama-lore-integrator.sh\` to eliminate sed and awk usage for text processing.

## Current Issues
- Uses \`sed\` for extracting entry IDs and parsing (lines 115, 119, 170, 174, 249, 253, 363)
- Uses \`awk\` for section splitting (lines 138, 321, 339)
- Complex text parsing with fragile patterns

## Requirements
- Replace sed with cut, grep, or other tools
- Replace awk with proper text processing tools
- Maintain exact same functionality
- Improve robustness of parsing

## Example Transformation
**Before:**
\`\`\`bash
sections=\$(echo "\$analysis" | awk '/^## /{if(p){print s} s=""; p=1} {s=s\$0"\\n"} END{if(p){print s}}')
ENTRY_ID=\$(ls -t \$SKOGAI_DIR/knowledge/expanded/lore/entries/ | head -n 1 | sed 's/\.json//')
\`\`\`

**After:**
\`\`\`bash
# Use proper section splitting without awk
ENTRY_ID=\$(ls -t \$SKOGAI_DIR/knowledge/expanded/lore/entries/*.json | head -n 1 | xargs basename | cut -d. -f1)
\`\`\`

## Testing
- Verify all functions work: lore extraction, entry creation, persona creation, connection analysis
- Test with various input formats
- Ensure JSON output is valid

Related to #41
