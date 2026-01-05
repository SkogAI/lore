#!/bin/bash
#
# Lore Generation Flow
# Transforms technical changes into narrative lore through agent personas
#
# Usage: ./lore-flow.sh [git-diff|log|manual] [input-file-or-message]

set -e

LORE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PERSONA_MANAGER="$LORE_DIR/integration/persona-bridge/persona-manager.py"
ORCHESTRATOR="$LORE_DIR/orchestrator/orchestrator.py"
AGENT_API="$LORE_DIR/agents/api/agent_api.py"
LORE_API="$LORE_DIR/agents/api/lore_api.py"

# Session ID
SESSION_ID=$(date +%s)

# Parse input type and content
INPUT_TYPE=${1:-"manual"}
INPUT_CONTENT=${2:-""}

if [ -z "$INPUT_CONTENT" ]; then
  echo "Usage: $0 [git-diff|log|manual] [input-file-or-message]"
  echo ""
  echo "Examples:"
  echo "  $0 git-diff HEAD~1"
  echo "  $0 manual 'Amy implemented quantum mojito generator'"
  echo "  $0 log /path/to/agent.log"
  exit 1
fi

echo "=== Lore Generation Flow ==="
echo "Session: $SESSION_ID"
echo "Input Type: $INPUT_TYPE"
echo ""

# Step 1: Extract raw content based on input type
echo "[1/5] Extracting content..."
case $INPUT_TYPE in
  git-diff)
    # Get git diff
    RAW_CONTENT=$(git diff "$INPUT_CONTENT" || git show "$INPUT_CONTENT")
    # Try to extract author from commit
    GIT_AUTHOR=$(git log -1 --format='%an' "$INPUT_CONTENT" || echo "")
    ;;
  log)
    # Read from log file
    if [ -f "$INPUT_CONTENT" ]; then
      RAW_CONTENT=$(cat "$INPUT_CONTENT")
    else
      echo "Error: Log file not found: $INPUT_CONTENT"
      exit 1
    fi
    GIT_AUTHOR=""
    ;;
  manual)
    # Use input directly
    RAW_CONTENT="$INPUT_CONTENT"
    GIT_AUTHOR=""
    ;;
  *)
    echo "Error: Unknown input type: $INPUT_TYPE"
    echo "Valid types: git-diff, log, manual"
    exit 1
    ;;
esac

if [ -z "$RAW_CONTENT" ]; then
  echo "Error: No content extracted"
  exit 1
fi

echo "Content extracted: ${#RAW_CONTENT} characters"

# Step 2: Determine which persona should narrate
echo ""
echo "[2/5] Selecting persona..."

# Load persona mapping configuration
PERSONA_MAPPING="$LORE_DIR/integration/persona-mapping.conf"
DEFAULT_PERSONA="persona_1763820091"  # Village Elder

# Function to lookup persona by git author
lookup_persona() {
  local author=$1
  local mapping_file=$2

  if [ ! -f "$mapping_file" ]; then
    echo "$DEFAULT_PERSONA"
    return
  fi

  # Try exact match first
  local persona=$(grep "^${author}=" "$mapping_file" | cut -d'=' -f2 | tr -d ' ' | head -1)

  if [ -z "$persona" ]; then
    # Try case-insensitive match
    persona=$(grep -i "^${author}=" "$mapping_file" | cut -d'=' -f2 | tr -d ' ' | head -1)
  fi

  if [ -z "$persona" ]; then
    # Get DEFAULT from config
    persona=$(grep "^DEFAULT=" "$mapping_file" | cut -d'=' -f2 | tr -d ' ' | head -1)
  fi

  # Final fallback
  if [ -z "$persona" ]; then
    persona=$DEFAULT_PERSONA
  fi

  echo "$persona"
}

# Determine persona based on git author or use default
if [ -n "$GIT_AUTHOR" ]; then
  echo "Git author detected: $GIT_AUTHOR"
  PERSONA_ID=$(lookup_persona "$GIT_AUTHOR" "$PERSONA_MAPPING")
else
  # Use DEFAULT from mapping or hardcoded default
  PERSONA_ID=$(grep "^DEFAULT=" "$PERSONA_MAPPING" | cut -d'=' -f2 | tr -d ' ' || echo "$DEFAULT_PERSONA")
fi

# Get persona name from persona-manager
PERSONA_NAME=$(python3 "$PERSONA_MANAGER" --persona "$PERSONA_ID" --get-name || echo "Unknown")

if [ "$PERSONA_NAME" = "Unknown" ]; then
  echo "Warning: Persona $PERSONA_ID not found, using default"
  PERSONA_ID=$DEFAULT_PERSONA
  PERSONA_NAME="Village Elder"
fi

echo "Selected persona: $PERSONA_NAME ($PERSONA_ID)"

# Step 3: Load persona context
echo ""
echo "[3/5] Loading persona context..."

# Use persona-manager.py to get formatted context
PERSONA_PROMPT=$(python3 "$PERSONA_MANAGER" --persona "$PERSONA_ID" --render-prompt || echo "")

if [ -z "$PERSONA_PROMPT" ]; then
  echo "Warning: Could not load persona prompt, using basic template"
  PERSONA_PROMPT="You are $PERSONA_NAME, an AI agent in the SkogAI system."
fi

echo "Persona context loaded"

# Step 4: Generate narrative via LLM
echo ""
echo "[4/5] Generating narrative..."

# Save raw content to temp file for lore-integrator
TEMP_CONTENT="/tmp/lore-content-$SESSION_ID.txt"
cat > "$TEMP_CONTENT" <<EOF
# Technical Change - Session $SESSION_ID

$RAW_CONTENT

---
Narrated by: $PERSONA_NAME ($PERSONA_ID)
Source: $INPUT_TYPE
EOF

echo "Using llama-lore-integrator.sh to generate narrative..."

# Use existing lore-integrator tool to extract lore from content
# This tool already handles LLM calls via Anthropic API
LORE_INTEGRATOR="$LORE_DIR/tools/llama-lore-integrator.sh"

if [ ! -f "$LORE_INTEGRATOR" ]; then
  echo "Error: llama-lore-integrator.sh not found"
  exit 1
fi

# Determine model name from environment or use default
# Model name is first parameter to llama-lore-integrator.sh
# If not set, llama-lore-integrator.sh will use its default (llama3.2)
LLM_MODEL=${LLM_MODEL:-"llama3.2"}

# Extract lore from the content (outputs JSON or markdown)
# Use llama3.2 as default model if LLM_PROVIDER is not set
LORE_MODEL="${LLM_MODEL:-llama3.2}"
EXTRACTED_LORE=$("$LORE_INTEGRATOR" "$LORE_MODEL" extract-lore "$TEMP_CONTENT" json || echo "")

if [ -z "$EXTRACTED_LORE" ]; then
  echo "Warning: LLM extraction failed, creating basic entry"
  GENERATED_NARRATIVE="Technical change from $INPUT_TYPE at session $SESSION_ID"
else
  # Parse the JSON to get the narrative content
  GENERATED_NARRATIVE=$(echo "$EXTRACTED_LORE" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    entries = data.get('entries', [])
    if entries:
        print(entries[0].get('content', 'No content generated'))
    else:
        print('No entries extracted')
except:
    print('Failed to parse LLM output')
")
fi

echo "Narrative generated: ${#GENERATED_NARRATIVE} characters"

# Clean up temp file
rm -f "$TEMP_CONTENT"

# Step 5: Create lore entry
echo ""
echo "[5/5] Creating lore entry..."

# Determine lore entry type and title based on content
LORE_CATEGORY="event"  # Default
ENTRY_TITLE="$PERSONA_NAME's Tale - Session $SESSION_ID"

# If git diff, try to extract commit message for title
if [ "$INPUT_TYPE" = "git-diff" ] && [ -n "$INPUT_CONTENT" ]; then
  COMMIT_MSG=$(git log -1 --format='%s' "$INPUT_CONTENT" || echo "")
  if [ -n "$COMMIT_MSG" ]; then
    ENTRY_TITLE="$COMMIT_MSG"
  fi
fi

echo "Creating lore entry: $ENTRY_TITLE"
echo "Category: $LORE_CATEGORY"

# Create entry using manage-lore.sh
ENTRY_ID=$("$LORE_DIR/tools/manage-lore.sh" create-entry "$ENTRY_TITLE" "$LORE_CATEGORY" | grep -oP 'entry_\d+_[a-f0-9]+' | head -1 || echo "")

if [ -z "$ENTRY_ID" ]; then
  echo "Error: Failed to create lore entry"
  exit 1
fi

echo "Entry created: $ENTRY_ID"

# Update entry with generated content
ENTRY_FILE="$LORE_DIR/knowledge/expanded/lore/entries/${ENTRY_ID}.json"

if [ -f "$ENTRY_FILE" ]; then
  # Save narrative to temp file to avoid quote escaping issues
  TEMP_NARRATIVE="/tmp/narrative-$SESSION_ID.txt"
  echo "$GENERATED_NARRATIVE" > "$TEMP_NARRATIVE"

  # Use Python to update the JSON properly
  python3 -c "
import json

# Read the narrative from temp file
with open('$TEMP_NARRATIVE', 'r') as f:
    narrative = f.read()

# Update entry
with open('$ENTRY_FILE', 'r') as f:
    entry = json.load(f)

entry['content'] = narrative
entry['summary'] = 'Auto-generated lore from $INPUT_TYPE'
entry['tags'] = ['generated', 'automated', '$PERSONA_NAME', '$INPUT_TYPE']

with open('$ENTRY_FILE', 'w') as f:
    json.dump(entry, f, indent=2)
" && echo "Entry updated with narrative"

  # Clean up temp file
  rm -f "$TEMP_NARRATIVE"
else
  echo "Warning: Entry file not found, content not updated"
fi

# Add to persona's chronicle book
# Find or create the persona's chronicle
CHRONICLE_NAME="${PERSONA_NAME}'s Chronicles"
CHRONICLE_ID=$("$LORE_DIR/tools/manage-lore.sh" list-books | grep -F "$CHRONICLE_NAME" | grep -oP 'book_\d+' | head -1 || echo "")

if [ -z "$CHRONICLE_ID" ]; then
  echo "Creating chronicle book: $CHRONICLE_NAME"
  CHRONICLE_ID=$("$LORE_DIR/tools/manage-lore.sh" create-book "$CHRONICLE_NAME" "Automated chronicles of $PERSONA_NAME's adventures" | grep -oP 'book_\d+' || echo "")

  if [ -n "$CHRONICLE_ID" ]; then
    # Link to persona
    "$LORE_DIR/tools/manage-lore.sh" link-to-persona "$CHRONICLE_ID" "$PERSONA_ID"
  fi
fi

if [ -n "$CHRONICLE_ID" ]; then
  echo "Adding entry to chronicle: $CHRONICLE_ID"
  "$LORE_DIR/tools/manage-lore.sh" add-to-book "$ENTRY_ID" "$CHRONICLE_ID"
else
  echo "Warning: Could not create/find chronicle book"
fi

echo ""
echo "=== Lore Generation Complete ==="
echo "Entry ID: $ENTRY_ID"
echo "Persona: $PERSONA_NAME ($PERSONA_ID)"
echo "Chronicle: $CHRONICLE_ID"
echo "Session: $SESSION_ID"
echo ""
echo "View entry: $LORE_DIR/tools/manage-lore.sh show-entry $ENTRY_ID"
echo "View chronicle: $LORE_DIR/tools/manage-lore.sh show-book $CHRONICLE_ID"
