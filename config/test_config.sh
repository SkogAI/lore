#!/bin/bash
#
# Simple test script to verify the shell configuration system works correctly.
#

set -euo pipefail

echo "======================================================================"
echo "Configuration System Test (Shell)"
echo "======================================================================"
echo ""

# Source the configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/paths.sh"

echo "Testing basic path resolution..."

# Test that variables are set
if [ -z "$SKOGAI_BASE_DIR" ]; then
    echo "  ❌ SKOGAI_BASE_DIR not set"
    exit 1
fi
echo "  ✅ Base directory: $SKOGAI_BASE_DIR"

if [ -z "$SKOGAI_AGENTS_DIR" ]; then
    echo "  ❌ SKOGAI_AGENTS_DIR not set"
    exit 1
fi
echo "  ✅ Agents directory: $SKOGAI_AGENTS_DIR"

if [ -z "$SKOGAI_CONFIG_DIR" ]; then
    echo "  ❌ SKOGAI_CONFIG_DIR not set"
    exit 1
fi
echo "  ✅ Config directory: $SKOGAI_CONFIG_DIR"

if [ -z "$SKOGAI_DEMO_DIR" ]; then
    echo "  ❌ SKOGAI_DEMO_DIR not set"
    exit 1
fi
echo "  ✅ Demo directory: $SKOGAI_DEMO_DIR"

if [ -z "$SKOGAI_CONTEXT_DIR" ]; then
    echo "  ❌ SKOGAI_CONTEXT_DIR not set"
    exit 1
fi
echo "  ✅ Context directory: $SKOGAI_CONTEXT_DIR"

if [ -z "$SKOGAI_DOCS_DIR" ]; then
    echo "  ❌ SKOGAI_DOCS_DIR not set"
    exit 1
fi
echo "  ✅ Docs directory: $SKOGAI_DOCS_DIR"

if [ -z "$SKOGAI_KNOWLEDGE_DIR" ]; then
    echo "  ❌ SKOGAI_KNOWLEDGE_DIR not set"
    exit 1
fi
echo "  ✅ Knowledge directory: $SKOGAI_KNOWLEDGE_DIR"

if [ -z "$SKOGAI_LOREFILES_DIR" ]; then
    echo "  ❌ SKOGAI_LOREFILES_DIR not set"
    exit 1
fi
echo "  ✅ Lorefiles directory: $SKOGAI_LOREFILES_DIR"

echo ""
echo "Testing custom path construction..."

path1=$(skogai_get_path "demo" "workflow.py")
expected1="$SKOGAI_BASE_DIR/demo/workflow.py"
if [ "$path1" != "$expected1" ]; then
    echo "  ❌ Custom path 1: expected $expected1, got $path1"
    exit 1
fi
echo "  ✅ Custom path 1: $path1"

path2=$(skogai_get_path "agents" "api" "agent_api.py")
expected2="$SKOGAI_BASE_DIR/agents/api/agent_api.py"
if [ "$path2" != "$expected2" ]; then
    echo "  ❌ Custom path 2: expected $expected2, got $path2"
    exit 1
fi
echo "  ✅ Custom path 2: $path2"

echo ""
echo "Testing directory creation..."

# Create a temporary directory for testing
test_dir=$(mktemp -d)
trap "rm -rf $test_dir" EXIT

nested_dir="$test_dir/test/nested/dir"
skogai_ensure_dir "$nested_dir" >/dev/null

if [ ! -d "$nested_dir" ]; then
    echo "  ❌ Directory creation failed"
    exit 1
fi
echo "  ✅ Directory creation works"

echo ""
echo "======================================================================"
echo "✅ All tests passed!"
echo "======================================================================"
