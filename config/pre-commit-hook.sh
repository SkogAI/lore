#!/bin/bash
#
# Pre-commit hook to prevent hardcoded paths
#
# This hook checks staged files for hardcoded /home/skogix/skogai paths
# and blocks commits that introduce them.
#
# Installation:
#     cp config/pre-commit-hook.sh .git/hooks/pre-commit
#     chmod +x .git/hooks/pre-commit
#

set -euo pipefail

HARDCODED_PATH="/home/skogix/skogai"

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "Checking for hardcoded paths in staged files..."

# Get list of staged files
staged_files=$(git diff --cached --name-only --diff-filter=ACM)

violations_found=0

for file in $staged_files; do
    # Skip if file doesn't exist (e.g., deleted)
    [ -f "$file" ] || continue

    # Skip certain file types and directories
    if echo "$file" | grep -qE '\.(md|txt|json|lock)$'; then
        continue
    fi
    if echo "$file" | grep -qE '/(lorefiles|MASTER_KNOWLEDGE_COMPLETE|node_modules)/'; then
        continue
    fi
    if [[ "$(basename "$file")" == "validate.py" ]] || [[ "$(basename "$file")" == "validate.sh" ]]; then
        continue
    fi

    # Check for hardcoded paths in staged changes
    if git diff --cached "$file" | grep -q "^\+.*$HARDCODED_PATH"; then
        if [ $violations_found -eq 0 ]; then
            echo -e "${RED}❌ Hardcoded paths detected in staged files!${NC}"
            echo ""
        fi
        violations_found=1

        echo -e "${RED}File: $file${NC}"
        git diff --cached "$file" | grep --color=always "^\+.*$HARDCODED_PATH" || true
        echo ""
    fi
done

if [ $violations_found -eq 1 ]; then
    echo -e "${YELLOW}Commit blocked: Please use the configuration system instead.${NC}"
    echo ""
    echo "Python:"
    echo "  from config.paths import get_base_dir, get_path"
    echo "  base_dir = get_base_dir()"
    echo ""
    echo "Shell:"
    echo "  source \"\$(dirname \"\$0\")/config/paths.sh\""
    echo "  echo \"\$SKOGAI_BASE_DIR\""
    echo ""
    echo "See config/README.md for more information."
    echo ""
    echo "To bypass this check (not recommended):"
    echo "  git commit --no-verify"
    exit 1
fi

echo "✅ No hardcoded paths found in staged files."
exit 0
