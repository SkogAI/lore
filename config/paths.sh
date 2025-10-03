#!/bin/bash
#
# Centralized path configuration for LORE project (Shell/Bash)
#
# This script provides a single source of truth for all file system paths used
# throughout the LORE project shell scripts. It supports:
#
# - Environment variable overrides (SKOGAI_BASE_DIR)
# - Git-aware path resolution (auto-detects repository root)
# - Backward compatibility (defaults to /home/skogix/skogai)
# - Multiple deployment scenarios
#
# Usage:
#     source "$(dirname "$0")/config/paths.sh"
#     echo "Agents dir: $SKOGAI_AGENTS_DIR"
#     log_file="$(skogai_get_path "logs" "agent.log")"
#

# Get the repository root using git
skogai_get_repo_root() {
    if command -v git >/dev/null 2>&1; then
        git rev-parse --show-toplevel 2>/dev/null
    fi
}

# Get the base directory for the LORE project
# Resolution order:
# 1. SKOGAI_BASE_DIR environment variable
# 2. Git repository root (if available)
# 3. Default: /home/skogix/skogai (for backward compatibility)
skogai_get_base_dir() {
    if [ -n "$SKOGAI_BASE_DIR" ]; then
        echo "$SKOGAI_BASE_DIR"
    else
        local repo_root
        repo_root=$(skogai_get_repo_root)
        if [ -n "$repo_root" ]; then
            echo "$repo_root"
        else
            echo "/home/skogix/skogai"
        fi
    fi
}

# Initialize base directory
SKOGAI_BASE_DIR="${SKOGAI_BASE_DIR:-$(skogai_get_base_dir)}"

# Export standard directory paths
export SKOGAI_BASE_DIR
export SKOGAI_AGENTS_DIR="${SKOGAI_BASE_DIR}/agents"
export SKOGAI_CONFIG_DIR="${SKOGAI_BASE_DIR}/config"
export SKOGAI_DEMO_DIR="${SKOGAI_BASE_DIR}/demo"
export SKOGAI_DOCS_DIR="${SKOGAI_BASE_DIR}/docs"
export SKOGAI_LOGS_DIR="${SKOGAI_LOGS_DIR:-${SKOGAI_BASE_DIR}/logs}"
export SKOGAI_LOREFILES_DIR="${SKOGAI_BASE_DIR}/lorefiles"
export SKOGAI_TOOLS_DIR="${SKOGAI_BASE_DIR}/tools"

# Get a path relative to the base directory
# Usage: skogai_get_path "logs" "agent.log"
skogai_get_path() {
    local path="$SKOGAI_BASE_DIR"
    for part in "$@"; do
        path="$path/$part"
    done
    echo "$path"
}

# Ensure a directory exists
# Usage: skogai_ensure_dir "$SKOGAI_LOGS_DIR"
skogai_ensure_dir() {
    local dir="$1"
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
    fi
    echo "$dir"
}

# Get a log file path, ensuring the logs directory exists
# Usage: log_file=$(skogai_get_log_file "agent.log")
skogai_get_log_file() {
    local filename="$1"
    skogai_ensure_dir "$SKOGAI_LOGS_DIR" >/dev/null
    echo "$SKOGAI_LOGS_DIR/$filename"
}

# Print configuration (for debugging)
skogai_print_config() {
    echo "LORE Configuration:"
    echo "  Base Directory:      $SKOGAI_BASE_DIR"
    echo "  Agents Directory:    $SKOGAI_AGENTS_DIR"
    echo "  Config Directory:    $SKOGAI_CONFIG_DIR"
    echo "  Demo Directory:      $SKOGAI_DEMO_DIR"
    echo "  Docs Directory:      $SKOGAI_DOCS_DIR"
    echo "  Logs Directory:      $SKOGAI_LOGS_DIR"
    echo "  Lorefiles Directory: $SKOGAI_LOREFILES_DIR"
    echo "  Tools Directory:     $SKOGAI_TOOLS_DIR"
}

# If sourced with --print flag, print configuration
if [ "$1" = "--print" ]; then
    skogai_print_config
fi
