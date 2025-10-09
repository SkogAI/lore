# 🚀 SkogAI Lore - Quick Start Guide

Get up and running with SkogAI Lore in 5 minutes.

## Prerequisites

- Python 3.12+ ([Download](https://www.python.org/downloads/))
- Git ([Download](https://git-scm.com/downloads))

## Setup (3 commands)

```bash
# 1. Clone the repository
git clone https://github.com/SkogAI/lore.git && cd lore

# 2. Run setup script
./setup.sh

# 3. Activate environment
source .venv/bin/activate
```

## Run Applications

### Start Chat UI (Streamlit)
```bash
./start-chat-ui.sh
```
Opens at: http://localhost:8501

### Alternative: Gradio Chat
```bash
python skogai-chat.py
```

### Terminal Lore Browser
```bash
python lore_tui.py
```

### Generate Agent Lore
```bash
python generate-agent-lore.py
```

## Common Tasks

### Add a Dependency
```bash
# Option 1: With uv (fast)
uv add package-name && uv lock && uv sync

# Option 2: With pip (standard)
pip install package-name
# Then update pyproject.toml AND requirements.txt
```

### Update Dependencies
```bash
# With uv
uv lock --upgrade && uv sync

# With pip
pip install --upgrade -r requirements.txt
```

### Test Your Setup
```bash
python test_imports.py
```

### Check Python Environment
```bash
which python    # Should show .venv/bin/python
pip list        # Show installed packages
```

## Troubleshooting

### Setup Script Fails?
```bash
# Manual setup
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Import Errors?
```bash
# Reinstall dependencies
source .venv/bin/activate
pip install -r requirements.txt
```

### Wrong Python Version?
```bash
python3 --version  # Should be 3.12+
# Install newer Python if needed
```

## Need More Help?

- **Detailed Setup**: See [docs/SETUP.md](docs/SETUP.md)
- **Development Guide**: See [CLAUDE.md](CLAUDE.md)
- **Full Documentation**: See [DOCUMENTATION.md](DOCUMENTATION.md)
- **Issues**: Create an issue on GitHub

## The Prime Directive

> *"Automate EVERYTHING so we can drink mojitos on a beach"*

Welcome to the SkogAI multiverse! 🤖🏖️
