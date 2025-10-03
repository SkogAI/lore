# Configuration System Migration Roadmap

## Overview

This roadmap outlines the systematic migration of 509 files with hardcoded `/home/skogix/skogai` paths to a centralized configuration system with environment variable support.

## Current State

**Analysis Results:**
- **509 files** contain hardcoded paths
- **Python files:** ~25+ core files (agents, demos, tools, apps)
- **Shell scripts:** ~23 scripts (services, tools, workflows)
- **Config files:** Service definitions, desktop files
- **Archive files:** Hundreds of files in lorefiles/ (low priority)

## Migration Strategy

### Phase 1: Foundation (Week 1)

**Issue: Create Configuration System**
- Implement `config/paths.py` (Python API)
- Implement `config/paths.sh` (Shell API)
- Create validation tools
- Setup pre-commit hooks
- Write comprehensive documentation

**Priority:** CRITICAL - All other phases depend on this

### Phase 2: Core Components (Week 2-3)

**Issue: Migrate Core Agent Files**
- `agents/api/agent_api.py`
- `agents/implementations/small_model_agents.py`
- `agents/api/lore_api.py`

**Issue: Migrate Main Applications**
- `streamlit_chat.py`
- `skogai-chat.py`
- `main.py`
- `st-lore-export.py`
- `generate-agent-lore.py`

**Priority:** HIGH - These are the most frequently used files

### Phase 3: Workflows and Tools (Week 3-4)

**Issue: Migrate Demo and Workflow Scripts**
- `demo/small_model_workflow.py`
- `demo/chat_ui_demo.py`
- `demo/lore_demo.py`
- Shell workflow scripts

**Issue: Migrate Tool Scripts**
- `tools/context-manager.sh`
- `tools/index-knowledge.sh`
- `tools/setup-lore-service.sh`
- Other tool scripts

**Priority:** MEDIUM - Important but less frequently used

### Phase 4: Integration and Services (Week 4-5)

**Issue: Migrate Service and System Files**
- `skogai-agent-small-service.sh`
- `skogai-lore-service.sh`
- Systemd service files
- Desktop integration

**Issue: Migrate OpenRouter Scripts**
- `openrouter/or-free.py`
- `openrouter/openrouter-models-new.sh`
- Other OpenRouter integration

**Priority:** MEDIUM - System integration

### Phase 5: Utilities and Metrics (Week 5)

**Issue: Migrate Metrics and Utilities**
- `metrics/collect-metrics.sh`
- `create_issues_from_script.py`
- Documentation generators

**Priority:** LOW - Nice to have

### Phase 6: Documentation and Validation (Week 6)

**Issue: Create Migration Guide**
- Write `MIGRATION_GUIDE.md`
- Update `config/README.md`
- Update installation docs
- Create examples

**Issue: Final Validation and Testing**
- Automated validation (zero hardcoded paths)
- Functional testing (all features work)
- Environment testing (all configs work)
- Backward compatibility testing
- Performance testing

**Priority:** CRITICAL - Ensures quality

## Files Excluded from Migration

### Archive/Backup Files (lorefiles/)
These are historical archives and don't need migration:
- `lorefiles/mnt_*` directories (hundreds of archived files)
- MASTER_KNOWLEDGE_COMPLETE archives
- Old backup directories

### Node Modules
- `node_modules/` - Third-party dependencies

### Documentation/Examples
- Files that mention paths as examples/documentation
- README files with path references (unless installation guides)

## Migration Workflow

### For Each File:

1. **Audit**
   - Identify all hardcoded paths
   - Determine appropriate configuration function

2. **Migrate**
   - Import/source configuration system
   - Replace hardcoded paths with function calls
   - Add any missing `ensure_dir()` calls

3. **Test**
   - Test with default configuration
   - Test with environment variables
   - Test with custom base directory
   - Verify backward compatibility

4. **Validate**
   - Run automated path checker
   - Review pre-commit hook output
   - Update documentation if needed

## Success Metrics

- [ ] **Zero** hardcoded paths in active Python files
- [ ] **Zero** hardcoded paths in active Shell scripts
- [ ] **100%** of core features work with custom configurations
- [ ] **100%** backward compatibility maintained
- [ ] Pre-commit hooks prevent new hardcoded paths
- [ ] Complete API documentation
- [ ] Complete migration guide

## Environment Variables

### Primary Variables
- `SKOGAI_BASE_DIR` - Base directory for all paths
- `SKOGAI_CONFIG_DIR` - Configuration files
- `SKOGAI_AGENTS_DIR` - Agent implementations
- `SKOGAI_DEMO_DIR` - Demo outputs
- `SKOGAI_CONTEXT_DIR` - Context files
- `SKOGAI_KNOWLEDGE_DIR` - Knowledge base

### Path Resolution Priority
1. **Environment variable** (if set)
2. **Git repository root** (if in git repo)
3. **Legacy path** (`/home/skogix/skogai`)

## Getting Started

### 1. Create the Issues

Run the issue creation script:
```bash
./create-migration-issues.sh
```

This creates 10 focused issues covering all migration work.

### 2. Start with Foundation

Begin with the **Configuration System Foundation** issue. All other work depends on this.

### 3. Migrate Systematically

Work through issues in order, or parallelize after the foundation is complete:
- Core components (agents, apps) can be done in parallel
- Tools and workflows can be done in parallel
- Services and integrations can be done in parallel

### 4. Validate Continuously

Run validation tools after each migration:
```bash
# Check Python files
python tools/check_hardcoded_paths.py path/to/file.py

# Check Shell scripts
bash tools/check_hardcoded_paths.sh path/to/script.sh
```

### 5. Complete with Testing

Finish with comprehensive testing (Final Validation issue) to ensure everything works.

## Timeline

**Conservative Estimate:** 6 weeks
**Aggressive Estimate:** 3-4 weeks (with parallel work)

The timeline depends on:
- Availability of developers
- Complexity discovered during migration
- Testing thoroughness
- Documentation quality requirements

## Notes

- Migration can be done incrementally (files work with or without configuration system)
- Backward compatibility is maintained throughout
- Pre-commit hooks prevent regression
- Documentation is created alongside code changes

## Issues Created

Run `./create-migration-issues.sh` to create:

1. **Configuration System Foundation** (prerequisite)
2. **Migrate Core Agent Files**
3. **Migrate Demo and Workflow Scripts**
4. **Migrate Tool Scripts**
5. **Migrate Service and System Files**
6. **Migrate Main Applications**
7. **Migrate OpenRouter Scripts**
8. **Migrate Metrics and Utilities**
9. **Create Migration Guide and Documentation**
10. **Final Validation and Testing**

Each issue contains:
- Specific files to migrate
- Migration patterns (before/after examples)
- Testing requirements
- Acceptance criteria
- Dependencies
