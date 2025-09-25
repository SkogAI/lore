# Code Style and Conventions

## Python Code Style
- **Black** for code formatting (automatic)
- **Ruff** for linting with auto-fix enabled
- **isort** for import sorting
- **Type hints** required for new code
- **Docstrings** for classes and public methods

## File Organization Conventions

### Task Files (`tasks/`)
- **YAML frontmatter** with required fields: `state`, `created`
- **Optional metadata**: `priority`, `tags`, `depends`
- **Markdown body** with subtasks using `- [x]` checkboxes
- **Clear titles** and success criteria
- **Relative paths** from repository root for links

### Journal Entries (`journal/`)
- **ISO date format** in filenames: `2025-06-20.md`
- **Session summaries** and knowledge capture
- **Cross-references** to tasks, people, and knowledge
- **Daily discoveries** and learning moments

### Knowledge Base (`knowledge/`)
- **Topic-focused** markdown files
- **Technical insights** and architectural understanding
- **Process documentation** and best practices
- **Links to related resources**

## Naming Conventions
- **kebab-case** for file names and task IDs
- **snake_case** for Python variables and functions
- **PascalCase** for Python classes
- **UPPER_CASE** for constants

## Documentation Standards
- **Descriptive link text** that makes sense out of context
- **Relative paths** from repository root when possible
- **Cross-references** between related documents
- **Version information** in technical documentation

## Git Conventions
- **Meaningful commit messages** with context
- **Feature branch workflow** with descriptive names
- **Pre-commit hooks** for validation
- **Submodule awareness** (this workspace is a git submodule)