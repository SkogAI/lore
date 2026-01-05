#!/bin/bash
# Process Queue Script
# Process pending lore generation tasks from the queue

set -e

SKOGAI_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
QUEUE_DIR="${SKOGAI_DIR}/queue"
PENDING_DIR="${QUEUE_DIR}/pending"
PROCESSING_DIR="${QUEUE_DIR}/processing"
COMPLETED_DIR="${QUEUE_DIR}/completed"
FAILED_DIR="${QUEUE_DIR}/failed"

# LLM Provider configuration (can be overridden via environment)
PROVIDER=${LLM_PROVIDER:-"ollama"}
MODEL_NAME=${LLM_MODEL:-"llama3.2:3b"}

# Ensure queue directories exist
mkdir -p "${PENDING_DIR}" "${PROCESSING_DIR}" "${COMPLETED_DIR}" "${FAILED_DIR}"

# Show help
show_help() {
  echo "Process Queue - Process pending lore generation tasks"
  echo ""
  echo "Usage: $0 [options]"
  echo ""
  echo "Options:"
  echo "  --provider PROVIDER  LLM provider to use (ollama, claude, openai)"
  echo "  --model MODEL        Model name to use (default: llama3.2:3b)"
  echo "  --limit N            Process at most N tasks (default: all)"
  echo "  --help               Show this help message"
  echo ""
  echo "Environment Variables:"
  echo "  LLM_PROVIDER         LLM provider (default: ollama)"
  echo "  LLM_MODEL            Model name (default: llama3.2:3b)"
  echo "  OPENAI_API_KEY       API key for openai provider"
  echo "  OPENAI_BASE_URL      API base URL for openai provider"
  echo ""
  echo "Examples:"
  echo "  $0"
  echo "  LLM_PROVIDER=ollama $0"
  echo "  LLM_PROVIDER=openai LLM_MODEL=gpt-4 $0"
  echo "  $0 --provider claude --limit 5"
}

# Process a single task
process_task() {
  local task_file="$1"
  local task_id=$(basename "$task_file" .json)
  
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "🔄 Processing task: $task_id"
  
  # Move to processing directory
  mv "$task_file" "${PROCESSING_DIR}/${task_id}.json"
  task_file="${PROCESSING_DIR}/${task_id}.json"
  
  # Parse task
  local task_type=$(jq -r '.type' "$task_file")
  local title=$(jq -r '.data.title' "$task_file")
  local category=$(jq -r '.data.category' "$task_file")
  local persona_id=$(jq -r '.persona_id // empty' "$task_file")
  
  echo "   Type: $task_type"
  echo "   Title: $title"
  echo "   Category: $category"
  if [ -n "$persona_id" ]; then
    echo "   Persona: $persona_id"
  fi
  echo ""
  
  # Process based on task type
  local result=""
  local error_msg=""
  
  case "$task_type" in
    entry)
      # Call llama-lore-creator.sh to generate the entry
      echo "   Generating lore entry..."
      
      # Set environment and call the creator
      export LLM_PROVIDER="$PROVIDER"
      
      if result=$(cd "$SKOGAI_DIR" && ./tools/llama-lore-creator.sh "$MODEL_NAME" entry "$title" "$category" 2>&1); then
        # Extract the entry ID from the output
        local entry_id=$(echo "$result" | grep -oE 'entry_[0-9_]+' | tail -n 1)
        
        if [ -n "$entry_id" ]; then
          echo "   ✅ Successfully created: $entry_id"
          
          # Update task with result
          jq --arg entry_id "$entry_id" \
             --arg completed_at "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
             --arg status "completed" \
             '.status = $status | .completed_at = $completed_at | .result = { "entry_id": $entry_id }' \
             "$task_file" > "${task_file}.tmp"
          mv "${task_file}.tmp" "$task_file"
          
          # Move to completed
          mv "$task_file" "${COMPLETED_DIR}/${task_id}.json"
          return 0
        else
          error_msg="Could not extract entry_id from output"
        fi
      else
        error_msg="Failed to generate lore entry: $result"
      fi
      ;;
    *)
      error_msg="Unknown task type: $task_type"
      ;;
  esac
  
  # If we got here, there was an error
  echo "   ❌ Failed: $error_msg"
  
  # Update task with error
  jq --arg error "$error_msg" \
     --arg failed_at "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
     --arg status "failed" \
     '.status = $status | .failed_at = $failed_at | .error = $error' \
     "$task_file" > "${task_file}.tmp"
  mv "${task_file}.tmp" "$task_file"
  
  # Move to failed
  mv "$task_file" "${FAILED_DIR}/${task_id}.json"
  return 1
}

# Main processing function
process_queue() {
  local limit="$1"
  
  echo "🚀 Starting queue processing"
  echo "   Provider: $PROVIDER"
  echo "   Model: $MODEL_NAME"
  if [ -n "$limit" ]; then
    echo "   Limit: $limit tasks"
  fi
  echo ""
  
  # Get list of pending tasks, sorted by priority
  local tasks=()
  local high_priority=()
  local normal_priority=()
  local low_priority=()
  
  for task_file in "${PENDING_DIR}"/*.json; do
    if [ -f "$task_file" ]; then
      local priority=$(jq -r '.priority // "normal"' "$task_file")
      case "$priority" in
        high)
          high_priority+=("$task_file")
          ;;
        low)
          low_priority+=("$task_file")
          ;;
        *)
          normal_priority+=("$task_file")
          ;;
      esac
    fi
  done
  
  # Combine in priority order
  tasks=("${high_priority[@]}" "${normal_priority[@]}" "${low_priority[@]}")
  
  if [ ${#tasks[@]} -eq 0 ]; then
    echo "📭 No pending tasks in queue"
    return 0
  fi
  
  echo "📋 Found ${#tasks[@]} pending task(s)"
  echo ""
  
  local processed=0
  local succeeded=0
  local failed=0
  
  for task_file in "${tasks[@]}"; do
    if [ -n "$limit" ] && [ $processed -ge $limit ]; then
      echo "⚠️  Reached task limit ($limit)"
      break
    fi
    
    if process_task "$task_file"; then
      succeeded=$((succeeded + 1))
    else
      failed=$((failed + 1))
    fi
    
    processed=$((processed + 1))
    echo ""
  done
  
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "✨ Queue processing complete"
  echo "   Processed: $processed"
  echo "   Succeeded: $succeeded"
  echo "   Failed: $failed"
  echo ""
  
  # Show remaining queue status
  "${SKOGAI_DIR}/tools/queue-task.sh" status
}

# Parse command line arguments
LIMIT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --provider)
      PROVIDER="$2"
      shift 2
      ;;
    --model)
      MODEL_NAME="$2"
      shift 2
      ;;
    --limit)
      LIMIT="$2"
      shift 2
      ;;
    --help|-h|help)
      show_help
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      echo "Run '$0 --help' for usage information." >&2
      exit 1
      ;;
  esac
done

# Run queue processing
process_queue "$LIMIT"
