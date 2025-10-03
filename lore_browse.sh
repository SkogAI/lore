#!/usr/bin/env bash
# Interactive lore browser launcher

# Activate virtual environment if it exists
source .venv/bin/activate

# Run the TUI
python3 lore_tui.py "$@"
