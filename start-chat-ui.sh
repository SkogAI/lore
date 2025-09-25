#!/bin/bash
source ./.venv/bin/activate
# Launch SkogAI Chat UI using Streamlit
cd "$(dirname "$0")"

# Set path to streamlit executable
# STREAMLIT_PATH="$HOME/.local/share/uv/tools/pip/bin/streamlit"

echo "Starting SkogAI Chat..."
streamlit run streamlit_chat.py --server.port=8501 --server.address=0.0.0.0 "$@"
