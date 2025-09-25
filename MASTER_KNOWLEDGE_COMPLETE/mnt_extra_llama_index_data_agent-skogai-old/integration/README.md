# SkogAI Integration Knowledge Base

This directory contains documentation and configuration for integrating the enhanced context system with different SkogAI components.

## Files

- **agent_base_enhanced.yaml**: Configuration for the enhanced SkogAI base agent
- **skogai_simple_settings.yaml**: Simplified settings for quick integration
- **legacy_integration_steps.md**: Step-by-step guide for integrating with legacy systems
- **legacy_integration_doc.md**: Overview of legacy integration approach

## Patch Scripts

Two key patch scripts provide automated integration:

- **/context-system-patch.sh**: Patches .skogai-base with context system
- **/patch-fork.sh**: Updates fork.sh to include context system

## Usage

These files document different approaches to integration, from simple configuration to more comprehensive implementation. The primary focus is maintaining backward compatibility while adding new capabilities.

1. For existing .skogai-base, run `/context-system-patch.sh`
2. For agent forking system, run `/patch-fork.sh`
3. Follow documentation in `legacy_integration_steps.md`

## Branch Information

- **master**: Current working implementation with legacy compatibility
- **skogcli-integration**: Experimental branch for deeper skogcli integration (requires skogcli code changes)

## Related

- [Context Implementation](../claude-context-implementation.md)
- [Patching Strategy Todo](../../journal/2025-03-22-todo-patching.md)
- [Fork Patch Documentation](../fork-patch.md)
- [Patching Implementation](../../journal/2025-03-22-implementation-patching.md)
