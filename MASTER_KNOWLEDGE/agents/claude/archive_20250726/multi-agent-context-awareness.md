# Multi-Agent Context Awareness

## The Problem with Hardcoded Paths

Different agents and users work from different directories in the SkogAI ecosystem, making hardcoded paths break across contexts.

## Context Mapping

### Working Directories by Agent/User

- **Claude Assistant**: `/home/skogix/SkogAI/.claude`
- **User (skogix)**: `/home/skogix/SkogAI`
- **Librarian Agent**: `/home/skogix/skogai/tools/agents/librarian`
- **Other Tools**: Various symlinked directories

### Why Hardcoded Paths Fail

```bash

# This only works from one specific context
cat "/home/skogix/SkogAI/docs/official/$document"
```

When the librarian agent runs this from its working directory with symlinked folders, the path resolution fails.

## Solution: Environment Variables

### Proper Approach

```bash

# @env SKOGAI_DOCS The path to SkogAI documentation directory
cat "$SKOGAI_DOCS/$document"
```

### Benefits

1. **Context Independence** - Works from any working directory
2. **Symlink Compatibility** - Resolves correctly through symlinks
3. **Agent Flexibility** - Each agent can set appropriate paths
4. **Configuration Transparency** - @env declarations document expectations

## Real Example

### Before (context-dependent):
```bash

# Only works for Claude assistant in .claude directory
ls -la "/home/skogix/SkogAI/docs/official"
```

### After (context-aware):
```bash

# @env SKOGAI_DOCS The path to SkogAI documentation directory
ls -la "$SKOGAI_DOCS"
```

## Implementation Pattern

1. **Identify all hardcoded paths** in tools
2. **Replace with environment variables** using descriptive names
3. **Add @env declarations** documenting what each variable should contain
4. **Test across different agent contexts** to verify compatibility

This ensures tools work consistently whether called by Claude, the user, librarian agent, or any other context in the SkogAI ecosystem.