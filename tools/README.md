# SkogAI Tools Directory

This directory contains utility scripts and tools for managing the SkogAI ecosystem.

## Helper Scripts for AI Agents

### gh-create-issue.sh
Simple wrapper for creating GitHub issues. Designed for use by Claude and other AI agents.

**Usage:**
```bash
./gh-create-issue.sh "Issue Title" "Issue Body" [labels]
```

**Examples:**
```bash
# Simple issue
./gh-create-issue.sh "Fix login bug" "Users cannot login" "bug,urgent"

# Issue with multi-line body
./gh-create-issue.sh "Migrate scripts" "$(cat <<'EOF'
### Overview
Migration details...

### Tasks
- [ ] Task 1
- [ ] Task 2
EOF
)" "migration"

# Read body from file
./gh-create-issue.sh "New feature" "$(cat issue_body.md)" "feature"
```

**Requirements:**
- `gh` CLI installed and authenticated
- Write access to SkogAI/lore repository

### create-file.sh
Safe file creation with automatic directory creation and overwrite protection.

**Usage:**
```bash
./create-file.sh [OPTIONS] FILE_PATH [CONTENT]
```

**Options:**
- `--force`: Overwrite existing files
- `--help`: Show help message

**Examples:**
```bash
# Create a simple file
./create-file.sh docs/new-doc.md "# New Documentation"

# Create from stdin
echo "content" | ./create-file.sh output.txt

# Multi-line content
./create-file.sh config/new-config.json "$(cat <<'EOF'
{
  "setting": "value"
}
EOF
)"

# Overwrite existing file
./create-file.sh --force existing.txt "New content"
```

**Features:**
- Automatically creates parent directories
- Prevents accidental overwrites (unless --force)
- Validates paths are within repository
- Works with relative or absolute paths

## Other Tools

### issue-creator.py
Comprehensive issue creation workflow with templates and interactive mode.

**Usage:**
```bash
python tools/issue-creator.py interactive
python tools/issue-creator.py templates
python tools/issue-creator.py create "Title" "Description" --type feature
```

### create-issue.sh
Shell wrapper for the issue-creator.py script.

### context-manager.sh
Manages SkogAI context files and agent state.

### index-knowledge.sh
Indexes knowledge base files for search and retrieval.

### llama-lore-creator.sh
Creates lore files from agent interactions.

### llama-lore-integrator.sh
Integrates lore files into the knowledge base.

### create-persona.sh
Creates new agent persona configurations.

### setup-lore-service.sh
Sets up the lore service for background operation.

### check_hardcoded_paths.py
Checks Python files for hardcoded paths that should use the config system.

### check_hardcoded_paths.sh
Checks shell scripts for hardcoded paths that should use the config system.

## Development Guidelines

When adding new tools:
1. Follow existing naming conventions (kebab-case for shell scripts)
2. Include usage documentation in script headers
3. Add help/usage functions
4. Test thoroughly before committing
5. Update this README with new tools
6. Consider security implications (path validation, permissions, etc.)

## Security Considerations

- File creation scripts validate paths to prevent directory traversal
- Issue creation scripts require proper GitHub authentication
- All scripts should run with minimal necessary permissions
- Avoid exposing sensitive data in script outputs or error messages

## Testing

Test new scripts manually:
```bash
# Test help messages
./tools/script-name.sh --help

# Test with valid inputs
./tools/script-name.sh valid-input

# Test error conditions
./tools/script-name.sh invalid-input
```

## Related Documentation

- `CLAUDE.md` - Claude Code integration guide
- `config/README.md` - Configuration system documentation
- `HOW_TO_CREATE_ISSUES.md` - GitHub issue creation guide
