# Technology Stack

## Languages

**Primary:**
- **Python 3.12+** - Core APIs, agents, orchestrator, and tools
- **Bash/Shell** - Primary operational interface, integrations, utilities
- **jq** - JSON querying and transformation (CRUD operations)

## Frameworks & Libraries

### Python Dependencies

**API Clients:**
- `anthropic>=0.68.0` - Anthropic Claude API integration
- `openai>=1.109.1` - OpenAI API integration
- `requests>=2.31.0` - HTTP client for API calls

**UI Frameworks:**
- `streamlit>=1.50.0` - Web-based UI framework
- `gradio>=5.48.0` - ML interface builder
- `textual>=1.0.0` - Terminal UI framework

**Data & Utilities:**
- `pyyaml>=6.0` - YAML parsing
- `numpy>=2.3.3` - Numerical computing
- `rich>=13.7.0` - Rich terminal formatting
- `click>=8.1.0` - CLI framework

**Build & Packaging:**
- `setuptools>=61.0` - Python packaging
- `wheel` - Wheel distribution format

## Build Tools & Package Managers

- **uv** - Primary Python package manager (with `uv.lock`)
- **pre-commit** - Git hook framework (v6.0.0+)
- **argc** - Bash argument parser (provides Argcfile.sh CLI)

## External CLI Tools

- `git` - Version control operations
- `jq` - JSON command-line processor (CRUD operations library)
- `ollama` - Local LLM inference (optional)
- `claude` CLI - Anthropic Claude command-line tool (optional)
- `curl` - HTTP requests for API calls

## Key Dependencies

**Core Technologies:**
- JSON files as primary data store (no database)
- Shell scripts as canonical interface (preferred over Python)
- LLM APIs (OpenRouter gateway architecture)
- Schema validation via JSON Schema
- Git integration for workflow automation
