#!/usr/bin/env python3
"""
Create configuration system migration issues from markdown files.

This script reads issue markdown files and creates GitHub issues using the gh CLI.
"""

import os
import sys
import subprocess
import re
from pathlib import Path
from typing import Dict, Optional

# Repository configuration
REPO = "SkogAI/lore"
LABELS = ["refactoring", "configuration-system", "migration"]
MASTER_ISSUE_LABELS = ["refactoring", "configuration-system", "tracking", "epic"]


def extract_title(content: str) -> Optional[str]:
    """Extract title from markdown content."""
    match = re.search(r'^## Title\s*\n(.+?)$', content, re.MULTILINE)
    return match.group(1).strip() if match else None


def extract_body(content: str) -> Optional[str]:
    """Extract body content from markdown."""
    match = re.search(r'^## Body\s*\n(.+)', content, re.MULTILINE | re.DOTALL)
    return match.group(1).strip() if match else None


def check_gh_cli() -> bool:
    """Check if gh CLI is available and authenticated."""
    try:
        subprocess.run(
            ["gh", "auth", "status"],
            check=True,
            capture_output=True,
            text=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def create_issue(title: str, body: str, labels: list) -> Optional[str]:
    """Create a GitHub issue using gh CLI."""
    try:
        result = subprocess.run(
            [
                "gh", "issue", "create",
                "--repo", REPO,
                "--title", title,
                "--body", body,
                "--label", ",".join(labels)
            ],
            check=True,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error creating issue: {e.stderr}", file=sys.stderr)
        return None


def process_issue_file(filepath: Path, labels: list) -> Optional[str]:
    """Process a single issue markdown file and create the issue."""
    try:
        content = filepath.read_text()
        title = extract_title(content)
        body = extract_body(content)
        
        if not title or not body:
            print(f"Error: Could not extract title or body from {filepath.name}")
            return None
        
        print(f"Creating issue: {title}")
        issue_url = create_issue(title, body, labels)
        
        if issue_url:
            print(f"✓ Created: {issue_url}")
        else:
            print(f"✗ Failed to create issue from {filepath.name}")
        
        return issue_url
        
    except Exception as e:
        print(f"Error processing {filepath.name}: {e}", file=sys.stderr)
        return None


def main():
    """Main function to create all issues."""
    # Get the directory containing this script
    script_dir = Path(__file__).parent
    
    print(f"Creating configuration system migration issues for {REPO}")
    print("=" * 60)
    print()
    
    # Check gh CLI availability
    if not check_gh_cli():
        print("Error: gh CLI is not available or not authenticated", file=sys.stderr)
        print("Install from: https://cli.github.com/", file=sys.stderr)
        print("Then authenticate with: gh auth login", file=sys.stderr)
        sys.exit(1)
    
    created_issues = []
    
    # Create issues 1-15 first
    for i in range(1, 16):
        issue_file = script_dir / f"issue_{i:02d}.md"
        
        if not issue_file.exists():
            print(f"Skipping issue_{i:02d}.md (file not found)")
            continue
        
        issue_url = process_issue_file(issue_file, LABELS)
        if issue_url:
            created_issues.append(issue_url)
        
        print()
    
    # Create master tracking issue last (issue 16)
    master_issue_file = script_dir / "issue_16.md"
    if master_issue_file.exists():
        print("Creating master tracking issue...")
        issue_url = process_issue_file(master_issue_file, MASTER_ISSUE_LABELS)
        if issue_url:
            created_issues.append(issue_url)
        print()
    
    # Summary
    print("=" * 60)
    print(f"Summary: Created {len(created_issues)} issues")
    print()
    print("Created issues:")
    for url in created_issues:
        print(f"  - {url}")
    
    print()
    print("Next steps:")
    print(f"1. Review created issues at: https://github.com/{REPO}/issues")
    print("2. Update issue #16 to reference specific issue numbers")
    print("3. Begin migration work following the MIGRATION_GUIDE.md")


if __name__ == "__main__":
    main()
