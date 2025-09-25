# Git-Flow Usage in SkogAI Multi-Submodule Environment

## Overview

SkogAI employs a sophisticated git workflow using git-flow across a complex system of 50-100+ submodules. This document explains how this system works, best practices, and common patterns for AI agents working in this environment.

## Core Concepts

### Submodule Structure

The SkogAI system consists of:
- A main repository (`SkogAI/SkogAI`)
- Multiple first-level submodules (including `.goose`)
- Second-level submodules within those repositories
- Potentially more nested levels

This structure allows modular development with specialized components while maintaining overall system coherence.

### Git-Flow Methodology

[Git-Flow](https://nvie.com/posts/a-successful-git-branching-model/) provides a structured branching strategy:
- `master` branch contains production code
- `develop` branch for ongoing development
- `feature/*` branches for new features
- `release/*` branches for release preparation
- `hotfix/*` branches for urgent fixes

All changes follow this flow: feature → develop → release → master → (hotfix if needed)

### Propagating Commands Across Submodules

The power of the SkogAI git workflow comes from the ability to propagate git-flow commands across all submodules at once:

```bash
# Apply the same command to all submodules
git submodule foreach git flow feature start my-feature

# Make changes to each submodule
git submodule foreach 'echo "Change" > file.txt && git add file.txt && git commit -m "Add file"'

# Finish the feature in all submodules
git submodule foreach git flow feature finish my-feature
```

This approach allows for coordinated changes across dozens of repositories with minimal commands.

## Best Practices for AI Agents

### DO:

1. **Use git-flow commands**: Always use `git flow` commands rather than raw git commands
   ```bash
   # Good
   git flow feature start my-feature
   
   # Avoid
   git checkout -b feature/my-feature develop
   ```

2. **Propagate across submodules**: Use `git submodule foreach` to apply changes consistently
   ```bash
   git submodule foreach git flow feature start agent-improvement
   ```

3. **Make atomic commits**: Keep changes focused and related
   ```bash
   # Instead of one big commit
   git submodule foreach 'git commit -am "Fix everything"'
   
   # Make specific commits
   git submodule foreach 'git add specific-file.txt && git commit -m "Fix specific issue"'
   ```

4. **Respect branch naming conventions**: Follow established patterns
   ```bash
   git flow feature start feature-name  # Creates feature/feature-name
   ```

### DON'T:

1. **Don't use raw git commands** for operations that should use git-flow
   ```bash
   # Avoid
   git merge feature/my-feature
   
   # Use instead
   git flow feature finish my-feature
   ```

2. **Don't commit directly to master or develop**
   ```bash
   # Avoid
   git checkout develop && git commit -m "Quick fix"
   ```

3. **Don't force push or rebase public branches**
   ```bash
   # Avoid
   git push --force origin develop
   ```

4. **Don't make massive changes without coordination**
   ```bash
   # Avoid
   find . -type f -exec sed -i 's/oldterm/newterm/g' {} \;
   ```

## Safety Mechanisms

The SkogAI git system has built-in safety mechanisms:

1. **Automatic reverting**: Problematic changes may be automatically reverted
2. **Branch protection**: Critical branches (master, develop) have protection rules
3. **Review requirements**: Changes require proper review before integration
4. **Consistency checks**: The system verifies changes don't break submodule relationships

## Common Workflows for AI Agents

### 1. Starting a New Feature

```bash
# Start the feature in all relevant submodules
git submodule foreach git flow feature start feature-name

# Make changes to necessary files
cd submodule
echo "Changes" >> file.txt
git add file.txt
git commit -m "Add changes for feature"

# Optional: Push feature branch for collaboration
git flow feature publish feature-name

# Finish feature when complete
git flow feature finish feature-name

# Push changes to remote
git push
```

### 2. Preparing a Release

```bash
# Start a release
git submodule foreach git flow release start v1.0.0

# Make final adjustments
cd submodule
sed -i 's/VERSION = "0.9.9"/VERSION = "1.0.0"/' version.py
git add version.py
git commit -m "Bump version to 1.0.0"

# Finish the release
git submodule foreach git flow release finish v1.0.0

# Push changes including tags
git submodule foreach "git push && git push --tags"
```

### 3. Viewing Changes Across Submodules

```bash
# View status of all submodules
git submodule foreach git status

# View differences between branches
git submodule foreach git flow feature diff

# Generate comprehensive diff
git submodule foreach git diff > /tmp/all-changes.diff
```

## Token Management

When working with large submodule structures, be aware of token limitations:

1. A full diff across all submodules may exceed 180k+ tokens
2. Use tools like `skogcli script run token` to measure content size
3. Focus on reviewing specific components rather than the entire change set

## Role of AI Agents

AI agents working in the SkogAI ecosystem typically:

1. Review specific changes rather than the entire codebase
2. Provide input on focused aspects of development
3. Help coordinate between different components
4. Document changes and decisions
5. Follow established git workflows rather than inventing new processes

## Final Recommendations

1. **Start small**: Begin with targeted changes to specific submodules
2. **Learn the patterns**: Observe how changes propagate through the system
3. **Follow established practices**: Use the same workflows as other agents
4. **Document your actions**: Keep clear records of what changed and why
5. **Ask for guidance**: When unsure, seek clarification rather than guessing

---

Last updated: 2025-06-11