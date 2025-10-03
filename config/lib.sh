#!/bin/bash
#
# Centralized library functions for LORE project (Shell/Bash)
#
# This script provides reusable helper functions to avoid complex
# sed/awk chains and promote code reuse across shell scripts.
#
# Usage:
#     source "$(dirname "$0")/../config/lib.sh"
#

# Convert comma-separated values to JSON array format
# Usage: json_array_from_csv "item1,item2,item3"
# Output: ["item1","item2","item3"]
json_array_from_csv() {
    local csv="$1"

    # Handle empty input
    if [ -z "$csv" ]; then
        echo "[]"
        return
    fi

    # Use jq for proper JSON formatting (handles escaping)
    if command -v jq &> /dev/null; then
        echo "$csv" | jq -R 'split(",") | map(gsub("^\\s+|\\s+$";""))'
    else
        # Fallback to bash if jq not available (less robust)
        echo "[$csv]" | sed 's/,/","/g' | sed 's/\[/["/' | sed 's/\]/"]/''
    fi
}

# Extract value from "KEY: value" formatted text
# Usage: extract_key_value "$text" "NAME"
# Output: extracted value
extract_key_value() {
    local text="$1"
    local key="$2"

    echo "$text" | grep -oP "^${key}: \K.*" | head -n 1
}

# Extract value from "KEY: value" formatted text (case-insensitive)
# Usage: extract_key_value_i "$text" "TRAITS"
# Output: extracted value
extract_key_value_i() {
    local text="$1"
    local key="$2"

    echo "$text" | grep -i "^${key}:" | head -n 1 | sed "s/${key}://i" | xargs
}

# Parse JSON and safely create a jq filter for array from CSV
# Usage: jq_array_from_csv "tag1,tag2,tag3"
# Output: jq filter ready string: ["tag1","tag2","tag3"]
jq_array_from_csv() {
    local csv="$1"

    # Handle empty input
    if [ -z "$csv" ]; then
        echo "[]"
        return
    fi

    # Use jq to properly handle escaping and formatting
    echo -n "$csv" | jq -R 'split(",") | map(gsub("^\\s+|\\s+$";""))'
}

# Get the repository root directory
# This replaces the common pattern: SKOGAI_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# Usage: SKOGAI_DIR=$(get_repo_root)
get_repo_root() {
    # Try git root first
    if git rev-parse --show-toplevel 2>/dev/null; then
        return
    fi

    # Fallback to parent directory traversal
    local script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    local current_dir="$script_dir"

    # Look for .git directory or key files
    while [ "$current_dir" != "/" ]; do
        if [ -d "$current_dir/.git" ] || [ -f "$current_dir/pyproject.toml" ]; then
            echo "$current_dir"
            return
        fi
        current_dir="$(dirname "$current_dir")"
    done

    # If nothing found, assume parent of script directory
    echo "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
}

# Load environment variables from skogcli config
# This should be called at the start of scripts that need environment variables
# Usage: load_skogcli_env
load_skogcli_env() {
    if command -v skogcli &> /dev/null; then
        eval "$(skogcli config export-env --namespace skogai,claude,openai 2>/dev/null || true)"
    fi
}

# Check if a command exists
# Usage: if has_command jq; then ... fi
has_command() {
    command -v "$1" &> /dev/null
}

# Ensure a directory exists
# Usage: ensure_dir "/path/to/dir"
ensure_dir() {
    local dir="$1"
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
    fi
}

# Generate a timestamp-based unique ID
# Usage: id=$(generate_id)
# Output: 1234567890_a1b2c3d4
generate_id() {
    if has_command openssl; then
        echo "$(date +%s)_$(openssl rand -hex 4)"
    else
        # Fallback without openssl
        echo "$(date +%s)_$(cat /dev/urandom | tr -dc 'a-f0-9' | head -c 8)"
    fi
}

# Get ISO 8601 timestamp
# Usage: timestamp=$(get_timestamp)
get_timestamp() {
    date -u +"%Y-%m-%dT%H:%M:%SZ"
}

# Pretty print a message with a prefix
# Usage: log_info "Starting process..."
log_info() {
    echo "[INFO] $*"
}

log_error() {
    echo "[ERROR] $*" >&2
}

log_warn() {
    echo "[WARN] $*" >&2
}

# Export functions for use in subshells if needed
export -f json_array_from_csv 2>/dev/null || true
export -f extract_key_value 2>/dev/null || true
export -f extract_key_value_i 2>/dev/null || true
export -f jq_array_from_csv 2>/dev/null || true
export -f get_repo_root 2>/dev/null || true
export -f load_skogcli_env 2>/dev/null || true
export -f has_command 2>/dev/null || true
export -f ensure_dir 2>/dev/null || true
export -f generate_id 2>/dev/null || true
export -f get_timestamp 2>/dev/null || true
export -f log_info 2>/dev/null || true
export -f log_error 2>/dev/null || true
export -f log_warn 2>/dev/null || true
