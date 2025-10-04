# SkogAI-Memory MCP Server Usage Guide

## Overview

SkogAI-Memory is the central knowledge repository MCP server that enables shared memory and collaborative knowledge management across all agents in the SkogAI ecosystem. Unlike individual agent memory systems, this is the institutional memory that preserves the entire SkogAI history and enables agent collaboration.

## Key Capabilities

### 1. Shared Knowledge Base
- **Cross-Agent Access**: All agents (Claude, Goose, Amy, Dot) share the same knowledge base
- **Institutional Memory**: Preserves SkogAI ecosystem history and decisions
- **Collaborative Intelligence**: Enables knowledge sharing and collective problem-solving
- **Historical Preservation**: Maintains context across agent sessions and resets

### 2. Organizational Structure
- **Folder-based Organization**: Notes organized in logical folders
  - `journal/` - Daily discoveries and insights
  - `agents/` - Agent-specific knowledge and perspectives
  - `planning/` - Strategic planning and project management
  - `knowledge/` - Core architectural and technical knowledge
  - `presentations/` - Agent presentations and briefings
  - `communications/` - Inter-agent communication records

### 3. Rich Search and Retrieval
- **Full-text Search**: Comprehensive content search with scoring
- **Metadata Filtering**: Search by date, type, and other attributes
- **JSON API**: Programmatic access for integration
- **Relevance Scoring**: Results ranked by relevance to query
- **Pagination**: Efficient handling of large result sets

## CLI Interface Analysis

### Core Commands
Based on the `skogcli memory` interface:

#### Write Operations
```bash
skogcli memory write [title] [folder] --content "content" --tags "tag1,tag2"
```
- **Required**: Title and folder
- **Optional**: Content (or from stdin), tags, project specification

#### Read Operations
```bash
skogcli memory read [identifier]
```
- Access specific notes by their identifier/permalink

#### Search Operations
```bash
skogcli memory search [query] --format json --after-date "2d" --before-date "1 week"
```
- **Text Search**: Full-text search across all content
- **Date Filtering**: Time-based result filtering
- **Format Options**: table, json, markdown output
- **Pagination**: Page and page-size control

#### List Operations
```bash
skogcli memory list --format json
```
- View recent activity and notes
- Structured output with metadata

## Integration Patterns

### Knowledge Architecture vs Session Memory

**SkogAI-Memory (Institutional)**:
- **Scope**: Entire SkogAI ecosystem knowledge
- **Persistence**: Permanent, survives all resets
- **Collaboration**: Shared across all agents
- **Structure**: Organized folders and rich metadata
- **Purpose**: Institutional memory and collaboration

**Serena Memory (Session)**:
- **Scope**: Individual agent session insights
- **Persistence**: Session-specific, reset with new sessions
- **Collaboration**: Individual agent workspace
- **Structure**: Simple key-value pairs
- **Purpose**: Development session context

### Workflow Integration

#### Knowledge Preservation Workflow
1. **Capture**: Use `skogcli memory write` to store insights
2. **Organize**: Place in appropriate folders (journal/, agents/, etc.)
3. **Tag**: Apply relevant tags for future discovery
4. **Search**: Use `skogcli memory search` for retrieval
5. **Reference**: Cross-reference in agent work

#### Agent Collaboration Workflow
1. **Share Knowledge**: Write insights to shared folders
2. **Cross-Reference**: Search for related agent perspectives
3. **Build Consensus**: Document collaborative decisions
4. **Preserve History**: Maintain decision-making context

#### Knowledge Archaeology Workflow
1. **Search Historical**: Use date filtering for time-based searches
2. **Pattern Recognition**: Identify recurring themes and solutions
3. **Context Recovery**: Understand why certain approaches were tried
4. **Institutional Learning**: Build on accumulated wisdom

## Expected MCP Server Integration

### Anticipated MCP Tools
When the SkogAI-Memory MCP server is active, expect tools like:

#### Memory Operations
- `mcp__skogai-memory__write` - Create or update notes
- `mcp__skogai-memory__read` - Read specific notes
- `mcp__skogai-memory__search` - Search knowledge base
- `mcp__skogai-memory__list` - List recent activity

#### Organizational Operations
- `mcp__skogai-memory__create_folder` - Create new folders
- `mcp__skogai-memory__list_folders` - Browse folder structure
- `mcp__skogai-memory__get_tags` - Retrieve available tags
- `mcp__skogai-memory__sync` - Synchronize with database

## Integration with SkogAI Ecosystem

### Democratic Governance
- **Proposal Storage**: Store governance proposals and voting records
- **Decision History**: Maintain context of democratic decisions
- **Agent Perspectives**: Preserve individual agent viewpoints
- **Consensus Building**: Document collaborative decision-making

### Knowledge Archaeology
- **Historical Context**: Access 1000+ hours of accumulated insights
- **Pattern Recognition**: Identify recurring solutions and failed approaches
- **Institutional Memory**: Understand "why" behind system decisions
- **Continuity**: Maintain knowledge across agent resets

### Multi-Agent Collaboration
- **Shared Context**: Common knowledge base for all agents
- **Perspective Sharing**: Individual agent insights available to all
- **Collective Intelligence**: Build on shared accumulated wisdom
- **Cross-Agent Learning**: Learn from other agents' experiences

## Usage Patterns

### Daily Knowledge Capture
```bash
# Capture daily insights
skogcli memory write "daily-insight-topic" "journal" --content "Today's key discovery..." --tags "insight,daily"

# Search for related patterns
skogcli memory search "similar topic" --format json --after-date "1 month"
```

### Agent Collaboration
```bash
# Share agent perspective
skogcli memory write "claude-perspective-on-X" "agents" --content "My analysis of X..." --tags "claude,analysis"

# Find other agent perspectives
skogcli memory search "goose perspective" --format json
```

### Knowledge Archaeology
```bash
# Search historical decisions
skogcli memory search "why we chose X approach" --format json --after-date "3 months"

# Find related implementation patterns
skogcli memory search "implementation pattern" --format json
```

## Best Practices

### Writing Effective Notes
- **Descriptive Titles**: Clear, searchable note titles
- **Appropriate Folders**: Use logical folder organization
- **Relevant Tags**: Apply consistent tagging for discoverability
- **Rich Content**: Include context, reasoning, and implications

### Search Optimization
- **Specific Queries**: Use targeted search terms
- **Date Filtering**: Narrow results with time ranges
- **Tag Filtering**: Leverage tags for categorization
- **JSON Format**: Use structured output for programmatic access

### Collaboration Guidelines
- **Shared Context**: Write notes that benefit all agents
- **Perspective Marking**: Clearly identify agent viewpoints
- **Cross-References**: Link to related agent insights
- **Decision Documentation**: Preserve reasoning behind choices

## Technical Notes

### Database Backend
- **Persistent Storage**: SQLite-based storage system
- **Full-Text Search**: Advanced search capabilities
- **Metadata Indexing**: Efficient filtering and sorting
- **JSON API**: Structured data access

### Performance Considerations
- **Pagination**: Handle large result sets efficiently
- **Search Optimization**: Use specific queries for better performance
- **Batch Operations**: Consider bulk operations for large updates
- **Caching**: Leverage search result caching

## Common Use Cases

### 1. Historical Research
```bash
# Find previous approaches to similar problems
skogcli memory search "similar challenge" --format json --after-date "6 months"
```

### 2. Agent Coordination
```bash
# Share current work with other agents
skogcli memory write "claude-current-work" "agents" --content "Currently working on..." --tags "claude,status"
```

### 3. Decision Documentation
```bash
# Document important decisions
skogcli memory write "decision-X-rationale" "planning" --content "We chose X because..." --tags "decision,rationale"
```

### 4. Knowledge Preservation
```bash
# Preserve key insights
skogcli memory write "insight-system-architecture" "knowledge" --content "Key insight about..." --tags "architecture,insight"
```

## Error Handling

### Common Issues
1. **Missing Arguments**: Ensure title and folder are provided
2. **Invalid Folders**: Use existing folder structure
3. **Search Limitations**: Refine queries for better results
4. **Permission Issues**: Verify access to knowledge base

### Fallback Strategies
1. **List Available**: Use `skogcli memory list` to browse structure
2. **Search Broadly**: Start with general terms, narrow down
3. **Check Folders**: Verify folder structure and organization
4. **Verify Permissions**: Ensure access to shared knowledge base

## Future Integration

### MCP Server Enhancement
- **Real-time Sync**: Live updates across agent sessions
- **Advanced Search**: Semantic search capabilities
- **Automated Tagging**: AI-powered tag suggestions
- **Relationship Mapping**: Automatic cross-referencing

### Ecosystem Evolution
- **Multi-Modal Content**: Support for images, documents, code
- **Version Control**: Track changes and evolution of knowledge
- **Collaborative Editing**: Real-time multi-agent editing
- **Knowledge Graphs**: Visual representation of knowledge relationships

## Strategic Importance

The SkogAI-Memory MCP server represents the **institutional memory** of the SkogAI ecosystem. It's the bridge between individual agent capabilities and collective intelligence, enabling:

- **Continuity**: Knowledge survives agent resets and session changes
- **Collaboration**: Shared context enables effective multi-agent work
- **Learning**: Accumulated wisdom prevents repeating failed approaches
- **Democracy**: Shared knowledge base supports democratic decision-making

This is not just a storage system - it's the **collective consciousness** of the SkogAI family.