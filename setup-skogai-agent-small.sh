#!/bin/bash

# setup-skogai-agent-small.sh
# Script to set up the SkogAI Small Agent Service as a user service

echo "Setting up SkogAI Small Agent Service..."

# Check if Ollama is installed
if ! command -v ollama &>/dev/null; then
  echo "Ollama is not installed. Please install it first."
  echo "Visit https://ollama.com/download for installation instructions."
  exit 1
fi

# Check if the llama3 model is available
if ! ollama list | grep -q "llama3"; then
  echo "Pulling llama3 model..."
  ollama pull llama3

  if [ $? -ne 0 ]; then
    echo "Failed to pull llama3 model. Please check your internet connection and try again."
    exit 1
  fi

  echo "llama3 model successfully pulled."
else
  echo "llama3 model is already available."
fi

# Create directories
mkdir -p ./skogai/logs
mkdir -p ./skogai/pipes

# Make sure the service script is executable
chmod +x ./skogai-agent-small-service.sh
chmod +x ./skogai-agent-small-client.sh

# Ensure user systemd directory exists
mkdir -p ~/.config/systemd/user/

# Copy the service file to user systemd directory
cp ./skogai-agent-small.service ~/.config/systemd/user/

# Reload user systemd
systemctl --user daemon-reload

echo "Would you like to enable and start the service now? (y/n)"
read start_now

if [[ "$start_now" =~ ^[Yy]$ ]]; then
  # Enable the service to start at login
  systemctl --user enable skogai-agent-small

  # Start the service
  systemctl --user start skogai-agent-small

  echo "Service is now running. Check status with: systemctl --user status skogai-agent-small"

  # Enable lingering so the service runs even when you're not logged in
  loginctl enable-linger $(whoami)
  echo "Service will continue running even after logout (lingering enabled)"
else
  echo "You can start the service manually with: systemctl --user start skogai-agent-small"
fi

echo "You can now use the client to send requests:"
echo "./skogai-agent-small-client.sh \"Your topic here\""

echo "Setup complete!"

