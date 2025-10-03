#!/bin/bash
#
# Create GitHub issues for configuration system migration
# This script creates a series of focused issues to systematically migrate
# hardcoded paths to a centralized configuration system.
#

set -e

REPO="SkogAI/lore"

echo "Creating migration issues for repository: $REPO"
echo "================================================"
echo ""

# Issue 1: Configuration System Foundation
echo "Creating issue: Configuration System Foundation..."
gh issue create --repo "$REPO" --title "Create centralized configuration system for path resolution" --body "$(cat <<'EOF'
### Overview

Before migrating files to use a configuration system, we need to create the centralized configuration infrastructure that will replace hardcoded paths throughout the codebase.

### Context

Issue #5 identified 509 files with hardcoded `/home/skogix/skogai` paths. This issue creates the foundation for systematic migration.

### Tasks

#### Python Configuration System

- [ ] Create `config/paths.py` with path resolution utilities
  - [ ] Support environment variables (`SKOGAI_BASE_DIR`, `SKOGAI_AGENTS_DIR`, etc.)
  - [ ] Git-aware defaults (auto-detect repository root)
  - [ ] Backward compatibility (fallback to `/home/skogix/skogai`)
  - [ ] Type-safe API with `pathlib.Path`
- [ ] Implement standard path getters:
  - [ ] `get_config_file(filename)` - Config files
  - [ ] `get_demo_output_dir(session_id, agent_type)` - Demo outputs
  - [ ] `get_context_dir()` - Context files
  - [ ] `get_agents_dir()` - Agent implementations
  - [ ] `get_knowledge_dir()` - Knowledge base
- [ ] Add `ensure_dir(path)` utility for directory creation

#### Shell Configuration System

- [ ] Create `config/paths.sh` shell library
  - [ ] Implement path resolution with env var support
  - [ ] Provide functions matching Python API
  - [ ] Git repository detection
  - [ ] Source-able library (not executable)

#### Documentation

- [ ] Create `config/README.md` with:
  - [ ] Complete API documentation
  - [ ] Usage examples (Python and Shell)
  - [ ] Environment variable reference
  - [ ] Migration patterns

#### Validation Tools

- [ ] Create `tools/check_hardcoded_paths.py` for Python files
- [ ] Create `tools/check_hardcoded_paths.sh` for shell scripts
- [ ] Configure `.pre-commit-config.yaml` to prevent new hardcoded paths

### Acceptance Criteria

- [ ] Configuration system supports both Python and Shell
- [ ] Environment variables take precedence over defaults
- [ ] Git-aware path resolution works correctly
- [ ] Backward compatibility maintained
- [ ] Pre-commit hooks prevent new hardcoded paths
- [ ] Comprehensive documentation with examples

### Related Issues

Part of the path resolution standardization effort (Issue #5)
EOF
)"

echo "✓ Created configuration system foundation issue"
echo ""

# Issue 2: Migrate Core Agent Files
echo "Creating issue: Migrate Core Agent Files..."
gh issue create --repo "$REPO" --title "Migrate core agent files to use configuration system" --body "$(cat <<'EOF'
### Overview

Migrate core agent implementation files to use the centralized configuration system instead of hardcoded paths.

### Prerequisites

- Configuration system must be implemented first (see related issue)
- `config/paths.py` and `config/paths.sh` must exist

### Files to Migrate

#### Python Files (Priority Order)

1. **Agent API** (`agents/api/agent_api.py`)
   - Lines: `config_path: str = "/home/skogix/skogai/config/llm_config.json"`
   - Replace with: `config_path: str = paths.get_config_file("llm_config.json")`

2. **Agent Implementations** (`agents/implementations/small_model_agents.py`)
   - Check for any hardcoded paths in agent initialization
   - Update to use configuration system

3. **Lore API** (`agents/api/lore_api.py`)
   - Audit and migrate any path references

### Migration Pattern

```python
# Before
config_path = "/home/skogix/skogai/config/llm_config.json"
output_dir = f"/home/skogix/skogai/demo/output_{timestamp}"

# After
from config import paths

config_path = paths.get_config_file("llm_config.json")
output_dir = paths.get_demo_output_dir(session_id, "agent_type")
paths.ensure_dir(output_dir)
```

### Testing

- [ ] Verify agents initialize correctly with configuration system
- [ ] Test with environment variables set
- [ ] Test with defaults (no env vars)
- [ ] Verify backward compatibility

### Acceptance Criteria

- [ ] All agent files use configuration system
- [ ] No hardcoded `/home/skogix/skogai` paths remain in agent files
- [ ] Tests pass with both environment variables and defaults
- [ ] Documentation updated if API changes

### Related Issues

- Depends on: Configuration System Foundation issue
- Part of: Issue #5 path resolution standardization
EOF
)"

echo "✓ Created agent migration issue"
echo ""

# Issue 3: Migrate Demo and Workflow Scripts
echo "Creating issue: Migrate Demo and Workflow Scripts..."
gh issue create --repo "$REPO" --title "Migrate demo and workflow scripts to use configuration system" --body "$(cat <<'EOF'
### Overview

Migrate demo scripts and workflow files to use the centralized configuration system instead of hardcoded paths.

### Prerequisites

- Configuration system must be implemented first
- Core agent files should be migrated first (recommended)

### Files to Migrate

#### Python Demo Files

1. **Small Model Workflow** (`demo/small_model_workflow.py`)
   - Line 11: `sys.path.append("/mnt/extra/backup/skogai-old-all/")`
   - Line 33: `output_dir = f"/home/skogix/skogai/demo/small_model_content_{timestamp}"`
   - Replace with configuration system calls

2. **Chat UI Demo** (`demo/chat_ui_demo.py`)
   - Audit for hardcoded paths
   - Migrate to configuration system

3. **Lore Demo** (`demo/lore_demo.py`)
   - Audit for hardcoded paths
   - Migrate to configuration system

4. **Issue Creator Demo** (`demo/issue_creator_demo.py`)
   - Audit for hardcoded paths
   - Migrate to configuration system

#### Shell Workflow Scripts

1. **Content Workflow** (`demo/content-workflow.sh`)
2. **Orchestrator Flow** (`integration/orchestrator-flow.sh`)
3. **Test Workflow** (`integration/workflows/test-workflow.sh`)

### Migration Pattern

**Python:**
```python
# Before
output_dir = f"/home/skogix/skogai/demo/output_{timestamp}"
sys.path.append("/home/skogix/skogai")

# After
from config import paths

output_dir = paths.get_demo_output_dir(session_id, "demo_type")
# sys.path configuration should use paths.get_base_dir()
```

**Shell:**
```bash
# Before
OUTPUT_DIR="/home/skogix/skogai/demo/output"

# After
source "$(dirname "$0")/../config/paths.sh"
OUTPUT_DIR=$(get_demo_output_dir "$session_id" "demo_type")
ensure_dir "$OUTPUT_DIR"
```

### Testing

- [ ] Run each demo script with environment variables
- [ ] Run each demo script with defaults
- [ ] Verify output directories created correctly
- [ ] Check workflow execution end-to-end

### Acceptance Criteria

- [ ] All demo and workflow scripts use configuration system
- [ ] No hardcoded paths remain in demo/workflow files
- [ ] Scripts work with both custom and default configurations
- [ ] Demo documentation updated if needed

### Related Issues

- Depends on: Configuration System Foundation issue
- Part of: Issue #5 path resolution standardization
EOF
)"

echo "✓ Created demo/workflow migration issue"
echo ""

# Issue 4: Migrate Tool Scripts
echo "Creating issue: Migrate Tool Scripts..."
gh issue create --repo "$REPO" --title "Migrate tool scripts to use configuration system" --body "$(cat <<'EOF'
### Overview

Migrate tool scripts (both Python and Shell) to use the centralized configuration system instead of hardcoded paths.

### Prerequisites

- Configuration system must be implemented first

### Files to Migrate

#### Shell Scripts (Priority Order)

1. **Context Manager** (`tools/context-manager.sh`)
   - Lines 10, 13-16, 24-25, 38, 42: Multiple `/home/skogix/skogai/context/` references
   - Replace with sourced configuration functions

2. **Index Knowledge** (`tools/index-knowledge.sh`)
   - Audit for hardcoded paths
   - Migrate to configuration system

3. **Setup Lore Service** (`tools/setup-lore-service.sh`)
   - Service installation paths
   - Migrate to configuration system

4. **Other Tool Scripts:**
   - `tools/create-persona.sh`
   - `tools/llama-lore-integrator.sh`
   - `tools/llama-lore-creator.sh`
   - `tools/create-issue.sh`
   - `tools/setup-gitflow-worktree.sh`
   - `tools/manage-lore.sh`

#### Python Scripts

1. **Issue Creator** (`tools/issue-creator.py`)
   - Audit for hardcoded paths
   - Migrate to configuration system

### Migration Pattern

**Shell Scripts:**
```bash
# Before
CONTEXT_DIR="/home/skogix/skogai/context"
TEMPLATE_PATH="/home/skogix/skogai/context/templates/${template}-context.json"

# After
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../config/paths.sh"

CONTEXT_DIR=$(get_context_dir)
TEMPLATE_PATH="$CONTEXT_DIR/templates/${template}-context.json"
```

**Python Scripts:**
```python
# Before
context_dir = "/home/skogix/skogai/context"

# After
from config import paths
context_dir = paths.get_context_dir()
```

### Testing

- [ ] Test each tool with environment variables
- [ ] Test each tool with defaults
- [ ] Verify backward compatibility
- [ ] Check error handling for missing directories

### Acceptance Criteria

- [ ] All tool scripts use configuration system
- [ ] No hardcoded paths remain in tools/
- [ ] Tools work with both custom and default configurations
- [ ] Error messages are informative
- [ ] Tool documentation updated if needed

### Related Issues

- Depends on: Configuration System Foundation issue
- Part of: Issue #5 path resolution standardization
EOF
)"

echo "✓ Created tool scripts migration issue"
echo ""

# Issue 5: Migrate Service and System Files
echo "Creating issue: Migrate Service and System Files..."
gh issue create --repo "$REPO" --title "Migrate service and system configuration files" --body "$(cat <<'EOF'
### Overview

Migrate service management scripts and system configuration files to use the centralized configuration system.

### Prerequisites

- Configuration system must be implemented first

### Files to Migrate

#### Service Scripts

1. **Agent Service** (`skogai-agent-small-service.sh`)
   - Hardcoded paths for service management
   - Update to use configuration system

2. **Lore Service** (`skogai-lore-service.sh`)
   - Hardcoded paths for service management
   - Update to use configuration system

3. **Setup Script** (`setup-skogai-agent-small.sh`)
   - Installation paths
   - Update to use configuration system

4. **Client Script** (`skogai-agent-small-client.sh`)
   - Hardcoded paths
   - Update to use configuration system

#### System Configuration Files

1. **Systemd Service Files:**
   - `skogai-agent-small.service`
   - `skogai-lore-service.service`
   - Note: These may need environment variable references instead

2. **Desktop File:**
   - `skogai-chat.desktop`
   - Update Exec and Path directives

### Migration Considerations

**For Systemd Services:**
- Use `Environment=` directives to set base paths
- Reference environment variables in `ExecStart=`
- Document required environment setup

**For Desktop Files:**
- May need wrapper script if direct env var use isn't supported
- Document setup requirements

### Migration Pattern

**Service Scripts:**
```bash
# Before
INSTALL_DIR="/home/skogix/skogai"
SERVICE_SCRIPT="$INSTALL_DIR/skogai-agent-small-service.sh"

# After
source "$(dirname "$0")/config/paths.sh"
INSTALL_DIR=$(get_base_dir)
SERVICE_SCRIPT="$INSTALL_DIR/skogai-agent-small-service.sh"
```

**Systemd Service:**
```ini
[Service]
Environment="SKOGAI_BASE_DIR=/home/skogix/skogai"
ExecStart=/bin/bash -c "source $SKOGAI_BASE_DIR/config/paths.sh && ..."
```

### Testing

- [ ] Test service installation with custom base directory
- [ ] Test service startup and shutdown
- [ ] Verify desktop launcher works
- [ ] Test with environment variables
- [ ] Verify backward compatibility

### Acceptance Criteria

- [ ] All service scripts use configuration system
- [ ] Systemd services documented with environment setup
- [ ] Desktop file works with configuration system
- [ ] Installation documentation updated
- [ ] Service management works with custom paths

### Related Issues

- Depends on: Configuration System Foundation issue
- Part of: Issue #5 path resolution standardization
EOF
)"

echo "✓ Created service/system migration issue"
echo ""

# Issue 6: Migrate Main Applications
echo "Creating issue: Migrate Main Applications..."
gh issue create --repo "$REPO" --title "Migrate main application files to use configuration system" --body "$(cat <<'EOF'
### Overview

Migrate the main application entry points and UI files to use the centralized configuration system.

### Prerequisites

- Configuration system must be implemented first
- Agent files should be migrated first (recommended)

### Files to Migrate

#### Main Applications

1. **Streamlit Chat** (`streamlit_chat.py`)
   - Audit for hardcoded paths
   - Migrate to configuration system
   - Test UI functionality after migration

2. **Skogai Chat** (`skogai-chat.py`)
   - Audit for hardcoded paths
   - Migrate to configuration system
   - Test chat functionality

3. **Main Entry Point** (`main.py`)
   - Audit for hardcoded paths
   - Migrate to configuration system

4. **Lore Export** (`st-lore-export.py`)
   - Audit for hardcoded paths
   - Migrate to configuration system

5. **Agent Lore Generator** (`generate-agent-lore.py`)
   - Audit for hardcoded paths
   - Migrate to configuration system

#### Integration Files

1. **Persona Manager** (`integration/persona-bridge/persona-manager.py`)
   - Audit for hardcoded paths
   - Migrate to configuration system

### Migration Pattern

```python
# Before
import sys
sys.path.append("/home/skogix/skogai")
config_file = "/home/skogix/skogai/config/app.json"

# After
from config import paths

# Path should be auto-detected
config_file = paths.get_config_file("app.json")
```

### Testing

- [ ] Test Streamlit UI launches correctly
- [ ] Test chat functionality end-to-end
- [ ] Verify file uploads/downloads work
- [ ] Test with environment variables
- [ ] Test with defaults
- [ ] Verify backward compatibility

### Acceptance Criteria

- [ ] All main applications use configuration system
- [ ] No hardcoded paths in main application files
- [ ] UI applications work with custom configurations
- [ ] User documentation updated
- [ ] Installation guide updated

### Related Issues

- Depends on: Configuration System Foundation issue
- Part of: Issue #5 path resolution standardization
EOF
)"

echo "✓ Created main applications migration issue"
echo ""

# Issue 7: Migrate OpenRouter Scripts
echo "Creating issue: Migrate OpenRouter Scripts..."
gh issue create --repo "$REPO" --title "Migrate OpenRouter integration scripts" --body "$(cat <<'EOF'
### Overview

Migrate OpenRouter API integration scripts to use the centralized configuration system.

### Prerequisites

- Configuration system must be implemented first

### Files to Migrate

#### Python Files

1. **OpenRouter Free** (`openrouter/or-free.py`)
   - Audit for hardcoded paths
   - Migrate to configuration system

2. **OpenRouter Helper** (`openrouter/or_free_helper.py`)
   - Audit for hardcoded paths
   - Migrate to configuration system

#### Shell Scripts

1. **OpenRouter Models (New)** (`openrouter/openrouter-models-new.sh`)
   - Audit for hardcoded paths
   - Migrate to configuration system

2. **OpenRouter Models** (`openrouter/openrouter-models.sh`)
   - Audit for hardcoded paths
   - Migrate to configuration system

3. **OpenRouter Free** (`openrouter/openrouter-free.sh`)
   - Audit for hardcoded paths
   - Migrate to configuration system

### Migration Pattern

**Python:**
```python
# Before
cache_dir = "/home/skogix/skogai/openrouter/cache"

# After
from config import paths
cache_dir = paths.get_cache_dir("openrouter")
paths.ensure_dir(cache_dir)
```

**Shell:**
```bash
# Before
CACHE_DIR="/home/skogix/skogai/openrouter/cache"

# After
source "$(dirname "$0")/../config/paths.sh"
CACHE_DIR=$(get_cache_dir "openrouter")
ensure_dir "$CACHE_DIR"
```

### Testing

- [ ] Test OpenRouter API calls
- [ ] Verify cache directory creation
- [ ] Test with environment variables
- [ ] Test with defaults
- [ ] Verify API key handling

### Acceptance Criteria

- [ ] All OpenRouter scripts use configuration system
- [ ] No hardcoded paths in openrouter/
- [ ] Cache and data directories work with custom paths
- [ ] API integration still functions correctly

### Related Issues

- Depends on: Configuration System Foundation issue
- Part of: Issue #5 path resolution standardization
EOF
)"

echo "✓ Created OpenRouter migration issue"
echo ""

# Issue 8: Migrate Metrics and Utilities
echo "Creating issue: Migrate Metrics and Utilities..."
gh issue create --repo "$REPO" --title "Migrate metrics collection and utility scripts" --body "$(cat <<'EOF'
### Overview

Migrate metrics collection scripts and miscellaneous utility files to use the centralized configuration system.

### Prerequisites

- Configuration system must be implemented first

### Files to Migrate

#### Metrics Scripts

1. **Collect Metrics** (`metrics/collect-metrics.sh`)
   - Audit for hardcoded paths
   - Migrate to configuration system
   - Verify metrics output location

#### Utility Scripts

1. **Create Issues Script** (`create_issues_from_script.py`)
   - Audit for hardcoded paths
   - Migrate to configuration system

2. **Script Refactor Issues** (`create-script-refactor-issues.sh`)
   - Audit for hardcoded paths
   - Migrate to configuration system

#### Documentation Generators

1. **Knowledge Docs Generator** (`docs/generators/knowledge-docs.sh`)
   - Audit for hardcoded paths
   - Migrate to configuration system

### Migration Pattern

**Metrics Scripts:**
```bash
# Before
METRICS_OUTPUT="/home/skogix/skogai/metrics/output"

# After
source "$(dirname "$0")/../config/paths.sh"
METRICS_OUTPUT=$(get_metrics_dir)
ensure_dir "$METRICS_OUTPUT"
```

**Utility Scripts:**
```python
# Before
output_file = "/home/skogix/skogai/tools/output.json"

# After
from config import paths
output_file = paths.get_tools_output_file("output.json")
```

### Testing

- [ ] Test metrics collection
- [ ] Verify metrics output saved correctly
- [ ] Test utility scripts
- [ ] Verify documentation generation
- [ ] Test with environment variables

### Acceptance Criteria

- [ ] All metrics and utility scripts use configuration system
- [ ] No hardcoded paths remain
- [ ] Output directories work with custom paths
- [ ] Scripts function correctly with configuration system

### Related Issues

- Depends on: Configuration System Foundation issue
- Part of: Issue #5 path resolution standardization
EOF
)"

echo "✓ Created metrics/utilities migration issue"
echo ""

# Issue 9: Update Documentation and Create Migration Guide
echo "Creating issue: Update Documentation and Create Migration Guide..."
gh issue create --repo "$REPO" --title "Create migration guide and update documentation" --label "documentation" --body "$(cat <<'EOF'
### Overview

Create comprehensive documentation for the configuration system migration, including a migration guide and updated installation instructions.

### Prerequisites

- Configuration system should be implemented
- At least one category of files should be migrated (for examples)

### Documentation to Create

#### 1. Migration Guide (`MIGRATION_GUIDE.md`)

- [ ] **Overview** - Why we're migrating, benefits
- [ ] **Configuration System** - How it works
- [ ] **Environment Variables** - Complete reference
- [ ] **Migration Patterns** - Common before/after examples
  - [ ] Python file migration
  - [ ] Shell script migration
  - [ ] Service file migration
- [ ] **Step-by-Step Guide** - How to migrate a file
- [ ] **Testing Procedures** - How to verify migration
- [ ] **Troubleshooting** - Common issues and solutions
- [ ] **Migration Status** - Inventory of remaining work

#### 2. Configuration README (`config/README.md`)

- [ ] **Quick Start** - Minimal example
- [ ] **API Reference** - All functions/methods
  - [ ] Python API
  - [ ] Shell API
- [ ] **Usage Examples** - Real-world scenarios
- [ ] **Environment Variables** - Complete list with defaults
- [ ] **Path Resolution** - How paths are determined
- [ ] **Best Practices** - Dos and don'ts

#### 3. Update Existing Documentation

- [ ] **README.md** - Update setup instructions
- [ ] **CLAUDE.md** - Add configuration system notes
- [ ] **Installation Guides** - Update for new configuration
- [ ] **Developer Docs** - Add configuration guidelines

#### 4. Create Examples

- [ ] Example Python script using configuration
- [ ] Example Shell script using configuration
- [ ] Example service setup with environment variables
- [ ] Example `.envrc` file for direnv users

### Documentation Standards

- Use clear, concise language
- Include copy-paste ready examples
- Show both Python and Shell for each pattern
- Include expected output/results
- Add troubleshooting for common issues
- Keep migration status up-to-date

### Acceptance Criteria

- [ ] Migration guide is comprehensive and clear
- [ ] Configuration README has complete API reference
- [ ] Examples are tested and work correctly
- [ ] Existing docs updated for configuration system
- [ ] Migration status tracking is in place

### Related Issues

- Part of: Issue #5 path resolution standardization
- Supports: All migration issues
EOF
)"

echo "✓ Created documentation issue"
echo ""

# Issue 10: Final Validation and Testing
echo "Creating issue: Final Validation and Testing..."
gh issue create --repo "$REPO" --title "Final validation and comprehensive testing of configuration system" --label "testing" --body "$(cat <<'EOF'
### Overview

Perform comprehensive validation and testing after all files have been migrated to the configuration system.

### Prerequisites

- Configuration system implemented
- All migration issues completed
- Documentation completed

### Validation Tasks

#### 1. Automated Validation

- [ ] Run `tools/check_hardcoded_paths.py` on all Python files
  - [ ] Verify zero hardcoded paths found
  - [ ] Review any exceptions/allowlisted paths
- [ ] Run `tools/check_hardcoded_paths.sh` on all shell scripts
  - [ ] Verify zero hardcoded paths found
  - [ ] Review any exceptions
- [ ] Pre-commit hooks installed and tested
  - [ ] Verify hooks prevent new hardcoded paths
  - [ ] Test hook performance

#### 2. Functional Testing

- [ ] **Agent Functionality**
  - [ ] Test all agents with default configuration
  - [ ] Test all agents with custom configuration
  - [ ] Verify agent outputs and behavior
- [ ] **Demo Scripts**
  - [ ] Run each demo with defaults
  - [ ] Run each demo with environment variables
  - [ ] Verify outputs saved correctly
- [ ] **Service Management**
  - [ ] Install services with custom paths
  - [ ] Start/stop/restart services
  - [ ] Verify service logs
- [ ] **UI Applications**
  - [ ] Launch Streamlit chat
  - [ ] Test chat functionality
  - [ ] Verify file operations
- [ ] **Tool Scripts**
  - [ ] Test context manager
  - [ ] Test knowledge indexer
  - [ ] Test other tools

#### 3. Environment Testing

Test with different configurations:

- [ ] **Default Configuration** (no env vars)
  - [ ] All features work
  - [ ] Paths resolve correctly
- [ ] **Custom Base Directory**
  - [ ] Set `SKOGAI_BASE_DIR`
  - [ ] Verify all paths resolve relative to custom base
- [ ] **Individual Path Overrides**
  - [ ] Test `SKOGAI_CONFIG_DIR`
  - [ ] Test `SKOGAI_AGENTS_DIR`
  - [ ] Test `SKOGAI_DEMO_DIR`
  - [ ] Test other environment variables
- [ ] **Git Repository Detection**
  - [ ] Verify auto-detection works
  - [ ] Test outside git repository

#### 4. Backward Compatibility

- [ ] Test on system with existing `/home/skogix/skogai` installation
- [ ] Verify fallback behavior works
- [ ] Test migration from old to new system

#### 5. Performance Testing

- [ ] Measure configuration system overhead
- [ ] Verify no significant performance impact
- [ ] Profile path resolution functions

### Documentation Review

- [ ] All documentation accurate
- [ ] Examples tested and work
- [ ] Migration guide complete
- [ ] API reference complete

### Acceptance Criteria

- [ ] **Zero** hardcoded paths in Python files (except documentation/examples)
- [ ] **Zero** hardcoded paths in Shell scripts (except documentation/examples)
- [ ] All functional tests pass
- [ ] All environment configurations work
- [ ] Backward compatibility verified
- [ ] Pre-commit hooks working
- [ ] Performance acceptable
- [ ] Documentation complete and accurate

### Final Checklist

- [ ] Configuration system implemented ✓
- [ ] All files migrated ✓
- [ ] Documentation complete ✓
- [ ] Automated validation passing ✓
- [ ] Functional tests passing ✓
- [ ] Environment tests passing ✓
- [ ] Backward compatibility verified ✓
- [ ] Performance acceptable ✓
- [ ] Ready for production use ✓

### Related Issues

- Depends on: All migration issues
- Closes: Issue #5
EOF
)"

echo "✓ Created validation/testing issue"
echo ""

echo "================================================"
echo "Successfully created all migration issues!"
echo ""
echo "Issue creation order:"
echo "1. Configuration System Foundation (prerequisite for all others)"
echo "2. Migrate Core Agent Files"
echo "3. Migrate Demo and Workflow Scripts"
echo "4. Migrate Tool Scripts"
echo "5. Migrate Service and System Files"
echo "6. Migrate Main Applications"
echo "7. Migrate OpenRouter Scripts"
echo "8. Migrate Metrics and Utilities"
echo "9. Create Migration Guide and Documentation"
echo "10. Final Validation and Testing"
echo ""
echo "Recommended workflow:"
echo "- Start with issue #1 (Configuration System Foundation)"
echo "- Work through issues #2-#8 (can be done in parallel after #1)"
echo "- Complete issue #9 (Documentation) alongside migrations"
echo "- Finish with issue #10 (Validation) to verify everything"
