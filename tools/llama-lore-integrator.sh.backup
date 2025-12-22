#!/bin/bash
# Tool to analyze and integrate existing content into the lore/persona system using LLM

set -e

SKOGAI_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODEL_NAME=${1:-"llama3.2"}
PROVIDER=${LLM_PROVIDER:-"ollama"}  # Set via env var or defaults to ollama

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
                -d "{\"model\":\"$MODEL_NAME\",\"messages\":[{\"role\":\"user\",\"content\":$(echo "$prompt" | jq -Rs .)}],\"max_tokens\":2048}" \
            | jq -r '.choices[0].message.content'
            ;;
        *)
            echo "Unknown provider: $PROVIDER" >&2
            return 1
            ;;
    esac
}

# Provider-specific setup
if [ "$PROVIDER" = "ollama" ]; then
    if ! command -v ollama &>/dev/null; then
        echo "Ollama not found. Please install it first:"
        echo "curl -fsSL https://ollama.com/install.sh | sh"
        exit 1
    fi

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

# Function to extract lore from text files
extract_lore_from_file() {
  local file_path="$1"
  local output_format="$2" # json or lore

  echo "Analyzing file: $file_path"
  echo "Using model: $MODEL_NAME"

  if [ ! -f "$file_path" ]; then
    echo "Error: File not found: $file_path"
    return 1
  fi

  # Get file content, limiting to first 8000 chars to avoid context issues
  local content=$(head -c 8000 "$file_path")

  # Prompt for lore extraction
  if [ "$output_format" == "json" ]; then
    PROMPT="Analyze the following text and extract structured lore information from it.

        TEXT:
        $content

        Extract lore entities as structured JSON. Include entries for characters, places, objects, events, or concepts mentioned in the text.

        Format your response as valid JSON like this:
        {
          \"entries\": [
            {
              \"title\": \"Entity Name\",
              \"category\": \"character/place/object/event/concept\",
              \"summary\": \"Brief description\",
              \"content\": \"Detailed description based on text\",
              \"tags\": [\"tag1\", \"tag2\"]
            }
          ]
        }

        Only include your JSON output, nothing else."
  else
    PROMPT="Analyze the following text and extract lore information from it.

        TEXT:
        $content

        Extract 3-5 key lore elements (characters, places, objects, events, or concepts) mentioned in the text.

        For each element, format your response like this:

        ## [CATEGORY: character/place/object/event/concept] TITLE
        SUMMARY: Brief one-sentence description
        CONTENT: 1-2 paragraphs of expanded details based on the text
        TAGS: tag1, tag2, tag3

        Be concise and focus on the most important lore elements."
  fi

  # Run LLM to analyze content
  ANALYSIS=$(run_llm "$PROMPT")

  # Output the analysis
  echo "$ANALYSIS"
}

# Function to create lore entries from analysis
create_entries_from_analysis() {
  local analysis="$1"
  local book_id="$2"

  # Create temporary file for analysis
  TEMP_FILE=$(mktemp)
  echo "$analysis" >"$TEMP_FILE"

  # Check if input is JSON
  if [[ "$analysis" == *"\"entries\":"* ]] && jq -e . >/dev/null 2>&1 <<<"$analysis"; then
    # Process JSON format
    echo "Processing JSON lore entries..."

    # Extract entries array
    entries=$(jq -c '.entries[]' <<<"$analysis")

    # Process each entry
    while IFS= read -r entry; do
      title=$(jq -r '.title' <<<"$entry")
      category=$(jq -r '.category' <<<"$entry")
      summary=$(jq -r '.summary' <<<"$entry")
      content=$(jq -r '.content' <<<"$entry")
      tags=$(jq -r '.tags | join(",")' <<<"$entry")

      # Create lore entry
      $SKOGAI_DIR/tools/manage-lore.sh create-entry "$title" "$category"

      # Get the ID of the created entry
      ENTRY_ID=$(ls -t $SKOGAI_DIR/knowledge/expanded/lore/entries/ | head -n 1 | sed 's/\.json//')

      # Update entry with extracted info using --arg for safe escaping
      TEMP_JSON=$(mktemp)
      jq --arg content "$content" --arg summary "$summary" --arg tags "$tags" \
        '.content = $content | .summary = $summary | .tags = ($tags | split(",") | map(gsub("^\\s+|\\s+$"; "")))' \
        "$SKOGAI_DIR/knowledge/expanded/lore/entries/$ENTRY_ID.json" >"$TEMP_JSON"

      mv "$TEMP_JSON" "$SKOGAI_DIR/knowledge/expanded/lore/entries/$ENTRY_ID.json"

      echo "Created lore entry: $title ($ENTRY_ID)"

      # Add to book if specified
      if [ ! -z "$book_id" ]; then
        $SKOGAI_DIR/tools/manage-lore.sh add-to-book "$ENTRY_ID" "$book_id"
        echo "Added entry to book: $book_id"
      fi
    done <<<"$entries"

  else
    # Process Markdown format
    echo "Processing Markdown lore entries..."

    # Use awk to split into sections and process each one
    echo "$analysis" | awk '
      /^## / {
        if (section != "") print section
        section = $0
        next
      }
      { section = section "\n" $0 }
      END { if (section != "") print section }
    ' | while IFS= read -r section; do
      # Skip empty sections
      [ -z "$section" ] && continue

      # Extract header line
      header=$(echo "$section" | head -n 1)

      # Extract category from [CATEGORY: xxx] or [xxx] format
      category=$(echo "$header" | sed -n 's/.*\[CATEGORY:[[:space:]]*\([^]]*\)\].*/\1/p' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
      if [ -z "$category" ]; then
        category=$(echo "$header" | sed -n 's/.*\[\([^]:]*\)\].*/\1/p' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
      fi
      if [ -z "$category" ]; then
        category="custom"
      fi

      # Extract title (text after the bracket or after ##)
      title=$(echo "$header" | sed 's/^##[[:space:]]*\[[^]]*\][[:space:]]*//' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
      if [ -z "$title" ]; then
        title=$(echo "$header" | sed 's/^##[[:space:]]*//' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
      fi

      # Extract summary, content, tags from the section body
      summary=$(echo "$section" | grep "^SUMMARY:" | head -n 1 | sed 's/^SUMMARY:[[:space:]]*//')
      tags=$(echo "$section" | grep "^TAGS:" | head -n 1 | sed 's/^TAGS:[[:space:]]*//' | sed 's/, /,/g')

      # Extract content between CONTENT: and TAGS: (or end of section)
      content=$(echo "$section" | sed -n '/^CONTENT:/,/^TAGS:\|$/p' | sed '1s/^CONTENT:[[:space:]]*//' | sed '/^TAGS:/d' | tr '\n' ' ' | sed 's/[[:space:]]*$//')

      if [ -z "$title" ]; then
        echo "Warning: Could not extract title from section, skipping"
        continue
      fi

      # Create lore entry
      $SKOGAI_DIR/tools/manage-lore.sh create-entry "$title" "$category"

      # Get the ID of the created entry
      ENTRY_ID=$(ls -t $SKOGAI_DIR/knowledge/expanded/lore/entries/ | head -n 1 | sed 's/\.json//')

      # Update entry with extracted info using --arg for safe escaping
      TEMP_JSON=$(mktemp)
      jq --arg content "$content" --arg summary "$summary" --arg tags "$tags" \
        '.content = $content | .summary = $summary | .tags = ($tags | split(",") | map(gsub("^\\s+|\\s+$"; "")))' \
        "$SKOGAI_DIR/knowledge/expanded/lore/entries/$ENTRY_ID.json" >"$TEMP_JSON"

      mv "$TEMP_JSON" "$SKOGAI_DIR/knowledge/expanded/lore/entries/$ENTRY_ID.json"

      echo "Created lore entry: $title ($ENTRY_ID)"

      # Add to book if specified
      if [ ! -z "$book_id" ]; then
        $SKOGAI_DIR/tools/manage-lore.sh add-to-book "$ENTRY_ID" "$book_id"
        echo "Added entry to book: $book_id"
      fi
    done
  fi

  # Cleanup
  rm "$TEMP_FILE"
}

# Function to create a persona from text analysis
create_persona_from_text() {
  local file_path="$1"

  echo "Creating persona from: $file_path"
  echo "Using model: $MODEL_NAME"

  if [ ! -f "$file_path" ]; then
    echo "Error: File not found: $file_path"
    return 1
  fi

  # Get file content, limiting to first 8000 chars
  local content=$(head -c 8000 "$file_path")

  # Prompt for persona extraction
  PROMPT="Analyze the following text and extract information about a character or persona.

    TEXT:
    $content

    Based on this text, create a detailed persona profile with the following:

    NAME: The character's name
    DESCRIPTION: A brief description (1-2 sentences)
    TRAITS: List 4-6 personality traits, comma-separated
    VOICE: Description of their speaking style and voice
    BACKGROUND: Their origin or background story
    EXPERTISE: Areas of knowledge or skill, comma-separated
    LIMITATIONS: Weaknesses or gaps in knowledge, comma-separated

    Format your response exactly as shown above, with each field on a separate line."

  # Run LLM to analyze content
  ANALYSIS=$(run_llm "$PROMPT")

  # Extract information from analysis
  NAME=$(echo "$ANALYSIS" | grep -oP '^NAME: \K.*' | head -n 1)
  DESCRIPTION=$(echo "$ANALYSIS" | grep -oP '^DESCRIPTION: \K.*' | head -n 1)
  TRAITS=$(echo "$ANALYSIS" | grep -oP '^TRAITS: \K.*' | head -n 1)
  VOICE=$(echo "$ANALYSIS" | grep -oP '^VOICE: \K.*' | head -n 1)
  BACKGROUND=$(echo "$ANALYSIS" | grep -oP '^BACKGROUND: \K.*' | head -n 1)
  EXPERTISE=$(echo "$ANALYSIS" | grep -oP '^EXPERTISE: \K.*' | head -n 1)
  LIMITATIONS=$(echo "$ANALYSIS" | grep -oP '^LIMITATIONS: \K.*' | head -n 1)

  if [ -z "$NAME" ] || [ -z "$TRAITS" ]; then
    echo "Failed to extract proper persona information. Raw output:"
    echo "$ANALYSIS"
    return 1
  fi

  # Create the persona
  $SKOGAI_DIR/tools/create-persona.sh create "$NAME" "$DESCRIPTION" "$TRAITS" "$VOICE"

  # Get the ID of the created persona
  PERSONA_ID=$(ls -t $SKOGAI_DIR/knowledge/expanded/personas/ | head -n 1 | sed 's/\.json//')

  # Update with additional information
  TEMP_JSON=$(mktemp)
  jq ".background.origin = \"$BACKGROUND\" | .knowledge.expertise = [$(echo "$EXPERTISE" | sed 's/,/","/g' | sed 's/^/"/' | sed 's/$/"/')] | .knowledge.limitations = [$(echo "$LIMITATIONS" | sed 's/,/","/g' | sed 's/^/"/' | sed 's/$/"/')]" \
    "$SKOGAI_DIR/knowledge/expanded/personas/$PERSONA_ID.json" >"$TEMP_JSON"

  mv "$TEMP_JSON" "$SKOGAI_DIR/knowledge/expanded/personas/$PERSONA_ID.json"

  echo "Created persona: $NAME ($PERSONA_ID)"
  echo "Use ./tools/create-persona.sh show $PERSONA_ID to view details"

  echo "$PERSONA_ID"
}

# Function to analyze connections between lore entries
analyze_lore_connections() {
  local book_id="$1"

  echo "Analyzing connections in lorebook: $book_id"
  echo "Using model: $MODEL_NAME"

  if [ -z "$book_id" ]; then
    echo "Error: No book ID provided"
    return 1
  fi

  # Get book information
  BOOK_FILE="$SKOGAI_DIR/knowledge/expanded/lore/books/$book_id.json"
  if [ ! -f "$BOOK_FILE" ]; then
    echo "Error: Book not found: $book_id"
    return 1
  fi

  # Get all entries in the book
  ENTRIES=$(jq -r '.entries[]' "$BOOK_FILE")

  # Prepare entry data for analysis
  ENTRY_DATA=""
  for entry_id in $ENTRIES; do
    ENTRY_FILE="$SKOGAI_DIR/knowledge/expanded/lore/entries/$entry_id.json"
    if [ -f "$ENTRY_FILE" ]; then
      TITLE=$(jq -r '.title' "$ENTRY_FILE")
      CATEGORY=$(jq -r '.category' "$ENTRY_FILE")
      SUMMARY=$(jq -r '.summary' "$ENTRY_FILE")

      ENTRY_DATA+="ID: $entry_id\n"
      ENTRY_DATA+="TITLE: $TITLE\n"
      ENTRY_DATA+="CATEGORY: $CATEGORY\n"
      ENTRY_DATA+="SUMMARY: $SUMMARY\n\n"
    fi
  done

  # Prompt for connection analysis
  PROMPT="Analyze these lore entries and identify meaningful connections between them:

    $ENTRY_DATA

    For each connection you find, format your response like this:

    ## CONNECTION
    SOURCE: [entry_id of source]
    TARGET: [entry_id of target]
    RELATIONSHIP: [describe relationship type: part_of, located_in, created_by, opposes, allies_with, etc.]
    DESCRIPTION: [1-2 sentences describing the connection]

    Identify at least 3-5 meaningful connections."

  # Run LLM to analyze connections
  CONNECTIONS=$(run_llm "$PROMPT")

  # Process the connections by splitting on ## CONNECTION headers
  echo "$CONNECTIONS" | awk '
    /^## CONNECTION/ {
      if (section != "") print section
      section = ""
      next
    }
    { section = section $0 "\n" }
    END { if (section != "") print section }
  ' | while IFS= read -r section; do
    # Skip empty sections
    [ -z "$section" ] && continue

    # Extract fields using sed instead of grep -oP
    SOURCE=$(echo "$section" | grep "^SOURCE:" | head -n 1 | sed 's/^SOURCE:[[:space:]]*//' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    TARGET=$(echo "$section" | grep "^TARGET:" | head -n 1 | sed 's/^TARGET:[[:space:]]*//' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    RELATIONSHIP=$(echo "$section" | grep "^RELATIONSHIP:" | head -n 1 | sed 's/^RELATIONSHIP:[[:space:]]*//' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    DESCRIPTION=$(echo "$section" | grep "^DESCRIPTION:" | head -n 1 | sed 's/^DESCRIPTION:[[:space:]]*//' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

    if [ ! -z "$SOURCE" ] && [ ! -z "$TARGET" ]; then
      # Add connection to source entry
      SOURCE_FILE="$SKOGAI_DIR/knowledge/expanded/lore/entries/$SOURCE.json"
      if [ -f "$SOURCE_FILE" ]; then
        TEMP_JSON=$(mktemp)
        jq --arg target "$TARGET" --arg rel "$RELATIONSHIP" --arg desc "$DESCRIPTION" \
          '.relationships += [{"target_id": $target, "relationship_type": $rel, "description": $desc}]' \
          "$SOURCE_FILE" >"$TEMP_JSON"

        mv "$TEMP_JSON" "$SOURCE_FILE"
        echo "Added connection: $SOURCE -> $TARGET ($RELATIONSHIP)"
      else
        echo "Warning: Source entry not found: $SOURCE"
      fi
    fi
  done

  echo "Connections analysis complete"
}

# Function to create a lorebook from a directory of files
create_lorebook_from_directory() {
  local dir_path="$1"
  local book_title="$2"
  local book_description="$3"

  echo "Creating lorebook from directory: $dir_path"
  echo "Book title: $book_title"
  echo "Using model: $MODEL_NAME"

  if [ ! -d "$dir_path" ]; then
    echo "Error: Directory not found: $dir_path"
    return 1
  fi

  # Create the lorebook
  $SKOGAI_DIR/tools/manage-lore.sh create-book "$book_title" "$book_description"

  # Get the ID of the created book
  BOOK_ID=$(ls -t $SKOGAI_DIR/knowledge/expanded/lore/books/ | head -n 1 | sed 's/\.json//')

  # Process each file in the directory
  echo "Processing files..."
  for file in "$dir_path"/*; do
    if [ -f "$file" ]; then
      # Skip non-text files
      if file "$file" | grep -q text; then
        echo "Analyzing file: $(basename "$file")"

        # Extract lore entries
        ANALYSIS=$(extract_lore_from_file "$file" "lore")

        # Create entries from analysis
        create_entries_from_analysis "$ANALYSIS" "$BOOK_ID"
      fi
    fi
  done

  # Analyze connections
  analyze_lore_connections "$BOOK_ID"

  echo "Lorebook creation complete: $BOOK_ID"
  echo "Use ./tools/manage-lore.sh show-book $BOOK_ID to view it"
}

# Show help info
show_help() {
  echo "Lore Integrator - Analyze and integrate existing content into lore/persona system"
  echo ""
  echo "Usage: $0 [model_name] [command] [options]"
  echo ""
  echo "Commands:"
  echo "  extract-lore file.txt [json/lore]      Extract lore from a text file"
  echo "  create-entries \"analysis text\" [book_id]  Create entries from analysis"
  echo "  create-persona file.txt                Create a persona from text file"
  echo "  analyze-connections book_id            Find connections between entries"
  echo "  import-directory dir \"Title\" \"Desc\"    Create lorebook from directory"
  echo "  help                                   Show this help message"
  echo ""
  echo "Environment Variables:"
  echo "  LLM_PROVIDER    Provider to use: ollama (default), claude, openai"
  echo "  OPENAI_API_KEY  API key for openai provider"
  echo "  OPENAI_BASE_URL API base URL (default: https://openrouter.ai/api/v1)"
  echo ""
  echo "Example:"
  echo "  $0 llama3 extract-lore story.txt json"
  echo "  LLM_PROVIDER=claude $0 - create-persona character.txt"
  echo "  LLM_PROVIDER=openai $0 gpt-4 import-directory /path/to/world \"My World\" \"Description\""
}

# Main command processing
case "$2" in
extract-lore)
  extract_lore_from_file "$3" "${4:-lore}"
  ;;
create-entries)
  create_entries_from_analysis "$3" "$4"
  ;;
create-persona)
  create_persona_from_text "$3"
  ;;
analyze-connections)
  analyze_lore_connections "$3"
  ;;
import-directory)
  create_lorebook_from_directory "$3" "$4" "$5"
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
