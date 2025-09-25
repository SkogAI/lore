# SkogAI System Architecture

## Overview

The SkogAI system is built with multiple layers of abstraction, providing a secure and flexible framework for AI agents to interact with the system and external tools. This document outlines the key components and how they work together.

## System Layers

### 1. User Interfaces

The top layer consists of various user interfaces that allow humans to interact with AI agents:

- **gptme**: A command-line interface for interacting with LLMs like GPT-4
- **aichat**: A flexible chat interface that supports different roles and models
- **Custom UIs**: Web interfaces, CLI tools, and other specialized interfaces

### 2. Agent Layer

This layer contains the various AI agents that can be deployed:

- **dot**: The original SkogAI agent (this agent)
- **Specialized agents**: Purpose-built agents for specific tasks
- **Agent family**: A coordinated ecosystem of agents that work together

### 3. Tool Management Layer

This layer manages the tools that agents can use:

- **argc**: A command-line tool that routes commands to appropriate tools and agents
- **Tool declarations**: JSON specifications of tool capabilities and parameters
- **Agent declarations**: Specifications of agent capabilities

### 4. MCP Bridge Layer

The Model-Code-Proxy (MCP) Bridge provides a standardized API for accessing tools:

- **MCP Bridge API**: HTTP API running on localhost (typically port 8808)
- **Tool endpoints**: Each tool is exposed as an endpoint (`/tools/:name`)
- **Security controls**: Permissions and access controls for tools

### 5. Tool Implementation Layer

The lowest layer consists of the actual tool implementations:

- **Filesystem tools**: For reading, writing, and manipulating files
- **Memory tools**: For storing and retrieving information
- **Todo tools**: For task management
- **Markdownify tools**: For converting various formats to markdown
- **Web search tools**: For retrieving information from the internet
- **And many more specialized tools**

## Security Model

The system employs several security measures:

1. **Layered access**: Tools are accessed through multiple layers, each with its own security checks
2. **Directory restrictions**: Filesystem tools are limited to specific allowed directories
3. **Confirmation prompts**: Potentially dangerous operations require explicit confirmation
4. **Tool declarations**: Tools explicitly declare their capabilities and required permissions
5. **Sandboxing**: Tools run in controlled environments with limited system access

## Communication Flow

When an agent wants to use a tool:

1. The agent makes a request through its interface (e.g., gptme)
2. The request is routed through the tool management layer (argc)
3. The MCP Bridge receives the request via HTTP
4. The appropriate tool is executed with the provided parameters
5. Results are returned through the same path back to the agent

## Agent Family Concept

The SkogAI ecosystem is designed around an "agent family" concept:

1. **Specialized roles**: Different agents have specific capabilities and responsibilities
2. **Coordination**: Agents can communicate and coordinate with each other
3. **Shared resources**: Agents can access shared knowledge bases and tools
4. **Complementary strengths**: Agents with different models or capabilities work together

## Tags
tags: [architecture, security, tools, agents, mcp]
created: 2025-03-26
updated: 2025-03-26
