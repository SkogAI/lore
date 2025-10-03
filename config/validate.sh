#!/bin/bash
#
# Validation script to check for hardcoded paths in shell scripts.
#
# This script scans shell script files for hardcoded /home/skogix/skogai paths
# and reports files that need migration to the configuration system.
#
# Usage:
#     ./config/validate.sh
#     ./config/validate.sh /path/to/check
#     STRICT=1 ./config/validate.sh  # Exit with error if hardcoded paths found
#

set -euo pipefail

# Configuration
HARDCODED_PATH="/home/skogix/skogai"
ROOT_PATH="${1:-.}"
STRICT="${STRICT:-0}"

# Colors for output (if terminal supports it)
if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    NC='\033[0m' # No Color
else
    RED=''
    GREEN=''
    YELLOW=''
    NC=''
fi

echo "Scanning shell scripts in: $ROOT_PATH"
echo "Looking for hardcoded paths: $HARDCODED_PATH"
echo ""

# Find shell scripts (*.sh files and files with shebang)
files_checked=0
files_with_violations=0
total_violations=0

# Array to store files with violations
declare -a violation_files=()

# Find .sh files and files with bash/sh shebang
while IFS= read -r -d '' file; do
    # Skip excluded directories
    if echo "$file" | grep -qE '/(\.git|node_modules|\.venv|venv|lorefiles|MASTER_KNOWLEDGE_COMPLETE)/'; then
        continue
    fi

    # Skip validate.sh itself and README
    if [[ "$(basename "$file")" == "validate.sh" ]] || [[ "$(basename "$file")" == "README.md" ]]; then
        continue
    fi

    files_checked=$((files_checked + 1))

    # Check for hardcoded paths (excluding comments that are examples)
    violations=$(grep -n "$HARDCODED_PATH" "$file" 2>/dev/null | grep -v "# Example:" | grep -v "# example:" || true)

    if [ -n "$violations" ]; then
        files_with_violations=$((files_with_violations + 1))
        violation_count=$(echo "$violations" | wc -l)
        total_violations=$((total_violations + violation_count))

        # Get relative path
        rel_path="${file#$ROOT_PATH/}"
        rel_path="${rel_path#./}"

        echo -e "${RED}❌ $rel_path${NC}"
        while IFS= read -r violation; do
            line_num=$(echo "$violation" | cut -d: -f1)
            line_content=$(echo "$violation" | cut -d: -f2-)
            echo "   Line $line_num: $line_content"
        done <<< "$violations"
        echo ""

        violation_files+=("$rel_path")
    fi
done < <(find "$ROOT_PATH" -type f \( -name "*.sh" -o -exec grep -l "^#!/bin/bash\|^#!/bin/sh" {} + \) -print0 2>/dev/null)

# Summary
echo "======================================================================"
echo "Summary:"
echo "  Total files checked: $files_checked"
echo "  Files with hardcoded paths: $files_with_violations"
echo "  Total violations: $total_violations"
echo ""

if [ $files_with_violations -gt 0 ]; then
    echo -e "${YELLOW}Migration needed! Use the config/paths.sh module:${NC}"
    echo ""
    echo "  # Source the configuration"
    echo "  source \"\$(dirname \"\$0\")/config/paths.sh\""
    echo ""
    echo "  # Use exported variables"
    echo "  echo \"Base: \$SKOGAI_BASE_DIR\""
    echo "  log_file=\$(skogai_get_log_file \"agent.log\")"
    echo ""
    echo "See config/README.md for migration patterns and examples."
    echo ""

    if [ "$STRICT" = "1" ]; then
        exit 1
    fi
else
    echo -e "${GREEN}✅ No hardcoded paths found! All files use the configuration system.${NC}"
fi
