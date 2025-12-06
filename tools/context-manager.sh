#!/bin/bash

# Script to manage context transitions

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CONTEXT_DIR="${BASE_DIR}/context"
TEMPLATES_DIR="${CONTEXT_DIR}/templates"
CURRENT_DIR="${CONTEXT_DIR}/current"
ARCHIVE_DIR="${CONTEXT_DIR}/archive"

# Ensure directories exist
mkdir -p "${TEMPLATES_DIR}"
mkdir -p "${CURRENT_DIR}"
mkdir -p "${ARCHIVE_DIR}"

function create_context() {
  local template=$1
  local context_type=${2:-"base"}
  local session_id=$(date +%s)

  if [ -z "$template" ]; then
    echo "Error: template name required"
    echo "Usage: context-manager.sh create <template> [context_type]"
    return 1
  fi

  local template_file="${TEMPLATES_DIR}/${template}-context.json"
  local context_file="${CURRENT_DIR}/context-${session_id}.json"

  if [ ! -f "$template_file" ]; then
    echo "Error: Template not found: $template_file"
    return 1
  fi

  cp "$template_file" "$context_file"

  # Update fields using jq
  local timestamp=$(date -Iseconds)
  jq ".created = \"$timestamp\" | .last_updated = \"$timestamp\" | .session_id = \"$session_id\" | .context_type = \"$context_type\"" \
    "$context_file" > "${context_file}.tmp" && mv "${context_file}.tmp" "$context_file"

  echo $session_id
}

function archive_context() {
  local session_id=$1

  if [ -z "$session_id" ]; then
    echo "Error: session_id required"
    echo "Usage: context-manager.sh archive <session_id>"
    return 1
  fi

  local context_file="${CURRENT_DIR}/context-${session_id}.json"
  local archive_file="${ARCHIVE_DIR}/context-${session_id}.json"

  if [ -f "$context_file" ]; then
    mv "$context_file" "$archive_file"
    echo "Context archived successfully."
  else
    echo "Error: Context not found: $context_file"
    return 1
  fi
}

function update_context() {
  local session_id=$1
  local key=$2
  local value=$3

  if [ -z "$session_id" ] || [ -z "$key" ] || [ -z "$value" ]; then
    echo "Error: session_id, key, and value required"
    echo "Usage: context-manager.sh update <session_id> <key> <value>"
    return 1
  fi

  local context_file="${CURRENT_DIR}/context-${session_id}.json"

  if [ -f "$context_file" ]; then
    local timestamp=$(date -Iseconds)
    jq ".[\"$key\"] = \"$value\" | .last_updated = \"$timestamp\"" \
      "$context_file" > "${context_file}.tmp" && mv "${context_file}.tmp" "$context_file"
    echo "Context updated successfully."
  else
    echo "Error: Context not found: $context_file"
    return 1
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