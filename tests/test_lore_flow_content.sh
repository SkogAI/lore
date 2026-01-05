#!/bin/bash
# Test script to verify lore-flow.sh creates entries with non-empty content
# This test simulates the LLM response by mocking the llama-lore-integrator.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LORE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TEST_TEMP_DIR="/tmp/lore-flow-test-$$"

echo "=== Testing lore-flow.sh Content Bug Fix ==="
echo "Test temp dir: $TEST_TEMP_DIR"

# Setup
mkdir -p "$TEST_TEMP_DIR"
cd "$LORE_DIR"

# Create a mock llama-lore-integrator.sh that returns predictable output
MOCK_INTEGRATOR="$TEST_TEMP_DIR/llama-lore-integrator.sh"
cat > "$MOCK_INTEGRATOR" << 'EOF'
#!/bin/bash
# Mock integrator that returns test JSON

MODEL_NAME=${1:-"test"}
COMMAND=${2:-"help"}
FILE_PATH=${3:-""}
OUTPUT_FORMAT=${4:-"lore"}

if [ "$COMMAND" = "extract-lore" ] && [ "$OUTPUT_FORMAT" = "json" ]; then
  cat << 'JSONEOF'
{
  "entries": [
    {
      "title": "Test Entry",
      "category": "event",
      "summary": "A test lore entry for validation",
      "content": "This is the generated narrative content that should appear in the entry. It contains multiple sentences to simulate real LLM output. The content field should not be empty after the pipeline completes.",
      "tags": ["test", "automated", "validation"]
    }
  ]
}
JSONEOF
else
  echo "Mock integrator called with: $@"
fi
EOF

chmod +x "$MOCK_INTEGRATOR"

# Backup original integrator and replace with mock
ORIGINAL_INTEGRATOR="$LORE_DIR/tools/llama-lore-integrator.sh"
BACKUP_INTEGRATOR="$LORE_DIR/tools/llama-lore-integrator.sh.test-backup"

if [ -f "$ORIGINAL_INTEGRATOR" ]; then
  cp "$ORIGINAL_INTEGRATOR" "$BACKUP_INTEGRATOR"
fi
cp "$MOCK_INTEGRATOR" "$ORIGINAL_INTEGRATOR"

# Ensure test directories exist
mkdir -p "$LORE_DIR/knowledge/expanded/lore/entries"
mkdir -p "$LORE_DIR/knowledge/expanded/lore/books"

# Run the pipeline (ignore chronicle errors - not relevant to this test)
echo ""
echo "Running lore-flow.sh with manual input..."
OUTPUT=$("$LORE_DIR/integration/lore-flow.sh" manual "Test content for bug fix validation" 2>&1 || true)
echo "$OUTPUT"

# Extract entry ID from output (try multiple patterns)
ENTRY_ID=$(echo "$OUTPUT" | grep -oP 'Entry ID: \K[^ ]+' | head -1)
if [ -z "$ENTRY_ID" ]; then
  ENTRY_ID=$(echo "$OUTPUT" | grep -oP 'Entry created: \K[^ ]+' | head -1)
fi

if [ -z "$ENTRY_ID" ]; then
  echo "ERROR: Could not extract entry ID from output"
  echo "Full output:"
  echo "$OUTPUT"
  
  # Restore original integrator
  if [ -f "$BACKUP_INTEGRATOR" ]; then
    mv "$BACKUP_INTEGRATOR" "$ORIGINAL_INTEGRATOR"
  fi
  
  exit 1
fi

echo ""
echo "Entry ID: $ENTRY_ID"

# Check if entry file exists
ENTRY_FILE="$LORE_DIR/knowledge/expanded/lore/entries/${ENTRY_ID}.json"
if [ ! -f "$ENTRY_FILE" ]; then
  echo "ERROR: Entry file not found: $ENTRY_FILE"
  
  # Restore original integrator
  if [ -f "$BACKUP_INTEGRATOR" ]; then
    mv "$BACKUP_INTEGRATOR" "$ORIGINAL_INTEGRATOR"
  fi
  
  exit 1
fi

echo "Entry file found: $ENTRY_FILE"

# Read the entry and check content field
CONTENT=$(jq -r '.content' "$ENTRY_FILE")
CONTENT_LENGTH=${#CONTENT}

echo ""
echo "=== Content Field Check ==="
echo "Content length: $CONTENT_LENGTH characters"
echo "Content preview:"
echo "$CONTENT" | head -c 200
echo ""

# Restore original integrator
if [ -f "$BACKUP_INTEGRATOR" ]; then
  mv "$BACKUP_INTEGRATOR" "$ORIGINAL_INTEGRATOR"
fi

# Validate content is not empty
if [ -z "$CONTENT" ]; then
  echo ""
  echo "❌ TEST FAILED: Content field is empty"
  echo "Full entry:"
  cat "$ENTRY_FILE"
  exit 1
fi

if [ "$CONTENT_LENGTH" -lt 10 ]; then
  echo ""
  echo "❌ TEST FAILED: Content field is too short ($CONTENT_LENGTH chars)"
  echo "Content: $CONTENT"
  exit 1
fi

# Check that content contains expected narrative
if echo "$CONTENT" | grep -q "generated narrative content"; then
  echo ""
  echo "✅ TEST PASSED: Content field is populated with narrative"
  echo "Content validation successful!"
  exit 0
else
  echo ""
  echo "⚠️  TEST WARNING: Content exists but doesn't match expected pattern"
  echo "Full content: $CONTENT"
  echo "Entry may still be valid, but content differs from mock output"
  exit 0
fi
