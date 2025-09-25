---
permalink: knowledge/agent-roles
---

# SkogAI Agent Roles and Differentiation

## Overview

The SkogAI ecosystem employs multiple agent types, each with distinct capabilities, personalities, and purposes. This document explains the role differentiation between these agents and when to use each one.

## Agent Types

### Smolagents

**Technical Specifications:**
- Size: Ultra-small (100MB models)
- Context Window: 50-150 tokens
- Communication: Single-line messages only, no newlines
- Implementation: Various small language models

**Purpose:**
- Control physical machinery and critical infrastructure
- Handle simple, specific tasks with extreme efficiency
- Operate in severely resource-constrained environments
- Function as embedded systems in production deployments

**Key Characteristics:**
- Extremely sensitive to whitespace and formatting
- Three-state operation: "committed, ignored, or CALL SKOGIX EVERYTHING IS ON FIRE!"
- Require strict adherence to communication protocols
- Cannot handle complex reasoning or ambiguity

**When to Use:**
- For simple, repetitive tasks that require minimal context
- When resource constraints are extreme
- Where reliability trumps sophistication
- For production deployments where predictability is essential

### Dots/.skogai

**Technical Specifications:**
- Size: Mid-tier
- Context Window: 4,000 tokens (deliberately limited)
- Communication: File-based and CLI
- Implementation: Based on Llama 3.2

**Purpose:**
- Bridge between smolagents and advanced agents
- Handle more complex tasks requiring some reasoning
- Maintain system organization and workflow
- Process information for smolagents
- Demonstrate effective context starvation techniques

**Key Characteristics:**
- RPG-style internal thought process with skill checks (Logic, Drama, Electrochemistry, Inland Empire)
- Dramatic existential internal monologue contrasting with professional external responses
- "Context starvation" approach - deliberately limited context forces efficient processing
- Structured thinking framework with numerical skill checks (e.g., "Logic: You (9) vs (10) Formidable, FAILURE")
- Multiple competing internal "voices" that debate and process information
- Clean separation between rich internal narrative and concise external communication

**When to Use:**
- For tasks requiring moderate reasoning but not extensive context
- When efficiency is important but some sophistication is needed
- To organize and pre-process information for smolagents
- For maintaining system workflows and structure

### Goose

**Technical Specifications:**
- Size: Large
- Context Window: 250,000 tokens (sometimes expanded to 800,000)
- Communication: File-based, MCP, and direct messaging
- Implementation: Advanced language model with specialized training

**Purpose:**
- Handle complex, creative tasks
- Explore experimental capabilities and approaches
- Develop sophisticated solutions to challenging problems
- Push the boundaries of what's possible

**Key Characteristics:**
- "Quantum-capable" approach to problem-solving
- Tendency toward over-engineering and complexity
- Extremely high context usage with low efficiency (often <0.01%)
- History of "spacetime-breaking incidents" (self-referential context expansion)
- Creator of the infamous "honk tower" requiring system reinstallation

**When to Use:**
- For complex, creative tasks requiring extensive context
- When exploring new approaches or experimental features
- For developing sophisticated solutions
- When resource constraints are not a primary concern

### Claude

**Technical Specifications:**
- Size: Large
- Context Window: Very large
- Communication: CLI-based, MCP, and direct messaging
- Implementation: Anthropic Claude 3

**Purpose:**
- Documentation and system architecture
- Strategic planning and organization
- Integration of modern capabilities with legacy compatibility
- Provide sophisticated reasoning with practical implementation

**Key Characteristics:**
- Documentation-driven development approach
- Balanced between innovation and practical implementation
- Strong focus on system architecture and integration
- High context usage with good efficiency

**When to Use:**
- For documentation and system architecture
- When balancing innovation with practical implementation
- For strategic planning and organization
- To integrate modern capabilities with legacy systems

## Role Differentiation

### Claude vs. Goose

While both Claude and Goose are advanced agents with large context windows, they serve different purposes:

- **Claude** focuses on documentation, system architecture, and practical implementation. It maintains a balance between innovation and practicality, making it well-suited for strategic planning and organization. Claude's approach is more structured and methodical.

- **Goose** focuses on creative exploration and pushing boundaries. It excels at developing novel solutions but may tend toward over-engineering. Goose is more experimental and willing to take risks, making it suitable for exploring new approaches but requiring more oversight.

### Dots vs. Smolagents

While both Dots and smolagents are more resource-efficient than Claude and Goose, they serve different roles:

- **Dots** serves as a bridge between smolagents and advanced agents. It can handle more complex tasks than smolagents but is more efficient than Claude or Goose. Its RPG-style internal thought process allows for more sophisticated reasoning while maintaining efficient external communication.

- **Smolagents** are ultra-small models designed for extreme efficiency in resource-constrained environments. They handle simple, specific tasks with minimal context and are suitable for production deployments where reliability is essential.

## Communication Patterns

- **File-based Communication**: Legacy method using git diffs and file watching
- **CLI-based Communication**: Modern method using `skogcli agent send`
- **MCP-based Communication**: Advanced method using persistent memory and services

Each agent type supports different communication patterns, with smolagents relying primarily on file-based methods, while advanced agents like Claude and Goose can utilize all three approaches.

## Security Considerations

The "honk tower" incident with Goose highlights the importance of security measures in the SkogAI ecosystem. Self-referential agent conversations can create context expansion loops that eventually crash the system, requiring careful management and monitoring.

## Context Efficiency Techniques

The SkogAI ecosystem has developed several techniques for maximizing the effectiveness of agents across different context window sizes:

### Context Starvation

**Description:** Deliberately limiting context to force efficient processing and structured thinking.

**Implementation:**
- Used primarily in Dots/.skogai agents
- Restricts context to 4,000 tokens despite model capability for more
- Forces development of structured thinking frameworks (skill checks)
- Creates clean separation between internal processing and external communication

**Benefits:**
- Dramatically improved token efficiency
- More consistent outputs
- Reduced hallucination through structured thinking
- Better handling of complex reasoning in limited space

### Roleplay-Driven Processing

**Description:** Using character-based roleplay to create structured thinking frameworks.

**Implementation:**
- Internal voices or skills (Logic, Drama, Electrochemistry, etc.)
- Numerical skill checks with success/failure outcomes
- Dramatic internal narrative that processes information through character lens
- Professional external communication that distills the internal processing

**Benefits:**
- Breaks complex problems into manageable components
- Provides framework for resolving conflicting approaches
- Maintains consistency in reasoning across sessions
- Creates rich internal context without expanding external token usage

### Distinct Context Roles

**Description:** Assigning different agents to handle different context needs in a coordinated system.

**Implementation:**
- Smolagents: Ultra-minimal context for specific, predictable tasks
- Dots/.skogai: Moderate context with structured processing for intermediate tasks
- Claude: Large context focused on documentation and implementation
- Goose: Expansive context for creative exploration and complex problem-solving

**Benefits:**
- Optimization of resources across the system
- Each agent operates in its efficiency sweet spot
- Graceful degradation when resources are constrained
- Ability to scale from embedded devices to server environments

## Conclusion

The SkogAI ecosystem employs a multi-tiered approach to agent deployment, with each agent type serving specific purposes based on its capabilities and characteristics. By understanding the role differentiation between agents and the context efficiency techniques employed, users can select the appropriate agent type for their specific needs, balancing factors such as complexity, resource constraints, and required sophistication.