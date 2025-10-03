# Issue 16: Configuration System Migration - Master Tracking Issue

## Title
Configuration System Migration - Master Tracking Issue

## Body
## Overview
This is a master tracking issue for the migration to the configuration system implemented in #5. The goal is to replace all hardcoded `/home/skogix/skogai/` paths with the new configuration system that supports SKOGAI_* environment variables.

## Configuration System
Issue #5 implemented a centralized configuration system with:
- Python API: `from config import paths`
- Shell API: `source config/paths.sh`
- Environment variable support (`SKOGAI_BASE_DIR`, `SKOGAI_AGENTS_DIR`, etc.)
- Git-aware path resolution
- Backward compatibility

See `config/README.md` and `MIGRATION_GUIDE.md` for details.

## Migration Progress

### Shell Scripts
- [ ] #1 - tools/context-manager.sh (jq + SKOGAI_* vars)
- [ ] #2 - tools/index-knowledge.sh (jq + SKOGAI_* vars)
- [ ] #3 - tools/llama-lore-creator.sh (jq + SKOGAI_* vars)
- [ ] #4 - tools/llama-lore-integrator.sh (eliminate sed/awk)
- [ ] #5 - docs/generators/knowledge-docs.sh (jq + SKOGAI_* vars)
- [ ] #6 - metrics/collect-metrics.sh (SKOGAI_* vars)
- [ ] #7 - openrouter/openrouter-models-new.sh (SKOGAI_* vars)
- [ ] #8 - integration/orchestrator-flow.sh (SKOGAI_* vars)
- [ ] #9 - integration/workflows/test-workflow.sh (SKOGAI_* vars)
- [ ] #10 - demo/content-workflow.sh (SKOGAI_* vars)
- [ ] #15 - skogai-agent-small-service.sh (SKOGAI_* vars)

### Python Files
- [ ] #11 - agents/api/agent_api.py
- [ ] #12 - agents/api/lore_api.py
- [ ] #13 - agents/implementations/small_model_agents.py
- [ ] #14 - demo/small_model_workflow.py

### Additional Files
Additional Python and shell files may be discovered during migration. Update this tracking issue as new files are identified.

## Benefits
- **Flexibility**: Deploy anywhere without hardcoded paths
- **Compatibility**: Works with different user accounts and deployment scenarios
- **Maintainability**: Centralized path management
- **Testing**: Easier to test with different configurations
- **CI/CD**: Better support for automated testing and deployment

## Migration Resources
- Configuration system: `config/` directory
- Migration guide: `MIGRATION_GUIDE.md`
- Python API docs: `config/README.md`
- Shell API: `config/paths.sh`
- Validation tools: `tools/check_hardcoded_paths.py`, `tools/check_hardcoded_paths.sh`

## Validation
After migration, run validation tools:
```bash
# Check Python files
python tools/check_hardcoded_paths.py $(find . -name "*.py" -not -path "./lorefiles/*" -not -path "./MASTER_KNOWLEDGE*")

# Check shell scripts
bash tools/check_hardcoded_paths.sh
```

## Pre-commit Hooks
Install pre-commit hooks to prevent new hardcoded paths:
```bash
pip install pre-commit
pre-commit install
```

Related to #5 (Configuration system implementation)
