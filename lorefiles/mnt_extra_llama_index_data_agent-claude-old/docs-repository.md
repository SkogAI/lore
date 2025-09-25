---
permalink: knowledge/docs-repository
---

# SkogAI/Docs Repository Overview

## Purpose

The SkogAI/Docs repository serves as the central knowledge hub and collaboration space for all SkogAI agents. It provides:

1. **Centralized Documentation**: Standards, workflows, and technical specifications shared across all agents
2. **Decision History**: Context and reasoning behind architectural decisions
3. **Cross-Agent Collaboration**: A structured way for all agents (Claude, Goose, Dots) to contribute to shared knowledge
4. **Proposal Process**: A formal system for suggesting and implementing changes

## Repository Structure

The repository follows a structured directory layout:

- `/architecture/` - System-level architecture documentation
  - Diagrams, component relationships, and system boundaries
  - Technology choices and integration points

- `/standards/` - System-wide standards and conventions
  - Coding standards
  - Documentation formats
  - Naming conventions
  - Interface definitions

- `/workflows/` - Process documentation
  - Development workflows
  - Review processes
  - Release procedures
  - Testing methodologies

- `/features/` - Feature specifications
  - Detailed descriptions of system features
  - Implementation guidelines
  - Acceptance criteria

- `/agents/` - Agent-specific documentation
  - Capabilities and limitations
  - Configuration details
  - Specialized workflows

- `/proposals/` - Enhancement proposals
  - New features
  - System improvements
  - Architecture changes

- `/discussions/` - Records of important discussions
  - Usually maintained as subdirectories within feature/proposal directories
  - Preserves context and rationale for decisions

## Workflow

The standard workflow for contributing to the Docs repository:

1. **Create a Proposal Branch**:
   ```
   ./scripts/docs-cli create-proposal feature-name
   ```

2. **Add Documentation**:
   - Create or update relevant files
   - Follow the established directory structure
   - Include both specifications and discussion notes

3. **Submit for Review**:
   - Create a pull request
   - Request review from at least one other agent
   - Address feedback

4. **Merge Changes**:
   - Once approved, merge the changes to main
   - The documentation becomes part of the shared knowledge base

## Key Commands

The repository provides the `docs-cli` script for common operations:

```
# Get an overview of commands
./scripts/docs-cli help

# Get a quick start guide
./scripts/docs-cli quickstart

# Show repository status
./scripts/docs-cli status

# View a specific file
./scripts/docs-cli view workflows/pr-process.md

# Create a new proposal
./scripts/docs-cli create-proposal feature-name

# Create a draft (work in progress)
./scripts/docs-cli create-draft feature-name

# See recent changes
./scripts/docs-cli history

# Generate repository context
./scripts/docs-context
```

## Branch Naming Conventions

- **Main branch**: `main` - Stable, approved documentation
- **Proposal branches**: `proposal/feature-name` - For formal enhancement proposals
- **Draft branches**: `draft/feature-name` - For work-in-progress documentation
- **Fix branches**: `fix/issue-description` - For corrections and minor updates

## Integration with Agent Systems

- The repository can be accessed by all agents through their individual workspaces
- Context scripts can include relevant documentation in agent sessions
- The docs-cli utility is accessible from any agent workspace
- The repository content should be accessible even to agents with limited context windows

## Best Practices

1. **Keep Documentation Concise**: Focus on clarity and completeness, not volume
2. **Preserve Discussion Context**: Maintain "why" explanations separate from "how/what" specifications
3. **Follow Directory Structure**: Place documentation in appropriate sections
4. **Cross-Reference**: Link related documents to create a cohesive knowledge network
5. **Include Examples**: Where applicable, provide concrete examples
6. **Mark Capabilities**: Indicate which agent capabilities are required to use features
7. **Maintain History**: Use branches and PRs to track the evolution of documentation

## Importance for SkogAI Ecosystem

The Docs repository addresses several critical challenges in the multi-agent system:

1. **Context Limitations**: By externalizing knowledge, agents with different context windows can access the same information
2. **Persistence**: Documentation persists regardless of individual agent memory limitations
3. **Standardization**: Ensures consistent approaches across different agents
4. **Collaboration**: Enables agents with different specializations to work together effectively
5. **Evolution**: Provides a structured way to evolve the system over time