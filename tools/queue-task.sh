#!/bin/bash
# Queue Task Management Script
# Add and manage lore generation tasks in the queue

set -e

SKOGAI_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
QUEUE_DIR="${SKOGAI_DIR}/queue"
PENDING_DIR="${QUEUE_DIR}/pending"
PROCESSING_DIR="${QUEUE_DIR}/processing"
COMPLETED_DIR="${QUEUE_DIR}/completed"
FAILED_DIR="${QUEUE_DIR}/failed"

# Ensure queue directories exist
mkdir -p "${PENDING_DIR}" "${PROCESSING_DIR}" "${COMPLETED_DIR}" "${FAILED_DIR}"

# Generate a unique task ID
generate_task_id() {
  echo "task_$(date +%s)"
}

# Show help
show_help() {
  echo "Queue Task Management - Add and manage lore generation tasks"
  echo ""
  echo "Usage: $0 [command] [options]"
  echo ""
  echo "Commands:"
  echo "  entry \"Title\" \"category\" [--persona NAME|ID] [--priority PRIORITY]"
  echo "      Add a lore entry generation task to the queue"
  echo ""
  echo "  status"
  echo "      Show queue status (counts of pending, processing, completed, failed)"
  echo ""
  echo "  list [STATE]"
  echo "      List tasks. STATE can be: pending, processing, completed, failed, all"
  echo "      Default: pending"
  echo ""
  echo "  show TASK_ID"
  echo "      Show details of a specific task"
  echo ""
  echo "  clear [STATE]"
  echo "      Clear tasks. STATE can be: completed, failed, all"
  echo ""
  echo "  help"
  echo "      Show this help message"
  echo ""
  echo "Options:"
  echo "  --persona NAME|ID    Associate with a persona (name or persona_id)"
  echo "  --priority PRIORITY  Set priority (low, normal, high). Default: normal"
  echo ""
  echo "Examples:"
  echo "  $0 entry \"The Dark Tower\" \"place\""
  echo "  $0 entry \"Elara the Wise\" \"character\" --persona amy"
  echo "  $0 entry \"The Great War\" \"event\" --priority high"
  echo "  $0 status"
  echo "  $0 list pending"
  echo "  $0 show task_1704567890"
}

# Add an entry task to the queue
add_entry_task() {
  local title="$1"
  local category="$2"
  shift 2
  
  # Parse optional arguments
  local persona_id=""
  local priority="normal"
  
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --persona)
        persona_id="$2"
        shift 2
        ;;
      --priority)
        priority="$2"
        shift 2
        ;;
      *)
        echo "Unknown option: $1" >&2
        return 1
        ;;
    esac
  done
  
  # Validate inputs
  if [ -z "$title" ] || [ -z "$category" ]; then
    echo "Error: Title and category are required" >&2
    echo "Usage: $0 entry \"Title\" \"category\" [--persona NAME|ID] [--priority PRIORITY]" >&2
    return 1
  fi
  
  # Validate category
  if [[ ! "$category" =~ ^(place|character|object|event|concept|custom)$ ]]; then
    echo "Warning: Category '$category' is not standard. Valid categories: place, character, object, event, concept, custom" >&2
  fi
  
  # Validate priority
  if [[ ! "$priority" =~ ^(low|normal|high)$ ]]; then
    echo "Error: Priority must be one of: low, normal, high" >&2
    return 1
  fi
  
  # If persona is a name, try to resolve to ID
  if [ -n "$persona_id" ] && [[ ! "$persona_id" =~ ^persona_ ]]; then
    # Try to find persona by name
    local found_id=""
    for persona_file in "${SKOGAI_DIR}/knowledge/expanded/personas"/*.json; do
      if [ -f "$persona_file" ]; then
        local name=$(jq -r '.name // empty' "$persona_file" 2>/dev/null | tr '[:upper:]' '[:lower:]')
        if [ "$name" = "$(echo "$persona_id" | tr '[:upper:]' '[:lower:]')" ]; then
          found_id=$(jq -r '.id' "$persona_file")
          break
        fi
      fi
    done
    
    if [ -n "$found_id" ]; then
      persona_id="$found_id"
      echo "Resolved persona name to ID: $persona_id"
    else
      echo "Warning: Could not find persona '$persona_id', using as-is" >&2
    fi
  fi
  
  # Generate task
  local task_id=$(generate_task_id)
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  local task_file="${PENDING_DIR}/${task_id}.json"
  
  # Create task JSON
  cat > "$task_file" <<EOF
{
  "id": "$task_id",
  "type": "entry",
  "prompt_ref": "prompts/lore-entry-generation.yaml",
  "data": {
    "title": "$title",
    "category": "$category"
  },
  "created_at": "$timestamp",
  "priority": "$priority",
  "persona_id": "$persona_id",
  "status": "pending"
}
EOF
  
  echo "✅ Task added to queue: $task_id"
  echo "   Title: $title"
  echo "   Category: $category"
  if [ -n "$persona_id" ]; then
    echo "   Persona: $persona_id"
  fi
  echo "   Priority: $priority"
  echo ""
  echo "Run './tools/process-queue.sh' to process pending tasks"
}

# Show queue status
show_status() {
  local pending_count=$(ls -1 "${PENDING_DIR}"/*.json 2>/dev/null | wc -l)
  local processing_count=$(ls -1 "${PROCESSING_DIR}"/*.json 2>/dev/null | wc -l)
  local completed_count=$(ls -1 "${COMPLETED_DIR}"/*.json 2>/dev/null | wc -l)
  local failed_count=$(ls -1 "${FAILED_DIR}"/*.json 2>/dev/null | wc -l)
  
  echo "📊 Queue Status"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  Pending:    $pending_count tasks"
  echo "  Processing: $processing_count tasks"
  echo "  Completed:  $completed_count tasks"
  echo "  Failed:     $failed_count tasks"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# List tasks
list_tasks() {
  local state="${1:-pending}"
  
  case "$state" in
    pending|processing|completed|failed)
      local dir="${QUEUE_DIR}/${state}"
      ;;
    all)
      list_tasks pending
      echo ""
      list_tasks processing
      echo ""
      list_tasks completed
      echo ""
      list_tasks failed
      return
      ;;
    *)
      echo "Error: Invalid state. Must be: pending, processing, completed, failed, or all" >&2
      return 1
      ;;
  esac
  
  echo "📋 Tasks ($state)"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  
  local count=0
  for task_file in "$dir"/*.json; do
    if [ -f "$task_file" ]; then
      local task_id=$(basename "$task_file" .json)
      local title=$(jq -r '.data.title // "N/A"' "$task_file")
      local category=$(jq -r '.data.category // "N/A"' "$task_file")
      local priority=$(jq -r '.priority // "normal"' "$task_file")
      local created_at=$(jq -r '.created_at // "N/A"' "$task_file")
      
      echo "  $task_id"
      echo "    Title: $title"
      echo "    Category: $category"
      echo "    Priority: $priority"
      echo "    Created: $created_at"
      echo ""
      count=$((count + 1))
    fi
  done
  
  if [ $count -eq 0 ]; then
    echo "  No tasks found"
    echo ""
  fi
}

# Show task details
show_task() {
  local task_id="$1"
  
  if [ -z "$task_id" ]; then
    echo "Error: Task ID required" >&2
    return 1
  fi
  
  # Search for task in all directories
  local task_file=""
  for dir in "$PENDING_DIR" "$PROCESSING_DIR" "$COMPLETED_DIR" "$FAILED_DIR"; do
    if [ -f "$dir/${task_id}.json" ]; then
      task_file="$dir/${task_id}.json"
      break
    fi
  done
  
  if [ -z "$task_file" ]; then
    echo "Error: Task not found: $task_id" >&2
    return 1
  fi
  
  echo "📄 Task Details: $task_id"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  jq . "$task_file"
}

# Clear completed or failed tasks
clear_tasks() {
  local state="${1:-completed}"
  
  case "$state" in
    completed)
      local dir="${COMPLETED_DIR}"
      ;;
    failed)
      local dir="${FAILED_DIR}"
      ;;
    all)
      clear_tasks completed
      clear_tasks failed
      return
      ;;
    *)
      echo "Error: Can only clear 'completed', 'failed', or 'all'" >&2
      return 1
      ;;
  esac
  
  local count=$(ls -1 "$dir"/*.json 2>/dev/null | wc -l)
  
  if [ $count -eq 0 ]; then
    echo "No $state tasks to clear"
    return 0
  fi
  
  echo "Clear $count $state task(s)? (y/N)"
  read -r confirm
  
  if [[ "$confirm" =~ ^[Yy]$ ]]; then
    rm -f "$dir"/*.json
    echo "✅ Cleared $count $state task(s)"
  else
    echo "Cancelled"
  fi
}

# Main command processing
case "$1" in
  entry)
    add_entry_task "$2" "$3" "${@:4}"
    ;;
  status)
    show_status
    ;;
  list)
    list_tasks "$2"
    ;;
  show)
    show_task "$2"
    ;;
  clear)
    clear_tasks "$2"
    ;;
  help|--help|-h|"")
    show_help
    ;;
  *)
    echo "Unknown command: $1" >&2
    echo "Run '$0 help' for usage information." >&2
    exit 1
    ;;
esac
