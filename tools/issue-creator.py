#!/usr/bin/env python3
"""
SkogAI Issue Creator Workflow

A comprehensive issue creation workflow that integrates with Linear MCP server
for streamlined issue management within the SkogAI ecosystem.

Usage:
    python issue-creator.py create "Title" "Description" --type feature --priority high
    python issue-creator.py interactive
    python issue-creator.py templates
    python issue-creator.py help
"""

import os
import sys
import json
import argparse
import time
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("issue_creator")

class IssueCreator:
    """Issue creator workflow for SkogAI using Linear MCP integration."""
    
    def __init__(self):
        """Initialize the issue creator with SkogAI configuration."""
        self.skogai_team_id = os.environ.get("SKOGAI_TEAM_ID")
        if not self.skogai_team_id:
            logger.error("Environment variable SKOGAI_TEAM_ID must be set. Please set it before running this tool.")
            sys.exit(1)
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.templates_dir = os.path.join(self.base_dir, "issue_templates")
        self.output_dir = os.path.join(self.base_dir, "issue_outputs")
        
        # Ensure directories exist
        os.makedirs(self.templates_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize templates if they don't exist
        self._init_templates()
    
    def _init_templates(self):
        """Ensure issue templates exist in the templates directory by copying from a single source of truth if needed."""
        default_templates_path = os.path.join(self.base_dir, "default_templates.json")
        if not os.path.exists(default_templates_path):
            logger.error(f"Default templates file not found: {default_templates_path}")
            raise FileNotFoundError(f"Default templates file not found: {default_templates_path}")
        with open(default_templates_path, "r", encoding="utf-8") as f:
            templates = json.load(f)
        for template_name, template_content in templates.items():
            template_file = os.path.join(self.templates_dir, f"{template_name}.json")
            if not os.path.exists(template_file):
                with open(template_file, "w", encoding="utf-8") as tf:
                    json.dump(template_content, tf, indent=2)
### Actual Behavior
{actual}

### Environment
{environment}

### Additional Context
{context}
""",
                "labels": ["bug", "urgent"],
                "priority": 1
            },
            "knowledge": {
                "title_template": "Knowledge Archaeology: {topic}",
                "description_template": """## Knowledge Recovery Task

### Topic
{topic}

### Objective
{objective}

### Known Information
{known_info}

### Research Areas
{research_areas}

### Deliverables
{deliverables}

### Timeline
{timeline}
""",
                "labels": ["knowledge", "archaeology", "research"],
                "priority": 3
            },
            "governance": {
                "title_template": "Proposal: {proposal_title}",
                "description_template": """## Governance Proposal

### Proposal Summary
{summary}

### Background
{background}

### Proposed Changes
{changes}

### Impact Assessment
{impact}

### Implementation Plan
{implementation}

### Voting Instructions
Agents please vote with +1 (support), -1 (oppose), or 0 (abstain) in comments below.
""",
                "labels": ["governance", "proposal", "democracy"],
                "priority": 2
            },
            "architecture": {
                "title_template": "Architecture: {component_name}",
                "description_template": """## Architecture Design

### Component
{component}

### Purpose
{purpose}

### Requirements
{requirements}

### Design Decisions
{decisions}

### Trade-offs
{tradeoffs}

### Implementation Plan
{implementation}
""",
                "labels": ["architecture", "design", "technical"],
                "priority": 2
            }
        }
        
        for template_name, template_data in templates.items():
            template_path = os.path.join(self.templates_dir, f"{template_name}.json")
            if not os.path.exists(template_path):
                with open(template_path, 'w') as f:
                    json.dump(template_data, f, indent=2)
    
    def list_templates(self):
        """List available issue templates."""
        print("Available Issue Templates:")
        print("-" * 30)
        
        for template_file in os.listdir(self.templates_dir):
            if template_file.endswith('.json'):
                template_name = template_file[:-5]  # Remove .json
                template_path = os.path.join(self.templates_dir, template_file)
                
                try:
                    with open(template_path, 'r') as f:
                        template_data = json.load(f)
                    
                    print(f"• {template_name}")
                    print(f"  Title: {template_data.get('title_template', 'N/A')}")
                    print(f"  Labels: {', '.join(template_data.get('labels', []))}")
                    print(f"  Priority: {template_data.get('priority', 3)}")
                    print()
                    
                except json.JSONDecodeError:
                    print(f"• {template_name} (corrupted template)")
                    print()
    
    def create_issue_interactive(self):
        """Interactive issue creation workflow."""
        print("=== SkogAI Issue Creator - Interactive Mode ===")
        print()
        
        # Choose template
        self.list_templates()
        template_type = input("Choose issue template type: ").strip()
        
        # Load template
        template_path = os.path.join(self.templates_dir, f"{template_type}.json")
        if not os.path.exists(template_path):
            print(f"Template '{template_type}' not found.")
            return False
        
        with open(template_path, 'r') as f:
            template = json.load(f)
        
        # Collect issue data
        print(f"\n=== Creating {template_type} issue ===")
        issue_data = self._collect_issue_data_interactive(template)
        
        # Create the issue
        return self._create_issue(issue_data, template)
    
    def _collect_issue_data_interactive(self, template: Dict[str, Any]) -> Dict[str, Any]:
        """Collect issue data interactively from user."""
        print("\nPlease provide the following information:")
        
        # Basic information
        title = input("Issue title: ").strip()
        description = input("Issue description: ").strip()
        
        # Priority selection
        print("\nPriority levels:")
        print("  1 - Urgent")
        print("  2 - High") 
        print("  3 - Normal (default)")
        print("  4 - Low")
        
        priority_input = input(f"Priority [default: {template.get('priority', 3)}]: ").strip()
        priority = int(priority_input) if priority_input.isdigit() else template.get('priority', 3)
        
        # Labels
        default_labels = template.get('labels', [])
        labels_input = input(f"Labels [default: {', '.join(default_labels)}]: ").strip()
        labels = [l.strip() for l in labels_input.split(',')] if labels_input else default_labels
        
        # Assignee
        assignee = input("Assignee (optional): ").strip()
        
        return {
            'title': title,
            'description': description,
            'priority': priority,
            'labels': labels,
            'assignee': assignee if assignee else None,
            'teamId': self.skogai_team_id
        }
    
    def create_issue_from_args(self, title: str, description: str, 
                              issue_type: str = "feature", priority: int = 3,
                              labels: List[str] = None, assignee: str = None) -> bool:
        """Create issue from command line arguments."""
        
        # Load template
        template_path = os.path.join(self.templates_dir, f"{issue_type}.json")
        if os.path.exists(template_path):
            with open(template_path, 'r') as f:
                template = json.load(f)
        else:
            template = {"labels": [], "priority": 3}
        
        # Merge provided data with template defaults
        issue_data = {
            'title': title,
            'description': description,
            'priority': priority,
            'labels': labels if labels else template.get('labels', []),
            'assignee': assignee,
            'teamId': self.skogai_team_id
        }
        
        return self._create_issue(issue_data, template)
    
    def _create_issue(self, issue_data: Dict[str, Any], template: Dict[str, Any]) -> bool:
        """Create the issue using Linear MCP (simulated for now)."""
        
        # Generate session ID for tracking
        session_id = int(time.time())
        session_dir = os.path.join(self.output_dir, f"issue_{session_id}")
        os.makedirs(session_dir, exist_ok=True)
        
        # Save issue data
        issue_file = os.path.join(session_dir, "issue_data.json")
        with open(issue_file, 'w') as f:
            json.dump(issue_data, f, indent=2)
        
        # Create Linear MCP command template
        mcp_command = self._generate_mcp_command(issue_data)
        command_file = os.path.join(session_dir, "linear_mcp_command.txt")
        with open(command_file, 'w') as f:
            f.write(mcp_command)
        
        # Log the issue creation
        logger.info(f"Issue created with session ID: {session_id}")
        logger.info(f"Title: {issue_data['title']}")
        logger.info(f"Priority: {issue_data['priority']}")
        logger.info(f"Labels: {', '.join(issue_data['labels'])}")
        
        print(f"\n=== Issue Creation Summary ===")
        print(f"Session ID: {session_id}")
        print(f"Title: {issue_data['title']}")
        print(f"Description: {issue_data['description'][:100]}...")
        print(f"Priority: {issue_data['priority']}")
        print(f"Labels: {', '.join(issue_data['labels'])}")
        print(f"Team ID: {issue_data['teamId']}")
        
        if issue_data.get('assignee'):
            print(f"Assignee: {issue_data['assignee']}")
        
        print(f"\nFiles saved to: {session_dir}")
        print(f"Linear MCP command: {command_file}")
        
        # In a real implementation, this would execute the MCP command
        print(f"\nTo execute with Linear MCP:")
        print(f"cat {command_file}")
        
        return True
    
    def _generate_mcp_command(self, issue_data: Dict[str, Any]) -> str:
        """Generate Linear MCP command for issue creation."""
        
        # Basic create_issue command
        command_parts = [
            "# Linear MCP Issue Creation Command",
            "# Execute this with your Linear MCP server",
            "",
            "create_issue",
            f'  title: {json.dumps(issue_data["title"])}',
            f'  teamId: {json.dumps(issue_data["teamId"])}',
            f'  description: {json.dumps(issue_data["description"])}',
            f'  priority: {issue_data["priority"]}'
        ]
        
        # Add optional fields
        if issue_data.get('assignee'):
            command_parts.append(f'  assigneeId: {json.dumps(issue_data["assignee"])}')
        
        if issue_data.get('labels'):
            command_parts.append(f'  labels: {json.dumps(issue_data["labels"])}')
        
        return '\n'.join(command_parts)


def main():
    """Main entry point for the issue creator workflow."""
    parser = argparse.ArgumentParser(
        description="SkogAI Issue Creator Workflow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s interactive                    # Interactive mode
  %(prog)s templates                      # List available templates  
  %(prog)s create "Fix login bug" "Login fails on mobile" --type bug --priority 1
  %(prog)s create "Add search feature" "Implement search functionality" --type feature
        """
    )
    
    parser.add_argument('command', 
                       choices=['create', 'interactive', 'templates', 'help'],
                       help='Command to execute')
    
    parser.add_argument('title', nargs='?', 
                       help='Issue title (required for create command)')
    
    parser.add_argument('description', nargs='?', 
                       help='Issue description (required for create command)')
    
    parser.add_argument('--type', default='feature',
                       choices=['feature', 'bug', 'knowledge', 'governance', 'architecture'],
                       help='Type of issue (default: feature)')
    
    parser.add_argument('--priority', type=int, default=3,
                       choices=[1, 2, 3, 4],
                       help='Priority level (1=urgent, 2=high, 3=normal, 4=low)')
    
    parser.add_argument('--labels', nargs='*',
                       help='Issue labels (space-separated)')
    
    parser.add_argument('--assignee',
                       help='Assignee for the issue')
    
    args = parser.parse_args()
    
    # Initialize issue creator
    creator = IssueCreator()
    
    # Execute command
    if args.command == 'templates':
        creator.list_templates()
    
    elif args.command == 'interactive':
        creator.create_issue_interactive()
    
    elif args.command == 'create':
        if not args.title or not args.description:
            print("Error: Both title and description are required for create command")
            parser.print_help()
            sys.exit(1)
        
        success = creator.create_issue_from_args(
            title=args.title,
            description=args.description,
            issue_type=args.type,
            priority=args.priority,
            labels=args.labels,
            assignee=args.assignee
        )
        
        if success:
            print("\nIssue created successfully!")
        else:
            print("\nError creating issue.")
            sys.exit(1)
    
    elif args.command == 'help':
        parser.print_help()
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()