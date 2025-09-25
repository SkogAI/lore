#!/usr/bin/env python3
"""
SkogAI Issue Creator Workflow Demo

This demo showcases the issue creator workflow capabilities,
demonstrating various issue types and integration patterns.
"""

import os
import sys
import subprocess
import time

def run_demo():
    """Run the issue creator workflow demonstration."""
    print("=== SkogAI Issue Creator Workflow Demo ===")
    print()
    
    # Get the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    issue_creator = os.path.join(project_root, "tools", "create-issue.sh")
    
    if not os.path.exists(issue_creator):
        print(f"Error: Issue creator not found at {issue_creator}")
        return False
    
    print("1. Listing available templates...")
    subprocess.run([issue_creator, "templates"])
    
    print("\n" + "="*50)
    print("2. Creating sample issues for different workflows...")
    print()
    
    # Demo issues with different types
    demo_issues = [
        {
            "type": "feature",
            "title": "Enhance issue creator with batch mode",
            "description": "Add capability to create multiple issues from a configuration file or CSV input",
            "priority": 3,
            "assignee": "claude"
        },
        {
            "type": "bug", 
            "title": "Template validation error",
            "description": "Custom templates with invalid JSON structure cause workflow to crash",
            "priority": 1,
            "assignee": "goose"
        },
        {
            "type": "knowledge",
            "title": "Document MCP integration patterns", 
            "description": "Research and document best practices for integrating MCP servers in SkogAI workflows",
            "priority": 2,
            "assignee": "claude"
        },
        {
            "type": "governance",
            "title": "Standardize issue labeling taxonomy",
            "description": "Proposal to establish consistent labeling standards across all SkogAI repositories and workflows",
            "priority": 2
        },
        {
            "type": "architecture",
            "title": "Issue workflow service architecture",
            "description": "Design scalable architecture for issue management service that can handle multiple MCP integrations",
            "priority": 2,
            "assignee": "dot"
        }
    ]
    
    created_issues = []
    
    for i, issue in enumerate(demo_issues, 1):
        print(f"Creating issue {i}/{len(demo_issues)}: {issue['title']}")
        
        # Build command
        cmd = [
            issue_creator,
            issue["type"],
            issue["title"],
            issue["description"],
            "--priority", str(issue["priority"])
        ]
        
        if issue.get("assignee"):
            cmd.extend(["--assignee", issue["assignee"]])
        
        # Execute command
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ Created {issue['type']} issue successfully")
            created_issues.append(issue)
        else:
            print(f"✗ Failed to create {issue['type']} issue")
            print(f"Error: {result.stderr}")
        
        # Small delay between issues
        time.sleep(0.5)
    
    print("\n" + "="*50)
    print("3. Demo Summary")
    print(f"Successfully created {len(created_issues)} issues:")
    
    for issue in created_issues:
        print(f"• {issue['type'].upper()}: {issue['title']}")
        if issue.get('assignee'):
            print(f"  Assigned to: {issue['assignee']}")
        print(f"  Priority: {issue['priority']}")
        print()
    
    print("4. Integration Examples")
    print("The created issues demonstrate:")
    print("• Feature development workflow")
    print("• Bug tracking and prioritization") 
    print("• Knowledge archaeology processes")
    print("• Democratic governance proposals")
    print("• Architecture design documentation")
    print()
    
    print("5. Next Steps")
    print("• Execute the generated Linear MCP commands")
    print("• Review and assign issues in Linear workspace")  
    print("• Use issue tracking for project management")
    print("• Integrate with git workflows and CI/CD")
    print()
    
    print("Demo completed successfully!")
    return True

def show_usage():
    """Show usage information."""
    print("SkogAI Issue Creator Workflow Demo")
    print()
    print("Usage:")
    print("  python3 demo/issue_creator_demo.py")
    print()
    print("This demo will:")
    print("• List available issue templates")
    print("• Create sample issues of different types")
    print("• Show integration patterns")
    print("• Demonstrate workflow capabilities")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ["--help", "-h", "help"]:
        show_usage()
    else:
        run_demo()