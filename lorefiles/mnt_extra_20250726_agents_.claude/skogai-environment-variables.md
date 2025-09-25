# SkogAI Environment Variables

## Standard SkogAI Environment Variables

### Core Path Variables

```bash

# @env SKOGAI_HOME Base directory for SkogAI installation

# @env SKOGAI_DOCS Path to SkogAI documentation directory

# @env SKOGAI_TOOLS Path to SkogAI tools directory

# @env SKOGAI_CONFIG Path to SkogAI configuration directory
```

### Tool-Specific Variables

```bash

# @env SKOGAI_LOG_LEVEL Logging level (debug|info|warn|error)

# @env SKOGAI_CACHE_DIR Cache directory for temporary files

# @env SKOGAI_DATA_DIR Data storage directory
```

## Declaration Pattern

### In argc Tools:
```bash

#!/usr/bin/env bash

# @env SKOGAI_DOCS The path to SkogAI documentation directory

# @env SKOGAI_HOME Base directory for SkogAI installation

# Use variables directly - argc handles validation
cat "$SKOGAI_DOCS/$argc_document"
```

### In Python Tools:
```python
import os

# With fallback defaults
SKOGAI_DOCS = os.environ.get('SKOGAI_DOCS', '/home/skogix/SkogAI/docs')
SKOGAI_HOME = os.environ.get('SKOGAI_HOME', '/home/skogix/SkogAI')
```

## Why Environment Variables Matter

### 1. Multi-Agent Compatibility
Different agents work from different directories:
- Claude: `/home/skogix/SkogAI/.claude`
- Librarian: `/home/skogix/skogai/tools/agents/librarian`
- User: `/home/skogix/SkogAI`

### 2. Deployment Flexibility
Tools work across different:
- Development environments
- Production deployments
- Container configurations
- User setups

### 3. Security
- No hardcoded paths in source code
- Configuration separate from code
- Easy to audit and change

## Real Implementation Example

### Before (hardcoded):
```bash

# Only works in one specific context
ls -la "/home/skogix/SkogAI/docs/official"
cat "/home/skogix/SkogAI/docs/official/$document"
```

### After (environment-aware):
```bash

# @env SKOGAI_DOCS The path to SkogAI documentation directory

# Works across all contexts
ls -la "$SKOGAI_DOCS"
cat "$SKOGAI_DOCS/$document"
```

## Configuration Management

### Setting Variables

```bash

# In ~/.bashrc or environment setup
export SKOGAI_HOME="/home/skogix/SkogAI"
export SKOGAI_DOCS="$SKOGAI_HOME/docs/official"
export SKOGAI_TOOLS="$SKOGAI_HOME/tools"
export SKOGAI_CONFIG="$HOME/.config/skogai"
```

### In .envrc (direnv):
```bash

# Auto-loaded when entering directory
export SKOGAI_HOME="$(pwd)"
export SKOGAI_DOCS="$SKOGAI_HOME/docs/official"
export SKOGAI_TOOLS="$SKOGAI_HOME/tools"
```

### In Docker/Containers:
```dockerfile
ENV SKOGAI_HOME=/opt/skogai
ENV SKOGAI_DOCS=/opt/skogai/docs/official
ENV SKOGAI_TOOLS=/opt/skogai/tools
```

## Validation Pattern

### Check Required Variables:
```bash

# Simple validation
: "${SKOGAI_DOCS:?SKOGAI_DOCS environment variable must be set}"

# Or with argc @env - framework handles validation automatically
```

## Benefits

1. **Cross-context compatibility** - Tools work for all agents
2. **Easy configuration** - Change paths without code changes
3. **Development flexibility** - Different setups for different users
4. **Production readiness** - Container and deployment friendly
5. **Security** - No sensitive paths in source code
6. **Documentation** - @env declarations show dependencies

Following this pattern ensures SkogAI tools work consistently across the entire ecosystem.