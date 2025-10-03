#!/bin/bash
#
# Centralized path configuration for LORE project (Shell/Bash)
#
# This script provides a single source of truth for all file system paths used
# throughout the LORE project shell scripts.
#
# Requirements:
# - SKOGAI_LORE must be set (via skogcli config export-env --namespace skogai)
#
# Usage:
#     source "$(dirname "$0")/config/paths.sh"
#     echo "Agents dir: $SKOGAI_AGENTS_DIR"
#     custom_path="$(skogai_get_path "demo" "workflow.py")"
#

# Verify SKOGAI_LORE is set
if [ -z "$SKOGAI_LORE" ]; then
    echo "ERROR: SKOGAI_LORE environment variable not set" >&2
    echo "Please ensure 'skogcli config export-env --namespace skogai' is sourced" >&2
    if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
        exit 1
    else
        return 1
    fi
fi

# Export base directory (SKOGAI_LORE)
export SKOGAI_BASE_DIR="$SKOGAI_LORE"

# Export lore-specific directory paths
export SKOGAI_AGENTS_DIR="${SKOGAI_LORE}/agents"
export SKOGAI_CONFIG_DIR="${SKOGAI_LORE}/config"
export SKOGAI_CONTEXT_DIR="${SKOGAI_LORE}/context"
export SKOGAI_DEMO_DIR="${SKOGAI_LORE}/demo"
export SKOGAI_DOCS_DIR="${SKOGAI_LORE}/docs"
export SKOGAI_KNOWLEDGE_DIR="${SKOGAI_LORE}/knowledge"
export SKOGAI_LOREFILES_DIR="${SKOGAI_LORE}/lorefiles"

# Note: SKOGAI_LOGS_DIR is managed by skogai config (not lore-specific)
# Note: SKOGAI_TOOLS_DIR is managed by skogcli scripts (not lore-specific)

# Get a path relative to the base directory
# Usage: skogai_get_path "demo" "workflow.py"
skogai_get_path() {
    local path="$SKOGAI_LORE"
    for part in "$@"; do
        path="$path/$part"
    done
    echo "$path"
}

# Ensure a directory exists
# Usage: skogai_ensure_dir "$SKOGAI_AGENTS_DIR"
skogai_ensure_dir() {
    local dir="$1"
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
    fi
    echo "$dir"
}

# Print configuration (for debugging)
skogai_print_config() {
    echo "LORE Configuration:"
    echo "  Base Directory (LORE): $SKOGAI_LORE"
    echo "  Agents Directory:      $SKOGAI_AGENTS_DIR"
    echo "  Config Directory:      $SKOGAI_CONFIG_DIR"
    echo "  Context Directory:     $SKOGAI_CONTEXT_DIR"
    echo "  Demo Directory:        $SKOGAI_DEMO_DIR"
    echo "  Docs Directory:        $SKOGAI_DOCS_DIR"
    echo "  Knowledge Directory:   $SKOGAI_KNOWLEDGE_DIR"
    echo "  Lorefiles Directory:   $SKOGAI_LOREFILES_DIR"
    echo ""
    echo "External (managed by skogai/skogcli):"
    echo "  Logs Directory:        \${SKOGAI_LOGS_DIR} (from skogai config)"
    echo "  Tools:                 via skogcli scripts"
}

# If sourced with --print flag, print configuration
if [ "${1:-}" = "--print" ]; then
    skogai_print_config
fi
