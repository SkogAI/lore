# SkogAI External Dependency Mapping

## Problem Statement

When migrating to a new SkogAI structure, tools may have dependencies on the old file system layout that need to be identified and addressed.

## Discovery Method

### 1. Search for Hardcoded Paths
```bash

# Find files with hardcoded SkogAI paths
git grep -r "/home/skogix/SkogAI" --exclude-dir=.git
rg "/home/skogix/SkogAI" --type-not=binary
```

### 2. Check Configuration Files
```bash

# Look in common config locations
find ~/.config -name "*.py" -o -name "*.sh" | xargs grep -l "SkogAI"
```

### 3. Analyze Integration Scripts
Look for scripts that bridge between different parts of the system.

## Real Example: SkogCLI Integration

### External Dependency Found:
- **File**: `/home/skogix/.config/skogcli/misc/docs.py`
- **Dependency**: Hardcoded path to `/home/skogix/SkogAI/docs/democracy/`
- **Impact**: SkogCLI docs commands fail when this directory doesn't exist in expected location

### Code Pattern:
```python

# In /home/skogix/.config/skogcli/misc/docs.py
docs_path = "/home/skogix/SkogAI/docs/democracy/"  # Hardcoded external dependency
```

## Dependency Classification

### Types of External Dependencies:

1. **Configuration Files** - Tools with hardcoded paths in config
2. **Integration Scripts** - Bridge scripts between different systems
3. **Symlinks** - Symbolic links pointing to external locations
4. **Data Directories** - Required data outside new structure
5. **Submodules** - Git submodules pointing to external repos

## Resolution Strategies

### 1. Environment Variables
Replace hardcoded paths with configurable environment variables:
```bash
docs_path = os.environ.get('SKOGAI_DOCS', '/home/skogix/SkogAI/docs/democracy/')
```

### 2. Migration
Move dependencies into new structure and update references.

### 3. Symlinks
Create symlinks from new location to maintain compatibility:
```bash
ln -s /home/skogix/SkogAI/docs/democracy/ ./docs/democracy
```

### 4. Configuration Management
Use configuration files instead of hardcoded paths.

## Documentation Pattern

For each external dependency found:

1. **Location** - Where the dependency is defined
2. **Target** - What external path/resource it depends on
3. **Impact** - What breaks if dependency is missing
4. **Resolution** - How to address the dependency

This systematic approach ensures no dependencies are missed during system migrations or restructuring.