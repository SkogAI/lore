#!/usr/bin/env python3
"""
Extract issue definitions from the create-script-refactor-issues.sh script
and create GitHub issues using the GitHub API or gh CLI.
"""

import os
import sys
import subprocess
import re
import json
from typing import List, Dict, Any

def parse_shell_script(script_path: str) -> List[Dict[str, Any]]:
    """
    Parse the shell script to extract issue definitions.
    
    Returns a list of dictionaries containing:
    - title: Issue title
    - body: Issue body
    - number: Issue number (1-10)
    """
    issues = []
    with open(script_path, 'r') as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i]
        if "gh issue create" in line:
            # Extract --title "..."
            title_match = re.search(r'--title\s+"([^"]+)"', line)
            title = title_match.group(1) if title_match else ""

            # Find --body "$(cat <<'EOF'"
            body = ""
            if '--body "$(' in line and "cat <<'EOF'" in line:
                # Find heredoc start
                # The heredoc may start on this line or the next
                # Find the line with "cat <<'EOF'"
                while i < len(lines) and "cat <<'EOF'" not in lines[i]:
                    i += 1
                i += 1  # Move to first line of body
                body_lines = []
                while i < len(lines) and lines[i].strip() != "EOF":
                    body_lines.append(lines[i].rstrip('\n'))
                    i += 1
                body = "\n".join(body_lines)
                # Move past EOF
                i += 1
            else:
                # If not heredoc, try to extract --body "..."
                body_match = re.search(r'--body\s+"([^"]+)"', line)
                body = body_match.group(1) if body_match else ""

            issues.append({
                'number': len(issues) + 1,
                'title': title,
                'body': body
            })
        else:
            i += 1
    return issues


def create_issue_with_gh(repo: str, title: str, body: str) -> bool:
    """Create an issue using gh CLI."""
    try:
        result = subprocess.run(
            ['gh', 'issue', 'create', '--repo', repo, '--title', title, '--body', body],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            print(f"✓ Created issue: {title}")
            print(f"  {result.stdout.strip()}")
            return True
        else:
            print(f"✗ Failed to create issue: {title}")
            print(f"  Error: {result.stderr.strip()}")
            return False
            
    except Exception as e:
        print(f"✗ Exception creating issue: {title}")
        print(f"  Error: {str(e)}")
        return False


def save_issues_to_files(issues: List[Dict[str, Any]], output_dir: str):
    """Save issues to individual markdown files for manual creation."""
    os.makedirs(output_dir, exist_ok=True)
    
    for issue in issues:
        filename = f"issue_{issue['number']:02d}.md"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write(f"# Issue {issue['number']}: {issue['title']}\n\n")
            f.write(f"## Title\n{issue['title']}\n\n")
            f.write(f"## Body\n{issue['body']}\n")
        
        print(f"Saved issue {issue['number']} to {filepath}")
    
    # Create a summary file
    summary_path = os.path.join(output_dir, "README.md")
    with open(summary_path, 'w') as f:
        f.write("# Shell Script Refactoring Issues\n\n")
        f.write("This directory contains 10 issues for refactoring shell scripts.\n\n")
        f.write("## Issues\n\n")
        for issue in issues:
            f.write(f"{issue['number']}. {issue['title']}\n")
        f.write("\n## To Create These Issues\n\n")
        f.write("### Option 1: Using gh CLI\n")
        f.write("```bash\n")
        f.write("# Set GH_TOKEN environment variable with your GitHub token\n")
        f.write("export GH_TOKEN=your_token_here\n\n")
        f.write("# Run the original script\n")
        f.write("./create-script-refactor-issues.sh\n")
        f.write("```\n\n")
        f.write("### Option 2: Manual Creation\n")
        f.write("Use the individual markdown files in this directory to create issues manually.\n")
    
    print(f"\nSummary saved to {summary_path}")


def main():
    """Main execution function."""
    script_path = '/home/runner/work/lore/lore/create-script-refactor-issues.sh'
    output_dir = os.environ.get('ISSUES_OUTPUT_DIR', 'issues_to_create')
    repo = 'SkogAI/lore'
    
    print("=== GitHub Issues Creator ===")
    print(f"Parsing script: {script_path}")
    print()
    
    # Parse the shell script
    try:
        issues = parse_shell_script(script_path)
        print(f"Found {len(issues)} issues to create\n")
    except Exception as e:
        print(f"Error parsing script: {e}")
        sys.exit(1)
    
    # Display issues
    print("Issues to be created:")
    for issue in issues:
        print(f"{issue['number']}. {issue['title']}")
    print()
    
    # Try to create issues with gh CLI
    print("Attempting to create issues with gh CLI...")
    print()
    
    created_count = 0
    for issue in issues:
        if create_issue_with_gh(repo, issue['title'], issue['body']):
            created_count += 1
    
    print()
    print(f"Successfully created {created_count}/{len(issues)} issues")
    
    # Save to files as backup/documentation
    print()
    print("Saving issue definitions to files for reference...")
    save_issues_to_files(issues, output_dir)
    
    print()
    if created_count == len(issues):
        print("✅ All issues created successfully!")
        return 0
    elif created_count > 0:
        print(f"⚠️  Partially successful: {created_count}/{len(issues)} issues created")
        return 1
    else:
        print("❌ Failed to create issues via gh CLI")
        print(f"   Issue definitions saved to {output_dir}/")
        print("   You can create them manually or run the original script with proper authentication.")
        return 2


if __name__ == '__main__':
    sys.exit(main())
