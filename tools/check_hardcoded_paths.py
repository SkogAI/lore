#!/usr/bin/env python3
"""Pre-commit hook to detect hardcoded paths in Python files.

This script scans Python files for hardcoded absolute paths that should
be replaced with the configuration system.
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple


# Patterns to detect hardcoded paths
HARDCODED_PATTERNS = [
    r"/home/[a-zA-Z0-9_]+/skogai",
    r"/home/[a-zA-Z0-9_]+/lore",
    r"['\"]\/mnt\/[^'\"]+['\"]",  # Any /mnt/ paths
]

# Files/directories to exclude from checks
EXCLUDE_PATTERNS = [
    "node_modules/",
    "MASTER_KNOWLEDGE/",
    "MASTER_KNOWLEDGE_COMPLETE/",
    ".git/",
    "lorefiles/",
    "config/",  # Exclude config module itself
    "tools/check_hardcoded_paths.py",  # Exclude this file
    ".pre-commit-config.yaml",
]


def should_exclude(filepath: str) -> bool:
    """Check if a file should be excluded from scanning."""
    for pattern in EXCLUDE_PATTERNS:
        if pattern in filepath:
            return True
    return False


def check_file(filepath: str) -> List[Tuple[int, str]]:
    """Check a Python file for hardcoded paths.

    Args:
        filepath: Path to the file to check

    Returns:
        List of tuples (line_number, line_content) containing hardcoded paths
    """
    violations = []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                # Skip comments
                if line.strip().startswith("#"):
                    continue

                # Check each pattern
                for pattern in HARDCODED_PATTERNS:
                    if re.search(pattern, line):
                        violations.append((line_num, line.strip()))
                        break

    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)

    return violations


def main(files: List[str]) -> int:
    """Main function to check files for hardcoded paths.

    Args:
        files: List of file paths to check

    Returns:
        Exit code (0 for success, 1 for violations found)
    """
    total_violations = 0

    for filepath in files:
        if should_exclude(filepath):
            continue

        violations = check_file(filepath)

        if violations:
            print(f"\n❌ Hardcoded paths found in {filepath}:")
            for line_num, line in violations:
                print(f"  Line {line_num}: {line}")
            total_violations += len(violations)

    if total_violations > 0:
        print(f"\n❌ Found {total_violations} hardcoded path(s)")
        print("\nPlease use the configuration system instead:")
        print("  from config import paths")
        print("  path = paths.get_agent_path('implementations/...')")
        print("\nSee config/README.md for documentation.")
        return 1

    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: check_hardcoded_paths.py <file1> [file2 ...]")
        sys.exit(1)

    exit_code = main(sys.argv[1:])
    sys.exit(exit_code)
