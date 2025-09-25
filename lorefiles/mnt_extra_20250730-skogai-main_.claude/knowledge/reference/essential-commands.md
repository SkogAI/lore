# Essential Commands Reference

## Git Flow (ALWAYS use scripts)
```bash
./scripts/git/stage.sh <file>           # Stage specific file
./scripts/git/feature-start.sh <name>   # Start feature branch
./scripts/git/feature-finish.sh         # Finish feature branch
./scripts/git/current-feature.sh        # Show current feature
git commit -m "message"                 # Commit with proper format
```

## Serena Memory Management
```bash
mcp__serena__list_memories              # List available memories
mcp__serena__read_memory <name>         # Read specific memory
mcp__serena__write_memory <name>        # Create new memory
mcp__serena__get_current_config         # Show current Serena config
```

## Knowledge Base Queries
```bash
echo "[@rag:claude-home:query]" | skogparse --execute
echo "[@amys-blog:message]" | skogparse --execute  
echo "[@goose:query]" | skogparse --execute
```

## Context and State
```bash
./scripts/update-context.sh            # Regenerate context
./run                                   # Entry point for sessions
cat ./tmp/context.md                    # Current context snapshot
```

## File Organization Patterns
- `./state/` - Immutable session state
- `./tmp/` - Temporary files and context
- `./scripts/` - All operations via scripts
- `./knowledge/` - Long-term reference
- `./.claude/skogai/` - Core principle files

## Plan Management
- `plan.md` - Organized in batches, simple task lists
- Batch 1 (Critical) → Batch 6 (Specific tasks)
- Keep explanatory content in knowledge/ files
- Use checkbox format for smaller agent compatibility