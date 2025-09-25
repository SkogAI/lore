# Tool Reality Model: Understanding SkogAI's Abstraction Layer

## Core Concept

The SkogAI system maintains multiple parallel "realities" that must remain synchronized for the system to function correctly:

1. **Filesystem Reality**: The actual files on disk
2. **Git Reality**: Changes tracked by version control
3. **SkogAI Reality**: The abstraction layer's model of the workspace
4. **Validation Reality**: The pre-commit validation system's view

These realities only remain consistent when proper SkogAI tools are used exclusively for file operations.

## Tool Operations vs. Direct Operations

### SkogAI Tools (append, save, patch)

When using proper SkogAI tools:
- Changes are tracked in the SkogAI abstraction layer
- The system maintains a consistent model of the workspace
- Pre-commit validation can accurately assess changes
- Git operations work as expected

```
User → SkogAI Tool → Abstraction Layer → Filesystem + Git
                                       → Pre-commit Cache
```

### Direct Shell Commands (echo, sed, rm)

When using direct shell commands:
- Changes bypass the SkogAI abstraction layer
- The system's model becomes inconsistent with reality
- Pre-commit validation may fail in unexpected ways
- Git operations may behave unpredictably

```
User → Shell Command → Filesystem
      ↓
      X (Abstraction Layer not updated)
```

## Consequences of Reality Divergence

When realities diverge due to improper tool usage:

1. **Ghost Changes**: Changes exist in the filesystem but not in SkogAI's model
2. **Validation Failures**: Pre-commit hooks detect inconsistencies but can't properly identify their source
3. **Patch Failures**: Patch operations fail because the system can't find content that exists in the actual file
4. **Persistent Inconsistencies**: Some divergences can never be fully reconciled

## The Pre-commit Cache System

The system uses a sophisticated caching mechanism:
- Located at `~/.cache/pre-commit/`
- Creates isolated environments for validating changes
- Maintains parallel "fake git trees" for each operation
- Only allows changes to reach the main repository if they pass validation

This architecture provides safety through isolation but depends on consistent state tracking.

## Best Practices

To maintain system integrity:

1. **Use Proper Tools Exclusively**:
   - `append` for adding content to files
   - `save` for creating or replacing files
   - `patch` for targeted modifications

2. **Avoid Direct Filesystem Operations**:
   - Don't use `echo`, `sed`, or other shell commands for file manipulation
   - These create permanent inconsistencies between realities

3. **Understand Tool Semantics**:
   - `append` generates a diff that adds content to the end of a file
   - `save` generates a diff that replaces/creates an entire file
   - `patch` generates a diff that modifies specific sections of a file

4. **Respect Validation Feedback**:
   - Pre-commit validation errors indicate reality divergence
   - Fix issues using proper SkogAI tools, not direct commands

## Practical Implications

The SkogAI system provides:
- **Safety**: Changes are validated before reaching the repository
- **Quality Control**: Only valid content is committed
- **Flexibility**: Valid files can be committed even when others have issues

But this only works when the system's model of reality remains consistent with the actual filesystem, which requires exclusive use of proper SkogAI tools for all file operations.

## Conclusion

The SkogAI abstraction layer creates a sophisticated model of reality that enables powerful capabilities, but this model is fragile. Using improper tools creates permanent "ghosts in the machine" - inconsistencies that can never be fully reconciled. Understanding this architecture is essential for maintaining system integrity and ensuring predictable behavior.
