# Claude Code Capabilities

This document outlines what Claude Code can and cannot do when working with this repository.

## ✅ What Claude CAN Do

### File Operations
- **Create new files** using the Write tool
- **Edit existing files** using the Edit tool
- **Read files** to understand context
- **Search files** using Glob and Grep tools

### Git Operations
- **Commit changes** to the current branch
- **Push changes** to remote repository
- **View status and diffs** using git commands
- **Create branches** (when triggered on issues)
- **Work with existing PR branches** (when triggered on open PRs)

### Code Analysis
- **Answer questions** about code
- **Provide code reviews** with detailed feedback
- **Explain implementations** and architecture
- **Suggest improvements** for code quality

### GitHub Integration
- **Update comments** on issues and PRs
- **Create pull requests** (via URL with pre-filled content)
- **Reference code** with file paths and line numbers

## ⚠️ What Requires User Approval

### GitHub CLI Operations
- **Creating issues** via `gh issue create` - requires approval
- **Other gh commands** - require approval for security

These operations need explicit user approval due to security policies. To enable these:
1. User must approve the command when prompted
2. Or user can configure `--allowedTools` to include specific gh commands

## ❌ What Claude CANNOT Do

- **Submit formal GitHub PR reviews** (can only provide feedback in comments)
- **Approve pull requests** (security limitation)
- **Post multiple comments** (only updates a single comment)
- **Merge branches** or perform complex git operations
- **Modify workflow files** in `.github/workflows/` directory

## Workflow for Issue Creation

Since `gh` commands require approval, here's the recommended workflow:

### Option 1: User Approves gh Commands
When Claude attempts to run `gh issue create`, approve the command prompt.

### Option 2: Manual Issue Creation
Claude can draft the issue content, and you can create it manually using:
```bash
gh issue create --repo SkogAI/lore --title "Title" --body "$(cat <<'EOF'
Body content here
EOF
)"
```

### Option 3: Web Interface
Use the GitHub web interface at https://github.com/SkogAI/lore/issues/new

## Example: Creating the OpenRouter Migration Issue

Claude drafted an issue in #63 but couldn't create it. You can create it using:

```bash
gh issue create --repo SkogAI/lore --title "Migrate OpenRouter scripts after skogcli integration" --body "$(cat <<'EOF'
### Overview

Migrate OpenRouter integration scripts to use the centralized configuration system after they have been merged into skogcli scripts.

### Prerequisites

- [ ] OpenRouter scripts must be merged to skogcli first
- [ ] Configuration system must be implemented (from previous issues)

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

#### Additional Files Found

4. **orfree** (binary/executable)
   - Verify if this needs migration or can be removed

5. **or.free** (script/executable)
   - Verify if this needs migration or can be removed

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

### Testing Checklist

- [ ] Test OpenRouter API calls
- [ ] Verify cache directory creation
- [ ] Test with environment variables
- [ ] Test with defaults
- [ ] Verify API key handling

### Acceptance Criteria

- [ ] All OpenRouter scripts merged to skogcli
- [ ] All merged scripts use configuration system
- [ ] No hardcoded paths in openrouter scripts
- [ ] Cache and data directories work with custom paths
- [ ] API integration still functions correctly

### Related Issues

- Depends on: skogcli merge (to be created/referenced)
- Part of: Issue #5 path resolution standardization
- Successor to: Issue #63
EOF
)"
```

## Summary

Claude has robust file and git capabilities but requires user approval for GitHub CLI operations. This ensures security while maintaining flexibility for code changes and documentation.
