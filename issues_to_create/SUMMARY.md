# Configuration System Migration - Follow-up Issues Summary

## Overview

This document summarizes the follow-up issues created to continue the configuration system migration work started in issue #5.

## Background

Issue #5 implemented a comprehensive configuration system to replace hardcoded `/home/skogix/skogai/` paths throughout the codebase. The system provides:
- Python API: `from config import paths`
- Shell API: `source config/paths.sh`
- Environment variable support
- Git-aware path resolution
- Backward compatibility

However, the work noted that **87+ Python files and 15+ shell scripts still need migration** to use this new system.

## Follow-up Issues Created

### Master Tracking Issue (1 issue)
- **Issue #16**: Configuration System Migration - Master Tracking Issue
  - Epic/tracking issue that references all migration issues
  - Provides overview of benefits, progress tracking, and validation steps

### Shell Script Migrations (11 issues)
Issues #1-10 and #15 focus on migrating shell scripts:

1. **tools/context-manager.sh** - Replace sed with jq, add SKOGAI_* vars
2. **tools/index-knowledge.sh** - Replace sed with jq, add SKOGAI_* vars
3. **tools/llama-lore-creator.sh** - Replace sed with jq, add SKOGAI_* vars
4. **tools/llama-lore-integrator.sh** - Eliminate sed/awk usage
5. **docs/generators/knowledge-docs.sh** - Use jq and SKOGAI_* vars
6. **metrics/collect-metrics.sh** - Use SKOGAI_* vars
7. **openrouter/openrouter-models-new.sh** - Use SKOGAI_* vars
8. **integration/orchestrator-flow.sh** - Use SKOGAI_* vars
9. **integration/workflows/test-workflow.sh** - Use SKOGAI_* vars
10. **demo/content-workflow.sh** - Use SKOGAI_* vars
15. **skogai-agent-small-service.sh** - Use SKOGAI_* vars

### Python File Migrations (4 issues)
Issues #11-14 focus on migrating Python files:

11. **agents/api/agent_api.py** - 4 hardcoded paths to migrate
12. **agents/api/lore_api.py** - 2 hardcoded paths to migrate
13. **agents/implementations/small_model_agents.py** - 1 hardcoded path to migrate
14. **demo/small_model_workflow.py** - 1 hardcoded path to migrate

## Issue Structure

Each issue includes:
- **Description**: What needs to be changed and why
- **Current Issues**: Specific hardcoded paths and their locations (with line numbers)
- **Requirements**: What the migrated code should do
- **Example Transformation**: Before/after code examples
- **Environment Variables to Use**: Specific SKOGAI_* variables for the file
- **Testing**: How to verify the migration works correctly
- **Related Issue**: Links back to #5 (configuration system implementation)

## How to Create These Issues

Three options are provided:

### Option 1: Automated Scripts (Recommended)
Use either the shell script or Python script to create all issues automatically:
```bash
cd issues_to_create
./create_all_issues.sh
# OR
python3 create_issues.py
```

### Option 2: Individual Issue Creation
Create issues one at a time using gh CLI:
```bash
gh issue create --repo SkogAI/lore --title "..." --body-file issue_11.md
```

### Option 3: Manual Web Interface
Copy/paste title and body from each markdown file into GitHub's issue creation form.

## Files Created

- `issue_11.md` through `issue_16.md` - New issue definitions
- `create_all_issues.sh` - Shell script to create all issues
- `create_issues.py` - Python script to create all issues
- `README.md` - Updated to include new issues
- `SUMMARY.md` - This file
- `HOW_TO_CREATE_ISSUES.md` - Updated with new instructions

## Migration Benefits

- **Flexibility**: Deploy anywhere without hardcoded paths
- **Compatibility**: Works with different user accounts
- **Maintainability**: Centralized path management
- **Testing**: Easier to test with different configurations
- **CI/CD**: Better automated testing and deployment

## Next Steps

1. **Create the issues** using one of the provided methods
2. **Review issue #16** (master tracking issue) to understand the full scope
3. **Begin migration** following the patterns in each issue
4. **Validate changes** using the provided validation tools
5. **Update issue #16** to track progress as issues are completed

## Validation Tools

After migration, use these tools to verify no hardcoded paths remain:
```bash
# Check Python files
python tools/check_hardcoded_paths.py $(find . -name "*.py" -not -path "./lorefiles/*")

# Check shell scripts
bash tools/check_hardcoded_paths.sh

# Install pre-commit hooks
pip install pre-commit
pre-commit install
```

## Related Documentation

- Issue #5 - Configuration system implementation
- `config/README.md` - Configuration API documentation (from #5)
- `MIGRATION_GUIDE.md` - Migration guide (from #5)
- Environment variable docs in lorefiles

## Labels to Apply

When creating issues, use these labels:
- All issues: `refactoring`, `configuration-system`, `migration`
- Issue #16 only: Also add `tracking`, `epic`

## Statistics

- **Total issues**: 16 (1 tracking + 11 shell + 4 Python)
- **Shell scripts to migrate**: 11 files
- **Python files to migrate**: 4 files (core files with hardcoded paths identified)
- **Additional files**: Many more files may be discovered during migration
- **Related to**: Issue #5 (Configuration system implementation)

## Impact

This migration will make the SkogAI lore repository much more flexible and easier to deploy in various environments, including:
- Different user accounts (not just `/home/skogix/`)
- CI/CD environments
- Docker containers
- Different file system layouts
- Team development environments
