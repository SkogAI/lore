#!/usr/bin/env bash
# Setup script for SkogAI Lore repository
# This script sets up the Python virtual environment and installs all dependencies

set -e

echo "🤖 SkogAI Lore - Development Environment Setup"
echo "=============================================="
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

echo "✓ Found Python $PYTHON_VERSION"

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 12 ]); then
    echo "❌ Error: Python 3.12 or higher is required"
    echo "   Current version: $PYTHON_VERSION"
    exit 1
fi

# Check if uv is available
if command -v uv &> /dev/null; then
    echo "✓ Found uv package manager"
    USE_UV=true
else
    echo "ℹ uv package manager not found, using standard pip/venv"
    USE_UV=false
fi

echo ""
echo "Setting up virtual environment..."

# Setup virtual environment based on available tools
if [ "$USE_UV" = true ]; then
    echo "Using uv for virtual environment setup..."
    
    # Create venv if it doesn't exist
    if [ ! -d ".venv" ]; then
        uv venv
    fi
    
    # Install dependencies
    echo "Installing dependencies with uv..."
    uv pip sync uv.lock 2>/dev/null || uv pip install -e .
    
else
    echo "Using standard Python venv..."
    
    # Create virtual environment if it doesn't exist
    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
    fi
    
    # Activate virtual environment
    source .venv/bin/activate
    
    # Upgrade pip
    echo "Upgrading pip..."
    pip install --upgrade pip --no-warn-script-location
    
    # Install dependencies
    echo "Installing dependencies..."
    # Try pyproject.toml first, fallback to requirements.txt
    if pip install -e . 2>/dev/null; then
        echo "✓ Installed from pyproject.toml"
    elif [ -f "requirements.txt" ]; then
        echo "ℹ Falling back to requirements.txt"
        pip install -r requirements.txt
    else
        echo "❌ Error: Could not install dependencies"
        exit 1
    fi
    
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source .venv/bin/activate"
echo ""
echo "To start the chat UI, run:"
echo "  ./start-chat-ui.sh"
echo ""
echo "For more information, see README.md and CLAUDE.md"
