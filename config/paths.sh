#!/bin/bash
# SkogAI Path Resolution Library for Shell Scripts
#
# Usage:
#   source "$(dirname "$0")/../config/paths.sh"
#   context_dir=$(get_context_dir)
#   agent_file=$(get_agent_path "implementations/research.py")

# Resolve base directory
resolve_base_dir() {
    # Priority order:
    # 1. SKOGAI_BASE_DIR environment variable
    # 2. Git repository root
    # 3. Legacy /home/skogix/skogai

    if [ -n "$SKOGAI_BASE_DIR" ]; then
        echo "$SKOGAI_BASE_DIR"
        return
    fi

    # Try to find git repository root
    local current="$PWD"
    while [ "$current" != "/" ]; do
        if [ -d "$current/.git" ]; then
            echo "$current"
            return
        fi
        current=$(dirname "$current")
    done

    # Fallback to legacy path
    echo "/home/skogix/skogai"
}

# Export base directory
export SKOGAI_BASE_DIR="${SKOGAI_BASE_DIR:-$(resolve_base_dir)}"

# Directory getters
get_base_dir() {
    echo "$SKOGAI_BASE_DIR"
}

get_agents_dir() {
    echo "${SKOGAI_AGENTS_DIR:-$SKOGAI_BASE_DIR/agents}"
}

get_context_dir() {
    echo "${SKOGAI_CONTEXT_DIR:-$SKOGAI_BASE_DIR/context}"
}

get_knowledge_dir() {
    echo "${SKOGAI_KNOWLEDGE_DIR:-$SKOGAI_BASE_DIR/knowledge}"
}

get_config_dir() {
    echo "${SKOGAI_CONFIG_DIR:-$SKOGAI_BASE_DIR/config}"
}

get_demo_dir() {
    echo "${SKOGAI_DEMO_DIR:-$SKOGAI_BASE_DIR/demo}"
}

get_tools_dir() {
    echo "${SKOGAI_TOOLS_DIR:-$SKOGAI_BASE_DIR/tools}"
}

get_metrics_dir() {
    echo "${SKOGAI_METRICS_DIR:-$SKOGAI_BASE_DIR/metrics}"
}

get_venv_dir() {
    echo "${SKOGAI_VENV_DIR:-$SKOGAI_BASE_DIR/.venv}"
}

# Path builders
get_agent_path() {
    local relative_path="$1"
    echo "$(get_agents_dir)/$relative_path"
}

get_context_path() {
    local relative_path="$1"
    echo "$(get_context_dir)/$relative_path"
}

get_knowledge_path() {
    local relative_path="$1"
    echo "$(get_knowledge_dir)/$relative_path"
}

get_config_file() {
    local filename="$1"
    echo "$(get_config_dir)/$filename"
}

get_demo_output_dir() {
    local session_id="$1"
    local prefix="${2:-output}"
    if [ -n "$session_id" ]; then
        echo "$(get_demo_dir)/${prefix}_${session_id}"
    else
        echo "$(get_demo_dir)/$prefix"
    fi
}

# Utility function to ensure directory exists
ensure_dir() {
    local dir="$1"
    mkdir -p "$dir"
    echo "$dir"
}
