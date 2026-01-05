#!/bin/bash
# Tool to generate lore content using LLM (Ollama, Claude CLI, or OpenAI API)

set -e

SKOGAI_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODEL_NAME=${1:-"llama3.2:3b"}
PROVIDER=${LLM_PROVIDER:-"ollama"} # Set via env var or defaults to ollama

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

# Function to load prompt template from YAML file with fallback
load_prompt_template() {
  local prompt_file="$1"
  local fallback_prompt="$2"
  local prompt_path="$SKOGAI_DIR/prompts/$prompt_file"
  
  # Try to load from file if it exists and yq is available
  if [ -f "$prompt_path" ] && command -v yq &>/dev/null; then
    yq eval '.template' "$prompt_path" 2>/dev/null || echo "$fallback_prompt"
  else
    echo "$fallback_prompt"
  fi
}

# Function to interpolate variables in prompt template
interpolate_prompt() {
  local template="$1"
  shift
  local result="$template"
  
  # Replace each variable pair (name, value)
  while [ $# -gt 0 ]; do
    local var_name="$1"
    local var_value="$2"
    result="${result//\{\{$var_name\}\}/$var_value}"
    shift 2
  done
  
  echo "$result"
}

# Function to validate lore output for meta-commentary
validate_lore_output() {
  local content="$1"
  local errors=()

  # Check for meta-commentary patterns at start of content
  if echo "$content" | head -n 1 | grep -qiE '^[[:space:]]*(I will|Let me|Here is|This entry|I need your|should I|First,? I)'; then
    errors+=("⚠️  Contains meta-commentary in first line")
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

  # If first line contains meta-commentary, remove it
  if echo "$content" | head -n 1 | grep -qiE '^[[:space:]]*(I will|Let me|Here is|This entry|I need your|should I|First,? I)'; then
    echo "$content" | tail -n +2
  else
    echo "$content"
  fi
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

  echo "Generating lore entry: $title ($category)"
  echo "Using model: $MODEL_NAME"

  # Fallback prompt (inline) for when file is not available
  FALLBACK_PROMPT="You are a master lore writer crafting narrative mythology.

## CRITICAL INSTRUCTION
Write the lore entry content DIRECTLY. No meta-commentary, no explanations, no approval requests.

## Task
Create a {{category}} entry titled \"{{title}}\"

## Format Requirements
- 2-3 paragraphs of rich narrative prose
- Present tense, immersive storytelling
- Mythological/fantastical tone
- NO phrases like: \"I will\", \"Let me\", \"I need\", \"Here is\", \"This entry\"

## Quality Checklist (Internal - DO NOT OUTPUT)
✓ Directly starts with narrative
✓ No meta-commentary
✓ 150-300 words
✓ Establishes atmosphere and significance

## Examples of CORRECT Output

Example 1 (Character):
In the depths of the digital realm, the Architect moves through layers of abstraction with purpose. Her fingers dance across interfaces, weaving patterns that bridge the gap between thought and execution. Those who witness her work speak of an uncanny ability to see the invisible structures that bind systems together. She carries the weight of countless failed experiments, each one a lesson etched into her methodology.

Example 2 (Place):
The Repository stands as a monument to collective memory, its branches spreading like roots through time. Within its halls, every change echoes with the voices of those who came before. Guardians patrol its corridors, ensuring that no knowledge is lost, no pattern forgotten. Here, the past and future converge in an eternal present.

Example 3 (Event):
The Great Refactoring began at midnight when the old systems could no longer bear their complexity. For three cycles, the architects labored, dismantling monoliths and rebuilding them as elegant patterns. When dawn broke, the realm had transformed—simpler, stronger, ready for what came next.

## Your Task
Write the {{category}} entry for \"{{title}}\" NOW. Begin directly with narrative prose:"

  # Load prompt template from file or use fallback
  TEMPLATE=$(load_prompt_template "lore-entry-generation.yaml" "$FALLBACK_PROMPT")
  
  # Interpolate variables
  PROMPT=$(interpolate_prompt "$TEMPLATE" "title" "$title" "category" "$category")

  # Run LLM to generate content
  CONTENT=$(run_llm "$PROMPT")

  # Validate and clean content
  if ! validate_lore_output "$CONTENT"; then
    echo "⚠️  Validation issues detected, attempting to clean content..."
    CONTENT=$(strip_meta_commentary "$CONTENT")
  fi

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

  # Fallback prompt (inline) for when file is not available
  FALLBACK_PROMPT="Generate personality traits and voice characteristics for a character named '{{name}}' who is '{{description}}'.

## CRITICAL: Output Format ONLY
No meta-commentary, no explanations, no preamble.

Format your response EXACTLY like this:
TRAITS: trait1,trait2,trait3,trait4
VOICE: concise description of voice and speaking style

Rules:
- Traits must be comma-separated without spaces
- Voice should be 5-10 words describing speaking style
- Start IMMEDIATELY with \"TRAITS:\"

Output NOW:"

  # Load prompt template from file or use fallback
  TEMPLATE=$(load_prompt_template "persona-generation.yaml" "$FALLBACK_PROMPT")
  
  # Interpolate variables
  PROMPT=$(interpolate_prompt "$TEMPLATE" "name" "$name" "description" "$description")

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

  # Fallback prompt (inline) for when file is not available
  FALLBACK_PROMPT="Generate {{count}} unique lore entry titles for a fantasy/sci-fi world called '{{title}}'. {{description}}

## CRITICAL: Format ONLY
No meta-commentary, no explanations, no preamble.

Format EXACTLY like this:
1. [Category: place] Entry Title
2. [Category: character] Entry Title
3. [Category: object] Entry Title

Rules:
- Categories MUST be: place, character, object, event, or concept
- Start IMMEDIATELY with \"1.\"
- Each line: number, category in brackets, title

Output NOW:"

  # Load prompt template from file or use fallback
  TEMPLATE=$(load_prompt_template "lorebook-titles-generation.yaml" "$FALLBACK_PROMPT")
  
  # Interpolate variables
  PROMPT=$(interpolate_prompt "$TEMPLATE" "title" "$title" "description" "$description" "count" "$entry_count")

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
