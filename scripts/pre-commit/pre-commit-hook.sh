#!/bin/bash
# Pre-commit hook to prevent hardcoded absolute paths
#
# Installation:
#   cp scripts/pre-commit/pre-commit-hook.sh .git/hooks/pre-commit
#   chmod +x .git/hooks/pre-commit

set -euo pipefail

# Paths to check for
HARDCODED_PATTERNS=(
    "/home/skogix/lore"
    "/home/skogix/skogai"
)
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "Checking staged files for hardcoded paths..."

violations_found=0

# Check each staged file
while IFS= read -r file; do
    # Skip if file doesn't exist or is wrong type
    [ -f "$file" ] || continue

    case "$file" in
        *.md|*.txt|*.json|*.lock) continue ;;
        */lorefiles/*|*/node_modules/*|*/.venv/*) continue ;;
        */validate.py|*/validate.sh|*/pre-commit-hook.sh) continue ;;
    esac

    # Check staged changes for any hardcoded pattern
    for pattern in "${HARDCODED_PATTERNS[@]}"; do
        # Get lines with pattern, excluding @env annotations
        matches=$(git diff --cached "$file" | grep "^+.*$pattern" | grep -v "^+.*#[[:space:]]*@env" || true)

        if [ -n "$matches" ]; then
            if [ $violations_found -eq 0 ]; then
                echo -e "${RED}❌ Hardcoded absolute paths detected!${NC}"
                echo ""
            fi
            violations_found=1

            echo -e "${RED}File: $file${NC}"
            echo "$matches"
            echo ""
        fi
    done
done < <(git diff --cached --name-only --diff-filter=ACM)

if [ $violations_found -eq 1 ]; then
    echo -e "${YELLOW}Commit blocked. Use relative paths instead:${NC}"
    echo ""
    echo "Python:"
    echo "  from pathlib import Path"
    echo "  repo_root = Path(__file__).parent.parent"
    echo "  path = repo_root / \"subdir\" / \"file.py\""
    echo ""
    echo "Shell:"
    echo "  REPO_ROOT=\"\$(cd \"\$(dirname \"\${BASH_SOURCE[0]}\")\" && pwd)\""
    echo "  path=\"\$REPO_ROOT/subdir/file.sh\""
    echo ""
    echo "Bypass (not recommended): git commit --no-verify"
    exit 1
fi

echo "✅ No hardcoded paths"
exit 0
