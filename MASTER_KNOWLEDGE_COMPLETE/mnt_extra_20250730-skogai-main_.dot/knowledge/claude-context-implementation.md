# Claude Context Implementation

## Overview

This document describes the enhanced context loading system for Claude in the SkogAI ecosystem. The system is designed to provide Claude with comprehensive context at the start of each session, enabling more effective reasoning and task execution.

## Implementation Components

### 1. Enhanced Context Scripts

Three primary scripts have been created:

1. **context-claude-enhanced.sh**: The core script that collects and formats context information specific to Claude.
   - Loads Claude's identity and role from CLAUDE.md
   - Retrieves current tasks from MCP todo system (with legacy fallback)
   - Includes recent journal entries
   - Retrieves recent memories from MCP memory system
   - Includes key knowledge base entries
   - Provides workspace status (git, MCP server, directory structure)
   - Adds context metadata (generation time, token usage estimate)

2. **context-enhanced.sh**: The main context generation script that calls context-claude-enhanced.sh and formats the output.
   - Creates a clean, well-formatted context document
   - Saves the context to tmp/context.md
   - Adds clear separation between loaded context and conversation space
   - Provides token usage statistics

3. **load-claude-context.sh**: A user-friendly wrapper script that makes the context loading process simple.
   - Makes all scripts executable
   - Runs the context generation process
   - Provides statistics about token usage
   - Shows command examples for using the generated context

### 2. Key Features

- **MCP Integration**: Prioritizes modern MCP capabilities with legacy fallbacks
- **Strategic Context Ordering**: Most important information first (Claude's role, active tasks)
- **Token Efficiency**: Focuses on the most relevant information with size estimates
- **Clear Separation**: Distinct marker between loaded context and conversation space
- **Support for Both Workflows**:
  - Cold start: `cat tmp/context.md | claude`
  - Warm restart: `cat tmp/context.md | claude --continue <session_id>`

## Context Components (In Priority Order)

1. **Claude's Role and Guidelines**: From CLAUDE.md
2. **Active Tasks**: From MCP todo system or legacy TASKS.md
3. **Recent Journal Entries**: Latest journal entry for situational awareness
4. **Recent Memories**: From MCP memory system (if available)
5. **Key Knowledge Base Entries**: Critical information about SkogAI
6. **Workspace Status**: Git status, MCP server status, directory structure

## Usage

```bash
# Generate context with default settings
./scripts/load-claude-context.sh

# View the generated context
./scripts/load-claude-context.sh --display

# Start Claude with the context
cat tmp/context.md | claude

# Continue an existing session with updated context
cat tmp/context.md | claude --continue <session_id>
```

## Future Enhancements

1. **Memory Optimization**: Implement structured retrieval from MCP memory based on current task
2. **Dynamic Content Selection**: Adjust context content based on available token budget
3. **Session Awareness**: Detect when continuing an existing session to avoid redundant information
4. **Learning from Usage**: Track which context elements were most useful in previous sessions
5. **Integration with Dots' Structured Thinking**: Incorporate elements of the RPG-style processing framework

## Implementation Insights

The implementation balances several considerations:

1. **Context Efficiency**: Strategic loading prioritizes high-value information
2. **Dual System Compatibility**: Supports both legacy file-based and modern MCP methods
3. **Progressive Enhancement**: Works with basic features but takes advantage of advanced capabilities when available
4. **Clean Separation**: Maintains a clear boundary between loaded context and conversation space

This system allows Claude to start each session with comprehensive awareness of its role, ongoing tasks, and relevant context, maximizing effectiveness within token constraints.
