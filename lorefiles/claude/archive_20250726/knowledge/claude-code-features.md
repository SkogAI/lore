# Claude Code Features

## @ Files System

### Overview
The @ files system allows importing additional files into CLAUDE.md memory files, enabling modular context management and code sharing.

### Syntax
```
@path/to/import
```

### Key Features
- **Multiple Imports**: Can import multiple files in a single memory file
- **Recursive Imports**: Supports up to 5 hops deep
- **Path Flexibility**: Supports both relative and absolute paths
- **Code Block Safety**: Imports are not evaluated inside code spans or code blocks

### Usage Patterns
```markdown
See @README for project overview and @package.json for npm commands.

# Additional Instructions
- git workflow @docs/git-instructions.md
```

### Use Cases
- Sharing project guidelines across teams
- Personal preferences and configurations
- Modular context management
- Replacing deprecated CLAUDE.local.md approach

### Management
- Use `/memory` command to view loaded memory files
- Supports team or personal instruction sharing

## Hooks System

### Overview
User-defined shell commands that execute at specific points in Claude Code's lifecycle, providing deterministic control over behavior.

### Hook Events
1. **PreToolUse**: Runs before tool calls, can block execution
2. **PostToolUse**: Runs after tool completion
3. **Notification**: Triggered during notifications
4. **Stop**: Runs when main agent finishes
5. **SubagentStop**: Runs when subagent completes

### Configuration Structure
```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here"
          }
        ]
      }
    ]
  }
}
```

### Configuration Locations
- `~/.claude/settings.json` (User settings)
- `.claude/settings.json` (Project settings)
- `.claude/settings.local.json` (Local project settings)

### Hook Output Control
**Exit Codes:**
- 0: Success
- 2: Blocking error
- Other: Non-blocking error

**JSON Output:**
- Control continuation
- Provide decision control
- Specify reasons for blocking

### Security
⚠️ **Warning**: Hooks execute with full user permissions, requiring careful configuration.

### Common Use Cases
- Automatic code formatting
- Logging command executions
- Custom notifications
- Permission management
- Code convention feedback

## Caching and Persistence

### Conversation Caching
- **Automatic Saving**: Conversations saved locally with full message history
- **Resume Support**: `--continue` and `--resume` commands available
- **Tool State Preservation**: Maintains tool state and results from previous conversations
- **Context Restoration**: Restores entire message history to maintain context

### Performance Features
- **Parallel Sessions**: Supports Git worktrees for isolation
- **Multiple Tasks**: Work on multiple tasks simultaneously without interference
- **Context Preservation**: Maintains state across session boundaries

## Command System

### Command Types
- **Project-specific**: Located in `.claude/commands` directories
- **Personal**: User-level commands
- **Global**: System-wide commands

### Command Features
- **Argument Placeholders**: Support for `$ARGUMENTS` and other placeholders
- **Custom Slash Commands**: Project and personal level customization
- **Flexible Execution**: Integration with existing workflows

### Output Formats
- **Default Text**: Standard text output
- **JSON**: Structured output with metadata
- **Streaming JSON**: Real-time processing support
- **Piping**: Input and output piping capabilities

## Extended Thinking

### Activation
Triggered by phrases like:
- "think"
- "think more"
- "think harder"

### Features
- **Deeper Reasoning**: Enhanced analysis for complex tasks
- **Visible Process**: Displays thinking process as italic gray text
- **Use Cases**: Architectural decisions, debugging, implementation planning

### Display
- Shows reasoning process above the response
- Provides transparency into decision-making
- Useful for understanding complex problem-solving approaches

## Integration Patterns

### Workflow Integration
- **Git Integration**: Works with Git worktrees and repositories
- **IDE Integration**: Supports various IDE configurations
- **MCP Integration**: Model Context Protocol support for extended functionality

### Development Workflows
- **Isolated Environments**: Parallel development without interference
- **Context-Aware**: Maintains awareness of project structure and history
- **Tool Integration**: Seamless integration with development tools and processes