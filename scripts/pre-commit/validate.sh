#!/bin/bash
# Check for hardcoded absolute paths in shell scripts
# Usage: ./scripts/pre-commit/validate.sh [directory] [STRICT=1 for error on violations]

set -euo pipefail

HARDCODED_PATTERNS=(
    "/home/skogix/lore"
    "/home/skogix/skogai"
)
ROOT_PATH="${1:-.}"
STRICT="${STRICT:-0}"

# Colors if terminal
if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    NC='\033[0m'
else
    RED='' GREEN='' YELLOW='' NC=''
fi

echo "Scanning: $ROOT_PATH for hardcoded paths"
echo ""

files_checked=0
files_with_violations=0
total_violations=0

# Find shell scripts
while IFS= read -r file; do
    # Skip excluded paths
    case "$file" in
        */.git/*|*/node_modules/*|*/.venv/*|*/venv/*|*/lorefiles/*) continue ;;
        */validate.sh|*/README.md|*/pre-commit-hook.sh) continue ;;
    esac

    files_checked=$((files_checked + 1))

    # Check file for hardcoded paths
    violations=0
    for pattern in "${HARDCODED_PATTERNS[@]}"; do
        while IFS=: read -r line_num line_content; do
            # Skip example comments and @env annotations (argc documentation)
            [[ "$line_content" =~ ^[[:space:]]*#.*[Ee]xample ]] && continue
            [[ "$line_content" =~ ^[[:space:]]*#[[:space:]]*@env ]] && continue

            violations=$((violations + 1))
            total_violations=$((total_violations + 1))

            if [ $violations -eq 1 ]; then
                files_with_violations=$((files_with_violations + 1))
                rel_path="${file#$ROOT_PATH/}"
                echo -e "${RED}❌ ${rel_path#./}${NC}"
            fi

            echo "   Line $line_num: $line_content"
        done < <(grep -n "$pattern" "$file" 2>/dev/null || true)
    done

    [ $violations -gt 0 ] && echo ""
done < <(find "$ROOT_PATH" -type f -name "*.sh" 2>/dev/null)

# Summary
echo "======================================================================"
echo "Summary:"
echo "  Files checked: $files_checked"
echo "  Files with violations: $files_with_violations"
echo "  Total violations: $total_violations"
echo ""

if [ $files_with_violations -gt 0 ]; then
    echo -e "${YELLOW}Fix by using relative paths:${NC}"
    echo "  REPO_ROOT=\"\$(cd \"\$(dirname \"\${BASH_SOURCE[0]}\")\" && pwd)\""
    echo "  path=\"\$REPO_ROOT/subdir/file.sh\""
    echo ""
    [ "$STRICT" = "1" ] && exit 1
else
    echo -e "${GREEN}✅ No hardcoded absolute paths found${NC}"
fi
