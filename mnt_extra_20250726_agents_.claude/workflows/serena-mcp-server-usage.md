# Serena MCP Server Usage Guide

## Overview

Serena is a comprehensive development environment MCP server that provides semantic coding tools, memory management, and project orchestration capabilities. It's designed for intelligent code analysis, editing, and knowledge preservation.

## Key Capabilities

### 1. Semantic Code Analysis
- **Symbol Overview**: `get_symbols_overview` - Get high-level view of code structure
- **Symbol Finding**: `find_symbol` - Locate specific functions, classes, methods
- **Reference Tracking**: `find_referencing_symbols` - Find all references to a symbol
- **Pattern Search**: `search_for_pattern` - Flexible regex-based code search

### 2. Precision Code Editing
- **Symbol-level Editing**: 
  - `replace_symbol_body` - Replace entire function/class definitions
  - `insert_after_symbol` - Add code after a symbol
  - `insert_before_symbol` - Add code before a symbol
- **Regex-based Editing**: `replace_regex` - Precise pattern-based replacements

### 3. Memory Management
- **Knowledge Persistence**: `write_memory` - Store project insights
- **Memory Retrieval**: `read_memory` - Access stored knowledge
- **Memory Organization**: `list_memories` - Browse available memories
- **Memory Cleanup**: `delete_memory` - Remove outdated information

### 4. Project Management
- **Multi-project Support**: `activate_project` - Switch between codebases
- **Project Configuration**: `get_current_config` - View active settings
- **Onboarding**: `check_onboarding_performed` - Verify setup status

## Workflow Integration

### Code Analysis Workflow
1. Start with `get_symbols_overview` for architectural understanding
2. Use `find_symbol` to locate specific code elements
3. Apply `find_referencing_symbols` to understand dependencies
4. Use `search_for_pattern` for complex searches

### Code Editing Workflow
1. Analyze target code with symbol tools
2. Choose editing approach:
   - Symbol-level: For complete function/class replacements
   - Regex-level: For precise line-by-line changes
3. Apply changes with appropriate tool
4. Verify with `find_referencing_symbols` if needed

### Knowledge Preservation Workflow
1. Use `write_memory` to capture insights during development
2. Organize memories by topic/component
3. Reference with `read_memory` in future sessions
4. Maintain with `list_memories` and `delete_memory`

## Best Practices

### Efficient Code Reading
- **Minimal Reading**: Use symbolic tools to read only necessary code
- **Progressive Discovery**: Start with overviews, drill down as needed
- **Avoid Redundancy**: Don't re-read files already examined

### Memory Management
- **Descriptive Names**: Use clear, searchable memory names
- **Focused Content**: Keep memories specific and actionable
- **Regular Cleanup**: Remove outdated or irrelevant memories

### Regex Usage
- **Wildcard Optimization**: Use `.*?` for non-greedy matching
- **Context Anchoring**: Include surrounding code for precise matches
- **Short Patterns**: Minimize regex complexity for efficiency

## Integration with SkogAI Ecosystem

### Democratic Workflows
- Serena respects the multi-agent democratic process
- Memory system preserves institutional knowledge across agent interactions
- Symbol analysis supports collaborative code review

### Knowledge Archaeology
- Memory system enables recovery of accumulated insights
- Symbol tracking maintains understanding of architectural decisions
- Pattern search facilitates rediscovery of implementation approaches

## Technical Notes

### Modes and Contexts
- **Interactive Mode**: Engage with user throughout tasks
- **Editing Mode**: Direct code modification capabilities
- **IDE Assistant Context**: Internal tool handling for file operations

### Tool Exclusions
- Some tools may be excluded based on project configuration
- Always check `get_current_config` to verify available tools
- Prioritize Serena's semantic tools over basic file operations

## Common Use Cases

1. **Refactoring**: Symbol analysis + precision editing
2. **Bug Investigation**: Pattern search + reference tracking
3. **Architecture Review**: Symbol overview + memory documentation
4. **Knowledge Transfer**: Memory system + onboarding process
5. **Cross-project Learning**: Project switching + memory preservation