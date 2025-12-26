# Worktree-Todo System - Quick Start

## 5-Minute Setup

### 1. View Example Todos

```bash
ls -la todos/
# You'll see:
# 001-ready-p1-example-implement-feature.md
# 002-ready-p2-example-refactor-code.md
# 003-pending-p3-example-documentation.md
```

### 2. Check Status

```bash
./tools/worktree-todo-manager.sh status
# Shows: No mappings found (nothing created yet)
```

### 3. Create Worktrees for Ready Todos

```bash
./tools/worktree-todo-manager.sh batch
# Creates worktrees for todos 001 and 002 (ready status)
# Todo 003 is skipped (pending status)
```

### 4. View Created Worktrees

```bash
git worktree list
# Shows all worktrees including:
# - .worktrees/todo-001-example-implement-feature
# - .worktrees/todo-002-example-refactor-code
```

### 5. Work in a Worktree

```bash
cd .worktrees/todo-001-example-implement-feature
# Make changes, commit
git add .
git commit -m "Implement feature"
cd ../..
```

### 6. Complete the Todo

```bash
./tools/worktree-todo-manager.sh complete 001
# This will:
# 1. Update todo status (ready → complete)
# 2. Generate lore entry from commits
# 3. Update mapping
# 4. Ask to cleanup worktree
```

## Real-World Usage

### Creating Your First Real Todo

```bash
# 1. Copy template
cp assets/todo-template.md todos/004-pending-p1-my-real-task.md

# 2. Edit the todo file
# - Fill in Problem Statement
# - Add Proposed Solutions
# - Set Acceptance Criteria
# - Update YAML: issue_id: "004"

# 3. Approve it
mv todos/004-pending-p1-my-real-task.md todos/004-ready-p1-my-real-task.md
sed -i 's/status: pending/status: ready/' todos/004-ready-p1-my-real-task.md

# 4. Create worktree
./tools/worktree-todo-manager.sh select
# Select option 3 (your new todo)

# 5. Start working
cd .worktrees/todo-004-my-real-task
```

### Planning a Sprint

```bash
# 1. Create 5 todos for sprint work
for i in {005..009}; do
  cp assets/todo-template.md "todos/${i}-pending-p2-sprint-task-${i}.md"
  # Edit each with specific details
done

# 2. Triage and approve all
for todo in todos/00{5..9}-pending-*.md; do
  new_name=$(echo "$todo" | sed 's/pending/ready/')
  mv "$todo" "$new_name"
  sed -i 's/status: pending/status: ready/' "$new_name"
done

# 3. Batch create all worktrees
./tools/worktree-todo-manager.sh batch

# 4. Work on them throughout the sprint
# Different terminals, different worktrees, no interference!
```

## Common Commands

```bash
# View all worktree-todo mappings
./tools/worktree-todo-manager.sh status

# Create single worktree interactively
./tools/worktree-todo-manager.sh select

# Create all ready worktrees
./tools/worktree-todo-manager.sh batch

# Complete a todo
./tools/worktree-todo-manager.sh complete <issue_id>

# Help
./tools/worktree-todo-manager.sh help
```

## Tips

1. **Start small** - Create 1-2 todos, test the workflow
2. **Use priorities** - p1 for urgent, p2 for important, p3 for nice-to-have
3. **Keep todos focused** - Each should be 1-4 hours of work
4. **Update work logs** - Add entries as you progress
5. **Use dependencies** - Set `dependencies: ["001"]` to block on other work
6. **Clean up regularly** - Run `complete` when done to avoid clutter

## Next Steps

- Read full documentation: `docs/WORKTREE_TODO_SYSTEM.md`
- Delete example todos: `rm todos/00{1,2,3}-*.md`
- Clean up example worktrees: `git worktree remove todo-001-example-implement-feature`
- Create real todos for your work!

## Integration with Lore

When you complete todos, the system automatically:

1. Extracts your git commits
2. Calls the lore-flow pipeline
3. Maps git author → persona
4. Generates narrative entry in persona's voice
5. Links to persona's chronicle book

Your technical work becomes mythology! 🎉
