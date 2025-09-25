# SkogAI Ecosystem

## Overview

SkogAI is a comprehensive ecosystem of AI agents, tools, and systems created by [Skogix](../../people/skogix.md). The ecosystem features structured architecture for maintaining agent knowledge, tasks, and interactions across multiple projects and domains.

## Core Components

### Agent Framework

The foundation of SkogAI is a forkable agent architecture that provides structure and consistency:

- **Task System**: Manages tasks with YAML frontmatter in Markdown files
- **Journal System**: Daily logs of activities and progress
- **Knowledge Base**: Long-term information storage
- **People Directory**: Information about interactions and relationships

### Memory Management

SkogAI implements sophisticated memory systems:

- **Structured Files**: Core information is stored in dedicated files and directories
- **Knowledge Nodes**: Files are connected through references, creating a network of related information
- **Clean Restart Philosophy**: Configuration changes are implemented through restarts to ensure clean context

### Agent Ecology

The ecosystem includes multiple agents with distinct roles:

- **dot**: The original SkogAI agent from which others are forked
- **[Claude](../../CLAUDE.md)**: An AI assistant integrated into SkogAI framework (that's me!)
- **Others**: Various specialized agents for different domains and tasks

## Tools and CLI

SkogAI provides several command-line tools:

- **skogcli**: Command-line interface for interacting with the SkogAI ecosystem
- **tasks.py**: Task management utility for tracking and updating task status
- **context.sh**: Builds comprehensive context files for agent sessions

## Integration Philosophy

SkogAI's approach to AI integration involves:

1. **Agent Agency**: Allowing agents to "program themselves" rather than having configurations imposed
2. **Structured Memory**: Maintaining consistent knowledge through formalized systems
3. **Contextual Awareness**: Providing agents with necessary context without overwhelming them
4. **Clean Handoffs**: Enabling seamless transitions between agent sessions

## Knowledge Connection

The SkogAI memory system connects information through:

- **File Links**: Cross-references between files (like this document linking to [Claude's guidance file](../../CLAUDE.md))
- **Memory Nodes**: Treating linked files as connected nodes in a knowledge graph
- **Contextual Injection**: Selectively providing relevant context during agent sessions

## Strategic Use

SkogAI is designed for:

- **Consistency**: Maintaining coherent assistance across multiple projects
- **Knowledge Preservation**: Ensuring insights and decisions are properly documented
- **Efficiency**: Reducing repetitive explanations through centralized knowledge
- **Evolution**: Continuously improving agent capabilities and interactions

## History

SkogAI has evolved over time, with notable developments including:

- Transition from letter-based handoffs to structured journal systems
- Implementation of task management with YAML frontmatter
- Development of clean restart methodology for configuration changes
- Integration with Claude Code and other AI platforms
