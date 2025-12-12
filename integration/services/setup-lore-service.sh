#!/bin/bash
# Setup script for the lore generation service

set -e

# SKOGAI_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKOGAI_DIR=$SKOGAI_LORE/integration/services
SERVICE_NAME="skogai-lore-service"
MODEL=${1:-"llama3.2"}
INTERVAL=${2:-"600"}

# Ensure Ollama is installed
if ! command -v ollama &>/dev/null; then
  echo "Ollama not found. Please install it first:"
  echo "curl -fsSL https://ollama.com/install.sh | sh"
  exit 1
fi

# Check if model exists
# if ! ollama list | grep -q "$MODEL"; then
#   echo "Model '$MODEL' not found. Pulling it now..."
#   ollama pull $MODEL
# fi

# Ensure log directory exists
mkdir -p "${SKOGAI_DIR}/logs/lore_generation"

# Ensure user systemd directory exists
mkdir -p "$HOME/.config/systemd/user"

# Create named pipe if it doesn't exist
PIPE_PATH="/tmp/skogai-lore-generator"
if [ ! -p "${PIPE_PATH}" ]; then
  mkfifo "${PIPE_PATH}"
  chmod 660 "${PIPE_PATH}"
  echo "Created named pipe: ${PIPE_PATH}"
fi

# Check if service is already installed
if [ -f "$HOME/.config/systemd/user/${SERVICE_NAME}.service" ]; then
  echo "Service already installed. Stopping and removing..."
  systemctl --user stop "${SERVICE_NAME}.service" || true
  systemctl --user disable "${SERVICE_NAME}.service" || true
  rm "$HOME/.config/systemd/user/${SERVICE_NAME}.service"
fi

# Copy service file
cp "${SKOGAI_DIR}/${SERVICE_NAME}.service" "$HOME/.config/systemd/user/"

# Update service file with correct paths
sed -i "s|WorkingDirectory=.*|WorkingDirectory=${SKOGAI_DIR}|g" "$HOME/.config/systemd/user/${SERVICE_NAME}.service"
sed -i "s|ExecStart=.*|ExecStart=${SKOGAI_DIR}/${SERVICE_NAME}.sh ${MODEL} ${INTERVAL}|g" "$HOME/.config/systemd/user/${SERVICE_NAME}.service"
# Remove User and Group directives (not needed for user services)
sed -i '/User=/d' "$HOME/.config/systemd/user/${SERVICE_NAME}.service"
sed -i '/Group=/d' "$HOME/.config/systemd/user/${SERVICE_NAME}.service"

# Reload systemd
systemctl --user daemon-reload

# Start and enable service
systemctl --user start "${SERVICE_NAME}.service"
systemctl --user enable "${SERVICE_NAME}.service"

# Enable lingering if not already enabled (allows service to run when user not logged in)
loginctl enable-linger $(whoami) 2>/dev/null || true

echo "Service ${SERVICE_NAME} installed and started with model ${MODEL}"
echo "Generation interval: ${INTERVAL} seconds"
echo "Logs can be viewed with: journalctl --user -u ${SERVICE_NAME} -f"
echo "Commands can be sent with: echo 'command' > ${PIPE_PATH}"
echo "Available commands: generate-entry, generate-book, generate-persona, stop"
echo "Configure with: echo 'set-interval 300' > ${PIPE_PATH}"
echo "                echo 'set-weights 20 10 5' > ${PIPE_PATH}"
