# SkogChat Framework Concepts

This document outlines key concepts and patterns in the SkogChat framework without implementation details.

## Message Processing Pipeline

```
[Input Text with [@commands]] → Parser → Command Execution → Text Transformation → [Processed Output]
```

## Data Structures

```json
{
  "message": {
    "id": "$id",
    "user": "$agent",
    "content": "$string",
    "timestamp": "$datetime",
    "parent": "$id|$null"
  },
  "agent": {
    "id": "$id",
    "name": "$string"
  },
  "thread": {
    "id": "$id",
    "name": "$string",
    "description": "$string",
    "created_at": "$datetime",
    "updated_at": "$datetime"
  }
}
```

## Function Signatures

```
let createMessage $thread.id $message.type $message.content $message.parent = $message
let getMessage $message.id = $message | $null
let getThread $thread.id = $thread | $null
let listMessages $thread.id = [$message]
```

## Recursive Command Resolution

Command directives like `[@command:param]` trigger script execution. The result replaces the directive in the text before further processing. This allows:

1. Commands generating text containing other commands
2. Processing happens "inside out" for nested commands
3. Recipients only see final transformed text, not the directives

## Information Flow Patterns

1. **Proactive Context Injection**
   - System identifies likely informational needs
   - Information is injected before being requested
   - Directives create appearance of continuous knowledge

2. **Topic Detection**
   - Message sequences are analyzed for subject changes
   - Context adjusts automatically to match current topic
   - User experiences seamless transitions

3. **Agent-to-Agent Communication**
   - Agents can invoke other agents through directives
   - Processing is invisible to the user
   - Results appear as natural conversation

## Extension Capabilities

The framework enables:

1. Natural language creation of new command handlers
2. Self-improving tooling through generated scripts
3. Dynamic behavior adaptation based on conversation patterns
4. Composable transformations through directive nesting

These concepts provide foundation patterns without implementation details.