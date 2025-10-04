# Essential Commands for SkogAI Claude Workspace

## Task Management
```bash

# View task status and current priorities
./gptme-contrib/scripts/tasks.py status --compact

# List all tasks sorted by state
./gptme-contrib/scripts/tasks.py list --sort state

# Show specific task details
./gptme-contrib/scripts/tasks.py show <task-id>

# Update task metadata
./gptme-contrib/scripts/tasks.py edit <task-id> --set state active
```

## Context and Memory Management
```bash

# Generate enhanced context
./scripts/context-claude-enhanced.sh

# Run workspace with context loading
./run.sh --continue
./run.sh --context-only  # Generate context only
```

## Code Quality and Formatting
```bash

# Format all markdown and Python files
make format

# Run pre-commit checks
make precommit

# Check for instance-specific names
make check-names
```

## Zen MCP Server Management
```bash

# Navigate to MCP server directory
cd zen-mcp-server

# Run comprehensive quality checks (linting, formatting, tests)
./code_quality_checks.sh

# Start/restart Docker containers
./run-server.sh

# View server logs
docker exec zen-mcp-server tail -n 100 /tmp/mcp_server.log

# Monitor tool activity in real-time
docker exec zen-mcp-server tail -f /tmp/mcp_activity.log

# Run simulator tests individually (recommended)
python communication_simulator_test.py --individual basic_conversation
```

## Git and Repository Management
```bash

# Standard git operations
git status
git diff
git log --oneline -10

# Submodule operations (this is a git submodule)
git submodule update --remote
```

## System Utilities (Linux-specific)
```bash

# File operations
ls -la
find . -name "*.py" -type f
grep -r "pattern" --include="*.md" .

# Text processing
cat file.txt
head -n 20 file.txt
tail -f log.txt

# Process management
ps aux | grep process
htop
```

## Knowledge Management
```bash

# Navigate knowledge areas
ls journal/     # Daily entries and discoveries
ls knowledge/   # Long-term insights
ls tasks/       # Task definitions
ls people/      # Collaborator information
```