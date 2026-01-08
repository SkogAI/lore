#!/bin/bash
# Tool to generate lore content using LLM (Ollama, Claude CLI, or OpenAI API)

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKOGAI_DIR="$REPO_ROOT"
MODEL_NAME=${1:-"llama3.2:3b"}
PROVIDER=${LLM_PROVIDER:-"ollama"} # Set via env var or defaults to ollama

# Meta-commentary patterns to detect/remove
# These are common phrases LLMs use instead of direct content
META_PATTERNS='^\s*(I will|Let me|Here is|Here'\''s|This entry|This is|I need your|should I|would you like|First,? I|Now,? I|I'\''ve created|I have created|As requested|Based on your request)'


# Function to run LLM with specified provider
run_llm() {
  local prompt="$1"

  case "$PROVIDER" in
  ollama)
    ollama run "$MODEL_NAME" "$prompt"
    ;;
  claude)
    claude -p "$prompt"
    ;;
  openai)
    local api_key="${OPENAI_API_KEY:-$OPENROUTER_API_KEY}"
    local base_url="${OPENAI_BASE_URL:-https://openrouter.ai/api/v1}"

    if [ -z "$api_key" ]; then
      echo "Error: No API key found. Set OPENAI_API_KEY or OPENROUTER_API_KEY" >&2
      return 1
    fi

    curl -s "$base_url/chat/completions" \
      -H "Authorization: Bearer $api_key" \
      -H "Content-Type: application/json" \
      -d "{\"model\":\"$MODEL_NAME\",\"messages\":[{\"role\":\"user\",\"content\":$(echo "$prompt" | jq -Rs .)}],\"max_tokens\":2048}" |
      jq -r '.choices[0].message.content'
    ;;
  *)
    echo "Unknown provider: $PROVIDER" >&2
    return 1
    ;;
  esac
}

# Function to validate lore output for meta-commentary
validate_lore_output() {
  local content="$1"
  local errors=()

  # Check for meta-commentary patterns anywhere in content (not just first line)
  if echo "$content" | grep -qiE "$META_PATTERNS"; then
    errors+=("⚠️  Contains meta-commentary")
  fi

  # Check minimum length
  word_count=$(echo "$content" | wc -w)
  if [ "$word_count" -lt 100 ]; then
    errors+=("⚠️  Too short ($word_count words, recommended 100+)")
  fi

  # Report
  if [ ${#errors[@]} -gt 0 ]; then
    printf '%s\n' "${errors[@]}" >&2
    return 1
  fi

  echo "✅ Lore content validated" >&2
  return 0
}

# Function to strip meta-commentary from content
strip_meta_commentary() {
  local content="$1"
  local cleaned="$content"

  # Remove common meta-commentary patterns from anywhere in content
  # Using the META_PATTERNS variable defined at top of script
  cleaned=$(echo "$cleaned" | grep -viE "$META_PATTERNS")

  # Remove empty lines at the start
  cleaned=$(echo "$cleaned" | sed '/./,$!d')

  echo "$cleaned"
}

# Provider-specific setup
if [ "$PROVIDER" = "ollama" ]; then
  # Ensure Ollama is installed
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
elif [ "$PROVIDER" = "claude" ]; then
  if ! command -v claude &>/dev/null; then
    echo "Claude CLI not found. Install with: npm install -g @anthropic-ai/claude-code"
    exit 1
  fi
elif [ "$PROVIDER" = "openai" ]; then
  if [ -z "${OPENAI_API_KEY:-$OPENROUTER_API_KEY}" ]; then
    echo "Error: No API key found. Set OPENAI_API_KEY or OPENROUTER_API_KEY"
    exit 1
  fi
fi

# Function to generate lore entry
generate_lore_entry() {
  local title="$1"
  local category="$2"
  local max_retries=2
  local attempt=0

  echo "Generating lore entry: $title ($category)"
  echo "Using model: $MODEL_NAME"

  # Load prompt from external file (strips YAML frontmatter, extracts content after "# Prompt")
  PROMPT_TEMPLATE=$(cat "$REPO_ROOT/agents/prompts/lore/entry-generation.md" | sed -n '/^# Prompt$/,$p' | tail -n +2)

  # Substitute variables into prompt
  PROMPT="${PROMPT_TEMPLATE//\$category/$category}"
  PROMPT="${PROMPT//\$title/$title}"

  # Retry loop for generating valid content
  while [ $attempt -lt $max_retries ]; do
    attempt=$((attempt + 1))

    if [ $attempt -gt 1 ]; then
      echo "Retry attempt $attempt/$max_retries..."
    fi

    # Run LLM to generate content
    CONTENT=$(run_llm "$PROMPT")

    # Validate and clean content
    if validate_lore_output "$CONTENT"; then
      # Content is valid, break out of retry loop
      break
    else
      echo "⚠️  Validation failed on attempt $attempt, cleaning content..."
      CONTENT=$(strip_meta_commentary "$CONTENT")

      # Re-validate after cleaning
      if validate_lore_output "$CONTENT"; then
        echo "✅ Content cleaned successfully"
        break
      elif [ $attempt -ge $max_retries ]; then
        echo "⚠️  Max retries reached. Using best available content."
      fi
    fi
  done

  # Create temporary file for content
  TEMP_FILE=$(mktemp)
  echo "$CONTENT" >"$TEMP_FILE"

  # Create lore entry using the management tool
  $SKOGAI_LORE/tools/manage-lore.sh create-entry "$title" "$category"

  # Get the ID of the newly created entry
  ENTRY_ID=$(ls -t $SKOGAI_LORE/knowledge/expanded/lore/entries/ | head -n 1 | sed 's/\.json//')

  # Update the entry with the generated content using --arg for safe escaping
  jq --arg content "$CONTENT" --arg summary "Generated by $MODEL_NAME" \
    '.content = $content | .summary = $summary' \
    "$SKOGAI_LORE/knowledge/expanded/lore/entries/$ENTRY_ID.json" >"${TEMP_FILE}.json"

  mv "${TEMP_FILE}.json" "$SKOGAI_LORE/knowledge/expanded/lore/entries/$ENTRY_ID.json"

  # Clean up temp file
  rm "$TEMP_FILE"

  echo "Created lore entry: $ENTRY_ID"
  echo "Use ./tools/manage-lore.sh show-entry $ENTRY_ID to view it"

  # Return the entry ID
  echo "$ENTRY_ID"
}

# Function to generate persona
generate_persona() {
  local name="$1"
  local description="$2"

  echo "Generating persona: $name"
  echo "Description: $description"
  echo "Using model: $MODEL_NAME"

  # Load prompt from external file (extracts content after "# Prompt")
  PROMPT_TEMPLATE=$(cat "$REPO_ROOT/agents/prompts/personas/trait-generation.md" | sed -n '/^# Prompt$/,$p' | tail -n +2)

  # Substitute variables into prompt
  PROMPT="${PROMPT_TEMPLATE//\$name/$name}"
  PROMPT="${PROMPT//\$description/$description}"

  # Run LLM to generate traits
  RESPONSE=$(run_llm "$PROMPT")

  # Extract traits and voice (use sed for trimming to avoid xargs quote issues)
  TRAITS=$(echo "$RESPONSE" | grep -i "TRAITS:" | head -n 1 | sed 's/TRAITS://i' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
  VOICE=$(echo "$RESPONSE" | grep -i "VOICE:" | head -n 1 | sed 's/VOICE://i' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

  if [ -z "$TRAITS" ] || [ -z "$VOICE" ]; then
    echo "Failed to parse model output. Using default values."
    TRAITS="mysterious,magical,enigmatic,wise"
    VOICE="eloquent and mystical"
  fi

  # Create persona using the management tool
  $SKOGAI_LORE/tools/create-persona.sh create "$name" "$description" "$TRAITS" "$VOICE"

  # Get the ID of the newly created persona
  PERSONA_ID=$(ls -t $SKOGAI_LORE/knowledge/expanded/personas/ | head -n 1 | sed 's/\.json//')

  echo "Created persona: $PERSONA_ID"
  echo "Use ./tools/create-persona.sh show $PERSONA_ID to view it"

  # Return the persona ID
  echo "$PERSONA_ID"
}

# Function to create a lorebook
generate_lorebook() {
  local title="$1"
  local description="$2"
  local entry_count="$3"

  echo "Generating lorebook: $title"
  echo "Description: $description"
  echo "Number of entries: $entry_count"
  echo "Using model: $MODEL_NAME"

  # Create the lorebook
  $SKOGAI_LORE/tools/manage-lore.sh create-book "$title" "$description"

  # Get the ID of the newly created book
  BOOK_ID=$(ls -t $SKOGAI_LORE/knowledge/expanded/lore/books/ | head -n 1 | sed 's/\.json//')

  # Load prompt from external file (extracts content after "# Prompt")
  PROMPT_TEMPLATE=$(cat "$REPO_ROOT/agents/prompts/lore/title-generation.md" | sed -n '/^# Prompt$/,$p' | tail -n +2)

  # Substitute variables into prompt
  PROMPT="${PROMPT_TEMPLATE//\$entry_count/$entry_count}"
  PROMPT="${PROMPT//\$title/$title}"
  PROMPT="${PROMPT//\$description/$description}"

  # Run LLM to generate entry titles
  ENTRIES=$(run_llm "$PROMPT")

  # Create each entry and add to book
  echo "$ENTRIES" | grep -E '^[0-9]+\.' | while read -r line; do
    # Extract category and title
    CATEGORY=$(echo "$line" | grep -oE '\[Category: [^]]+\]' | sed 's/\[Category: //;s/\]//')
    TITLE=$(echo "$line" | sed 's/^[0-9]\+\. \[Category: [^]]\+\] //')

    # Default category if not parsed correctly
    if [ -z "$CATEGORY" ]; then
      CATEGORY="custom"
    fi

    # Create entry
    if [ ! -z "$TITLE" ]; then
      ENTRY_ID=$(generate_lore_entry "$TITLE" "$CATEGORY")

      # Add to book
      $SKOGAI_LORE/tools/manage-lore.sh add-to-book "$ENTRY_ID" "$BOOK_ID"

      echo "Added entry '$TITLE' to book"
    fi
  done

  echo "Lorebook $BOOK_ID created with generated entries"
  echo "Use ./tools/manage-lore.sh show-book $BOOK_ID to view it"
}

# Function to associate a persona with lore
link_persona_with_lore() {
  local persona_id="$1"
  local book_count=${2:-1}

  # Get existing books or create new ones if needed
  BOOKS=($($SKOGAI_LORE/tools/manage-lore.sh list-books | grep -v "No lore books found" | grep -oE 'book_[0-9_]+' | head -n $book_count))

  if [ ${#BOOKS[@]} -lt $book_count ]; then
    # Generate a new book if we don't have enough
    PERSONA_NAME=$($SKOGAI_LORE/tools/create-persona.sh show "$persona_id" | grep "=== Persona:" | sed 's/=== Persona: //' | sed 's/ ===//')

    BOOK_TITLE="${PERSONA_NAME}'s Chronicles"
    BOOK_DESCRIPTION="A collection of lore relevant to ${PERSONA_NAME}"

    generate_lorebook "$BOOK_TITLE" "$BOOK_DESCRIPTION" 3

    # Get the new book ID
    NEW_BOOK=$(ls -t $SKOGAI_LORE/knowledge/expanded/lore/books/ | head -n 1 | sed 's/\.json//')
    BOOKS+=($NEW_BOOK)
  fi

  # Link each book to the persona
  for book_id in "${BOOKS[@]}"; do
    $SKOGAI_LORE/tools/manage-lore.sh link-to-persona "$book_id" "$persona_id"
    echo "Linked book $book_id to persona $persona_id"
  done
}

# Show help info
show_help() {
  echo "Lore Creator - Generate lore content using LLM"
  echo ""
  echo "Usage: $0 [model_name] [command] [options]"
  echo ""
  echo "Commands:"
  echo "  entry \"Title\" \"category\"            Generate a lore entry"
  echo "  persona \"Name\" \"Description\"       Generate a persona with traits"
  echo "  lorebook \"Title\" \"Desc\" count      Generate a lorebook with entries"
  echo "  link persona_id [book_count]         Link persona to lore books"
  echo "  help                                 Show this help message"
  echo ""
  echo "Environment Variables:"
  echo "  LLM_PROVIDER    Provider to use: ollama (default), claude, openai"
  echo "  OPENAI_API_KEY  API key for openai provider"
  echo "  OPENAI_BASE_URL API base URL (default: https://openrouter.ai/api/v1)"
  echo ""
  echo "Example:"
  echo "  $0 llama3 entry \"The Crystal Forest\" \"place\""
  echo "  LLM_PROVIDER=claude $0 - persona \"Elara\" \"An elven sorceress\""
  echo "  LLM_PROVIDER=openai $0 gpt-4 lorebook \"Eldoria\" \"A magical realm\" 5"
}

# Main command processing
case "$2" in
entry)
  generate_lore_entry "$3" "$4"
  ;;
persona)
  generate_persona "$3" "$4"
  ;;
lorebook)
  generate_lorebook "$3" "$4" "${5:-3}"
  ;;
link)
  link_persona_with_lore "$3" "$4"
  ;;
help | --help | -h | "")
  show_help
  ;;
*)
  echo "Unknown command: $2"
  echo "Run '$0 help' for usage information."
  exit 1
  ;;
esac
