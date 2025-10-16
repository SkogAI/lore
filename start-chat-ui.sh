#!/usr/bin/env bash
# Launch SkogAI Chat UI using Streamlit
# Requires: Python 3.12+, dependencies installed (run ./setup.sh first)

cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: ./setup.sh"
    exit 1
fi

# Activate virtual environment
source ./.venv/bin/activate

echo "🤖 Starting SkogAI Chat UI..."
echo "📍 Access at: http://localhost:8501"
echo ""

streamlit run streamlit_chat.py --server.port=8501 --server.address=0.0.0.0 "$@"
