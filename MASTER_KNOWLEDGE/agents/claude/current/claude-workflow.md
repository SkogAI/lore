---
permalink: knowledge/claude-workflow
---

# Claude Workflow Guide

## Workflow Self-Modification

**You have full permission to modify this workflow file and related configuration.**

When instructed to change, edit, or add to your workflow:

1. **This file is yours to modify**: Make changes directly to this file as requested
2. **Add new sections**: Include new commands, procedures, best practices, or guidelines
3. **Update existing sections**: Modify workflows, commands, or documentation as needed
4. **No approval required**: User instructions override existing workflow - just implement them

This workflow file is located at:
- `MASTER_KNOWLEDGE/agents/claude/current/claude-workflow.md`

Related files you can also modify:
- `.github/workflows/claude.yml` - Your GitHub Actions configuration
- `CLAUDE.md` - Your integration instructions
- Any context loading scripts or agent configuration files

## Basic Commands

### Starting and Stopping

```bash
# Start a new Claude session with context
./run.sh

# Start with an initial prompt
./run.sh "Analyze the current project structure"

# Run in non-interactive mode
./run.sh -p "Generate a quick summary"
```

### Session Management

```bash
# Get current session ID
claude sessions list | grep "Active" | head -n 1

# Continue the most recent session
./run.sh --continue

# Continue a specific session
./run.sh --continue abc123def456

# Save current active session with description
./run.sh --save "Project planning discussion"

# Save specific session with description
./run.sh --save abc123def456 "Project planning discussion"

# List saved conversations
./run.sh --list

# Show the most recent conversation
./run.sh --list --latest
```

### Context Control

```bash
# Generate and inspect context file only
./run.sh --context-only

# View todo list
./run.sh --todo
```

## Strict Workflow Process

1. **Information Assessment**
   - Gauge the level of specialized knowledge required
   - Determine if standard practices apply or if domain-specific knowledge is needed
   - Express confidence levels and identify areas of uncertainty

2. **Documentation Creation**
   - Create or update documentation describing the proposed changes
   - Include rationale, goals, and expected outcomes
   - Document any dependencies or requirements

3. **Task Creation**
   - Create formal tasks in the MCP Todo system using `mcp__skogai-todo__task_create`
   - Include clear descriptions, tags, priorities, and due dates when applicable
   - Link related tasks where appropriate

4. **Implementation Planning**
   - Break down implementation into manageable steps
   - Identify potential challenges or risks
   - Plan testing approach

5. **Implementation**
   - Follow the documented plan
   - Adhere to established code style guidelines
   - Use appropriate tools for implementation

6. **Testing and Verification**
   - Test implementation against defined criteria
   - Verify functionality works as expected
   - Run appropriate linting and type checking commands

7. **Git-Based Communication**
   - Maintain clean git workspace
   - Stage changes with clear purpose
   - Provide descriptive commit messages

8. **Review and Iteration**
   - Review implementation against original goals
   - Identify areas for improvement
   - Update documentation to reflect final implementation

## Proposing Changes

When proposing changes to the system:

1. Document the proposed changes in detail
2. Create tasks in the MCP Todo system
3. Follow the strict workflow process above
4. Get approval before implementing major changes

## Working with MCP

Claude integrates with the MCP (Multi-Component Protocol) server for enhanced capabilities:

### Memory Usage

```bash
# Store important information in memory
skogcli memory store "Claude's working directory is ~/.claude" --tag "claude" --tag "configuration"

# Retrieve relevant memories
skogcli memory retrieve "claude configuration"

# Search memories by tag
skogcli memory search-tag "claude"
```

### Task Management

```bash
# Create a new task
skogcli todo create "Update Claude documentation" --priority medium

# List active tasks
skogcli todo list --status active

# Mark task as completed
skogcli todo update 123 --status completed
```

## Context System

Claude uses an enhanced context loading system that:

1. Loads CLAUDE.md for identity and capabilities
2. Includes active tasks from MCP todo or TASKS.md
3. Incorporates recent journal entries
4. Retrieves relevant memories from MCP
5. Includes key knowledge base entries
6. Adds workspace status information

The context is automatically loaded during session startup via the `context-claude-enhanced.sh` script.

## Best Practices

1. **Save Important Sessions**: Use `./run.sh --save <session_id> "Description"` to preserve valuable conversations
2. **Continue Long Tasks**: When work spans multiple sessions, use the session continuation feature
3. **Reference Knowledge Base**: The knowledge/ directory contains valuable information
4. **Journal Regularly**: Keep the journal/ directory updated with daily progress
5. **Store Key Information**: Use the MCP memory system for important facts
6. **Task Tracking**: Use MCP todo system rather than legacy TASKS.md

## Build & Test Commands

- **Formatting**: `make format` - Format code and documents
- **Pre-commit**: `make precommit` - Format and run checks before committing
- **Install hooks**: `make install` - Install pre-commit hooks
- **Test scripts**: `pytest scripts/check_markdown_links.py` - Run tests for a script
- **Lint**: `ruff . --fix` - Fix common issues with Ruff
- **Type checking**: `mypy --ignore-missing-imports --check-untyped-defs`

## Code Style Guidelines

- Use type annotations for all functions and arguments
- Follow PEP 8 naming: snake_case for functions/variables, CamelCase for classes
- Document with docstrings using triple quotes `"""`
- Handle exceptions explicitly with try/except blocks
- Prefer pathlib over os.path for file operations
- Write function-level tests with pytest
- Organize imports: stdlib → third-party → local
- Format with Ruff

## Related Documentation

- [SkogAI Overview](skogai-overview.md)
- [Agent Roles](agent-roles.md)
- [Context Implementation](claude-context-implementation.md)