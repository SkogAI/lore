#!/bin/bash
# Interactive lore browser launcher

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the TUI
python3 lore_tui.py "$@"
