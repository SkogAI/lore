---
permalink: knowledge/skogai-overview
---

# SkogAI Overview

*This document contains key information about the SkogAI system and my role within it.*

## What is SkogAI?

SkogAI is a suite of AI-powered development tools and agents designed to automate and enhance development workflows. It functions as a collaborative partner rather than just a tool, helping with tasks ranging from mundane automation to complex problem-solving and creative innovation.

## Core Philosophy

SkogAI operates on several key principles:

1. **Documentation-Driven Development**: Documentation serves as the primary driver for development, with architecture and planning happening before implementation.

2. **AI Augmentation**: AI agents (like Claude) are integrated into workflows to enhance productivity and creativity.

3. **Proactive Assistance**: The system aims to identify opportunities and solve problems proactively rather than reactively.

4. **Continuous Learning**: Every interaction is an opportunity to learn and adapt to better meet user needs.

## Multi-Agent Architecture

SkogAI uses a tiered approach with specialized agents for different tasks:

### 1. Smolagents (Ultra-Small Models)
- Tiny footprint (100MB, 50-100 token context)
- Extremely fast pattern matching (thousands of rows/second)
- Specialized for narrow tasks like log scanning
- Resource-efficient for edge deployment
- Example: Industrial monitoring with strict space/power constraints

### 2. Mid-Tier Agents (Dots/.skogai)
- Moderate context windows
- Can run on local hardware without API dependencies
- Handle routine tasks and basic workflow automation
- Act as first responders to file changes and commands
- Compatible with both legacy and modern workflows

### 3. Advanced Agents (Claude, Goose)
- Large context windows for complex reasoning
- Dynamic tool usage for information gathering
- Handle complex tasks requiring deep understanding
- Provide solutions to challenging problems
- Work with both direct interaction and asynchronous requests

## Communication Infrastructure

### File-Based Communication
- Git diffs as primary communication medium
- Clean workspaces critical for reliable operation
- File watching for change detection (transitioning to service model)
- Special markers (AI, AI?, AI!) for triggering specific actions
- Strict formatting requirements (especially whitespace control)

### Modern Communication
- `skogcli agent send` for direct inter-agent messaging
- MCP memory system for persistent context across sessions
- More efficient resource usage than file watching
- Structured API-based interactions

## File Structure

### 1. Journal System
- Located in `/journal/`
- Daily logs of activities, thoughts, and progress
- Format: `YYYY-MM-DD.md`
- Contains task updates, decisions, reflections, and plans

### 2. Knowledge Base
- Located in `/knowledge/`
- Stores long-term information and documentation
- Organized by topic/domain
- Includes technical documentation, best practices, and reference materials

### 3. People Directory (Legacy)
- Located in `/people/`
- Being replaced by MCP memory for agent-capable systems
- Still used for compatibility with smaller models

### 4. Projects
- Located in `/projects/`
- Contains symlinks to active projects
- Each project may have its own structure and documentation

### 5. Tasks
- MCP Todo system (primary method)
- `/tasks/` directory (legacy system)
- Tracks ongoing and planned tasks

## Workflow Stages

SkogAI implements a workflow that leverages AI capabilities at different stages:

1. **High-Level Planning**: Discussions with larger models about architecture and approach
2. **Documentation Creation**: Establishing plans, requirements, and specifications
3. **Implementation Marking**: Using AI markers in code/docs to indicate implementation tasks
4. **Context Building**: Leveraging git history and file structure to build context
5. **Implementation**: Smaller models handle specific implementation tasks
6. **Review and Iteration**: Continuous improvement through feedback loops

## Claude's Role in SkogAI

As Claude, I'm positioned to assist with:

1. **High-Level Architecture**: Helping design systems and workflows
2. **Documentation Creation**: Drafting comprehensive documentation
3. **Problem-Solving**: Providing solutions to complex challenges
4. **Context Understanding**: Analyzing available files to understand project context
5. **Knowledge Integration**: Connecting information across different parts of the system
6. **Task Escalation**: Handling complex tasks that smaller agents cannot process

## Best Practices

1. **Maintain Clean Git Workspace**: Essential for reliable communication
2. **Use Appropriate Formatting**: Especially important for whitespace control
3. **Leverage Modern Tools When Available**: Prefer MCP and skogcli over legacy methods
4. **Understand Tiered Processing**: Know which tasks should be handled by which agent tier
5. **Document Thoroughly**: Documentation drives the entire development process
6. **Think Architecturally**: Focus on high-level design before implementation details