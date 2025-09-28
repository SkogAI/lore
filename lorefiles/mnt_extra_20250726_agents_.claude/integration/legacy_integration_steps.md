---
permalink: knowledge/integration/legacy-integration-steps
---

# SkogAI Base Enhancement Steps

> **IMPORTANT**: The more advanced integration approach is available in the `skogcli-integration` branch, which contains deeper integration with skogcli (requiring skogcli code changes). This document covers the immediately implementable approach.

## 1. Apply the Context System Patch

```bash

# From the .claude directory
./context-system-patch.sh
```

This creates all the necessary scripts in `.skogai-base` but preserves legacy run.sh until reviewed.

## 2. Review and Apply run.sh Changes

```bash

# In the .skogai-base directory
diff -u run.sh run.sh.new
mv run.sh.new run.sh
chmod +x run.sh
```

## 3. Register the Enhanced Agent

```bash

# Add the enhanced agent configuration
skogcli settings add-file agent_base_enhanced agent_base_enhanced.yaml
```

## 4. Test Functionality

Basic tests:
```bash

# Test context-only functionality (should work)
cd /home/skogix/.skogai-base && ./run.sh --context-only

# Test todo functionality (should work)
cd /home/skogix/.skogai-base && ./run.sh --todo
```

## 5. Usage

The enhanced agent can be used normally with skogcli:

```bash

# Chat with enhanced base agent
skogcli agent chat skogai_base_enhanced

# Send a message to enhanced base agent
skogcli agent send skogai_base_enhanced "Your message"
```

Both legacy and enhanced functionality should work simultaneously - the old agent config continues to work with legacy features, while the new agent config enables enhanced functionality.

## Note on Differences

- `agent_base.yaml`: Legacy configuration (context_system: false)
- `agent_base_enhanced.yaml`: Enhanced configuration (context_system: true)

Both point to the same directory (.skogai-base) but signal different usage patterns.
