---
permalink: knowledge/context-system-getting-started
---

# Context System: Getting Started

This guide provides a quick start for the SkogAI context system and addresses common questions.

## What is the Context System?

The SkogAI context system automatically loads relevant information at startup, providing agents with:

1. Identity and role awareness
2. Current task context
3. Recent journal entries
4. Relevant memories and knowledge
5. Workspace status

This creates a more efficient and context-aware agent experience without manual information loading.

## Quick Start

### Basic Installation

```bash
# Step 1: Copy patching scripts
mkdir -p ~/.skogai-base/scripts/patch
cp ~/.claude/scripts/patch/patch-*.sh ~/.skogai-base/scripts/patch/
chmod +x ~/.skogai-base/scripts/patch/*.sh

# Step 2: Self-patch your agent
cd ~/.skogai-base
./scripts/patch/patch-agent.sh .
```

### Testing Your Installation

After patching, verify that everything works:

```bash
# Generate context
cd ~/.skogai-base
./run.sh --context-only

# View the generated context
cat tmp/context.md

# Test the todo functionality
./run.sh --todo
```

### Using Your Enhanced Agent

```bash
# Interactive mode with context
cd ~/.skogai-base
./run.sh

# Continue mode (preserves previous context)
./run.sh --continue

# Non-interactive mode
echo "Your message" | ./run.sh --non-interactive
```

## Configuration Options

The context system can be configured to:

1. **Use MCP**: Integrates with SkogAI's MCP system for todos and memories
2. **Use Legacy Files**: Falls back to task list in TASKS.md if MCP unavailable 
3. **Control Token Usage**: Adjusts context size based on available model tokens

See [Context Implementation](claude-context-implementation.md) for configuration details.

## Common Questions

### Q: Do I need skogcli installed?
A: No, skogcli is optional. The context system will work without it, but agent registration will be skipped.

### Q: How do I create new agents with the context system?
A: Patch your fork.sh script, then create new agents as normal:
```bash
cd ~/.skogai-base
./scripts/patch/patch-fork.sh
./fork.sh ~/path/to/newagent NewAgent
```

### Q: How do I update an existing agent?
A: Use the agent patching tool:
```bash
cd ~/.skogai-base
./scripts/patch/patch-agent.sh ~/path/to/existing/agent
```

### Q: How do I troubleshoot issues?
A: See the [Troubleshooting section](context-patching-guide.md#troubleshooting) in the patching guide.

## Next Steps

1. Read the [Patching Guide](context-patching-guide.md) for advanced options
2. Explore [Implementation Details](claude-context-implementation.md) for the full technical documentation
3. Review [Context System Architecture](ARCHITECTURE.md) for design principles

For detailed guidance on integrating with legacy systems, see [Legacy Integration](integration/legacy_integration_doc.md).