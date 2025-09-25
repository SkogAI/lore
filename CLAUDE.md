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