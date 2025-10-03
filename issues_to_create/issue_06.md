# Issue 6: Refactor metrics/collect-metrics.sh to use SKOGAI_* environment variables

## Title
Refactor metrics/collect-metrics.sh to use SKOGAI_* environment variables

## Body
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
