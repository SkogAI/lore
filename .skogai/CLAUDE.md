# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Test Commands
- Start chat UI: `./start-chat-ui.sh` or `streamlit run streamlit_chat.py`
- Run small model workflow: `python demo/small_model_workflow.py`
- Run UI demo: `python demo/chat_ui_demo.py`
- Test agent API functionality: `python agents/api/agent_api.py`
- Tests: Manual verification (no formal test framework)

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

## Discovered Workflows

### GitHub Issue Creation
When creating GitHub issues, use the `gh` CLI tool with proper formatting:
```bash
gh issue create --repo SkogAI/lore --title "Title" --body "$(cat <<'EOF'
Body with proper formatting
EOF
)"
```
Evidence: Successfully created issue #4 addressing branch naming inconsistencies

### Session Handover Documentation
When ending a session, create/update `docs/handover.md` with:
- What was accomplished
- Context for next session
- Active session IDs
- Repository state
- Next steps

This ensures smooth continuation between work sessions.