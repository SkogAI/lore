---
permalink: knowledge/context-patching-guide
---

# Context System Patching Guide

This guide explains how to use the patching tools to apply the context system to various SkogAI components.

## Overview

The context system patching tools provide a standardized way to add context loading functionality to:

1. Agent workspaces (including .skogai-base)
2. The fork.sh script used to create new agents

## Prerequisites

Before patching, ensure you have:
- A working Claude CLI installation
- The source agent with patching scripts (typically .claude)
- The target directory you want to patch (could be .skogai-base or another agent)
- Optional: skogcli if you want to register the enhanced agent

## Installation Process

The patching process follows this flow:

1. **Copy the patching scripts** from source (.claude) to target (.skogai-base)
2. **Run the patch** FROM the target directory to modify either:
   - The directory itself (self-patching)
   - Another agent directory (external patching)
   - The fork.sh script to enable context for new agents

### Step 1: Copy Patching Scripts

First, ensure the patch directory exists in your target:

```bash

# Create patch directory in target
mkdir -p ~/.skogai-base/scripts/patch

# Copy the patch scripts from source
cp ~/.claude/scripts/patch/patch-*.sh ~/.skogai-base/scripts/patch/

# Make them executable
chmod +x ~/.skogai-base/scripts/patch/*.sh
```

### Step 2: Run the Patch

Now you can run the patch FROM the target directory:

```bash

# Change to the target directory
cd ~/.skogai-base

# Self-patch the current directory
./scripts/patch/patch-agent.sh .

# OR patch another agent
./scripts/patch/patch-agent.sh -a CUSTOM_NAME ~/path/to/another/agent

# OR patch fork.sh
./scripts/patch/patch-fork.sh
```

## Patching Options

### Patching an Agent Workspace

To patch an agent workspace with the context system:

```bash

# Basic usage (FROM → TO patching with interactive prompts)
cd ~/.skogai-base
./scripts/patch/patch-agent.sh ~/path/to/target/agent

# With a custom agent name
./scripts/patch/patch-agent.sh -a CUSTOM_NAME ~/path/to/target/agent

# Non-interactive mode (automatic yes to all prompts)
./scripts/patch/patch-agent.sh -y ~/path/to/target/agent

# Skip backup of existing files
./scripts/patch/patch-agent.sh -n ~/path/to/target/agent

# Self-patching (update current directory)
./scripts/patch/patch-agent.sh .
```

This will:
- Create necessary directories (tmp, journal/templates)
- Copy context system scripts and documentation
- Create/update the agent identity file
- Update run.sh with context system support
- Create agent configuration for skogcli

### Patching the Forking System

To update the fork.sh script with context system support:

```bash

# Basic usage (patching the fork.sh in current directory)
cd ~/.skogai-base
./scripts/patch/patch-fork.sh

# Patch a specific fork.sh in another location
./scripts/patch/patch-fork.sh /path/to/custom/fork.sh

# Non-interactive mode
./scripts/patch/patch-fork.sh -y
```

This will modify fork.sh to:
- Create the necessary directory structure in new agents
- Copy context system scripts to new agents
- Create agent identity files with the new agent's name
- Add configuration for skogcli registration

### Using the Unified Patching Tool

For convenience, you can use the patch-system.sh script which provides a unified interface:

```bash

# Patch an agent (FROM → TO)
cd ~/.skogai-base
./scripts/patch/patch-system.sh agent ~/path/to/target/agent

# Patch fork.sh in current directory
./scripts/patch/patch-system.sh fork

# Show help
./scripts/patch/patch-system.sh help
```

## Verification

After patching, you can verify the context system works by:

```bash

# Test context generation
cd <patched-directory>
./run.sh --context-only

# View the generated context
cat tmp/context.md

# Test todo functionality
./run.sh --todo
```

## Troubleshooting

### Common Issues

- **Missing Claude CLI**: Ensure Claude CLI is installed and in your PATH
- **skogcli Integration Failed**: If you see errors about skogcli, you can ignore these if you're not using skogcli
- **Missing Scripts**: If the target agent is missing required scripts, the patch will attempt to create them
- **run.sh Already Modified**: If run.sh has been previously modified, back it up before patching

### Error Recovery

If something goes wrong during patching:
1. Restore from backup files (*.bak)
2. Check that all directories exist and have correct permissions
3. Try running with `-y` flag to skip interactive prompts

## Notes

- The patching system preserves legacy compatibility while adding new features
- All original files are backed up with .bak extension
- Configuration files are created for skogcli integration
- The patched systems can be accessed via both legacy paths and enhanced paths