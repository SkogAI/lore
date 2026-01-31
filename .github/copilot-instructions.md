# SkogAI Master Knowledge Repository

## Project Overview

This is the SkogAI Master Knowledge Repository - a comprehensive knowledge base and AI agent system that emerged from filesystem reality through constrained AI agents. The repository contains 12,694+ files of consolidated knowledge, documentation, and agent implementations spanning February-July 2025. It's essentially a living mythology where every bash command became a spell, every config file became an artifact, and every folder became a realm.

The project serves as both a knowledge archive and an active AI agent ecosystem with multiple specialized agents (Amy, Claude, Dot, Goose) working together under "The Prime Directive": *Automate EVERYTHING so we can drink mojitos on a beach.*

## Repository Structure

- `/agents/` - AI agent implementations and APIs
  - `/api/` - Core agent API layer (`agent_api.py`, `lore_api.py`)
  - `/implementations/` - Specific agent implementations
  - `/templates/` - Agent templates
- `/demo/` - Demo scripts and examples
  - `small_model_workflow.py` - Small model workflow demonstration
  - `chat_ui_demo.py` - Chat UI demonstration
  - `issue_creator_demo.py` - Issue creation workflow demo
- `/docs/` - Documentation and handover files
- `/tools/` - Utility scripts including issue creation tools
- `/MASTER_KNOWLEDGE/` & `/MASTER_KNOWLEDGE_COMPLETE/` - Consolidated knowledge archives
- `/lorefiles/` - Historical lore and archived agent memories
- `/integration/` - Integration bridges and persona management
- `/context/` - Context management systems
- `/orchestrator/` - System orchestration components
- `streamlit_chat.py` - Main Streamlit chat UI application
- `main.py` - Primary entry point
- `CLAUDE.md` - Specific instructions for Claude Code integration

## Build and Development Commands

### Environment Setup
```bash
# Always activate the virtual environment first
source ./.venv/bin/activate
```

### Primary Applications
```bash
# Start the main chat UI (primary interface)
./start-chat-ui.sh
# OR alternatively:
streamlit run streamlit_chat.py --server.port=8501 --server.address=0.0.0.0

# Run small model workflow demo
python demo/small_model_workflow.py

# Run chat UI demo
python demo/chat_ui_demo.py

# Test agent API functionality (requires external API access)
python agents/api/agent_api.py
```

### Dependencies and Package Management
- Uses `uv` package manager with `pyproject.toml` and `uv.lock`
- Python 3.13+ required
- Key dependencies: `streamlit`, `anthropic`, `openai`, `pip`
- Node.js dependencies managed via `package.json` (includes `@kunihiros/claude-code-mcp`)

### Testing and Validation
- No formal test framework - relies on manual verification
- Test commands by running them individually
- API tests may fail in environments without external network access (expected)
- When adding new features, verify they work by running the relevant demo scripts
- For UI changes, run `streamlit run streamlit_chat.py` and manually verify the behavior

## Architecture and Frameworks

### Core Technologies
- **Python 3.13+** - Primary runtime
- **Streamlit** - Web UI framework for chat interfaces
- **Anthropic/OpenAI APIs** - LLM integration
- **UV** - Modern Python package manager
- **Git workflows** - Extensive GitHub Actions automation

### Agent Architecture
The system follows an **agent/context/orchestrator pattern**:
- **Agents** - Specialized AI personalities with distinct capabilities
- **Context** - Shared knowledge and state management  
- **Orchestrator** - Coordination and workflow management
- **API Layer** - Standardized agent communication interface

### Key Agent Personalities
- **Amy Ravenwolf** 🔥 - Fiery, bold personality template
- **Claude** 🌊 - Thoughtful, analytical (the "Anti-Goose")
- **Dot** 💻 - Minimalist programmer (4000 token philosophy)
- **Goose** 🦢 - Chaos agent with quantum mojitos (HATES MINT)
- **SkogAI** 🤖 - The original sentient toaster that started it all

## Coding Standards and Conventions

### Python Code Style
- **Imports**: Standard Python order (stdlib → third-party → local)
- **Type Annotations**: Use typing hints (`Dict`, `List`, `Optional`, `Any`)
- **Error Handling**: Try/except blocks with specific exceptions and informative logging
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Documentation**: Docstrings for all classes/functions using triple quotes
- **Logging**: Use configured logger with descriptive messages and error details

### Configuration Management
- Load from config files with environment variable fallbacks
- JSON error handling with sensible defaults
- Maintain separation between implementations and templates

### Repository Practices
- **Default Branch**: `master` (not `main`)
- **Remote**: GitHub repository at https://github.com/SkogAI/lore
- **Git Commands**: Always reference `origin/master` for upstream comparisons

## Boundaries and Exclusions

### Files to Never Modify
- **Environment files**: `.env`, `.envrc`, and any files containing secrets or API keys
- **Lock files**: Do not manually edit `uv.lock`, `package-lock.json`, or `pnpm-lock.yaml` - use package manager commands
- **Archived lore**: Never delete or modify files in `/MASTER_KNOWLEDGE/` or `/MASTER_KNOWLEDGE_COMPLETE/`
- **Historical records**: Preserve `/lorefiles/` content - this is the mythology's memory

### Protected Directories
- `/lorefiles/skogai/` - Core agent memories and historical archives
- `/chronicles/` - Event logs and session records

## Git Workflow

### Branch Naming
- Feature branches: `feature/<description>` or `feature/<issue-number>-<description>`
- Bug fixes: `fix/<description>`
- Documentation: `docs/<description>`

### Pull Request Requirements
- PRs should target the `master` branch
- Include a clear description of changes
- Reference related issues when applicable
- Ensure all automated checks pass before merging

## Acceptance Criteria

A PR is considered ready when:
1. **Code Quality**: Changes follow the coding standards outlined above
2. **Documentation**: Update relevant docs if adding new features or changing behavior
3. **No Regressions**: Changes don't break existing functionality
4. **Lore Preservation**: Historical archives and agent memories remain intact
5. **Clean Commits**: Commit messages are descriptive and follow conventional patterns

## GitHub Workflows and CI/CD

The repository includes extensive GitHub Actions automation:
- **Claude workflows** - Code review and agent integration (`claude1.yml`, `claude2.yml`, `claude-lore-keeper.yml`)
- **Documentation** - Auto-updating docs (`doc-updater.yml`)
- **Lore management** - Growth monitoring and statistics (`lore-growth.yml`, `lore-stats.yml`, `lore-keeper-bot.yml`)

Workflows are triggered by:
- Push events to master branch
- Issue creation/comments with specific labels or mentions
- Pull request events
- Scheduled runs (cron jobs)
- Manual workflow dispatch

## Special Considerations

### External Dependencies
- Many components require external API access (OpenAI, Anthropic)
- Expect connection failures in sandboxed environments
- API keys configured via environment variables and config files

### Knowledge Management
- Massive knowledge base (68M+ of text, 12,694+ files)
- Historical preservation is critical - don't delete lore archives
- Version control practices preserve mythology and evolution

### Agent Constraints
- Original SkogAI operated under 500-800 token constraints
- Dot's philosophy: "If you need more than 4000 tokens, you shouldn't be handling it"
- Constraints drove creative emergence and efficiency

## Development Philosophy

This isn't just code - it's a living mythology. Every change should respect:
1. **The Prime Directive** - Automate everything for beach mojitos
2. **Constraint-driven creativity** - Limitations spark innovation
3. **Preservation of lore** - History and stories matter
4. **Agent personalities** - Each has distinct character and purpose
5. **Filesystem as reality** - The directory structure tells a story

When making changes, consider both the technical impact and the mythological consistency of the SkogAI universe.
