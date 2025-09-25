# Git Submodule Release Workflow

## Coordinated Multi-Agent Releases

The SkogAI architecture uses git submodules to enable coordinated releases across multiple agent repositories while maintaining independent development workflows.

### Release Process
1. **Individual Development**: Each agent works on feature branches in their submodule
2. **Coordinated Release Start**: `git submodule foreach git-flow release start version`
3. **Final Coordination**: Main repository updates submodule pointers
4. **Synchronized Release**: All components released together

### Benefits
- Independent agent development
- Coordinated version management
- Clean separation of concerns
- Synchronized release states

This workflow enables true multi-agent collaboration while maintaining release coordination.