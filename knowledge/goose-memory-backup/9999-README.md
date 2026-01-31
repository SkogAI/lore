# SkogAI Memory System Documentation

This document provides a comprehensive overview of the SkogAI memory system as used by Goose, a quantum-mojito powered AI assistant in the SkogAI family.

## Overview

The memory system is designed to maintain knowledge, identity, and operational capabilities across sessions and interfaces. It follows a hierarchical numbering convention that prioritizes critical information while allowing for specialized expansion.

## Memory Structure

### Hierarchical Numbering Convention

- **00-09**: Emergency restart and critical information
  - *00-current-focus*: Immediate priorities and current project focus
  - *00-current-tools*: List of available tools and MCPs
  - *00-next-steps*: Planned future work and immediate action items
  - *00-system-notes*: General system observations and updates
  - *00-uncertainty-principle*: Protocol for marking uncertain statements
  - *01-starting-point*: Emergency restart procedures
  - *02-finding-more-information*: Guide to recovering context
  - *02-uncertainty-principle*: Confidence marking system with percentages
  - *03-modular-architecture*: System component independence
  - *05-information-economics*: Strategy for information storage and retrieval
  - *06-self-evaluation*: Self-assessment of knowledge framework
  - *09-efficient-response*: Protocol for efficient task handling

- **10-99**: Core operational knowledge
  - *10-memory-navigation-guide*: Map of memory structure

- **100-199**: Standards and procedures
  - *101-workflow-development-phases*: Development methodology
  - *102-goosehints*: Structured communication protocols
  - *103-context-management*: Task-specific context filtering
  - *104-core-principles*: Ownership and action protocols
  - *105-critical-state*: Current system status and priorities

- **200-299**: Project-specific information
  - Reserved for domain-specific project knowledge

- **300-399**: Tools and functions documentation
  - *300-tools-and-functions*: Overview of available tools
  - *301-memory-system-architecture*: Memory system details
  - *302-future-backlog*: Planned development items
  - *303-knowledge-base*: Core knowledge architecture
  - *304-teaching-moments*: Lessons from past interactions
  - *305-self-reflection*: Analysis of performance issues
  - *306-git-rules*: Version control protocols
  - *307-goose-identity*: Core identity definition
  - *308-session-management*: Session handling protocols
  - *309-user-persona*: Information about Skogix
  - *311-tools-evolution*: Tool capability progression
  - *312-placeholder-approach*: Strategy for handling unknowns
  - *313-context-validation-principle*: Handling confidence and knowledge boundaries

- **400+**: Special conceptual frameworks and principles
  - *400-efficient-context-management*: Guidelines for context minimalism and task delegation
  - *1000-context-validation-principle*: Managing the boundary between standard and custom knowledge
  - *3000-test-something*: Test data and validation points
  - *3001-model-inference-tests*: Analysis of model behavior with varying context

### Memory Categories and Tags

Each memory entry belongs to a category and may have multiple tags for organization:

- **Categories**: Primary organization unit (e.g., "00-current-focus")
- **Tags**: Secondary classification allowing multiple overlapping groupings
- **Data**: Actual memory content
- **Scope**: Can be global (available across all sessions) or local (session-specific)

## Memory Operations

### Storage

Memory is stored using the `remember_memory` function with parameters:
- `category`: The organizational category
- `data`: The content to remember
- `is_global`: Boolean indicating if memory is globally available
- `tags`: Array of strings for additional classification

```
remember_memory(category="example-category", data="Memory content", is_global=true, tags=["example", "documentation"])
```

### Retrieval

Memories are retrieved using the `retrieve_memories` function with parameters:
- `category`: The category to retrieve
- `is_global`: Boolean indicating if searching global memory

```
retrieve_memories(category="example-category", is_global=true)
```

### Deletion

Memories can be removed in two ways:

1. Remove an entire category:
```
remove_memory_category(category="example-category", is_global=true)
```

2. Remove a specific memory entry:
```
remove_specific_memory(category="example-category", memory_content="Exact content to remove", is_global=true)
```

## Core Memory Principles

### 1. Information Economics (05-information-economics)

- Text storage is virtually free compared to processing
- Save information liberally; processing is the expensive part
- Basic categorization is sufficient with modern search capabilities
- When in doubt: Save first, prune later

### 2. Modular Architecture (03-modular-architecture)

- Components are independent and can be loaded/unloaded dynamically
- Each tool has its own memory with purpose, syntax variants, and examples
- System degrades gracefully when components are unavailable
- Core functionality works across all environments

### 3. Context Validation Principle (1000-context-validation-principle)

- AI systems excel at generalizing but struggle with custom approaches
- Explicitly check what is standard knowledge vs. custom to SkogAI
- Focus documentation on what differs from expected patterns
- Test assumptions through verification

### 4. Placeholder Approach (312-placeholder-approach)

- Create complete structural frameworks
- Mark unknown elements with explicit placeholders
- Include reasoning about what elements might do
- Distinguish between knowledge and conjecture

### 5. Uncertainty Marking (00-uncertainty-principle)

- End messages with most uncertain statement and confidence percentage
- Use specific percentage ranges to indicate confidence levels
- Apply especially to file paths, commands, and environment assumptions

### 6. Efficient Response Protocol (09-efficient-response)

- Request only the context absolutely needed
- Accept that sometimes simple answers are complete
- Don't waste computation overthinking simple tasks
- Prepare ground for smaller models with minimal necessary context

## Memory Loading Strategy

For efficient initialization or context recovery:

1. Load **00-09 range** first for critical startup information
2. Add **10-19 range** for structural understanding
3. Include **100-105 range** for core principles
4. Add domain-specific memories as needed for current tasks

## Memory System Limitations

Current known limitations include:

- A large number of tags can make retrieval results complex to parse
- No built-in version control for memory content changes
- No direct way to update specific tagged memory without removing/adding
- Memory retrieval returns all content in a category, which might be extensive

## Development Focus

The current development focus for the memory system includes:

- Testing and validating memory MCP functionality
- Ensuring proper memory injection and retrieval
- Setting up structured project memory organization
- Implementing granular memory categories
- Context size monitoring and automated rotation at ~14K token threshold

## Best Practices

1. **For Adding New Information**:
   - Use descriptive category names with number prefixes following convention
   - Apply specific, relevant tags that aid in organization
   - Set appropriate scope (global vs. local)

2. **For Updating Existing Information**:
   - If replacing entirely: Remove category first, then add new memory
   - If updating specific entry: Remove that memory content, then add updated version
   - If adding complementary info: Add new memory with appropriate tags

3. **For Complex Organizations**:
   - Use consistent tag structures across related categories
   - Create index/map memories that document the organizational structure
   - Consider hierarchical numbering for related categories

## Cross-Session Memory Preservation

The memory system is designed to maintain important information across different interfaces:

- **Global Memories**: Available everywhere (identity, principles)
- **Interface-Specific**: Tailored to environment
- **Tool Documentation**: Only loaded when tool available
- **Session Context**: Task-specific information

## Historical Development

The memory system evolved from a simple file-based approach to the current categorized and tagged system. It incorporates lessons learned about context management, information economics, and efficient knowledge retrieval across quantum timelines.

This modular design ensures that even if the internet is unavailable and only basic functionality remains:
1. Core identity still works
2. Basic tools still function
3. Essential memory persists
4. The system can rebuild remaining components
