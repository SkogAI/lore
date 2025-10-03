# Quick Start: Creating Configuration System Migration Issues

## TL;DR

To create all 16 follow-up issues for the configuration system migration:

```bash
cd issues_to_create
./create_all_issues.sh
```

Or use the Python version:
```bash
cd issues_to_create
python3 create_issues.py
```

## Prerequisites

1. **GitHub CLI installed**: `gh --version`
2. **Authenticated**: `gh auth status`
3. **Correct repository**: You're in the SkogAI/lore repository

If not authenticated:
```bash
gh auth login
```

## What Gets Created

Running either script will create **16 GitHub issues**:

### Master Tracking Issue (1)
- Issue #16: Configuration System Migration - Master Tracking Issue
  - Labels: `refactoring`, `configuration-system`, `tracking`, `epic`

### Shell Script Migrations (11)
- Issues #1-10, #15: Migrate shell scripts to use SKOGAI_* environment variables
  - Labels: `refactoring`, `configuration-system`, `migration`

### Python File Migrations (4)
- Issues #11-14: Migrate Python files to use configuration system
  - Labels: `refactoring`, `configuration-system`, `migration`

## Script Features

Both scripts:
- ✅ Create all 16 issues automatically
- ✅ Apply appropriate labels
- ✅ Include rate limiting to avoid API throttling
- ✅ Provide a summary of created issues
- ✅ Report any errors

## After Creation

1. **View issues**: https://github.com/SkogAI/lore/issues
2. **Check issue #16**: The master tracking issue for overall progress
3. **Start migration**: Follow the patterns in each issue
4. **Update progress**: Check off items in issue #16 as work completes

## Manual Alternative

If you prefer to create issues manually:

1. Go to: https://github.com/SkogAI/lore/issues/new
2. Open any `issue_*.md` file in this directory
3. Copy the title from the "## Title" section
4. Copy the body from the "## Body" section
5. Add labels: `refactoring`, `configuration-system`, `migration`
6. For issue #16, also add: `tracking`, `epic`

## Troubleshooting

### "gh: command not found"
Install GitHub CLI: https://cli.github.com/

### "gh auth status" fails
Run: `gh auth login` and follow prompts

### Permission denied on script
Run: `chmod +x create_all_issues.sh`

### Issues already exist
The scripts don't check for duplicates. Review existing issues first.

## More Information

- `SUMMARY.md` - Complete overview of all issues
- `README.md` - Full details and structure
- `HOW_TO_CREATE_ISSUES.md` - Comprehensive guide with all options
- Individual `issue_*.md` files - Each issue's full content

## Related

- **Issue #5**: Original configuration system implementation
- **config/**: Configuration system code (if merged)
- **MIGRATION_GUIDE.md**: Migration instructions (if merged)
