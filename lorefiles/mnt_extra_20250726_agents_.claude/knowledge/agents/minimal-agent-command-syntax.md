# SkogPrompt Minimal Agent Command Syntax

## Core Concept

The primary insight from our architectural exploration is that specialized 
agents can understand domain-specific instructions with minimal tokens, enabling
efficient communication without context bloat.

## Command Syntax

```
<agent>command</agent>
```

Where:

- `agent` is the name of the specialized agent (e.g., aider, dot, goose)
- `command` is the instruction to be executed by that agent

## Examples

- `<aider>run tests</aider>` - Instructs the Aider agent to run tests
- `<dot>format code</dot>` - Instructs the Dot agent to format code
- `<goose>suggest architectural improvements</goose>` - Instructs the Goose agent to suggest architectural improvements

## Benefits

1. **Token Efficiency** - Minimizes tokens required for communication
2. **Focused Scope** - Each agent understands its own domain with minimal 
context
3. **Clear Delegation** - Simple syntax for task delegation to specialized 
agents
4. **Reduced Context Bloat** - Avoids redundant context between different agents
5. **Faster Processing** - Less context means faster agent response times

## Implementation Approach

1. **Command Detection**
   - Parse text for `<agent>command</agent>` pattern
   - Extract agent name and command content

2. **Template Selection**
   - Select appropriate template based on agent and command
   - Load agent-specific context if needed

3. **Context Generation**
   - Generate minimal context needed for the specialized agent
   - Include only what's necessary for the specific command

4. **Asynchronous Execution**
   - Send command to agent via MCP server
   - Continue conversation while waiting for response
   - Handle response when available

5. **Response Integration**
   - Format agent response appropriately
   - Incorporate into main conversation flow

## Architectural Implications

This minimal command syntax influences our architecture in several ways:

1. **Template Design**
   - Templates must be agent-aware
   - Support for command-specific context generation
   - Dynamic variables based on command needs

2. **Context Management**
   - Smart context selection based on agent requirements
   - Efficient loading of only necessary context
   - Caching of common agent contexts

3. **MCP Integration**
   - Asynchronous command execution
   - Response handling and formatting
   - Status tracking for ongoing commands

4. **Variable Prompt Components**
   - Support for user message prompts
   - Support for assistant message prompts
   - Dynamic prompts with variables
   - Regular prompts with fixed text
   - System prompts with instructions
   - Persona injection

## Future Directions

- Expand syntax to support parameters (e.g., `<agent param="value">command</agent>`)
- Develop agent-specific context providers
- Create template library for common agent commands
- Support chained commands between multiple agents

---

This minimal command syntax represents a significant architectural insight for 
SkogPrompt, enabling efficient communication with specialized agents while 
maintaining a clean and intuitive interface for users.