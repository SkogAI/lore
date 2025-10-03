#!/bin/bash

# Script to manage context transitions

# Load path configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../config/paths.sh"

function create_context() {
  template=$1
  context_type=$2
  session_id=$(date +%s)

  local context_dir=$(get_context_dir)
  local template_file="$context_dir/templates/${template}-context.json"
  local current_file="$context_dir/current/context-${session_id}.json"

  # Ensure directories exist
  ensure_dir "$context_dir/current"

  cp "$template_file" "$current_file"

  # Update basic fields
  sed -i "s/\"created\": \"\"/\"created\": \"$(date -Iseconds)\"/" "$current_file"
  sed -i "s/\"last_updated\": \"\"/\"last_updated\": \"$(date -Iseconds)\"/" "$current_file"
  sed -i "s/\"session_id\": \"\"/\"session_id\": \"${session_id}\"/" "$current_file"
  sed -i "s/\"context_type\": \"base\"/\"context_type\": \"${context_type}\"/" "$current_file"

  echo $session_id
}

function archive_context() {
  session_id=$1

  local context_dir=$(get_context_dir)
  local current_file="$context_dir/current/context-${session_id}.json"
  local archive_file="$context_dir/archive/context-${session_id}.json"

  if [ -f "$current_file" ]; then
    # Ensure archive directory exists
    ensure_dir "$context_dir/archive"

    mv "$current_file" "$archive_file"
    echo "Context archived successfully."
  else
    echo "Error: Context not found."
    exit 1
  fi
}

function update_context() {
  session_id=$1
  key=$2
  value=$3

  local context_dir=$(get_context_dir)
  local current_file="$context_dir/current/context-${session_id}.json"

  if [ -f "$current_file" ]; then
    # This is a simplistic approach - for production use a proper JSON tool like jq
    # For complex nested properties, this would need enhancement
    sed -i "s/\"${key}\": \".*\"/\"${key}\": \"${value}\"/" "$current_file"
    sed -i "s/\"last_updated\": \".*\"/\"last_updated\": \"$(date -Iseconds)\"/" "$current_file"
    echo "Context updated successfully."
  else
    echo "Error: Context not found."
    exit 1
  fi
}

# Command processing
command=$1
shift

case $command in
  create)
    create_context "$@"
    ;;
  archive)
    archive_context "$@"
    ;;
  update)
    update_context "$@"
    ;;
  *)
    echo "Usage: context-manager.sh [create|archive|update] [options]"
    exit 1
    ;;
esac