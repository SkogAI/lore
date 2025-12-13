#!/bin/bash

# skogai-agent-small-service.sh
# A simple script to run the small model agent service 24/7
# Usage: ./skogai-agent-small-service.sh [model_name]

# Default model name
MODEL_NAME=${1:-"llama3.2"}

# Set up logging
LOG_DIR="./logs"
LOG_FILE="$LOG_DIR/skogai-agent-small.log"
mkdir -p $LOG_DIR

echo "Starting SkogAI Small Agent Service with model: $MODEL_NAME"
echo "$(date): Service started with model: $MODEL_NAME" >>$LOG_FILE

# Function to handle requests
process_request() {
  local topic="$1"
  local timestamp=$(date +%s)
  echo "$(date): Processing request for topic: $topic" >>$LOG_FILE

  # Run the workflow script
  python /mnt/extra/backup/skogai-old-all/demo/small_model_workflow.py "$topic" --model "$MODEL_NAME" 2>&1 | tee -a $LOG_FILE

  echo "$(date): Completed request for topic: $topic" >>$LOG_FILE
  echo "----------------------------------------" >>$LOG_FILE
}

# Create a simple named pipe to receive requests
PIPE_DIR="./pipes"
PIPE="$PIPE_DIR/skogai-agent-small-requests"
mkdir -p $PIPE_DIR

# Remove pipe if it already exists
[ -p $PIPE ] && rm $PIPE
# Create a new pipe
mkfifo $PIPE

echo "Request pipe created at $PIPE"
echo "$(date): Request pipe created at $PIPE" >>$LOG_FILE
echo "To submit a request, use: echo \"Your topic here\" > $PIPE" >>$LOG_FILE

# Check for model availability
echo "Checking model availability: $MODEL_NAME"
if ! ollama list | grep -q "$MODEL_NAME"; then
  echo "Model '$MODEL_NAME' not found. Attempting to pull it..."
  echo "$(date): Model '$MODEL_NAME' not found. Attempting to pull it..." >>$LOG_FILE

  # Try to pull the model
  ollama pull $MODEL_NAME

  if [ $? -ne 0 ]; then
    echo "Failed to pull model '$MODEL_NAME'. Please check model name or pull it manually."
    echo "$(date): Failed to pull model '$MODEL_NAME'. Service may not function correctly." >>$LOG_FILE
    echo "Available models:"
    ollama list
  else
    echo "Model '$MODEL_NAME' successfully pulled."
    echo "$(date): Model '$MODEL_NAME' successfully pulled." >>$LOG_FILE
  fi
else
  echo "Model '$MODEL_NAME' is available."
  echo "$(date): Model '$MODEL_NAME' is available." >>$LOG_FILE
fi

# Main service loop
while true; do
  echo "Waiting for requests..."

  if read topic <$PIPE; then
    if [ "$topic" == "exit" ] || [ "$topic" == "quit" ]; then
      echo "Received exit command. Shutting down service."
      echo "$(date): Service shutting down by request." >>$LOG_FILE
      break
    fi

    # Process the request in the background so we can accept new ones
    process_request "$topic" &
  fi

  # Small delay to prevent CPU overload
  sleep 1
done

# Clean up
rm $PIPE
echo "Service stopped."
echo "$(date): Service stopped." >>$LOG_FILE
