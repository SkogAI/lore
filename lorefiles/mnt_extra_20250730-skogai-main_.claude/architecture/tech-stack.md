# Technology Stack and Architecture

## Core Technologies
- **Python 3.8+** - Main development language
- **Bash scripting** - Automation and system integration
- **Git with submodules** - Version control and multi-repository coordination
- **Docker** - Containerization for MCP services
- **Redis** - Conversation memory and caching
- **MCP (Model Context Protocol)** - AI tool integration

## Key Components

### 1. Zen MCP Server (`zen-mcp-server/`)
- **AI-powered tools** for code analysis, review, debugging, deep thinking
- **Multiple AI model providers** (OpenAI, Anthropic, Gemini, OpenRouter, XAI)
- **MCP protocol implementation** for tool discovery and execution
- **Comprehensive testing** with 361 unit tests + simulator tests

### 2. Task Management System
- **YAML frontmatter** for structured metadata
- **CLI tools** (`gptme-contrib/scripts/tasks.py`) for status tracking
- **Pre-commit validation** hooks for data integrity
- **State management**: new, active, paused, done, cancelled

### 3. Context Management
- **Enhanced context loading** (`scripts/context-claude-enhanced.sh`)
- **MCP integration** for memory and recent activity
- **Structured workspace** with consistent organization

### 4. SkogAI Integration
- **SkogParse** - Universal syntax processor (processes every document/prompt)
- **SkogCLI** - Secure execution environment with formal verification
- **Mathematical type system** - Security through impossibility of invalid operations
- **Universal tool ecosystem** - 150+ MCP servers with diverse capabilities