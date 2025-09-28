# run.sh Context Management

## The Problem with Information Overload

Instead of receiving targeted, relevant context for specific tasks, assistants often get overwhelming amounts of irrelevant information - creating noise instead of clarity.

## The "SkogAI Way" Approach

### Principle: Targeted Context Delivery
- **Give assistants only what they need** for the current task
- **Avoid dumping entire codebases** and expecting miracles
- **Context should be purposeful**, not comprehensive
- **Focus on the specific problem** being solved

### What This Means in Practice

#### WRONG - Kitchen Sink Approach:
```bash

# Throwing everything at the assistant
./run.sh --include-everything --all-files --all-dependencies
```

#### RIGHT - Targeted Context:
```bash

# Providing specific, relevant context for the task
./run.sh --context="argc-syntax-patterns,environment-variables" --task="fix-librarian-tool"
```

## Context vs Implementation Details

### External Implementation Details Are Noise

**You do NOT need to know:**
- Internal SkogCLI implementation details already pushed in patch releases
- Every architectural decision in external dependencies
- Historical evolution of unrelated codebases
- Complete API documentation for tools you're not modifying

**You DO need to know:**
- Specific patterns relevant to your current task
- Interface contracts you must respect
- Environment requirements for your work
- Direct dependencies of what you're building

## run.sh Philosophy

### Context Should Be:
1. **Task-specific** - Relevant to what you're actually doing
2. **Actionable** - Information you can immediately use
3. **Focused** - Not everything that exists
4. **Current** - Up-to-date for your specific context

### Not:
1. **Comprehensive** - Every possible detail
2. **Historical** - How things evolved over time
3. **Tangential** - Related but not directly needed
4. **Speculative** - "You might need this someday"

## Implementation Pattern

### Smart Context Selection:
```bash

# Based on task type, provide relevant knowledge branches
case "$task_type" in
    "fix-tool")
        include_context="argc-syntax-patterns unix-exit-codes"
        ;;
    "multi-agent")
        include_context="environment-variables context-awareness"
        ;;
    "security-review")
        include_context="security-antipatterns exit-codes"
        ;;
esac
```

### Context Filtering:
- **Include**: Direct dependencies, relevant patterns, immediate requirements
- **Exclude**: Implementation details of external tools, historical context, unrelated systems

## Benefits of Targeted Context

1. **Faster comprehension** - Less noise to filter through
2. **Better focus** - Attention on what matters for the task
3. **Reduced errors** - Less irrelevant information to misinterpret
4. **Efficient work** - Direct path to solution without detours

## Real Example

### Instead of:
"Here's the entire SkogCLI codebase, all external dependencies, complete git history, and every configuration file. Please fix this one argc syntax issue."

### Do:
"Here's the argc syntax patterns knowledge and the specific tool file that needs fixing. The issue is with default value declaration."

This approach respects the assistant's time and cognitive capacity while providing exactly what's needed to complete the task effectively.