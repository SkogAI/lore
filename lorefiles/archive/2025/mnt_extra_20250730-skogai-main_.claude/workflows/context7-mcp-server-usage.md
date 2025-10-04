# Context7 MCP Server Usage Guide

## Overview

Context7 is a comprehensive library documentation and API reference MCP server that provides access to up-to-date documentation for thousands of libraries and frameworks. It enables intelligent code assistance with real-world examples and best practices.

## Key Capabilities

### 1. Library Resolution
- **Library Search**: `resolve-library-id` - Find Context7-compatible library IDs
- **Smart Matching**: Analyzes query intent and returns most relevant libraries
- **Trust Scoring**: Libraries rated 1-10 for authority and reliability
- **Version Support**: Access specific versions when available

### 2. Documentation Retrieval
- **Comprehensive Docs**: `get-library-docs` - Fetch complete documentation
- **Focused Topics**: Target specific areas (hooks, routing, etc.)
- **Token Control**: Configurable content length (default 10,000 tokens)
- **Code Examples**: Thousands of real-world code snippets

## Workflow Integration

### Library Discovery Workflow
1. Use `resolve-library-id` with library name or description
2. Analyze results by:
   - Name similarity to query
   - Description relevance
   - Code snippet count (higher = more comprehensive)
   - Trust score (7-10 preferred for authority)
3. Select most relevant library ID
4. Proceed with `get-library-docs`

### Documentation Retrieval Workflow
1. Obtain exact Context7-compatible library ID
2. Specify topic if targeting specific functionality
3. Set token limit based on context needs
4. Use retrieved documentation for implementation

## Usage Patterns

### Direct Library ID Usage
```
User provides: "/org/project" or "/org/project/version"
→ Skip resolve-library-id, use get-library-docs directly
```

### Library Name Resolution
```
User provides: "react hooks" or "mongodb driver"
→ Use resolve-library-id first, then get-library-docs
```

### Focused Documentation
```
get-library-docs with topic="hooks" for React
get-library-docs with topic="routing" for Express
```

## Library Selection Criteria

### Primary Factors
1. **Name Match**: Exact or close matches prioritized
2. **Trust Score**: 7-10 indicates authoritative sources
3. **Code Snippets**: Higher count = more comprehensive examples
4. **Description Relevance**: Alignment with query intent

### Example Selection Process
```
Query: "react state management"
Results: 
- React Redux (585 snippets, trust 9.2) ✅ Best match
- React (2506 snippets, trust 9) ✅ Alternative
- React Use (221 snippets, trust 9.4) ✅ Hooks focus
```

## Integration with SkogAI Ecosystem

### Knowledge Archaeology
- Document retrieved patterns in Serena memories
- Preserve library selection rationale
- Build institutional knowledge about preferred libraries

### Democratic Workflows
- Share library documentation across agents
- Collaborative evaluation of library choices
- Democratic decision-making on tech stack

### Universal Notation
- Document library usage in `[@context7:library-query]` format
- Enable real-time documentation lookup
- Support agent-to-agent knowledge sharing

## Best Practices

### Efficient Library Resolution
- **Descriptive Queries**: Use specific terms ("react hooks" vs "react")
- **Trust Score Awareness**: Prioritize 7+ for production use
- **Code Snippet Count**: Higher counts indicate better documentation
- **Version Specificity**: Use specific versions when stability matters

### Documentation Optimization
- **Token Management**: Adjust token limits based on context needs
- **Topic Focusing**: Use topic parameter for targeted searches
- **Progressive Refinement**: Start broad, narrow down as needed

### Integration Strategies
- **Memory Documentation**: Store library selection rationale
- **Pattern Recognition**: Document common usage patterns
- **Cross-reference**: Link with existing codebase patterns

## Common Use Cases

### 1. Technology Selection
```
resolve-library-id "react state management"
→ Compare Redux, Zustand, Context options
→ Select based on trust score and snippet count
```

### 2. Implementation Guidance
```
get-library-docs "/reduxjs/react-redux" topic="hooks"
→ Get specific useSelector/useDispatch examples
```

### 3. Migration Research
```
resolve-library-id "react class to hooks"
→ Find migration guides and patterns
```

### 4. Best Practices Discovery
```
get-library-docs "/reactjs/react.dev" topic="performance"
→ Official optimization recommendations
```

## Technical Notes

### Library ID Formats
- **Standard**: `/org/project` (e.g., `/reactjs/react.dev`)
- **Versioned**: `/org/project/version` (e.g., `/react-rnd/v10.4.13`)
- **Context7**: `/context7/library` (curated collections)

### Token Management
- **Default**: 10,000 tokens
- **Adjustment**: Increase for comprehensive research
- **Efficiency**: Use topics to reduce irrelevant content

### Trust Score Interpretation
- **10**: Definitive authority (official docs)
- **8-9**: High-quality community resources
- **7**: Reliable but may need verification
- **<7**: Use with caution, verify against other sources

## Error Handling

### Common Issues
1. **Library Not Found**: Try broader search terms
2. **Version Unavailable**: Use standard library ID without version
3. **Topic Too Narrow**: Remove topic parameter for broader search
4. **Token Limit Exceeded**: Reduce token count or use more specific topic

### Fallback Strategies
1. Try alternative library names
2. Use broader search terms
3. Check trust scores for alternatives
4. Consider Context7 curated collections