# Shell Script Refactoring Issues

This directory contains 10 issues for refactoring shell scripts.

## Issues

1. Refactor tools/context-manager.sh to use jq instead of sed
2. Refactor tools/index-knowledge.sh to use jq instead of sed
3. Refactor tools/llama-lore-creator.sh to use jq instead of sed
4. Refactor tools/llama-lore-integrator.sh to eliminate sed/awk usage
5. Refactor docs/generators/knowledge-docs.sh to use jq and SKOGAI_* vars
6. Refactor metrics/collect-metrics.sh to use SKOGAI_* environment variables
7. Refactor openrouter/openrouter-models-new.sh to use SKOGAI_* environment variables
8. Refactor integration/orchestrator-flow.sh to use SKOGAI_* environment variables
9. Refactor integration/workflows/test-workflow.sh to use SKOGAI_* environment variables
10. Refactor demo/content-workflow.sh to use SKOGAI_* environment variables

## To Create These Issues

### Option 1: Using gh CLI
```bash
# Set GH_TOKEN environment variable with your GitHub token
export GH_TOKEN=your_token_here

# Run the original script
./create-script-refactor-issues.sh
```

### Option 2: Manual Creation
Use the individual markdown files in this directory to create issues manually.
