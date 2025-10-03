#!/bin/bash
# Simple wrapper script for creating files safely
# Designed for use by Claude and other AI agents
#
# Usage:
#   ./create-file.sh /path/to/file.txt "File contents"
#   ./create-file.sh /path/to/file.txt < input.txt
#
# Features:
#   - Creates parent directories automatically
#   - Prevents overwriting existing files (use --force to override)
#   - Validates paths (must be within repository)

set -e

# Get repository root
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

show_help() {
    echo "Usage: $0 [OPTIONS] FILE_PATH [CONTENT]"
    echo ""
    echo "Create a new file with the given content."
    echo ""
    echo "Arguments:"
    echo "  FILE_PATH    Path to the file to create (absolute or relative)"
    echo "  CONTENT      File content (optional, can be piped via stdin)"
    echo ""
    echo "Options:"
    echo "  --force      Overwrite if file exists"
    echo "  --help       Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 docs/new-doc.md \"# New Documentation\""
    echo "  echo \"content\" | $0 output.txt"
    echo "  $0 --force existing.txt \"New content\""
}

# Parse options
FORCE=false
while [[ $# -gt 0 ]]; do
    case $1 in
        --force)
            FORCE=true
            shift
            ;;
        --help|-h)
            show_help
            exit 0
            ;;
        -*)
            echo "Error: Unknown option: $1"
            show_help
            exit 1
            ;;
        *)
            break
            ;;
    esac
done

FILE_PATH="$1"
CONTENT="$2"

if [ -z "$FILE_PATH" ]; then
    echo "Error: FILE_PATH is required"
    show_help
    exit 1
fi

# Convert to absolute path if relative
if [[ "$FILE_PATH" != /* ]]; then
    FILE_PATH="$REPO_ROOT/$FILE_PATH"
fi

# Validate path is within repository
if [[ "$FILE_PATH" != "$REPO_ROOT"* ]]; then
    echo "Error: File path must be within repository: $REPO_ROOT"
    exit 1
fi

# Check if file exists
if [ -f "$FILE_PATH" ] && [ "$FORCE" = false ]; then
    echo "Error: File already exists: $FILE_PATH"
    echo "Use --force to overwrite"
    exit 1
fi

# Create parent directory if needed
DIR_PATH="$(dirname "$FILE_PATH")"
if [ ! -d "$DIR_PATH" ]; then
    echo "Creating directory: $DIR_PATH"
    mkdir -p "$DIR_PATH"
fi

# Write content to file
if [ -n "$CONTENT" ]; then
    # Content provided as argument
    echo "$CONTENT" > "$FILE_PATH"
elif [ ! -t 0 ]; then
    # Content from stdin
    cat > "$FILE_PATH"
else
    # No content provided
    echo "Error: No content provided (use argument or stdin)"
    show_help
    exit 1
fi

echo "✓ Successfully created: $FILE_PATH"
