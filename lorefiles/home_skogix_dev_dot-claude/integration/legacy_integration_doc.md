---
permalink: knowledge/integration/legacy-integration-doc
---

# SkogAI Legacy Integration

## Current Approach

For now, we'll use a simple settings-based approach with existing skogcli functionality:

1. Add `legacy_compatible: true` flag to agent settings
2. Add `context_system: true` flag to indicate the agent has enhanced context

## Usage with Current Tools

Using what exists today:

```bash
# Install the settings
skogcli settings add-file skogai_base skogai_simple_settings.yaml

# Chat with the agent
skogcli agent chat skogai_base

# Send a message
skogcli agent send skogai_base "Your message"
```

## Scripts Detect Legacy Mode

In the enhanced scripts at `.skogai-base`, we've maintained legacy compatibility:

1. `run.sh` supports both new flags and legacy mode
2. `scripts/context-enhanced.sh` fallbacks to legacy context script
3. All new features are optional and non-destructive

## Future Consideration (After Validation)

Once this approach is validated, we could consider:

1. Adding explicit context commands to the skogcli tool
2. Implementing a centralized context management system
3. Creating a formal API for context interaction between agents

For now, the primary goal is to maintain compatibility while adding the new context capabilities in a way that works with existing tools.
