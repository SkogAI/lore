#!/bin/bash
# Simple wrapper script for creating GitHub issues
# Designed for use by Claude and other AI agents
#
# Usage:
#   ./gh-create-issue.sh "Issue Title" "Issue Body" [label1,label2,...]
#
# Example:
#   ./gh-create-issue.sh "Fix bug" "This is a bug description" "bug,urgent"
#   ./gh-create-issue.sh "New feature" "$(cat issue_body.md)"

set -e

REPO="SkogAI/lore"

# Check if gh CLI is available
if ! command -v gh &> /dev/null; then
    echo "Error: gh CLI is not installed or not in PATH"
    echo "Install from: https://cli.github.com/"
    exit 1
fi

# Check authentication
if ! gh auth status &> /dev/null; then
    echo "Error: Not authenticated with GitHub"
    echo "Run: gh auth login"
    exit 1
fi

# Parse arguments
TITLE="$1"
BODY="$2"
LABELS="${3:-}"

if [ -z "$TITLE" ]; then
    echo "Usage: $0 \"Issue Title\" \"Issue Body\" [label1,label2,...]"
    echo ""
    echo "Examples:"
    echo "  $0 \"Fix login bug\" \"Users cannot login on mobile\" \"bug,urgent\""
    echo "  $0 \"Migrate OpenRouter scripts\" \"\$(cat issue_body.md)\" \"migration\""
    exit 1
fi

if [ -z "$BODY" ]; then
    echo "Error: Issue body cannot be empty"
    exit 1
fi

# Build the gh command
CMD=(gh issue create --repo "$REPO" --title "$TITLE" --body "$BODY")

# Add labels if provided
if [ -n "$LABELS" ]; then
    CMD+=(--label "$LABELS")
fi

# Create the issue
echo "Creating issue: $TITLE"
echo "Repository: $REPO"
if [ -n "$LABELS" ]; then
    echo "Labels: $LABELS"
fi
echo ""

ISSUE_URL=$("${CMD[@]}")

if [ $? -eq 0 ]; then
    echo "✓ Successfully created issue: $ISSUE_URL"
    exit 0
else
    echo "✗ Failed to create issue"
    exit 1
fi
