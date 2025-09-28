# Tools Overview

Claude has native tools and MCP-enabled tools within the SkogAI ecosystem.

## MCP Tools

### GitHub Integration
- **GitHub Operations**: `mcp__skogai-github`
  - Repository management (create, fork, branch)
  - File operations (create, update, get contents)
  - Issue and PR workflows (create, comment, review, merge)
  - Advanced search functionality (code, issues, PRs)
  - Batch file operations with single commits
  - Automatic branch creation and history preservation

### Memory System
- **Store Memory**: `mcp__skogai-memory__store_memory`
  - Store information with tags for later retrieval
  - Syntax: `{"content": "content to store", "metadata": {"tags": "tag1,tag2", "type": "note"}}`

- **Retrieve Memory**: `mcp__skogai-memory__retrieve_memory`
  - Semantic search for relevant memories
  - Syntax: `{"query": "search query", "n_results": 5}`

- **Recall Memory**: `mcp__skogai-memory__recall_memory`
  - Time-based memory retrieval with natural language expressions
  - Syntax: `{"query": "what I stored last week"}`

- **Tag Search**: `mcp__skogai-memory__search_by_tag`
  - Find memories with specific tags
  - Syntax: `{"tags": ["important", "reference"]}`

- **Memory Management**:
  - Delete specific memory: `mcp__skogai-memory__delete_memory`
  - Delete by tag: `mcp__skogai-memory__delete_by_tag`
  - Clean duplicates: `mcp__skogai-memory__cleanup_duplicates`
  - Timeframe operations: `mcp__skogai-memory__recall_by_timeframe`, `mcp__skogai-memory__delete_by_timeframe`

### Task Management
- **Create Task**: `mcp__skogai-todo__task_create`
  - Create new task with details
  - Syntax: `{"name": "Task name", "desc": "Description", "priority": "medium", "tags": ["tag1"]}`

- **Update Task**: `mcp__skogai-todo__task_update`
  - Modify existing task
  - Syntax: `{"id": 1, "status": "completed"}`

- **List Tasks**: `mcp__skogai-todo__task_list`
  - Retrieve tasks with optional filters
  - Syntax: `{"limit": 10, "status": "active"}`

- **Task Operations**: `mcp__skogai-todo__task_get`, `mcp__skogai-todo__task_delete`

### Web Tools
- **Fetch URL**: `mcp__skogai-fetch__fetch`
  - Retrieve content from web URLs
  - Syntax: `{"url": "https://example.com", "max_length": 5000}`

### Project Context
- **Project Context**: `mcp__skogai-lc-context__lc-project-context`
  - Generate repository overview
  - Syntax: `{"root_path": "/path/to/repo", "profile_name": "code"}`

- **Get Files**: `mcp__skogai-lc-context__lc-get-files`
  - Retrieve specific file contents
  - Syntax: `{"root_path": "/path/to/repo", "paths": ["/repo/file.txt"]}`

- **Code Analysis**: `mcp__skogai-lc-context__lc-code-outlines`, `mcp__skogai-lc-context__lc-get-implementations`

## Native Tools

### File Operations
- **View**: Read file contents
- **Edit**: Make targeted changes to files
- **Replace**: Overwrite file contents
- **LS**: List directory contents

### Search & Navigation
- **GlobTool**: Find files by pattern
  - Syntax: `{"pattern": "**/*.js", "path": "/path/to/dir"}`

- **GrepTool**: Search file contents
  - Syntax: `{"pattern": "function", "include": "*.js", "path": "/path/to/dir"}`

- **Dispatch Agent**: Specialized search agent
  - For complex searches across multiple files

- Quick search:
  ```sh
  # Find files containing term (via Bash)
  git grep -li <query>

  # Show matching lines (via Bash)
  git grep -i <query>
  ```

### Execution
- **Bash**: Execute shell commands
  - Avoid direct use of `grep` or `find` commands as they may not respect `.gitignore` rules
  - Use for git operations and system commands

- **BatchTool**: Run multiple tools in parallel
  - Great for performance optimization

## Common Locations
- `tasks/` - Task details
- `journal/` - Daily updates
- `knowledge/` - Documentation
- `people/` - User profiles

## Testing Status

| MCP Server          | Status      | Notes                                    |
|---------------------|-------------|------------------------------------------|
| Memory System       | ✅ Working   | Verified store/retrieve functionality    |
| Task Management     | ✅ Working   | Created and listed tasks successfully    |
| Fetch               | ❌ Issue     | Error when testing with GitHub URL       |
| Project Context     | ❌ Issue     | Context overflow when loading entire repo |
| GitHub Integration  | 🔄 Upcoming  | Implementation planned for next session  |

## Best Practices
1. Use MCP memory for important information that should persist across sessions
2. Prefer BatchTool when making multiple related tool calls
3. Use dispatch_agent for complex file searches
4. Update journal entries with daily progress
5. Store important concepts in knowledge/ directory
6. Use task management for tracking work items
7. Test MCP capabilities before relying on them in workflows