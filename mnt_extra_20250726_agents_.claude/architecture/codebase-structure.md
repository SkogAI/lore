# Codebase Structure Overview

## Root Directory Structure
```
/home/skogix/skogai/.claude/
├── journal/           # Daily discoveries and knowledge archaeology
├── knowledge/         # Long-term insights and technical documentation
├── tasks/             # Individual task files with YAML frontmatter
├── people/            # Information about collaborators
├── scripts/           # Automation and context generation scripts
├── zen-mcp-server/    # AI-powered tools MCP server (361 tests)
├── gptme-contrib/     # Task management CLI and additional tools
├── tmp/               # Temporary files and generated context
├── inbox/             # Incoming items and processing
├── chat/              # Chat logs and conversations
├── history/           # Historical information and artifacts
├── lessons/           # Specific lessons learned and insights
└── todo/              # Todo items and quick notes
```

## Key Configuration Files
- **CLAUDE.md** - Strategic context and operating principles
- **ARCHITECTURE.md** - SkogAI ecosystem technical architecture
- **TASKS.md** - Task management system documentation
- **README.md** - Workspace overview and introduction
- **gptme.toml** - Context files for consistent loading
- **run.sh** - Main workspace launcher with context management
- **Makefile** - Build automation and quality checks

## Important Subdirectories

### zen-mcp-server/
- **server.py** - Main MCP server implementation
- **tools/** - AI tool implementations (analyze, debug, codereview, etc.)
- **providers/** - AI model provider integrations
- **tests/** - Comprehensive unit test suite (361 tests)
- **simulator_tests/** - End-to-end integration tests
- **systemprompts/** - System prompt definitions for each tool

### gptme-contrib/
- **scripts/tasks.py** - Comprehensive task management CLI
- **scripts/bluesky/** - Social media integration tools
- **scripts/twitter/** - Twitter automation and workflows
- **tools/** - Additional gptme tool implementations

### scripts/
- **context-claude-enhanced.sh** - Enhanced context generation with MCP integration
- **extract.py** - Message extraction and conversation reconstruction
- **check_*.py** - Various validation and checking utilities

## Data Flow Patterns
- **Context generation** → MCP memory integration → Claude interface
- **Task creation** → YAML frontmatter → CLI management → Status tracking
- **Knowledge capture** → Journal entries → Knowledge base → Cross-references
- **Tool execution** → MCP protocol → AI providers → Structured responses