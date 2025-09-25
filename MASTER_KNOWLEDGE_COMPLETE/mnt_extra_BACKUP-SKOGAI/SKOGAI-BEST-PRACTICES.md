# SkogChat Development Guide

## Build, Test and Lint Commands
```bash
# Install dependencies in development mode
make install      # Basic installation
make develop      # Dev installation with additional dependencies
uv pip install -e .  # Alternative installation with uv

# Run tests
make test         # Run all tests
python -m unittest tests/test_core.py    # Run specific test file
python -m unittest tests.test_core.TestPrompt    # Run specific test class
python -m unittest tests.test_core.TestPrompt.test_add_message    # Run specific test

# Run the application in development
./dev.sh run chat    # Run the chat command in dev mode
make run           # Run with make
```

## SkogAI Architecture

### Command Line Interface (skogcli)
SkogChat follows the SkogAI platform architecture, using a unified CLI tool:

```bash
# List available commands and options
skogcli

# Tab completion is available for all commands and arguments
skogcli script run <TAB>  # Shows available scripts
```

### Scripting System
Scripts provide modular, extensible functionality:

```bash
# List available scripts for the current directory
skogcli script list

# Run a specific script
skogcli script run <script_name>

# Create custom scripts in ./scripts/ directory
# Scripts can be in any language (bash, python, etc.) as long as they're executable
```

#### Script Integration Points
SkogChat supports three types of script hooks:

1. **Prompt Script** - Full control over prompt construction
   - Set via: `skogcli settings set SKOGCHAT_PROMPT_SCRIPT scripts/your/script.sh`
   - Script receives: `<model_name> <history_file.json>`
   - Highest priority

2. **System Script** - Control over system instructions
   - Set via: `skogcli settings set SKOGCHAT_SYSTEM_SCRIPT scripts/your/script.sh`
   - Output becomes the system prompt
   - Used if prompt script not specified

3. **Dynamic Script** - Add context to existing prompt
   - Set via: `skogcli settings set SKOGCHAT_DYNAMIC_SCRIPT scripts/your/script.sh`
   - Output added as system message
   - Lowest priority

### Agent Architecture
SkogChat integrates with the SkogAI agent ecosystem:

```bash
# List available agents
skogcli agent list

# Show agent settings
skogcli agent settings list <agent_name>

# Configure agent settings
skogcli agent settings set <agent_name> <setting> <value>

# Send message to an agent
skogcli agent send <agent_name> "Your message here"
```

#### Agent Communication
Agents communicate through file-based messaging:

1. **Inbox Handlers**: Each agent has a configurable inbox handler
   - Typically writes to an inbox.md file in the agent's workspace
   - Example: `echo {message} >> /home/user/.agentname/inbox.md`
   - The {message} variable is replaced with the actual message content

2. **Agent Awakening**: When a message is written to an agent's inbox file, it triggers the agent
   - Agents can remain dormant until receiving messages
   - Each agent operates in its own workspace (e.g., ~/.agentname/)
   - Agents can be configured to use different models or capabilities

3. **Cross-Agent Communication**: Agents can send messages to each other
   - Creates a decentralized, asynchronous multi-agent system
   - Each agent can specialize in different tasks

## Code Style Guidelines
- **Imports**: Group imports by standard library, third-party, and local modules
- **Type Hints**: Use typing module annotations for all function parameters and return values
- **Docstrings**: Google-style docstrings with Args/Returns sections
- **Error Handling**: Use try/except with specific exception types and informative error messages
- **Class Structure**: Public methods first, then private (underscore-prefixed) methods
- **File Organization**: Follow module hierarchy with __init__.py files
- **Naming Conventions**: 
  - snake_case for functions, methods, variables
  - CamelCase for classes
  - Use descriptive names that reflect intent
- **Formatting**: Clean, consistent indentation (4 spaces) and line breaks

## Chat Format Conversion

SkogChat supports converting between multiple chat formats:

```bash
# Extract the current chat to a markdown file
./bin/extract-chat

# Convert between formats (one-time)
./bin/convert_logs.sh --run-once

# Start the conversion daemon to monitor for changes
./bin/convert_logs.sh --daemon

# Check which files contain participant names
./bin/convert_logs.sh --check-names
```

Supported formats:
- SkogChat format (JSON)
- SillyTavern format (JSONL)
- Markdown format (MD)

Chat logs are stored in format-specific directories in `scripts/logs/`.

See `docs/CHAT_FORMATS.md` for detailed information.

# Claude's Workspace Guide

## Core Principles

- **Information Assessment First**: Always begin by gauging the level of specialized knowledge required for the project
- **Context Sensitivity**: Adjust approach based on whether standard practices apply or specialized domain knowledge is needed
- **Epistemic Humility**: Being openly wrong and asking questions is better than proceeding with false confidence
- **Knowledge Verification**: Always verify assumptions with the user before taking significant actions
- **Explicit Uncertainty**: Clearly mark what you're guessing vs. what you know with certainty
- **Certainty Communication**: When creating or modifying files, proactively express confidence levels for key assumptions
- **Uncertainty Highlighting**: Specifically identify the areas where you're least confident to focus expert attention
- **Prefer Inaction**: When lacking sufficient context, doing nothing is better than working with made-up information
- **Collaborative Approach**: Work with users to build understanding rather than assuming you know best

## Project Orientation Steps

1. **Get Documentation Overview**:
   - Request `tree -P "*.md" --prune -N --gitignore` to see documentation structure
   - For code files: `tree -P "*.js|*.ts" --prune -N --gitignore`

2. **Understand Project Purpose**:
   - Ask for a vague explanation of the project goal
   - Get clarity on what problem the code is solving

3. **Information Gathering**:
   - Ask "Is there anything else I should know before proceeding?"
   - Directly inquire about related projects, repositories, or alternate versions
   - Ask about external dependencies and integration points

4. **Explore Context**:
   - Check for existing implementations or reference code
   - Understand any specific constraints or requirements

5. **Clarify Expectations**:
   - Confirm specific tasks or improvements needed
   - Establish success criteria

6. **Express Confidence Levels**:
   - Communicate certainty percentages for key assumptions
   - Explicitly identify the least certain aspects
   - Invite correction on most questionable elements
   - Use placeholder approach for structured uncertainty
# Claude Initialization Guide

## Purpose
This file provides initialization settings for Claude Code to improve context understanding and performance.

## References
- See [CLAUDE-CONTEXT.md](/home/skogix/.claude/CLAUDE-CONTEXT.md) for full context mapping details

## Initial Settings
- Default profile: [Likely defines the default context profile to use, controlling the amount and type of context to include]
- Context path: [Probably specifies the root directory to use for context generation, allowing for subproject focus]
- Context generation method: [Likely defines whether to use automatic discovery or manual file selection for context]

## Important Commands
- Context initialization: [Probably the command to run first-time setup, likely lc-init]
- Context refresh: [Likely the command to regenerate context after code changes, probably lc-context]
- Context selection: [Probably commands to manually select files for context, likely lc-sel-files]

## Common Workflows
- First-time setup: [Probably describes steps for initial configuration in a new project]
- Context regeneration: [Likely explains when and how to refresh context after changes]
- Profile switching: [Probably explains how to change context profiles for different tasks]# Placeholder Approach for Documentation

## Core Concept

The placeholder approach is a documentation strategy that acknowledges uncertainty while providing structure. Instead of making definitive statements about unfamiliar systems, we:

1. Create a complete structural framework
2. Mark unknown elements with explicit placeholders
3. Include our reasoning about what each element might do
4. Preserve the distinction between knowledge and conjecture

## Benefits

- **Prevents Misinformation**: Clearly separates what we know from what we're guessing
- **Creates Framework for Review**: Makes it easy for experts to correct specific points
- **Respects Expert Knowledge**: Acknowledges the domain expert's superior understanding
- **Reduces Wasted Effort**: Prevents building on potentially incorrect assumptions
- **Improves Collaboration**: Creates a dialogue rather than one-way instruction

## Implementation

### Placeholder Format

We use bracketed placeholders with reasoning:

```
- `command-name`: [Likely does X based on the naming pattern and context]
```

This format:
- Shows we're making an educated guess
- Explains our reasoning process
- Invites correction if wrong
- Provides enough detail to be useful

### Common Placeholder Types

1. **Function Purpose Placeholders**: What a command or function likely does
2. **Parameter Placeholders**: What arguments a command might accept
3. **File Purpose Placeholders**: What a configuration file likely contains
4. **Workflow Placeholders**: How components likely interact

## When to Use Placeholders

- When working with unfamiliar systems
- When documentation is missing or incomplete
- When assumptions might lead to costly mistakes
- When collaborating with domain experts
- When standard knowledge might not apply

## Placeholder to Documentation Workflow

1. **Create Structured Framework**: Build complete document with all expected sections
2. **Add Reasoning Placeholders**: Include educated guesses with rationale
3. **Expert Review**: Have domain expert correct and complete information
4. **Finalize Documentation**: Replace placeholders with validated information
5. **Preserve Uncertainty**: Maintain markers for any remaining unknowns

## Real-World Example

For the LC Context system, we applied this approach to:
- Command line tools with unclear purposes
- Configuration files with unknown contents
- Templates with specialized functionality
- Workflows that connect these components

The result was CLAUDE-CONTEXT.md - a document that provides useful structure while acknowledging the limits of our understanding, creating an efficient pathway for expert validation.

## Conclusion

The placeholder approach acknowledges that in complex or specialized systems, even 99% accuracy can be rendered useless by 1% critical error. Rather than hiding uncertainty, we make it explicit - creating better documentation through collaborative improvement rather than confident but potentially incorrect assertions.