#!/bin/bash
# Daemon service for continuous lore generation
# Similar to skogai-agent-small-service.sh but for lore generation

set -e

# SKOGAI_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKOGAI_DIR="/home/skogix/lore/"
MODEL_NAME=${1:-"llama3.2:3b"}
PIPE_NAME="skogai-lore-generator"
PIPE_PATH="/tmp/${PIPE_NAME}"
GENERATION_INTERVAL=${2:-"600"} # Default: 10 minutes between generations
HISTORY_DIR="${SKOGAI_DIR}/logs/lore_generation"
MAX_HISTORY_FILES=50

mkdir -p "${HISTORY_DIR}"

# Check if Ollama is installed
if ! command -v ollama &>/dev/null; then
  echo "Ollama not found. Please install it first:"
  echo "curl -fsSL https://ollama.com/install.sh | sh"
  exit 1
fi

# Check if model exists
if ! ollama list | grep -q "$MODEL_NAME"; then
  echo "Model '$MODEL_NAME' not found. Pulling it now..."
  ollama pull $MODEL_NAME
fi

# Create named pipe if it doesn't exist
if [ ! -p "${PIPE_PATH}" ]; then
  mkfifo "${PIPE_PATH}"
  chmod 660 "${PIPE_PATH}"
  echo "Created named pipe: ${PIPE_PATH}"
fi

echo "Starting SkogAI Lore Generator Service with model: $MODEL_NAME"
echo "Generation interval: ${GENERATION_INTERVAL} seconds"
echo "Send commands through the pipe: ${PIPE_PATH}"
echo "Commands: generate-entry, generate-book, generate-persona, stop"

# Cleanup function
cleanup() {
  echo "Cleaning up..."
  rm -f "${PIPE_PATH}"
  exit 0
}

trap cleanup EXIT INT TERM

# Generate random lore entry
generate_random_entry() {
  # Get list of categories
  CATEGORIES=("character" "place" "object" "event" "concept" "custom")
  RANDOM_CATEGORY=${CATEGORIES[$RANDOM % ${#CATEGORIES[@]}]}

  # Generate a random title using the model
  TITLE_PROMPT="Generate a single creative title for a fantasy/sci-fi $RANDOM_CATEGORY. Respond with only the title, nothing else."
  RANDOM_TITLE=$(ollama run $MODEL_NAME "$TITLE_PROMPT" | tr -d '\n')

  # Generate the entry
  echo "Generating random entry: $RANDOM_TITLE ($RANDOM_CATEGORY)"
  "${SKOGAI_DIR}/tools/llama-lore-creator.sh" $MODEL_NAME entry "$RANDOM_TITLE" "$RANDOM_CATEGORY"
}

# Generate random lorebook
generate_random_book() {
  # Generate a random title and description using the model
  TITLE_PROMPT="Generate a creative name for a fantasy/sci-fi world or setting. Respond with only the name, nothing else."
  RANDOM_TITLE=$(ollama run $MODEL_NAME "$TITLE_PROMPT" | tr -d '\n')

  DESC_PROMPT="Write a short one-sentence description for a fantasy/sci-fi setting called '$RANDOM_TITLE'. Be creative and evocative."
  RANDOM_DESC=$(ollama run $MODEL_NAME "$DESC_PROMPT" | tr -d '\n')

  # Generate random number of entries (3-7)
  ENTRY_COUNT=$((3 + RANDOM % 5))

  # Generate the book
  echo "Generating random book: $RANDOM_TITLE - $RANDOM_DESC ($ENTRY_COUNT entries)"
  "${SKOGAI_DIR}/tools/llama-lore-creator.sh" $MODEL_NAME lorebook "$RANDOM_TITLE" "$RANDOM_DESC" $ENTRY_COUNT
}

# Generate random persona with lore
generate_random_persona() {
  # Generate a random name and description
  NAME_PROMPT="Generate a creative character name for a fantasy/sci-fi setting. Respond with only the name, nothing else."
  RANDOM_NAME=$(ollama run $MODEL_NAME "$NAME_PROMPT" | tr -d '\n')

  DESC_PROMPT="Write a short one-sentence description for a character named '$RANDOM_NAME'. Be creative and evocative."
  RANDOM_DESC=$(ollama run $MODEL_NAME "$DESC_PROMPT" | tr -d '\n')

  # Generate the persona
  echo "Generating random persona: $RANDOM_NAME - $RANDOM_DESC"
  PERSONA_ID=$("${SKOGAI_DIR}/tools/llama-lore-creator.sh" $MODEL_NAME persona "$RANDOM_NAME" "$RANDOM_DESC" | grep "Created persona" | grep -o "persona_[0-9_]*")

  # Generate a lorebook and link it
  "${SKOGAI_DIR}/tools/llama-lore-creator.sh" $MODEL_NAME link "$PERSONA_ID" "1"
}

# Generate history timestamp
get_timestamp() {
  date +"%Y%m%d_%H%M%S"
}

# Save generation history
save_history() {
  local content="$1"
  local timestamp=$(get_timestamp)
  local history_file="${HISTORY_DIR}/lore_generation_${timestamp}.log"

  echo "$content" >"$history_file"

  # Limit number of history files
  if [ $(ls -1 "${HISTORY_DIR}" | wc -l) -gt $MAX_HISTORY_FILES ]; then
    rm "$(ls -1t "${HISTORY_DIR}" | tail -1)"
  fi
}

# Set default generation probability weights
ENTRY_WEIGHT=20
BOOK_WEIGHT=10
PERSONA_WEIGHT=5

# Main service loop
while true; do
  # Check for commands from the pipe (non-blocking)
  if read -t 0.1 line <"${PIPE_PATH}"; then
    case "$line" in
    generate-entry)
      OUTPUT=$(generate_random_entry)
      echo "$OUTPUT"
      save_history "$OUTPUT"
      ;;
    generate-book)
      OUTPUT=$(generate_random_book)
      echo "$OUTPUT"
      save_history "$OUTPUT"
      ;;
    generate-persona)
      OUTPUT=$(generate_random_persona)
      echo "$OUTPUT"
      save_history "$OUTPUT"
      ;;
    stop)
      echo "Stopping service..."
      exit 0
      ;;
    set-interval)
      VALUE=$(echo "$line" | cut -d' ' -f2)
      if [[ "$VALUE" =~ ^[0-9]+$ ]] && [ "$VALUE" -ge 60 ]; then
        GENERATION_INTERVAL=$VALUE
        echo "Generation interval set to $GENERATION_INTERVAL seconds"
      else
        echo "Invalid interval. Must be at least 60 seconds."
      fi
      ;;
    set-weights)
      E=$(echo "$line" | cut -d' ' -f2)
      B=$(echo "$line" | cut -d' ' -f3)
      P=$(echo "$line" | cut -d' ' -f4)
      if [[ "$E" =~ ^[0-9]+$ ]] && [[ "$B" =~ ^[0-9]+$ ]] && [[ "$P" =~ ^[0-9]+$ ]]; then
        ENTRY_WEIGHT=$E
        BOOK_WEIGHT=$B
        PERSONA_WEIGHT=$P
        echo "Generation weights set to: Entry=$ENTRY_WEIGHT, Book=$BOOK_WEIGHT, Persona=$PERSONA_WEIGHT"
      else
        echo "Invalid weights. Must be positive integers."
      fi
      ;;
    *)
      echo "Unknown command: $line"
      echo "Available commands: generate-entry, generate-book, generate-persona, stop, set-interval [seconds], set-weights [entry] [book] [persona]"
      ;;
    esac
  fi

  # Automatic generation based on interval
  if [ ! -f "/tmp/.lore_generation_disabled" ]; then
    # Use weighted random selection
    TOTAL_WEIGHT=$((ENTRY_WEIGHT + BOOK_WEIGHT + PERSONA_WEIGHT))
    RANDOM_VALUE=$((RANDOM % TOTAL_WEIGHT))

    OUTPUT=""
    if [ $RANDOM_VALUE -lt $ENTRY_WEIGHT ]; then
      echo "Scheduled generation: Entry"
      OUTPUT=$(generate_random_entry)
    elif [ $RANDOM_VALUE -lt $((ENTRY_WEIGHT + BOOK_WEIGHT)) ]; then
      echo "Scheduled generation: Book"
      OUTPUT=$(generate_random_book)
    else
      echo "Scheduled generation: Persona with Lore"
      OUTPUT=$(generate_random_persona)
    fi

    echo "$OUTPUT"
    save_history "$OUTPUT"

    echo "Next generation in $GENERATION_INTERVAL seconds..."
    sleep $GENERATION_INTERVAL
  else
    # Just wait a bit and check for commands again
    sleep 5
  fi
done
