#!/bin/bash
# Script to create GitHub issues for shell script refactoring
# This script creates 10 individual issues for refactoring shell scripts
# to remove sed/awk usage and use SKOGAI_* environment variables

set -e

REPO="SkogAI/lore"

echo "Creating GitHub issues for shell script refactoring..."
echo "Repository: $REPO"
echo ""

# Issue 1: tools/context-manager.sh
echo "Creating issue 1/10: tools/context-manager.sh"
gh issue create --repo "$REPO" --title "Refactor tools/context-manager.sh to use jq instead of sed" --body "$(cat <<'EOF'
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
EOF
)"

# Issue 2: tools/index-knowledge.sh
echo "Creating issue 2/10: tools/index-knowledge.sh"
gh issue create --repo "$REPO" --title "Refactor tools/index-knowledge.sh to use jq instead of sed" --body "$(cat <<'EOF'
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
EOF
)"

# Issue 3: tools/llama-lore-creator.sh
echo "Creating issue 3/10: tools/llama-lore-creator.sh"
gh issue create --repo "$REPO" --title "Refactor tools/llama-lore-creator.sh to use jq instead of sed" --body "$(cat <<'EOF'
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
EOF
)"

# Issue 4: tools/llama-lore-integrator.sh
echo "Creating issue 4/10: tools/llama-lore-integrator.sh"
gh issue create --repo "$REPO" --title "Refactor tools/llama-lore-integrator.sh to eliminate sed/awk usage" --body "$(cat <<'EOF'
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
EOF
)"

# Issue 5: docs/generators/knowledge-docs.sh
echo "Creating issue 5/10: docs/generators/knowledge-docs.sh"
gh issue create --repo "$REPO" --title "Refactor docs/generators/knowledge-docs.sh to use jq and SKOGAI_* vars" --body "$(cat <<'EOF'
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
EOF
)"

# Issue 6: metrics/collect-metrics.sh
echo "Creating issue 6/10: metrics/collect-metrics.sh"
gh issue create --repo "$REPO" --title "Refactor metrics/collect-metrics.sh to use SKOGAI_* environment variables" --body "$(cat <<'EOF'
## Description
Update \`metrics/collect-metrics.sh\` to use SKOGAI_* environment variables instead of hardcoded paths.

## Current Issues
- Hardcoded path: \`/home/skogix/skogai/metrics/system-metrics.json\`
- Hardcoded paths in find commands

## Requirements
- Use \`SKOGAI_HOME\` and \`SKOGAI_METRICS_DIR\` environment variables
- Maintain exact same functionality
- Ensure metrics collection works properly

## Environment Variables to Use
- \`SKOGAI_HOME\` - Base directory (default: \`\$HOME/skogai\` or \`\$(pwd)\`)
- \`SKOGAI_METRICS_DIR\` - Metrics directory (default: \`\$SKOGAI_HOME/metrics\`)
- \`SKOGAI_CONTEXT_DIR\` - Context directory (default: \`\$SKOGAI_HOME/context\`)
- \`SKOGAI_KNOWLEDGE_DIR\` - Knowledge directory (default: \`\$SKOGAI_HOME/knowledge\`)
- \`SKOGAI_AGENTS_DIR\` - Agents directory (default: \`\$SKOGAI_HOME/agents\`)

## Testing
- Verify metrics are collected correctly
- Test with and without environment variables set
- Ensure JSON output is valid

Related to #41
EOF
)"

# Issue 7: openrouter/openrouter-models-new.sh
echo "Creating issue 7/10: openrouter/openrouter-models-new.sh"
gh issue create --repo "$REPO" --title "Refactor openrouter/openrouter-models-new.sh to use SKOGAI_* environment variables" --body "$(cat <<'EOF'
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
EOF
)"

# Issue 8: integration/orchestrator-flow.sh
echo "Creating issue 8/10: integration/orchestrator-flow.sh"
gh issue create --repo "$REPO" --title "Refactor integration/orchestrator-flow.sh to use SKOGAI_* environment variables" --body "$(cat <<'EOF'
## Description
Update \`integration/orchestrator-flow.sh\` to use SKOGAI_* environment variables instead of hardcoded paths.

## Current Issues
- Likely contains hardcoded \`/home/skogix/skogai/\` paths

## Requirements
- Use \`SKOGAI_HOME\` and related environment variables
- Maintain exact same functionality
- Ensure integration flow works properly

## Environment Variables to Use
- \`SKOGAI_HOME\` - Base directory (default: \`\$HOME/skogai\` or \`\$(pwd)\`)
- Other relevant SKOGAI_* variables as needed

## Testing
- Verify orchestrator flow works correctly
- Test with and without environment variables set

Related to #41
EOF
)"

# Issue 9: integration/workflows/test-workflow.sh
echo "Creating issue 9/10: integration/workflows/test-workflow.sh"
gh issue create --repo "$REPO" --title "Refactor integration/workflows/test-workflow.sh to use SKOGAI_* environment variables" --body "$(cat <<'EOF'
## Description
Update \`integration/workflows/test-workflow.sh\` to use SKOGAI_* environment variables instead of hardcoded paths.

## Current Issues
- Likely contains hardcoded \`/home/skogix/skogai/\` paths

## Requirements
- Use \`SKOGAI_HOME\` and related environment variables
- Maintain exact same functionality
- Ensure test workflow executes properly

## Environment Variables to Use
- \`SKOGAI_HOME\` - Base directory (default: \`\$HOME/skogai\` or \`\$(pwd)\`)
- Other relevant SKOGAI_* variables as needed

## Testing
- Verify test workflow works correctly
- Test with and without environment variables set

Related to #41
EOF
)"

# Issue 10: demo/content-workflow.sh
echo "Creating issue 10/10: demo/content-workflow.sh"
gh issue create --repo "$REPO" --title "Refactor demo/content-workflow.sh to use SKOGAI_* environment variables" --body "$(cat <<'EOF'
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
EOF
)"

echo ""
echo "✅ Successfully created 10 issues for shell script refactoring!"
echo ""
echo "View all issues at: https://github.com/$REPO/issues"
