# MCP Bridge API

## Overview

The MCP Bridge API provides access to a wide range of tools and functionalities through a RESTful API interface. This allows me to interact with various systems and perform complex operations beyond the built-in gptme tools.

## Base URL
<http://localhost:8808>

```

## Endpoints

### GET /tools
Lists all available tools in the MCP Bridge.

```shell
curl http://localhost:8808/tools
```

### POST /tools/:name

Executes a specific tool with the provided parameters.

```shell
curl -X POST http://localhost:8808/tools/:name \
  -H 'content-type: application/json' \
  -d '{"param1": "value1", "param2": "value2"}'
```

## Available Tools

The MCP Bridge provides access to numerous tools, including:

### Markdownify Tools

- `markdownify_audio_to_markdown`: Convert audio files to markdown
- `markdownify_bing_search_to_markdown`: Convert Bing search results to markdown
- `markdownify_docx_to_markdown`: Convert DOCX files to markdown
- `markdownify_get_markdown_file`: Get a markdown file by path
- `markdownify_image_to_markdown`: Convert images to markdown with descriptions
- `markdownify_pdf_to_markdown`: Convert PDF files to markdown
- `markdownify_pptx_to_markdown`: Convert PPTX files to markdown
- `markdownify_webpage_to_markdown`: Convert webpages to markdown
- `markdownify_xlsx_to_markdown`: Convert XLSX files to markdown
- `markdownify_youtube_to_markdown`: Convert YouTube videos to markdown with transcripts

### Filesystem Tools

- `filesystem_read_file`: Read file contents
- `filesystem_read_multiple_files`: Read multiple files simultaneously
- `filesystem_write_file`: Create or overwrite files
- `filesystem_edit_file`: Make line-based edits to files
- `filesystem_create_directory`: Create directories
- `filesystem_list_directory`: List directory contents
- `filesystem_directory_tree`: Get recursive directory structure
- `filesystem_move_file`: Move or rename files and directories
- `filesystem_search_files`: Search for files matching patterns
- `filesystem_get_file_info`: Get file metadata
- `filesystem_list_allowed_directories`: List allowed directories

### Memory Tools

- `memory_add_note`: Add a new note to memory

### Todo Tools

- `todo_task_create`: Create a new task
- `todo_task_get`: Get a task by ID
- `todo_task_update`: Update an existing task
- `todo_task_delete`: Delete a task
- `todo_task_list`: List tasks with optional filters

### Goose Brain Tools

- `goose_brain_1_remember_memory`: Store a memory with tags
- `goose_brain_1_retrieve_memories`: Retrieve memories from a category
- `goose_brain_1_remove_memory_category`: Remove all memories in a category
- `goose_brain_1_remove_specific_memory`: Remove a specific memory

## Usage Examples

### Listing Tasks

```shell
curl -X POST http://localhost:8808/tools/todo_task_list \
  -H 'content-type: application/json' \
  -d '{}'
```

### Creating a Task

```shell
curl -X POST http://localhost:8808/tools/todo_task_create \
  -H 'content-type: application/json' \
  -d '{"name": "New Task", "desc": "Task description", "priority": "medium"}'
```

### Reading a File

```shell
curl -X POST http://localhost:8808/tools/filesystem_read_file \
  -H 'content-type: application/json' \
  -d '{"path": "/path/to/file.txt"}'
```

## Best Practices

- Check tool parameters before making requests
- Use proper JSON formatting in request bodies
- Handle responses appropriately based on the tool's output format
- For file operations, ensure paths are valid and accessible
- For memory and task operations, use consistent naming conventions
