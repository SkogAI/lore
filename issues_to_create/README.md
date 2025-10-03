# Configuration System Migration Issues

This directory contains issues for migrating to the configuration system implemented in #5.

## Master Tracking Issue
**Issue #16** - Configuration System Migration - Master Tracking Issue

This master issue tracks all migration work and provides an overview of the benefits and resources.

## Issues

### Shell Scripts (10 issues)
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
15. Migrate skogai-agent-small-service.sh to use SKOGAI_* environment variables

### Python Files (4 issues)
11. Migrate agents/api/agent_api.py to use configuration system
12. Migrate agents/api/lore_api.py to use configuration system
13. Migrate agents/implementations/small_model_agents.py to use configuration system
14. Migrate demo/small_model_workflow.py to use configuration system

## Background

Issue #5 implemented a comprehensive configuration system to replace hardcoded paths throughout the codebase. The system provides:
- Python API: `from config import paths`
- Shell API: `source config/paths.sh`
- Environment variable support
- Git-aware path resolution
- Backward compatibility

## Migration Benefits
- **Flexibility**: Deploy anywhere without hardcoded paths
- **Compatibility**: Works with different user accounts
- **Maintainability**: Centralized path management
- **Testing**: Easier to test with different configurations

## To Create These Issues

### Option 1: Using gh CLI
```bash
# Set GH_TOKEN environment variable with your GitHub token
export GH_TOKEN=your_token_here

# Create all issues (requires gh CLI script)
for i in {01..16}; do
  if [ -f "issue_$i.md" ]; then
    gh issue create --title "$(grep '^# Issue' issue_$i.md | head -1 | sed 's/^# Issue [0-9]*: //')" \
      --body-file issue_$i.md --label "refactoring,configuration-system"
  fi
done
```

### Option 2: Manual Creation
Use the individual markdown files in this directory to create issues manually.

### Option 3: Create Master Issue First
Create issue #16 first (master tracking issue) then create individual issues and reference #16.

## Related Documentation
- Configuration system implementation: Issue #5
- Migration guide: `MIGRATION_GUIDE.md` (if merged from #5)
- Configuration API docs: `config/README.md` (if merged from #5)
- Environment variables documentation: `lorefiles/mnt_extra_20250730-skogai-main_.claude/skogai-environment-variables.md`
