# How to Create Configuration System Migration Issues

This document explains how to create the 16 GitHub issues for migrating to the configuration system implemented in issue #5.

## Background

Issue #5 implemented a comprehensive configuration system to replace hardcoded paths throughout the codebase. The system provides:
- Python API: `from config import paths`
- Shell API: `source config/paths.sh`
- Environment variable support (`SKOGAI_BASE_DIR`, `SKOGAI_AGENTS_DIR`, etc.)
- Git-aware path resolution
- Backward compatibility

However, 87+ Python files and 15+ shell scripts still need migration to use this new system.

## The 16 Issues

### Shell Script Migrations (11 issues)
1. **Refactor tools/context-manager.sh to use jq instead of sed**
2. **Refactor tools/index-knowledge.sh to use jq instead of sed**
3. **Refactor tools/llama-lore-creator.sh to use jq instead of sed**
4. **Refactor tools/llama-lore-integrator.sh to eliminate sed/awk usage**
5. **Refactor docs/generators/knowledge-docs.sh to use jq and SKOGAI_* vars**
6. **Refactor metrics/collect-metrics.sh to use SKOGAI_* environment variables**
7. **Refactor openrouter/openrouter-models-new.sh to use SKOGAI_* environment variables**
8. **Refactor integration/orchestrator-flow.sh to use SKOGAI_* environment variables**
9. **Refactor integration/workflows/test-workflow.sh to use SKOGAI_* environment variables**
10. **Refactor demo/content-workflow.sh to use SKOGAI_* environment variables**
15. **Migrate skogai-agent-small-service.sh to use SKOGAI_* environment variables**

### Python File Migrations (4 issues)
11. **Migrate agents/api/agent_api.py to use configuration system**
12. **Migrate agents/api/lore_api.py to use configuration system**
13. **Migrate agents/implementations/small_model_agents.py to use configuration system**
14. **Migrate demo/small_model_workflow.py to use configuration system**

### Master Tracking Issue
16. **Configuration System Migration - Master Tracking Issue** (Epic/Tracking)

All issues reference #5 (the configuration system implementation).

## Option 1: Use the Automated Scripts (Recommended)

If you have GitHub CLI (`gh`) configured with authentication:

### Using the Shell Script
```bash
# Make sure you have gh CLI installed and authenticated
gh auth status

# Run the script to create all issues
cd issues_to_create
./create_all_issues.sh
```

### Using the Python Script
```bash
# Make sure you have gh CLI installed and authenticated
gh auth status

# Run the Python script
cd issues_to_create
python3 create_issues.py
```

Both scripts will:
- Create all 16 issues in the correct order
- Apply appropriate labels
- Provide a summary of created issues
- Add rate limiting to avoid API throttling

## Option 2: Run via GitHub Actions Workflow

Create a workflow file `.github/workflows/create-issues.yml`:

```yaml
name: Create Refactoring Issues

on:
  workflow_dispatch:  # Manual trigger only

jobs:
  create-issues:
    runs-on: ubuntu-latest
    permissions:
      issues: write
      contents: read
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Create Issues
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          chmod +x create-script-refactor-issues.sh
          ./create-script-refactor-issues.sh
```

Then trigger it manually from the Actions tab.

## Option 3: Create Individual Issues

Use the individual markdown files to create issues one at a time:

```bash
cd issues_to_create

# Create a single issue
gh issue create \
  --repo SkogAI/lore \
  --title "$(grep -A 1 '^## Title' issue_01.md | tail -1)" \
  --body "$(sed -n '/^## Body/,$ p' issue_01.md | tail -n +2)" \
  --label "refactoring,configuration-system,migration"
```

## Option 4: Manual Creation via Web Interface

The `issues_to_create/` directory contains individual markdown files for each issue:

- `issue_01.md` through `issue_16.md` 
- `README.md` with summary

You can:
1. Review each file
2. Manually create issues on GitHub using the web interface
3. Copy/paste the title from the "## Title" section
4. Copy/paste the body from the "## Body" section
5. Add labels: `refactoring`, `configuration-system`, `migration`
6. For issue #16, also add: `tracking`, `epic`

## Option 5: GitHub API with curl

For automation without `gh` CLI:

```bash
# Set your GitHub token
GITHUB_TOKEN="your_token_here"
REPO="SkogAI/lore"

# Example for issue 1 (repeat for all 10)
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/$REPO/issues" \
  -d @- << 'EOF'
{
  "title": "Refactor tools/context-manager.sh to use jq instead of sed",
  "body": "See issues_to_create/issue_01.md for full content",
  "labels": ["refactoring", "shell-scripts"]
}
EOF
```

## Verification

After creating the issues, verify:

```bash
# List recent issues
gh issue list --repo SkogAI/lore --limit 15

# Or check the web interface
open "https://github.com/SkogAI/lore/issues"
```

## Files in This Repository

- `issues_to_create/create_all_issues.sh` - Shell script to create all issues (recommended)
- `issues_to_create/create_issues.py` - Python script to create all issues (alternative)
- `issues_to_create/issue_01.md` through `issue_16.md` - Individual issue markdown files
- `issues_to_create/README.md` - Summary of all issues
- `HOW_TO_CREATE_ISSUES.md` - This file

## Notes

- All issues are related to issue #5 (configuration system implementation)
- Issue #16 is a master tracking issue that references all other issues
- Issues include detailed requirements, examples, and testing instructions
- Labels suggested: `refactoring`, `configuration-system`, `migration`
- For issue #16, add additional labels: `tracking`, `epic`
- Priority: These are technical debt/improvement issues that enable better deployment flexibility

## Related Documentation

- Issue #5 - Configuration system implementation (completed)
- `config/README.md` - Configuration system API documentation (if merged from #5)
- `MIGRATION_GUIDE.md` - Step-by-step migration guide (if merged from #5)
- `lorefiles/mnt_extra_20250730-skogai-main_.claude/skogai-environment-variables.md` - SKOGAI_* environment variable documentation
- `lorefiles/mnt_extra_20250726_agents_.claude/knowledge/code-style-rules.md` - Shell script coding standards

## Benefits of Migration

- **Flexibility**: Deploy anywhere without hardcoded paths
- **Compatibility**: Works with different user accounts and deployment scenarios
- **Maintainability**: Centralized path management
- **Testing**: Easier to test with different configurations
- **CI/CD**: Better support for automated testing and deployment

## Validation

After migration, validate changes using:
```bash
# Check Python files for hardcoded paths
python tools/check_hardcoded_paths.py $(find . -name "*.py" -not -path "./lorefiles/*")

# Check shell scripts for hardcoded paths
bash tools/check_hardcoded_paths.sh

# Install pre-commit hooks to prevent new hardcoded paths
pip install pre-commit
pre-commit install
```
