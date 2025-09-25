# SkogFlow Quick Reference

## Essential Commands

### Feature Development
```bash
git flow feature start my-feature      # Start new feature
git flow feature publish my-feature    # Share with other agents
git flow feature finish my-feature     # Merge to develop
```

### Release Coordination
```bash

# Coordinated release across all submodules
git submodule foreach git-flow release start skogai-0.4
git submodule foreach git-flow release publish skogai-0.4
git submodule foreach git-flow release finish skogai-0.4
```

### Collaboration
```bash
git flow feature track other-feature   # Track another agent's work
git flow log                          # See what's new since master
git flow feature pull origin feature  # Pull updates from remote
```

### Emergency Fixes
```bash
git flow hotfix start critical-fix     # Emergency fix to production
git flow hotfix finish critical-fix   # Deploy fix immediately
```

## Branch Overview
- **master**: Production (tagged releases)
- **develop**: Next release integration
- **feature/**: Individual development
- **release/**: Release preparation
- **hotfix/**: Emergency production fixes

## Multi-Agent Workflow
1. **Individual Work**: Feature branches in personal submodule
2. **Collaboration**: Publish features for cross-agent review
3. **Integration**: Features merge to develop
4. **Coordination**: Synchronized releases across ecosystem
5. **Distribution**: Tagged releases for public consumption

## Status Checking
```bash
git status                            # Local repository status
git submodule foreach git status      # All submodule status
git submodule foreach git branch      # Branch status across ecosystem
git flow feature                      # Active feature branches
```

## Best Practices
- ✅ **Descriptive commits**: Clear messages with SkogAI context
- ✅ **Regular publishing**: Share work early and often
- ✅ **Clean features**: Focused, atomic feature development
- ✅ **Coordinated releases**: Use ecosystem-wide release process
- ✅ **Democratic participation**: Engage in governance during releases

This is the foundation for 50+ agent collaboration! 🚀