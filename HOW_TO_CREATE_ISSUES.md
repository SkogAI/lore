# How to Create the Shell Script Refactoring Issues

This document explains how to create the 10 GitHub issues defined in `create-script-refactor-issues.sh`.

## Background

Claude created a comprehensive shell script (`create-script-refactor-issues.sh`) that defines 10 issues for refactoring shell scripts in the SkogAI/lore repository. These issues focus on:

1. Eliminating `sed` and `awk` usage in favor of `jq` and other modern tools
2. Replacing hardcoded paths with `SKOGAI_*` environment variables
3. Improving script robustness and maintainability

## The 10 Issues

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

All issues reference #41 (the parent issue about shell script refactoring).

## Option 1: Run the Script Directly (Recommended)

If you have GitHub CLI (`gh`) configured with authentication:

```bash
# Make sure you have gh CLI installed and authenticated
gh auth status

# Set the GH_TOKEN environment variable (if not already set)
export GH_TOKEN=$(gh auth token)

# Run the script
./create-script-refactor-issues.sh
```

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

## Option 3: Use the Python Helper Script

The `create_issues_from_script.py` script extracts issue data from the shell script:

```bash
# Run the Python script (will attempt gh CLI and save to files)
python3 create_issues_from_script.py
```

This will:
- Parse the shell script to extract all 10 issues
- Attempt to create them via `gh` CLI
- Save each issue as a markdown file in `issues_to_create/` directory
- Create a summary README

## Option 4: Use Individual Markdown Files

The `issues_to_create/` directory contains individual markdown files for each issue:

- `issue_01.md` through `issue_10.md` 
- `README.md` with summary

You can:
1. Review each file
2. Manually create issues on GitHub using the web interface
3. Copy/paste the title and body from each file

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

- `create-script-refactor-issues.sh` - Original shell script by Claude (executable)
- `create_issues_from_script.py` - Python helper to parse and create issues
- `issues_to_create/` - Directory with individual markdown files for each issue
- `issues_to_create/README.md` - Summary of all issues
- `HOW_TO_CREATE_ISSUES.md` - This file

## Notes

- All issues are related to issue #41 (shell script refactoring)
- Issues include detailed requirements, examples, and testing instructions
- Labels suggested: `refactoring`, `shell-scripts`, `environment-variables`
- Priority: These are technical debt/improvement issues

## Related Documentation

- `lorefiles/mnt_extra_20250730-skogai-main_.claude/skogai-environment-variables.md` - SKOGAI_* environment variable documentation
- `lorefiles/mnt_extra_20250726_agents_.claude/knowledge/code-style-rules.md` - Shell script coding standards

## Contact

For questions about these issues, see the original context in `output.txt` which contains Claude's analysis and reasoning for creating each issue.
