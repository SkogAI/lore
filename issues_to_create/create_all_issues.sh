#!/bin/bash
# Script to create all configuration system migration issues
# Usage: ./create_all_issues.sh

set -e

REPO="SkogAI/lore"
ISSUES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

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

echo "Creating configuration system migration issues for $REPO"
echo "=================================================="
echo ""

# Function to extract title from markdown file
get_title() {
    local file=$1
    # Extract title from "## Title" section
    grep -A 1 "^## Title" "$file" | tail -1 | sed 's/^[[:space:]]*//'
}

# Function to extract body from markdown file
get_body() {
    local file=$1
    # Extract everything after "## Body" line
    sed -n '/^## Body/,$ p' "$file" | tail -n +2
}

# Array to store created issue URLs
declare -a created_issues

# Create issues in order (master tracking issue last)
for i in {01..15}; do
    issue_file="$ISSUES_DIR/issue_${i}.md"
    
    if [ ! -f "$issue_file" ]; then
        echo "Skipping issue_${i}.md (file not found)"
        continue
    fi
    
    title=$(get_title "$issue_file")
    body=$(get_body "$issue_file")
    
    if [ -z "$title" ]; then
        echo "Error: Could not extract title from $issue_file"
        continue
    fi
    
    echo "Creating issue ${i}: $title"
    
    # Create the issue and capture the URL
    issue_url=$(gh issue create \
        --repo "$REPO" \
        --title "$title" \
        --body "$body" \
        --label "refactoring,configuration-system,migration" \
        2>&1)
    
    if [ $? -eq 0 ]; then
        echo "✓ Created: $issue_url"
        created_issues+=("$issue_url")
    else
        echo "✗ Failed to create issue ${i}"
        echo "  Error: $issue_url"
    fi
    
    echo ""
    
    # Rate limit protection
    sleep 2
done

# Create master tracking issue last (issue 16)
if [ -f "$ISSUES_DIR/issue_16.md" ]; then
    title=$(get_title "$ISSUES_DIR/issue_16.md")
    body=$(get_body "$ISSUES_DIR/issue_16.md")
    
    echo "Creating master tracking issue: $title"
    
    issue_url=$(gh issue create \
        --repo "$REPO" \
        --title "$title" \
        --body "$body" \
        --label "refactoring,configuration-system,tracking,epic" \
        2>&1)
    
    if [ $? -eq 0 ]; then
        echo "✓ Created master tracking issue: $issue_url"
        created_issues+=("$issue_url")
    else
        echo "✗ Failed to create master tracking issue"
        echo "  Error: $issue_url"
    fi
fi

echo ""
echo "=================================================="
echo "Summary: Created ${#created_issues[@]} issues"
echo ""
echo "Created issues:"
for url in "${created_issues[@]}"; do
    echo "  - $url"
done

echo ""
echo "Next steps:"
echo "1. Review created issues at: https://github.com/$REPO/issues"
echo "2. Update issue #16 to reference specific issue numbers"
echo "3. Begin migration work following the MIGRATION_GUIDE.md"
