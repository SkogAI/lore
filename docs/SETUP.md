# Development Environment Setup

This guide explains how to set up the SkogAI Lore development environment.

## Prerequisites

- **Python 3.12 or higher** (Python 3.13 recommended for full compatibility)
- **Git** for version control
- **Optional:** [uv](https://github.com/astral-sh/uv) package manager for faster dependency management

## Quick Start

### Automated Setup (Recommended)

The easiest way to get started is using the setup script:

```bash
./setup.sh
```

This script will:
- Check your Python version
- Create a virtual environment in `.venv`
- Install all required dependencies
- Provide activation instructions

### Manual Setup

If you prefer to set up manually or the script fails:

#### Option 1: Using uv (Faster)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv

# Activate the environment
source .venv/bin/activate

# Install dependencies
uv pip install -e .
```

#### Option 2: Using standard pip/venv

```bash
# Create virtual environment
python3 -m venv .venv

# Activate the environment
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies (choose one)
pip install -e .                    # From pyproject.toml
# OR
pip install -r requirements.txt     # From requirements.txt (simpler)
```

## Activating the Virtual Environment

After setup, you need to activate the virtual environment before working:

```bash
source .venv/bin/activate
```

You'll know it's activated when your prompt shows `(.venv)` at the beginning.

### Auto-activation with direnv (Optional)

The repository includes a `.envrc` file for automatic activation using [direnv](https://direnv.net/):

```bash
# Install direnv (if not already installed)
# On macOS: brew install direnv
# On Ubuntu/Debian: sudo apt-get install direnv

# Allow direnv for this directory
direnv allow

# Now the venv activates automatically when you cd into the directory
```

## Verifying Installation

After setup, verify everything works:

```bash
# Activate the environment
source .venv/bin/activate

# Check Python location (should be in .venv)
which python

# Check installed packages
pip list

# Try importing key dependencies
python -c "import streamlit, anthropic, openai, textual; print('✓ All imports successful')"
```

## Running Applications

### Chat UI (Streamlit)

```bash
./start-chat-ui.sh
# Or manually:
streamlit run streamlit_chat.py --server.port=8501 --server.address=0.0.0.0
```

### Gradio Chat Interface

```bash
python skogai-chat.py
```

### Terminal UI for Lore Browsing

```bash
python lore_tui.py
```

### Agent Lore Generator

```bash
python generate-agent-lore.py
```

## Managing Dependencies

The repository provides two ways to manage dependencies:

1. **pyproject.toml** - Full project configuration (preferred for development)
2. **requirements.txt** - Simplified dependency list (good for quick setup)

Both files should be kept in sync when dependencies change.

### Adding New Dependencies

When adding a new dependency:

#### Using uv:
```bash
uv add package-name
uv lock
uv sync
```

#### Using pip:
```bash
pip install package-name
# Then update both pyproject.toml AND requirements.txt manually
```

### Updating Dependencies

#### Using uv:
```bash
uv lock --upgrade
uv sync
```

#### Using pip:
```bash
pip install --upgrade -e .
```

## Dependencies Overview

### Core Dependencies

- **streamlit** - Main chat UI framework
- **anthropic** - Claude API integration
- **openai** - OpenAI API integration
- **requests** - HTTP requests for API calls
- **textual** - Terminal UI framework
- **rich** - Rich text formatting in terminal
- **gradio** - Alternative UI framework
- **numpy** - Numerical computing support

### Optional Dependencies

Development tools can be installed with:
```bash
pip install -e ".[dev]"
```

## Troubleshooting

### Python Version Issues

If you get errors about Python version:
```bash
# Check your Python version
python3 --version

# Make sure it's 3.12 or higher
# If not, install a newer version
```

### Import Errors

If you get import errors:
```bash
# Make sure the venv is activated
source .venv/bin/activate

# Reinstall dependencies
pip install -e .
```

### Virtual Environment Not Found

If `.venv` doesn't exist:
```bash
# Run setup again
./setup.sh
```

### Permission Errors

If you get permission errors:
```bash
# Make sure setup script is executable
chmod +x setup.sh

# Then run it
./setup.sh
```

## Environment Variables

The repository uses environment variables for configuration. These are typically loaded from:

- `.envrc` - Local environment configuration (auto-loaded with direnv)
- `config/paths.sh` - Path configuration
- External config via `skogcli` tool (if installed)

Key environment variables:
- `CLAUDE_API_KEY` - Claude API key
- `OPENAI_API_KEY` - OpenAI API key
- `SKOGAI_LORE` - Lore directory path
- `SKOGAI_LOGS_DIR` - Logs directory path

## Next Steps

After setting up your environment:

1. Read [README.md](../README.md) for project overview
2. Read [CLAUDE.md](../CLAUDE.md) for development guidelines
3. Check [DOCUMENTATION.md](../DOCUMENTATION.md) for detailed documentation
4. Explore the `agents/` directory for agent implementations

## Getting Help

- Check the [documentation](../DOCUMENTATION.md)
- Review [CLAUDE.md](../CLAUDE.md) for coding standards
- Create an issue on GitHub for problems
- Check the `lorefiles/` for historical context
