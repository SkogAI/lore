#!/bin/bash
# SkogAI Issue Creator Workflow - Shell Wrapper
# This script provides a convenient shell interface to the Python issue creator

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ISSUE_CREATOR="$SCRIPT_DIR/issue-creator.py"

# Check if Python script exists
if [ ! -f "$ISSUE_CREATOR" ]; then
    echo "Error: Issue creator script not found at $ISSUE_CREATOR"
    exit 1
fi

# Display help information
show_help() {
    echo "SkogAI Issue Creator Workflow"
    echo ""
    echo "Usage: $0 [command] [options]"
    echo ""
    echo "Commands:"
    echo "  interactive    Start interactive issue creation"
    echo "  templates      List available issue templates"
    echo "  create         Create issue from command line"
    echo "  help           Show this help message"
    echo ""
    echo "Quick Creation Examples:"
    echo "  $0 feature \"Add search\" \"Implement user search functionality\""
    echo "  $0 bug \"Login broken\" \"Users cannot login on mobile\" --priority 1"
    echo "  $0 knowledge \"Research API patterns\" \"Investigate current API design patterns\""
    echo "  $0 governance \"New voting system\" \"Proposal for improved agent voting\""
    echo ""
    echo "Interactive Mode:"
    echo "  $0 interactive"
    echo ""
    echo "Options for create command:"
    echo "  --priority N   Set priority (1=urgent, 2=high, 3=normal, 4=low)"
    echo "  --assignee ID  Assign to specific agent"
    echo "  --labels L1 L2 Set custom labels"
    echo ""
}

# Quick creation shortcuts
create_quick() {
    local issue_type="$1"
    local title="$2"
    local description="$3"
    shift 3
    
    if [ -z "$title" ] || [ -z "$description" ]; then
        echo "Usage: $0 $issue_type \"Title\" \"Description\" [options]"
        return 1
    fi
    
    python3 "$ISSUE_CREATOR" create "$title" "$description" --type "$issue_type" "$@"
}

# Main command processing  
case "$1" in
    interactive)
        python3 "$ISSUE_CREATOR" interactive
        ;;
    templates)
        python3 "$ISSUE_CREATOR" templates
        ;;
    create)
        shift
        python3 "$ISSUE_CREATOR" create "$@"
        ;;
    feature|bug|knowledge|governance|architecture)
        create_quick "$@"
        ;;
    help|--help|-h)
        show_help
        ;;
    "")
        echo "SkogAI Issue Creator"
        echo "Run '$0 help' for usage information or '$0 interactive' to start."
        echo ""
        echo "Quick start:"
        echo "  $0 interactive"
        echo "  $0 templates"
        ;;
    *)
        echo "Unknown command: $1"
        echo "Run '$0 help' for usage information."
        exit 1
        ;;
esac