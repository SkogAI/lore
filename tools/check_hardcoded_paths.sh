#!/bin/bash
# Pre-commit hook to detect hardcoded paths in shell scripts

# Patterns to detect (regex)
PATTERNS=(
    "/home/[a-zA-Z0-9_]+/skogai"
    "/home/[a-zA-Z0-9_]+/lore"
    "/mnt/[^ ]+"
)

# Directories to exclude
EXCLUDE_DIRS="node_modules|MASTER_KNOWLEDGE|MASTER_KNOWLEDGE_COMPLETE|.git|lorefiles|config"

check_file() {
    local file="$1"
    local violations=0

    # Skip excluded directories
    if echo "$file" | grep -E "$EXCLUDE_DIRS" > /dev/null; then
        return 0
    fi

    # Check each pattern
    for pattern in "${PATTERNS[@]}"; do
        if grep -n -E "$pattern" "$file" | grep -v "^#" > /tmp/violations_$$; then
            if [ $violations -eq 0 ]; then
                echo ""
                echo "❌ Hardcoded paths found in $file:"
            fi

            while IFS= read -r line; do
                echo "  $line"
                ((violations++))
            done < /tmp/violations_$$

            rm -f /tmp/violations_$$
        fi
    done

    return $violations
}

total_violations=0

# Check all provided files
for file in "$@"; do
    check_file "$file"
    violations=$?
    ((total_violations += violations))
done

if [ $total_violations -gt 0 ]; then
    echo ""
    echo "❌ Found $total_violations hardcoded path(s)"
    echo ""
    echo "Please use the configuration system instead:"
    echo "  source \"\$(dirname \"\$0\")/../config/paths.sh\""
    echo "  context_dir=\$(get_context_dir)"
    echo ""
    echo "See config/README.md for documentation."
    exit 1
fi

exit 0
