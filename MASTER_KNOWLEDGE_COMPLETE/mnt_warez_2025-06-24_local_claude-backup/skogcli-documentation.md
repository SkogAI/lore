# SkogCLI - Official Documentation

## Table of Contents
1. [Overview](#overview)
2. [Installation & Setup](#installation--setup)
3. [Architecture](#architecture)
4. [Script Management System](#script-management-system)
5. [Memory Module](#memory-module)
6. [Configuration Management](#configuration-management)
7. [Development Guidelines](#development-guidelines)
8. [Command Reference](#command-reference)
9. [Template System](#template-system)
10. [Testing](#testing)

## Overview

SkogCLI is a comprehensive Typer-based command-line interface framework designed for the SkogAI ecosystem. It provides powerful script management, knowledge base integration, and configuration management capabilities.

### Key Features
- **Script Management**: Create, run, edit, and organize custom scripts
- **Memory Integration**: Knowledge base operations (via basic-memory wrapper)
- **Template System**: Extensible script templates for rapid development
- **Rich Output**: Enhanced terminal display with formatting and tables
- **Global/User Scripts**: Support for both system-wide and user-specific scripts
- **Metadata Tracking**: Comprehensive script usage and modification tracking
- **Batch Operations**: Process multiple scripts simultaneously

### Core Philosophy
- **Test-Driven Development (TDD)**: All features must have comprehensive tests
- **Documentation-Driven Design (DDD)**: Documentation guides implementation
- **Type Safety**: Comprehensive Python type hints throughout
- **Rich User Experience**: Beautiful, informative CLI output

## Installation & Setup

### Prerequisites
- Python 3.12+
- UV package manager (replaces pip)

### Installation Commands
```bash
# Install development dependencies
uv add pytest && uv lock && uv sync

# Run SkogCLI
uv run skogcli

# Install completion (optional)
uv run skogcli --install-completion
```

### Directory Structure
```
skogcli/
├── src/skogcli/           # Main source code
│   ├── __init__.py        # Main app and subcommand registration
│   ├── script.py          # Script management system
│   ├── memory.py          # Memory/knowledge base integration
│   ├── settings.py        # Configuration management
│   ├── agent.py           # Agent functionality
│   ├── decorators.py      # Utility decorators
│   └── data/              # Templates and default settings
├── tests/                 # Test suite
├── docs/                  # Documentation
└── pyproject.toml         # Project configuration
```

## Architecture

### Main Application Structure
The application follows a modular design with separate Typer apps for each domain:

```python
# Main app with subcommands
app = Typer(no_args_is_help=True, name="SkogCLI")
app.add_typer(memory_app, name="memory")
app.add_typer(config_app, name="config")
app.add_typer(script_app, name="script")
app.add_typer(agent_app, name="agent")
```

### Core Components

#### 1. Script Management (`script.py`)
- **Purpose**: Complete lifecycle management of custom scripts
- **Features**: Creation, execution, editing, searching, batch processing
- **Storage**: `~/.config/skogcli/scripts/` (user) and `/usr/local/share/skogcli/scripts/` (global)

#### 2. Memory Module (`memory.py`)
- **Purpose**: Knowledge base integration via basic-memory
- **Status**: Currently placeholder implementation
- **Planned Features**: Note creation, search, synchronization

#### 3. Configuration (`settings.py`)
- **Purpose**: Application configuration management
- **Storage**: `~/.config/skogcli/config.json`
- **Features**: Show, set, reset configuration options

#### 4. Agent Module (`agent.py`)
- **Purpose**: Agent-specific functionality
- **Integration**: Part of broader SkogAI agent ecosystem

### Help System
Every command group includes a `--helpall` option that generates comprehensive documentation:

```bash
skogcli script --helpall    # Complete script command documentation
skogcli memory --helpall    # Complete memory command documentation
skogcli --helpall          # Complete application documentation
```

## Script Management System

The script management system is the most comprehensive component of SkogCLI, providing complete lifecycle management for custom scripts.

### Core Concepts

#### Script Types
- **Python Scripts**: `.py` files with `main()` function
- **Shell Scripts**: `.sh` files with shebang
- **Executable Scripts**: Any executable file

#### Storage Locations
- **User Scripts**: `~/.config/skogcli/scripts/` (default)
- **Global Scripts**: `/usr/local/share/skogcli/scripts/` (system-wide)

#### Metadata System
All scripts have associated metadata stored in `~/.config/skogcli/script_metadata.json`:
```json
{
  "/path/to/script.py": {
    "description": "Script description",
    "template": "basic",
    "type": "python",
    "created": "2024-01-01T12:00:00",
    "last_updated": "2024-01-01T12:00:00",
    "run_count": 5,
    "last_run": "2024-01-01T13:00:00"
  }
}
```

### Script Commands

#### `skogcli script list`
Lists all available scripts with optional metadata display.

**Options:**
- `--global/--no-global`: Include global scripts (default: true)
- `--metadata, -m`: Show detailed metadata table

**Examples:**
```bash
skogcli script list                    # List all scripts
skogcli script list --no-global        # User scripts only
skogcli script list --metadata         # Show detailed table
```

#### `skogcli script create`
Creates new scripts from templates.

**Arguments:**
- `name`: Name for the new script

**Options:**
- `--type, -t`: Script type (python/shell, default: python)
- `--template`: Template to use (default: basic)
- `--global, -g`: Create as global script
- `--description, -d`: Script description
- `--edit/--no-edit`: Open in editor after creation (default: true)
- `--editor, -e`: Specify editor (defaults to $EDITOR)

**Examples:**
```bash
skogcli script create my_script                           # Basic Python script
skogcli script create my_tool --type shell --template basic
skogcli script create data_processor --template data_processing
skogcli script create --global system_tool --description "System utility"
```

#### `skogcli script run`
Executes scripts with argument passing.

**Arguments:**
- `name`: Script name to run
- `args`: Arguments to pass to the script (optional)

**Options:**
- `--global/--no-global`: Include global scripts (default: true)

**Examples:**
```bash
skogcli script run my_script                    # Run without arguments
skogcli script run data_processor file.csv      # Run with arguments
skogcli script run --no-global my_script        # User scripts only
```

#### `skogcli script edit`
Opens scripts in configured editor.

**Arguments:**
- `name`: Script name to edit

**Options:**
- `--global/--no-global`: Include global scripts (default: true)
- `--editor, -e`: Specify editor (defaults to $EDITOR)

**Examples:**
```bash
skogcli script edit my_script                   # Edit with default editor
skogcli script edit my_script --editor vim      # Edit with specific editor
```

#### `skogcli script search`
Searches for text patterns within scripts.

**Arguments:**
- `pattern`: Text or regex pattern to search for

**Options:**
- `--regex, -r`: Treat pattern as regular expression
- `--case-sensitive, -c`: Case-sensitive search
- `--global/--no-global`: Include global scripts (default: true)
- `--output, -o`: Write results to file
- `--ignore-errors`: Continue on errors

**Examples:**
```bash
skogcli script search "import requests"         # Simple text search
skogcli script search "def \w+\(" --regex      # Regex pattern
skogcli script search "TODO" --output results.txt
```

#### `skogcli script transform`
Transforms script content using regular expressions.

**Arguments:**
- `name`: Script name to transform

**Options:**
- `--pattern, -p`: Regex pattern to search for (required)
- `--replacement, -r`: Replacement string (required)
- `--output, -o`: Write to file instead of updating script
- `--global/--no-global`: Include global scripts (default: true)
- `--backup/--no-backup`: Create backup before transforming (default: true)

**Examples:**
```bash
skogcli script transform my_script -p "old_function" -r "new_function"
skogcli script transform my_script -p "print\(" -r "logger.info(" --output updated.py
```

#### `skogcli script generate`
Generates scripts using AI or templates based on descriptions.

**Arguments:**
- `name`: Name for the new script
- `description`: Description of what the script should do

**Options:**
- `--type, -t`: Script type (python/shell, default: python)
- `--global, -g`: Create as global script
- `--edit/--no-edit`: Open in editor after creation (default: true)
- `--editor, -e`: Specify editor
- `--model, -m`: AI model to use (default: gpt-3.5-turbo)
- `--api-key, -k`: API key for AI service
- `--local, -l`: Use local templates instead of AI

**Examples:**
```bash
skogcli script generate csv_parser "Parse CSV files and extract specific columns"
skogcli script generate backup_tool "Create timestamped backups" --type shell
skogcli script generate data_analyzer "Analyze data files" --local
```

#### Advanced Commands

**`skogcli script batch`**: Process multiple scripts from a list file
**`skogcli script export`**: Export script to shareable JSON format
**`skogcli script import`**: Import script from JSON export
**`skogcli script copy`**: Copy existing script to create new one
**`skogcli script remove`**: Delete scripts with confirmation
**`skogcli script info`**: Show detailed script information
**`skogcli script code`**: View/update script content without editor

## Memory Module

The memory module provides integration with knowledge base systems for note-taking and information management.

### Current Status
- **Implementation**: Placeholder with "Not implemented yet" messages
- **Planned Integration**: Wrapper around basic-memory tool
- **Storage**: Local knowledge files synchronized with database

### Planned Commands

#### Command Mapping
| SkogCLI Command | basic-memory Equivalent | Description |
|-----------------|-------------------------|-------------|
| `memory create` | `tool write-note` | Create or update notes |
| `memory read` | `tool read-note` | Read notes with pagination |
| `memory search` | `tool search-notes` | Search across knowledge base |
| `memory list` | `tool recent-activity` | List recent activity |
| `memory sync` | `sync` | Synchronize files with database |
| `memory status` | `status` | Show sync status |

### Implementation Architecture
```python
def run_basic_memory(args: List[str]) -> subprocess.CompletedProcess:
    """Run basic-memory with the given arguments."""
    cmd = ["basic-memory"] + args
    return subprocess.run(cmd, capture_output=True, text=True)

def process_markdown(markdown_str: str, raw: bool = False) -> Union[str, Markdown]:
    """Process markdown string for display."""
    if raw:
        return markdown_str
    return Markdown(markdown_str)
```

## Configuration Management

SkogCLI provides comprehensive configuration management through the `config` command group.

### Configuration Storage
- **Location**: `~/.config/skogcli/config.json`
- **Format**: JSON with hierarchical structure
- **Defaults**: Loaded from `src/skogcli/data/default_settings.json`

### Configuration Commands

#### `skogcli config --show`
Displays current configuration in formatted table.

#### `skogcli config --list-keys`
Shows all available configuration keys and their default values.

#### `skogcli config --set <key> --value <value>`
Sets configuration values.

**Examples:**
```bash
skogcli config --set theme --value dark
skogcli config --set editor --value vim
skogcli config --set script.default_type --value shell
```

#### `skogcli config --reset`
Resets configuration to default values with confirmation.

## Development Guidelines

### Test-Driven Development (TDD)
1. **Always write tests first** - Non-negotiable requirement
2. **No source code modification** without corresponding tests
3. **Tests as specifications** - Validate documented behaviors precisely
4. **Red-Green-Refactor cycle** - Write failing tests, implement, refactor

### Documentation-Driven Design (DDD)
1. **Documentation guides implementation** - Follow docs for requirements
2. **Document before implementing** - New features need documentation first
3. **Documentation as source of truth** - Primary reference for behavior

### Code Standards
- **Type hints**: Comprehensive typing throughout codebase
- **Error handling**: Appropriate exception types with context
- **Import organization**: Standard lib → third-party → local
- **String formatting**: Use f-strings consistently
- **Docstrings**: All public functions and classes

### Testing Standards
- **Framework**: pytest with typer.testing.CliRunner
- **Coverage**: Verify exit codes and stdout content
- **Test organization**: One test file per module
- **Naming**: Descriptive test function names
- **Assertions**: Clear, specific assertions

### Package Management
```bash
# Add dependencies
uv add <package> && uv lock && uv sync

# Run commands
uv run <command>

# Development workflow
uv run pytest tests/                    # Run tests
uv run pytest tests/test_script.py     # Run specific tests
uv run pytest -v                       # Verbose output
```

## Command Reference

### Global Options
- `--help`: Show help message
- `--helpall`: Show comprehensive documentation
- `--install-completion`: Install shell completion
- `--show-completion`: Show completion script

### Main Commands
- `skogcli script`: Script management operations
- `skogcli memory`: Knowledge base operations
- `skogcli config`: Configuration management
- `skogcli agent`: Agent-specific functionality

### Script Subcommands
```bash
skogcli script list [--global/--no-global] [--metadata]
skogcli script create <name> [--type TYPE] [--template TEMPLATE] [--global]
skogcli script run <name> [args...] [--global/--no-global]
skogcli script edit <name> [--global/--no-global] [--editor EDITOR]
skogcli script search <pattern> [--regex] [--case-sensitive] [--output FILE]
skogcli script transform <name> --pattern PATTERN --replacement TEXT
skogcli script generate <name> <description> [--type TYPE] [--local]
skogcli script batch <list-file> [--command CMD] [--output-dir DIR]
skogcli script export <name> [--output FILE] [--metadata/--no-metadata]
skogcli script import <file> [--global] [--overwrite]
skogcli script copy <source> <destination> [--global-dest]
skogcli script remove <name> [--global/--no-global] [--force]
skogcli script info <name> [--global/--no-global]
skogcli script code <name> [--content TEXT] [--file FILE] [--output FILE]
skogcli script templates
skogcli script update-metadata <name> [--description TEXT]
skogcli script import-file <file> [--name NAME] [--global]
```

### Memory Subcommands (Planned)
```bash
skogcli memory create <title> [--folder FOLDER] [--content TEXT] [--tags TAGS]
skogcli memory read <identifier> [--raw] [--limit LIMIT] [--offset OFFSET]
skogcli memory search <query> [--folder FOLDER] [--tags TAGS] [--limit LIMIT]
skogcli memory list [--days DAYS] [--limit LIMIT]
skogcli memory sync [--force]
skogcli memory status
```

### Config Subcommands
```bash
skogcli config --show
skogcli config --list-keys
skogcli config --set <key> --value <value>
skogcli config --reset
```

## Template System

SkogCLI includes an extensible template system for rapid script creation.

### Template Locations
- **Package Templates**: `src/skogcli/data/templates/`
- **User Templates**: `~/.config/skogcli/templates/` (optional override)

### Template Structure
```
templates/
├── python/
│   ├── basic.py          # Simple Python script
│   ├── api_client.py     # HTTP API client template
│   ├── data_processing.py # Data processing template
│   └── line_counter.py   # File line counting utility
└── shell/
    ├── basic.sh          # Simple shell script
    ├── line_counter.sh   # Shell line counting utility
    └── system_info.sh    # System information script
```

### Built-in Templates

#### Python Templates
- **basic**: Simple script with main function and argument parsing
- **api_client**: HTTP client with requests library integration
- **data_processing**: CSV/JSON processing with pandas-style operations
- **line_counter**: File line counting utility

#### Shell Templates
- **basic**: Simple shell script with argument handling
- **line_counter**: File line counting in shell
- **system_info**: System information gathering script

### Creating Custom Templates
1. Create template file in appropriate type directory
2. Use descriptive filename (becomes template name)
3. Include appropriate shebang and basic structure
4. Add placeholder comments for customization

### Template Selection
The system automatically selects templates based on keywords in descriptions:
- **data_processing**: Keywords like "data", "csv", "json", "parse"
- **api_client**: Keywords like "api", "http", "request", "client"
- **system_info**: Keywords like "system", "info", "hardware"

## Testing

### Test Framework
- **Primary**: pytest with typer.testing.CliRunner
- **Coverage**: Comprehensive test coverage required
- **Organization**: One test file per module

### Running Tests
```bash
# All tests
uv run pytest tests/

# Specific test file
uv run pytest tests/test_script.py

# Specific test function
uv run pytest tests/test_script.py::test_script_creation

# Verbose output
uv run pytest tests/ -v

# Using test runner script
./tests/run_tests.sh [options]
```

### Test Structure
```python
from typer.testing import CliRunner
from skogcli.script import script_app

def test_script_list():
    runner = CliRunner()
    result = runner.invoke(script_app, ["list"])
    assert result.exit_code == 0
    assert "Available custom scripts:" in result.stdout
```

### Testing Best Practices
1. **Test CLI behavior**: Use CliRunner for command testing
2. **Verify exit codes**: Always check command success/failure
3. **Validate output**: Check stdout content for expected results
4. **Mock external dependencies**: Isolate unit tests from system state
5. **Test error conditions**: Verify error handling and messages

---

## Conclusion

SkogCLI provides a comprehensive, extensible CLI framework with powerful script management, planned knowledge base integration, and robust configuration management. Its modular architecture and rich feature set make it an ideal foundation for command-line tooling in the SkogAI ecosystem.

The emphasis on test-driven development, comprehensive documentation, and user experience ensures that SkogCLI maintains high quality standards while remaining approachable for both developers and end users.
