# Worktree-Todo Setup Branch

This branch contains the complete worktree-todo parallel async work system for the lore project.

## What's Included

### 1. Todo System Infrastructure

- **`todos/`** - Directory for tracking work items
- **`assets/todo-template.md`** - Template for creating new todos
- **Example todos** - 3 example todos demonstrating different statuses and priorities

### 2. Management Tools

- **`tools/worktree-todo-manager.sh`** - Main management script
  - `batch` - Create worktrees for all ready todos
  - `select` - Interactive single worktree creation
  - `status` - View all worktree-todo mappings
  - `complete <id>` - Complete a todo (status, lore, cleanup)

### 3. Documentation

- **`docs/WORKTREE_TODO_SYSTEM.md`** - Comprehensive guide
  - Architecture overview
  - Setup instructions
  - Usage examples
  - Integration with lore system
  - Troubleshooting

### 4. Mapping System

- **`.worktree-todo-mapping.json`** - Tracks todo → worktree relationships
  - Issue ID → worktree name
  - Priority and status tracking
  - Creation and completion timestamps

## Quick Start

```bash
# 1. Test the system with example todos
./tools/worktree-todo-manager.sh status

# 2. Create worktrees for ready examples
./tools/worktree-todo-manager.sh batch

# 3. View what was created
./tools/worktree-todo-manager.sh status
git worktree list

# 4. Clean up examples
./tools/worktree-todo-manager.sh complete 001
./tools/worktree-todo-manager.sh complete 002
```

## Merging to Main

This branch contains:

1. **New directories**: `todos/`, `assets/`
2. **New tools**: `tools/worktree-todo-manager.sh`
3. **Documentation**: `docs/WORKTREE_TODO_SYSTEM.md`
4. **Example todos**: 3 example files (can be deleted after merge)

To merge:

```bash
# Switch to main branch
cd /home/skogix/lore  # Main repo
git checkout master

# Merge this branch
git merge worktree-setup

# Delete example todos if desired
rm todos/00{1,2,3}-*.md

# Commit and push
git commit -m "Add worktree-todo parallel async work system"
git push origin master
```

## Features

✅ **Batch Creation** - Create all worktrees at once from ready todos
✅ **Status Tracking** - Track which todo corresponds to which worktree
✅ **Lore Integration** - Auto-generate lore entries from completed work
✅ **Auto-Cleanup** - Remove worktrees after completion
✅ **Dependencies** - Track blockers and sequence work
✅ **Priority Management** - p1/p2/p3 priorities with filtering
✅ **Interactive Mode** - Select specific todos to work on

## Integration Points

- **skogai-todos** - File-based todo tracking system
- **git worktrees** - Isolated work environments
- **lore-flow.sh** - Narrative documentation generation
- **persona-mapping** - Author → persona for lore entries

## Next Steps

1. Read `docs/WORKTREE_TODO_SYSTEM.md` for full documentation
2. Create real todos for your work
3. Use `batch` to create worktrees
4. Work in parallel across multiple todos
5. Use `complete` to finish with full workflow

## Files Added

```
assets/
  todo-template.md              # Template for new todos

todos/
  001-ready-p1-example-implement-feature.md
  002-ready-p2-example-refactor-code.md
  003-pending-p3-example-documentation.md

tools/
  worktree-todo-manager.sh      # Main management script

docs/
  WORKTREE_TODO_SYSTEM.md       # Comprehensive documentation
```

## Author

Created by Claude Code on 2025-12-26 in the worktree-setup worktree.

This system enables true parallel async development by combining file-based todo tracking with git worktrees and automated lore documentation.
