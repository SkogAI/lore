# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Privileges and Permissions

Claude Code has **full repository access** for this docs/lore repository, including:
- ✅ File operations (create, edit, read, search)
- ✅ Git operations (commit, push, branch management)
- ✅ GitHub CLI commands (issue creation, PR management) - **no approval required**
- ✅ Code analysis and documentation

Since this is a documentation and knowledge repository (not containing sensitive files like SSH keys), Claude has the same privileges as GitHub Copilot to facilitate efficient workflow automation.

## Available Tools for Claude

You have access to helper scripts that make common tasks easier:

### Issue Creation
```bash
./tools/gh-create-issue.sh "Title" "Body" "labels"
```
Creates GitHub issues in the SkogAI/lore repository. Requires `gh` CLI authentication.

### File Creation
```bash
./tools/create-file.sh path/to/file.txt "Content"
```
Safely creates files within the repository with automatic directory creation and overwrite protection.

## Environment Setup

### Initial Setup
```bash
# Run the automated setup script (recommended)
./setup.sh

# Or manually create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Activating Virtual Environment
```bash
# Always activate before running commands
source .venv/bin/activate

# Verify activation
which python  # Should show .venv/bin/python
```

## Build & Test Commands

### Starting Applications
```bash
# Main chat UI (Streamlit)
./start-chat-ui.sh
# Or manually:
streamlit run streamlit_chat.py --server.port=8501 --server.address=0.0.0.0

# Gradio chat interface
python skogai-chat.py

# Terminal UI for lore browsing
python lore_tui.py

# Generate agent lore
python generate-agent-lore.py
```

### Testing
- Manual verification (no formal test framework)
- Test agent API: `python agents/api/agent_api.py` (requires external API access)
- Tests may fail in sandboxed environments without network access

### Dependency Management
```bash
# Add new dependency (with uv)
uv add package-name && uv lock && uv sync

# Add new dependency (with pip)
pip install package-name
# Then update pyproject.toml manually

# Update all dependencies
uv lock --upgrade && uv sync  # with uv
pip install --upgrade -e .     # with pip
```

For detailed setup instructions, see [docs/SETUP.md](docs/SETUP.md).

## Code Style Guidelines
- **Imports**: Standard Python order (stdlib → third-party → local)
- **Type Annotations**: Use typing hints (Dict, List, Optional, Any)
- **Error Handling**: Try/except with specific exceptions and informative logging
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Documentation**: Docstrings for all classes/functions using triple quotes
- **Logging**: Use configured logger with descriptive messages and error details
- **Configuration**: Load from config files with environment variable fallbacks
- **JSON**: Proper error handling with sensible defaults
- **Structure**: Maintain separation between implementations and templates
- **Architecture**: Follow agent/context/orchestrator pattern

## Repository Configuration
- **Default Branch**: This repository uses `master` as the default branch (not `main`)
- **Remote**: GitHub repository at https://github.com/SkogAI/lore
- **Git Commands**: Always reference `origin/master` for upstream comparisons

## Workflow Self-Modification

You have **full permission** to modify your own workflow files as requested. This includes:

### Your Workflow Files
- **Primary Workflow Documentation**: `MASTER_KNOWLEDGE/agents/claude/current/claude-workflow.md`
- **GitHub Actions Workflow**: `.github/workflows/claude.yml`
- **Context Scripts**: Any scripts in the repository related to your operation

### Modifying Your Workflow

When asked to change, edit, or add to your workflow:

1. **Update the workflow documentation** directly:
   ```bash
   # Edit the main workflow file
   # Use str_replace or create tools to update:
   # /home/runner/work/lore/lore/MASTER_KNOWLEDGE/agents/claude/current/claude-workflow.md
   ```

2. **Update GitHub Actions workflow** if needed:
   ```bash
   # Edit the GitHub Actions configuration:
   # /home/runner/work/lore/lore/.github/workflows/claude.yml
   ```

3. **Add new sections** as requested:
   - New commands, procedures, or best practices
   - Tool integrations or workflow steps
   - Context loading modifications
   - Code style updates or build commands

4. **Examples of valid modifications**:
   - Adding new MCP tools or commands
   - Updating the strict workflow process
   - Adding new best practices or guidelines
   - Modifying context loading behavior
   - Adding new build/test commands
   - Updating code style guidelines

You do **not** need special permission to make these changes - you are authorized to modify your workflow as instructed by the user.

## Discovered Workflows

### GitHub Issue Creation
When creating GitHub issues, you have two options:

**Option 1: Use the wrapper script (Recommended)**
```bash
# Simple usage
./tools/gh-create-issue.sh "Issue Title" "Issue body text" "label1,label2"

# With multi-line body
./tools/gh-create-issue.sh "Migrate OpenRouter scripts" "$(cat <<'EOF'
### Overview
Migration details here...
EOF
)" "migration,refactoring"

# Reading body from file
./tools/gh-create-issue.sh "New Feature" "$(cat issue_body.md)" "feature"
```

**Option 2: Direct gh CLI usage**
```bash
gh issue create --repo SkogAI/lore --title "Title" --body "$(cat <<'EOF'
Body with proper formatting
EOF
)"
```

Evidence: Successfully created issue #4 addressing branch naming inconsistencies

### File Creation
When you need to create new files, use the wrapper script:
```bash
# Create a file with content
./tools/create-file.sh path/to/file.txt "File content here"

# Create a file from stdin
echo "content" | ./tools/create-file.sh path/to/file.txt

# Multi-line content
./tools/create-file.sh docs/new-doc.md "$(cat <<'EOF'
# New Documentation
Content here...
EOF
)"

# Overwrite existing file (use with caution)
./tools/create-file.sh --force existing.txt "New content"
```

The script will:
- Automatically create parent directories
- Prevent accidental overwrites (unless --force is used)
- Validate paths are within the repository

### Session Handover Documentation
When ending a session, create/update `docs/handover.md` with:
- What was accomplished
- Context for next session
- Active session IDs
- Repository state
- Next steps

This ensures smooth continuation between work sessions.