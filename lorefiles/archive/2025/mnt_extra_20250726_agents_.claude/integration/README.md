---
permalink: knowledge/integration/readme
---

# SkogAI Integration Knowledge Base

This directory contains documentation and configuration for integrating the enhanced context system with different SkogAI components.

## Files

- **agent_base_enhanced.yaml**: Configuration for the enhanced SkogAI base agent
- **skogai_simple_settings.yaml**: Simplified settings for quick integration
- **legacy_integration_steps.md**: Step-by-step guide for integrating with legacy systems
- **legacy_integration_doc.md**: Overview of legacy integration approach

## Patching System

A comprehensive patching system is now available in the `scripts/patch/` directory:

- **scripts/patch/patch-system.sh**: Unified patching tool
- **scripts/patch/patch-agent.sh**: Patches agent directories with context system
- **scripts/patch/patch-fork.sh**: Updates fork.sh to include context system

## Usage

For patching your agents and systems:

```bash

# Patch an agent:
./scripts/patch/patch-agent.sh ~/.skogai-base

# Patch fork.sh:
./scripts/patch/patch-fork.sh

# Using the unified tool:
./scripts/patch/patch-system.sh agent ~/.skogai-base
./scripts/patch/patch-system.sh fork
```

## Branch Information

- **master**: Current working implementation with legacy compatibility
- **skogcli-integration**: Experimental branch for deeper skogcli integration (requires skogcli code changes)

## Related

- [Context Implementation](../claude-context-implementation.md)
