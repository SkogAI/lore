---
permalink: knowledge/forking-workspace
---

# Workspace Structure for Forkable Agents

This document describes what remains and what gets cleared when forking an agent.

## Directory Structure Overview

```tree
.
├── README.md               # Overview (template remains, content updated)
├── ABOUT.md               # Agent identity (cleared and customized)
├── ARCHITECTURE.md        # System architecture (remains)
├── TOOLS.md               # Tool integrations (remains)
├── gptme.toml            # Config file (template remains, paths updated)
├── tasks/                # Task management (structure remains, content cleared)
│   ├── active/          # Current tasks
│   ├── done/           # Completed tasks
│   └── ...             # Other task states
├── journal/             # Daily logs (cleared)
│   └── templates/      # Journal templates (preserved)
├── knowledge/           # Knowledge base (partially preserved)
│   ├── ai/             # Technical knowledge (preserved)
│   ├── integration/    # Integration documentation (preserved)
│   └── ...             # Other knowledge (evaluated per-file)
├── people/             # Relationships (cleared except templates & creator)
├── projects/           # Project links (cleared)
├── scripts/            # System scripts (preserved and enhanced)
│   ├── context-*.sh   # Context loading scripts (preserved)
│   └── ...            # Other utility scripts
└── tmp/                # Temporary files (cleared, directory preserved)
    └── context.md     # Generated context file (cleared)
```

## What Stays

1. **System Structure**
   - Directory layout
   - Task management system
   - Documentation templates
   - Tool configurations
   - Context loading scripts

2. **Core Documentation**
   - ARCHITECTURE.md
   - Technical designs
   - Tool integration guides
   - Best practices
   - Context implementation docs

3. **Technical Knowledge**
   - AI/ML concepts
   - System architecture
   - Tool usage patterns
   - Context efficiency techniques
   - Integration documentation

## What Gets Cleared

1. **Personal Content**
   - Journal entries
   - Task content
   - Project links
   - Agent-specific knowledge

2. **Identity**
   - ABOUT.md
   - Visual identity
   - Social media presence
   - Personal profile

3. **Relationships**
   - People profiles (except creator)
   - Interaction history

## Fork Creation Steps

1. Copy workspace structure
2. Clear personal content
3. Initialize new identity
4. Update configurations
5. Configure context system
6. Create first task

For detailed forking process, see [`agent-forking.md`](./agent-forking.md).

## Context System Configuration

When forking an agent, consider these context system settings:

1. **Legacy Compatibility**
   - Set `legacy_compatible` flag in agent settings
   - Update references in context scripts if needed
   - Ensure backward compatibility with existing tools

2. **Context Structure**
   - Configure what information appears in context
   - Set priority order for context elements
   - Configure token usage limits

3. **Integration**
   - Register with `skogcli` if appropriate
   - Set `context_system: true` for enhanced agents
   - Configure appropriate chat and inbox commands

See [`integration/README.md`](./integration/README.md) for more details on integration approaches.