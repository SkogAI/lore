# Linear MCP Server Usage Guide

## Overview

Linear is a comprehensive project management and issue tracking MCP server that integrates with the Linear workspace. It provides full CRUD operations for issues, projects, teams, and enables seamless workflow management within the SkogAI ecosystem.

## Key Capabilities

### 1. Issue Management
- **Issue Operations**: Create, read, update, and list issues
- **Issue Details**: Get comprehensive issue information including attachments and git branches
- **Comment System**: Add and retrieve comments on issues
- **Status Tracking**: Manage issue states and workflows

### 2. Project Management
- **Project CRUD**: Create, read, update, and list projects
- **Project Organization**: Team-based project management
- **Timeline Management**: Start dates, target dates, and milestones

### 3. Team Management
- **Team Operations**: List and retrieve team information
- **Team Configuration**: Access team settings and workflows
- **User Management**: List and retrieve user information

### 4. Workflow Integration
- **Labels**: Manage issue categorization
- **Cycles**: Sprint and iteration management
- **Documentation**: Integrated document management

## Current SkogAI Integration

### Active Team
- **Team Name**: SkogAI
- **Team ID**: `ac4c7f2d-98ae-438f-b85a-33374856fd1b`
- **Created**: March 27, 2025
- **Icon**: Server

## Workflow Integration

### Issue Creation Workflow
1. Create issue with `create_issue`
2. Required: `title`, `teamId` (SkogAI team)
3. Optional: `description`, `assigneeId`, `priority`, `labels`
4. Link to git branches and external resources

### Issue Management Workflow
1. List issues with `list_issues` (filter by team, assignee, state)
2. Get detailed issue info with `get_issue`
3. Update issue status with `update_issue`
4. Add comments with `create_comment`

### Project Management Workflow
1. Create project with `create_project`
2. Associate with SkogAI team
3. Set timelines and milestones
4. Track progress through issue linking

## Usage Patterns

### Democratic Governance Integration
```
1. Create governance proposals as Linear issues
2. Use comments for agent voting and discussion
3. Track proposal status through issue states
4. Link to implementation branches
```

### Knowledge Archaeology Support
```
1. Create issues for knowledge recovery tasks
2. Document findings in issue descriptions
3. Link to relevant code repositories
4. Track archaeology progress through milestones
```

### Agent Collaboration
```
1. Assign issues to specific agents (Claude, Goose, Amy, Dot)
2. Use labels for task categorization
3. Comment-based communication and updates
4. Cross-reference with git branches
```

## Issue Configuration

### Priority Levels
- **0**: No priority
- **1**: Urgent
- **2**: High
- **3**: Normal (default)
- **4**: Low

### Common Label Categories
- **Agent**: claude, goose, amy, dot
- **Type**: feature, bug, documentation, architecture
- **Priority**: urgent, high, normal, low
- **Status**: in-progress, blocked, review, testing

### Issue States
- Use `list_issue_statuses` to get available states for SkogAI team
- Common states: Backlog, In Progress, Review, Done

## Integration with SkogAI Ecosystem

### Democratic Workflows
- **Proposal Tracking**: Issues for governance proposals
- **Voting Records**: Comments for agent votes and reasoning
- **Decision History**: Issue timeline preserves decision process

### Knowledge Management
- **Research Issues**: Track knowledge archaeology tasks
- **Documentation Issues**: Link to knowledge files
- **Integration Issues**: Track MCP server and tool integration

### Development Coordination
- **Feature Issues**: Link to implementation branches
- **Bug Issues**: Track resolution across multiple agents
- **Architecture Issues**: Document system design decisions

## Best Practices

### Issue Creation
- **Descriptive Titles**: Clear, searchable issue names
- **Comprehensive Descriptions**: Include context and requirements
- **Proper Labeling**: Use consistent label taxonomy
- **Git Integration**: Link to relevant branches when available

### Project Management
- **Team Association**: Always associate with SkogAI team
- **Timeline Planning**: Set realistic start and target dates
- **Milestone Tracking**: Use projects for major initiatives

### Collaboration
- **Agent Assignment**: Assign issues to appropriate agents
- **Comment Communication**: Use comments for status updates
- **Cross-referencing**: Link related issues and projects

## Common Use Cases

### 1. Feature Development
```
create_issue "Implement X feature for Y component"
→ Assign to relevant agent
→ Set priority and labels
→ Link to implementation branch
```

### 2. Bug Tracking
```
create_issue "Fix X bug in Y system"
→ Set priority: urgent/high
→ Add reproduction steps
→ Assign to agent with expertise
```

### 3. Knowledge Archaeology
```
create_issue "Recover knowledge about X system"
→ Label: knowledge, archaeology
→ Assign to Claude
→ Track progress through comments
```

### 4. Democratic Governance
```
create_issue "Proposal: New X policy"
→ Description: Full proposal details
→ Comments: Agent voting and discussion
→ Status: Track proposal lifecycle
```

## Technical Notes

### Authentication
- Server automatically handles Linear API authentication
- Uses configured workspace credentials
- No additional setup required

### Rate Limiting
- Linear API has standard rate limits
- Batch operations when possible
- Use filtering to reduce API calls

### Data Persistence
- All Linear data persists in Linear workspace
- Changes are immediately reflected across all agents
- No local caching or synchronization needed

## Error Handling

### Common Issues
1. **Invalid Team ID**: Verify SkogAI team ID is correct
2. **Permission Errors**: Check Linear workspace permissions
3. **Required Fields**: Ensure title and teamId are provided
4. **Invalid States**: Use `list_issue_statuses` to get valid states

### Fallback Strategies
1. Use `list_teams` to verify team access
2. Check `list_users` for valid assignee IDs
3. Use `list_issue_labels` for available labels
4. Verify issue states with `list_issue_statuses`

## Integration Commands

### Quick Team Reference
```
list_teams → Get SkogAI team ID
get_team "SkogAI" → Get team details
list_users → Get assignee options
```

### Issue Workflow
```
create_issue → New issue creation
get_issue → Detailed issue view
update_issue → Status and field updates
create_comment → Discussion and updates
```

### Project Management
```
create_project → New project creation
list_projects → Project overview
get_project → Project details
update_project → Project modifications
```