#!/bin/bash

# Script to manage context transitions

function create_context() {
  template=$1
  context_type=$2
  session_id=$(date +%s)
  
  cp "/home/skogix/skogai/context/templates/${template}-context.json" "/home/skogix/skogai/context/current/context-${session_id}.json"
  
  # Update basic fields
  sed -i "s/\"created\": \"\"/\"created\": \"$(date -Iseconds)\"/" "/home/skogix/skogai/context/current/context-${session_id}.json"
  sed -i "s/\"last_updated\": \"\"/\"last_updated\": \"$(date -Iseconds)\"/" "/home/skogix/skogai/context/current/context-${session_id}.json"
  sed -i "s/\"session_id\": \"\"/\"session_id\": \"${session_id}\"/" "/home/skogix/skogai/context/current/context-${session_id}.json"
  sed -i "s/\"context_type\": \"base\"/\"context_type\": \"${context_type}\"/" "/home/skogix/skogai/context/current/context-${session_id}.json"
  
  echo $session_id
}

function archive_context() {
  session_id=$1
  
  if [ -f "/home/skogix/skogai/context/current/context-${session_id}.json" ]; then
    mv "/home/skogix/skogai/context/current/context-${session_id}.json" "/home/skogix/skogai/context/archive/context-${session_id}.json"
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
  
  if [ -f "/home/skogix/skogai/context/current/context-${session_id}.json" ]; then
    # This is a simplistic approach - for production use a proper JSON tool like jq
    # For complex nested properties, this would need enhancement
    sed -i "s/\"${key}\": \".*\"/\"${key}\": \"${value}\"/" "/home/skogix/skogai/context/current/context-${session_id}.json"
    sed -i "s/\"last_updated\": \".*\"/\"last_updated\": \"$(date -Iseconds)\"/" "/home/skogix/skogai/context/current/context-${session_id}.json"
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