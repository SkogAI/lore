# SkogAI Issue Creator Workflow

A comprehensive issue creation workflow that integrates with Linear MCP server for streamlined issue management within the SkogAI ecosystem.

## Overview

The Issue Creator Workflow provides a structured approach to creating issues in Linear, following SkogAI best practices and supporting democratic governance, knowledge archaeology, feature development, and bug tracking workflows.

## Features

- **Template-Based Creation**: Pre-defined templates for different issue types
- **Interactive Mode**: Guided issue creation with prompts
- **Command Line Interface**: Quick issue creation from command line
- **Linear MCP Integration**: Generates proper Linear MCP commands
- **Session Tracking**: Each issue creation gets a unique session ID for tracking
- **Flexible Configuration**: Customizable templates and labels

## Installation & Setup

The workflow consists of two main components:

1. `issue-creator.py` - Python script with core functionality
2. `create-issue.sh` - Shell wrapper for convenient access

Both scripts are located in the `tools/` directory and are executable.

## Usage

### Quick Start

```bash
# Interactive mode (recommended for first-time users)
./tools/create-issue.sh interactive

# List available templates
./tools/create-issue.sh templates

# Quick issue creation
./tools/create-issue.sh feature "Add search functionality" "Implement user search with filters"
```

### Command Line Usage

#### Shell Script Interface

```bash
# Basic usage
./tools/create-issue.sh [type] "Title" "Description" [options]

# Examples
./tools/create-issue.sh feature "Add notifications" "Implement push notification system" --priority 2
./tools/create-issue.sh bug "Login fails" "Users cannot authenticate" --priority 1 --assignee claude
./tools/create-issue.sh knowledge "Research API patterns" "Document current API architecture"
./tools/create-issue.sh governance "New voting system" "Proposal for agent voting improvements"
```

#### Python Script Interface

```bash
# Direct Python script usage
python3 tools/issue-creator.py interactive
python3 tools/issue-creator.py templates
python3 tools/issue-creator.py create "Title" "Description" --type feature --priority 2
```

### Available Issue Types

#### 1. Feature Issues
- **Template**: `feature`
- **Purpose**: New feature development
- **Default Labels**: `feature`, `enhancement`
- **Default Priority**: 3 (Normal)

#### 2. Bug Issues
- **Template**: `bug`
- **Purpose**: Bug reports and fixes
- **Default Labels**: `bug`, `urgent`
- **Default Priority**: 1 (Urgent)

#### 3. Knowledge Archaeology
- **Template**: `knowledge`
- **Purpose**: Knowledge recovery and research tasks
- **Default Labels**: `knowledge`, `archaeology`, `research`
- **Default Priority**: 3 (Normal)

#### 4. Governance Proposals
- **Template**: `governance`
- **Purpose**: Democratic governance and policy proposals
- **Default Labels**: `governance`, `proposal`, `democracy`
- **Default Priority**: 2 (High)

#### 5. Architecture Design
- **Template**: `architecture`
- **Purpose**: System architecture and design decisions
- **Default Labels**: `architecture`, `design`, `technical`
- **Default Priority**: 2 (High)

## Options

### Priority Levels
- `1` - Urgent (red)
- `2` - High (orange)
- `3` - Normal (default)
- `4` - Low (gray)

### Common Labels
- **Agent Labels**: `claude`, `goose`, `amy`, `dot`
- **Type Labels**: `feature`, `bug`, `documentation`, `architecture`
- **Priority Labels**: `urgent`, `high`, `normal`, `low`
- **Status Labels**: `in-progress`, `blocked`, `review`, `testing`

### Command Line Options

```bash
--type TYPE        Issue type (feature, bug, knowledge, governance, architecture)
--priority N       Priority level (1=urgent, 2=high, 3=normal, 4=low)
--labels L1 L2     Custom labels (space-separated)
--assignee ID      Assign to specific agent
```

## Interactive Mode

The interactive mode guides you through issue creation:

1. **Template Selection**: Choose from available issue types
2. **Title & Description**: Provide issue details
3. **Priority Setting**: Select appropriate priority level
4. **Label Configuration**: Use default or custom labels
5. **Assignee Selection**: Optionally assign to an agent

## Output Structure

Each issue creation generates:

```
tools/issue_outputs/issue_[timestamp]/
├── issue_data.json          # Structured issue data
└── linear_mcp_command.txt   # Linear MCP command to execute
```

### Sample Linear MCP Command

```
# Linear MCP Issue Creation Command
# Execute this with your Linear MCP server

create_issue
  title: "Add search functionality"
  teamId: "ac4c7f2d-98ae-438f-b85a-33374856fd1b"
  description: "Implement user search with filters"
  priority: 2
  labels: ["feature", "enhancement"]
```

## Integration with Linear MCP

The workflow generates properly formatted Linear MCP commands that can be executed with:

1. **Manual Execution**: Copy/paste the generated command
2. **Script Integration**: Read the command file in your Linear MCP workflow
3. **API Integration**: Parse the JSON data for programmatic issue creation

### SkogAI Team Configuration

- **Team Name**: SkogAI
- **Team ID**: `ac4c7f2d-98ae-438f-b85a-33374856fd1b`
- **Created**: March 27, 2025
- **Icon**: Server

## Template Customization

Templates are stored in `tools/issue_templates/` as JSON files:

```json
{
  "title_template": "Implement {feature_name} for {component}",
  "description_template": "## Feature Request\n\n### Description\n{description}",
  "labels": ["feature", "enhancement"],
  "priority": 3
}
```

### Adding New Templates

1. Create a new JSON file in `tools/issue_templates/`
2. Follow the existing template structure
3. Use `{variable}` placeholders for dynamic content
4. The template will be automatically available

## Best Practices

### Issue Titles
- Be descriptive and specific
- Use action words (Fix, Add, Implement, Research)
- Include component/system names when relevant

### Issue Descriptions
- Provide clear context and requirements
- Use structured format (templates help with this)
- Include acceptance criteria for features
- Add reproduction steps for bugs

### Labels and Organization
- Use consistent label taxonomy
- Combine type and priority labels
- Tag appropriate agents for assignment
- Cross-reference related issues

### Democratic Governance
- Use governance template for proposals
- Include full proposal details in description
- Specify voting instructions in description
- Track proposal lifecycle through status updates

## Troubleshooting

### Common Issues

1. **Template Not Found**
   - Check template name spelling
   - Run `./tools/create-issue.sh templates` to see available templates

2. **Permission Errors**
   - Ensure scripts are executable: `chmod +x tools/*.sh tools/*.py`
   - Check directory permissions for output folder

3. **Python Import Errors**
   - Ensure Python 3 is available
   - No external dependencies required

### Error Messages

- "Template not found": Check available templates with `templates` command
- "Both title and description required": Provide both arguments for create command
- "Issue creator script not found": Ensure issue-creator.py exists in tools directory

## Integration Examples

### With Git Workflows

```bash
# Create feature issue and link to branch
./tools/create-issue.sh feature "Add user profiles" "Implement user profile management" --assignee claude
git checkout -b feature/user-profiles
# Link the issue number in commit messages
```

### With CI/CD

```bash
# Automated bug report from test failures
if [ "$TEST_FAILED" = "true" ]; then
    ./tools/create-issue.sh bug "Test failure in $MODULE" "$ERROR_DETAILS" --priority 1
fi
```

### With Agent Workflows

```bash
# Claude creates knowledge archaeology issue
./tools/create-issue.sh knowledge "Document $SYSTEM architecture" "Research and document current architecture" --assignee claude

# Goose creates technical issue
./tools/create-issue.sh architecture "Refactor $COMPONENT" "Improve $COMPONENT design" --assignee goose
```

## Future Enhancements

- **Direct Linear Integration**: Execute MCP commands automatically
- **Template Variables**: Dynamic template variable substitution
- **Bulk Issue Creation**: Create multiple related issues
- **Issue Linking**: Automatic cross-referencing
- **Webhook Integration**: Trigger from external events
- **Email Notifications**: Send creation confirmations

## Contributing

To contribute to the Issue Creator Workflow:

1. Follow existing code patterns and structure
2. Add tests for new functionality
3. Update documentation for new features
4. Ensure compatibility with existing templates
5. Test with both shell and Python interfaces

## License

Part of the SkogAI project ecosystem.