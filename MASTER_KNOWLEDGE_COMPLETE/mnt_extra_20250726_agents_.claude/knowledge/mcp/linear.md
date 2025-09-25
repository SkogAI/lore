# Linear MCP Server

## Purpose
Project management and issue tracking integration

## Functions

### Comment Management
- `mcp__Linear__list_comments` - Get comments for an issue
- `mcp__Linear__create_comment` - Add comment to an issue

### Cycle Management
- `mcp__Linear__list_cycles` - Get team cycles (current, previous, next, or all)

### Document Management
- `mcp__Linear__get_document` - Get document by ID or slug
- `mcp__Linear__list_documents` - List workspace documents

### Issue Management
- `mcp__Linear__get_issue` - Get issue details with attachments and git branch
- `mcp__Linear__list_issues` - List workspace issues with filters
- `mcp__Linear__create_issue` - Create new issues
- `mcp__Linear__update_issue` - Update existing issues
- `mcp__Linear__list_my_issues` - List current user's assigned issues

### Project Management
- `mcp__Linear__list_projects` - List workspace projects
- `mcp__Linear__get_project` - Get project details
- `mcp__Linear__create_project` - Create new projects
- `mcp__Linear__update_project` - Update existing projects

### Team Management
- `mcp__Linear__list_teams` - List workspace teams
- `mcp__Linear__get_team` - Get team details

### User Management
- `mcp__Linear__list_users` - List workspace users
- `mcp__Linear__get_user` - Get user details

### Status and Label Management
- `mcp__Linear__list_issue_statuses` - List team issue statuses
- `mcp__Linear__get_issue_status` - Get status details by name/ID
- `mcp__Linear__list_issue_labels` - List team issue labels

### Documentation Search
- `mcp__Linear__search_documentation` - Search Linear's documentation

## Key Parameters

### Issues
- `teamId`, `assigneeId`, `projectId`, `cycleId`, `stateId` for filtering
- `query` for text search
- `createdAt`, `updatedAt` for date filtering
- `includeArchived` for archived items

### Creation/Updates
- `title`, `description`, `priority` (0-4), `dueDate`
- `labelIds`, `links` arrays for metadata
- `parentId` for sub-issues

## Use Cases
- Managing development tasks and project coordination
- Issue tracking and assignment
- Project planning and cycle management
- Team collaboration and documentation
- Sprint/cycle planning and progress tracking

## Test Results
✅ **Tested**: Successfully listed SkogAI team and retrieved sample issues with full details

## Status
Available and functional