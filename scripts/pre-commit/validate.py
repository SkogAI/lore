#!/usr/bin/env python3
"""
Validation script to check for hardcoded paths in Python files.

This script scans Python files for hardcoded /home/skogix/skogai paths
and reports files that need migration to the configuration system.

Usage:
    python config/validate.py
    python config/validate.py --path /path/to/check
    python config/validate.py --strict  # Exit with error if hardcoded paths found
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple


# Pattern to match hardcoded paths
HARDCODED_PATH_PATTERN = re.compile(r'["\']*/home/skogix/skogai[^"\']*["\']?')

# Directories to skip
SKIP_DIRS = {
    ".git",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "env",
    "lorefiles",  # Archive files
    "MASTER_KNOWLEDGE_COMPLETE",  # Archive
    ".pytest_cache",
    ".mypy_cache",
}

# Files to skip (e.g., this validation script itself)
SKIP_FILES = {
    "validate.py",
    "README.md",  # Documentation can mention paths as examples
}


def find_python_files(root: Path) -> List[Path]:
    """Find all Python files in the directory tree."""
    python_files = []
    for path in root.rglob("*.py"):
        # Skip excluded directories
        if any(skip_dir in path.parts for skip_dir in SKIP_DIRS):
            continue
        # Skip excluded files
        if path.name in SKIP_FILES:
            continue
        python_files.append(path)
    return python_files


def check_file(file_path: Path) -> List[Tuple[int, str]]:
    """
    Check a file for hardcoded paths.

    Returns:
        List of (line_number, line_content) tuples where hardcoded paths were found
    """
    violations = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, start=1):
                # Skip comments that are just documentation
                stripped = line.strip()
                if stripped.startswith("#") and "example" in stripped.lower():
                    continue

                # Check for hardcoded path pattern
                if HARDCODED_PATH_PATTERN.search(line):
                    violations.append((line_num, line.rstrip()))
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)
    return violations


def main():
    parser = argparse.ArgumentParser(
        description="Validate Python files for hardcoded paths"
    )
    parser.add_argument(
        "--path",
        type=Path,
        default=Path("."),
        help="Root path to check (default: current directory)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with error code if hardcoded paths are found",
    )
    args = parser.parse_args()

    root_path = args.path.resolve()
    print(f"Scanning Python files in: {root_path}")
    print(f"Looking for hardcoded paths: /home/skogix/skogai")
    print()

    python_files = find_python_files(root_path)
    print(f"Found {len(python_files)} Python files to check")
    print()

    files_with_violations = 0
    total_violations = 0

    for file_path in sorted(python_files):
        violations = check_file(file_path)
        if violations:
            files_with_violations += 1
            total_violations += len(violations)

            # Print relative path from root
            try:
                rel_path = file_path.relative_to(root_path)
            except ValueError:
                rel_path = file_path

            print(f"❌ {rel_path}")
            for line_num, line_content in violations:
                print(f"   Line {line_num}: {line_content}")
            print()

    # Summary
    print("=" * 70)
    print(f"Summary:")
    print(f"  Total files checked: {len(python_files)}")
    print(f"  Files with hardcoded paths: {files_with_violations}")
    print(f"  Total violations: {total_violations}")
    print()

    if files_with_violations > 0:
        print("Migration needed! Use the config.paths module:")
        print()
        print("  from config.paths import get_base_dir, get_path")
        print("  base_dir = get_base_dir()")
        print("  custom_path = get_path('subdir', 'file.txt')")
        print()
        print("See config/README.md for migration patterns and examples.")

        if args.strict:
            sys.exit(1)
    else:
        print("✅ No hardcoded paths found! All files use the configuration system.")


if __name__ == "__main__":
    main()
