# Worktree-Todo Parallel Async Work System

A comprehensive system for managing parallel async work by combining the skogai-todos file-based tracking with git worktrees. This enables you to split large workloads into smaller work orders and work on them simultaneously.

## Core Concept

**Problem:** Large features or refactors require working on multiple independent pieces simultaneously. Switching branches disrupts flow and risks mixing concerns.

**Solution:** Each todo gets its own isolated worktree. Work on multiple todos in parallel without context switching overhead.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     todos/ Directory                         │
│  File-based todo tracking with YAML frontmatter             │
│  • 001-ready-p1-implement-auth.md                           │
│  • 002-ready-p2-add-logging.md                              │
│  • 003-pending-p3-refactor-db.md  ← Not ready yet           │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ↓ batch create
┌─────────────────────────────────────────────────────────────┐
│              .worktrees/ + Mapping System                    │
│  Each ready todo → isolated worktree                         │
│  • todo-001-implement-auth/                                  │
│  • todo-002-add-logging/                                     │
│                                                              │
│  Mapping: .worktree-todo-mapping.json                        │
│  {                                                           │
│    "001": {                                                  │
│      "worktree": "todo-001-implement-auth",                  │
│      "todo_file": "todos/001-ready-p1-implement-auth.md",    │
│      "priority": "p1",                                       │
│      "status": "active"                                      │
│    }                                                         │
│  }                                                           │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ↓ work in parallel
┌─────────────────────────────────────────────────────────────┐
│                    Development Flow                          │
│  cd .worktrees/todo-001-implement-auth                       │
│  • Make changes, commit locally                              │
│  • Test in isolation                                         │
│  • No interference from other work                           │
│                                                              │
│  cd .worktrees/todo-002-add-logging                          │
│  • Different context, different work                         │
│  • Completely independent                                    │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ↓ complete workflow
┌─────────────────────────────────────────────────────────────┐
│              Completion & Documentation                      │
│  ./tools/worktree-todo-manager.sh complete 001               │
│                                                              │
│  1. Mark todo as complete (ready → complete)                 │
│  2. Generate lore entry from git commits                     │
│  3. Update mapping status                                    │
│  4. Clean up worktree                                        │
└─────────────────────────────────────────────────────────────┘
```

## Setup

### 1. Initialize Todos System

```bash
# Todos directory already created with template
ls assets/todo-template.md  # ✓ Template available
```

### 2. Create Your First Todo

```bash
# Find next issue ID
next_id=$(ls todos/*.md 2>/dev/null | grep -o '^todos/[0-9]\+' | sed 's/todos\///' | sort -n | tail -1 | awk '{printf "%03d", $1+1}')
echo "Next ID: ${next_id:-001}"

# Copy template
cp assets/todo-template.md "todos/001-pending-p1-my-first-task.md"

# Edit the todo file:
# - Fill in Problem Statement
# - Add Proposed Solutions
# - Set Acceptance Criteria
# - Update YAML frontmatter (issue_id: "001", tags, etc.)
```

### 3. Triage and Approve

```bash
# Review pending todo
cat todos/001-pending-p1-my-first-task.md

# Approve it (pending → ready)
mv todos/001-pending-p1-my-first-task.md todos/001-ready-p1-my-first-task.md
sed -i 's/status: pending/status: ready/' todos/001-ready-p1-my-first-task.md

# Add "Recommended Action" section with clear implementation plan
```

## Usage

### Batch Create Worktrees

Create worktrees for all ready todos at once:

```bash
./tools/worktree-todo-manager.sh batch
```

**What happens:**

1. Scans `todos/` for all `*-ready-*.md` files
2. Shows list and asks for confirmation
3. For each ready todo:
   - Creates worktree: `todo-{issue_id}-{description}`
   - Updates todo YAML with worktree name
   - Adds mapping entry
   - Copies .env files automatically
4. Shows final status

**Output:**

```
=== Batch Creating Worktrees from Ready Todos ===

Found ready todos:
  p1 - 001: implement-auth
  p2 - 002: add-logging
  p1 - 003: fix-performance-bug

Create 3 worktrees? (y/n): y

Creating worktree: todo-001-implement-auth
✓ Created and linked worktree for issue 001

Creating worktree: todo-002-add-logging
✓ Created and linked worktree for issue 002

Creating worktree: todo-003-fix-performance-bug
✓ Created and linked worktree for issue 003

=== Batch Creation Complete ===
```

### Check Status

View all active worktree-todo mappings:

```bash
./tools/worktree-todo-manager.sh status
```

**Output:**

```
=== Worktree-Todo Status ===

Issue  Worktree                          Priority  Status
--------------------------------------------------------------
001    todo-001-implement-auth           p1        active
002    todo-002-add-logging              p2        active
003    todo-003-fix-performance-bug      p1        active
```

### Work on a Todo

```bash
# Switch to the worktree
cd .worktrees/todo-001-implement-auth

# Work normally
git status
# Make changes, test, commit
git add .
git commit -m "Implement user authentication"

# Return to main repo
cd ../..
```

### Complete a Todo

When you're done with a todo:

```bash
./tools/worktree-todo-manager.sh complete 001
```

**What happens:**

```
=== Completing Todo 001 ===

Todo: todos/001-ready-p1-implement-auth.md
Worktree: todo-001-implement-auth

[1/4] Updating todo status...
✓ Marked as complete

[2/4] Generating lore entry...
Commits to document:
abc1234 Implement user authentication
def5678 Add auth tests
✓ Lore entry created

[3/4] Updating mapping...
✓ Mapping updated

[4/4] Cleaning up worktree...
Remove worktree todo-001-implement-auth? (y/n): y
✓ Worktree cleaned up

=== Todo 001 Completed! ===
```

**Results:**

- `todos/001-ready-p1-implement-auth.md` → `todos/001-complete-p1-implement-auth.md`
- Status in YAML: `ready` → `complete`
- Lore entry created from git commits (if lore-flow.sh available)
- Mapping updated to `completed` status
- Worktree removed (optional)

### Interactive Selection

Create worktree for a single todo interactively:

```bash
./tools/worktree-todo-manager.sh select
```

**What happens:**

```
=== Select Todo to Create Worktree ===

1. [p1] 001: implement-auth
2. [p2] 002: add-logging
3. [p1] 003: fix-performance-bug

Select todo (1-3): 1

Creating worktree: todo-001-implement-auth
✓ Created and linked worktree
```

## Workflow Examples

### Feature Development Split into Multiple Todos

```bash
# 1. Create todos for a large feature
cp assets/todo-template.md todos/001-pending-p1-auth-backend.md
cp assets/todo-template.md todos/002-pending-p1-auth-frontend.md
cp assets/todo-template.md todos/003-pending-p2-auth-tests.md

# 2. Edit each todo with specific details
# ... fill in problem statements, solutions, acceptance criteria

# 3. Triage and approve all
for todo in todos/00{1,2,3}-pending-*.md; do
    new_name=$(echo "$todo" | sed 's/pending/ready/')
    mv "$todo" "$new_name"
    sed -i 's/status: pending/status: ready/' "$new_name"
done

# 4. Batch create worktrees
./tools/worktree-todo-manager.sh batch

# 5. Work on them in parallel
# Terminal 1:
cd .worktrees/todo-001-auth-backend
# ... work on backend

# Terminal 2:
cd .worktrees/todo-002-auth-frontend
# ... work on frontend

# Terminal 3:
cd .worktrees/todo-003-auth-tests
# ... write tests

# 6. Complete each as you finish
cd /path/to/main/repo
./tools/worktree-todo-manager.sh complete 001
./tools/worktree-todo-manager.sh complete 002
./tools/worktree-todo-manager.sh complete 003
```

### Bug Fixes and Technical Debt

```bash
# 1. Create todos from code review findings
# (Use /workflows:review to generate todos automatically)

# 2. Prioritize critical bugs
# 001-ready-p1-fix-security-vuln.md
# 002-ready-p2-refactor-db-queries.md
# 003-ready-p3-update-docs.md

# 3. Create worktrees for p1 items immediately
./tools/worktree-todo-manager.sh select
# Select: 001

# 4. Work on critical bug in isolation
cd .worktrees/todo-001-fix-security-vuln
# ... fix, test, commit

# 5. Complete with lore documentation
cd ../..
./tools/worktree-todo-manager.sh complete 001
# Generates narrative about the security fix
```

### Dependency Management

```bash
# todos/001-ready-p1-database-migration.md
# YAML:
#   dependencies: []

# todos/002-ready-p2-api-endpoints.md
# YAML:
#   dependencies: ["001"]  # Blocked by 001

# todos/003-ready-p2-frontend-ui.md
# YAML:
#   dependencies: ["002"]  # Blocked by 002

# Create worktree only for 001 (no blockers)
./tools/worktree-todo-manager.sh select
# Select: 001

# Work on 001, complete it
cd .worktrees/todo-001-database-migration
# ... work, commit
cd ../..
./tools/worktree-todo-manager.sh complete 001

# Now 002 is unblocked, create its worktree
# Update 002's dependencies to [] since 001 is complete
sed -i 's/dependencies: \["001"\]/dependencies: []/' todos/002-ready-p2-api-endpoints.md
./tools/worktree-todo-manager.sh select
# Select: 002
```

## Integration with Lore System

The completion workflow automatically integrates with the lore system to document your work narratively.

### How It Works

When you run `complete <issue_id>`:

1. **Extracts commits** from the worktree:
   ```bash
   cd .worktrees/todo-001-implement-auth
   git log master..HEAD --oneline
   ```

2. **Calls lore-flow.sh**:
   ```bash
   bash integration/lore-flow.sh git-diff HEAD
   ```

3. **Lore pipeline runs**:
   - Extracts git diff and commit messages
   - Maps git author → persona (from persona-mapping.conf)
   - Loads persona context and voice
   - LLM transforms technical changes → narrative
   - Creates lore entry with story in persona's voice
   - Links to persona's chronicle book

4. **Result**: Your todo becomes mythology
   ```
   Entry ID: entry_1764315234_a4b3c2d1
   Title: "The Authentication Ritual"
   Content: "In the depths of the digital realm, the keeper of secrets
            forged a new ward to protect the sacred data. Through careful
            incantations of JWT and bcrypt, the barrier was strengthened..."
   ```

### Example

```bash
# Complete todo 001
./tools/worktree-todo-manager.sh complete 001

# Output includes:
# [2/4] Generating lore entry...
# Commits to document:
#   abc1234 Implement user authentication
#   def5678 Add JWT token generation
#   ghi9012 Write auth tests
#
# === Lore Generation Complete ===
# Entry ID: entry_1764315234_a4b3c2d1
# Persona: Amy Ravenwolf (persona_1744992765)
# Chronicle: book_1764315000
```

Your technical work is now stored as narrative mythology that AI agents can load as context in future sessions!

## File Structure

```
lore/
├── todos/                              # Todo tracking
│   ├── 001-ready-p1-implement-auth.md
│   ├── 002-complete-p2-add-logging.md
│   └── 003-pending-p3-refactor-db.md
│
├── assets/
│   └── todo-template.md                # Template for new todos
│
├── .worktrees/                         # Isolated work environments
│   ├── todo-001-implement-auth/
│   └── todo-002-add-logging/
│
├── .worktree-todo-mapping.json         # Tracking system
│
└── tools/
    └── worktree-todo-manager.sh        # Main management script
```

## Mapping File Format

`.worktree-todo-mapping.json`:

```json
{
  "001": {
    "worktree": "todo-001-implement-auth",
    "todo_file": "todos/001-ready-p1-implement-auth.md",
    "priority": "p1",
    "status": "active",
    "created_at": "2025-12-26T10:30:00Z"
  },
  "002": {
    "worktree": "todo-002-add-logging",
    "todo_file": "todos/002-complete-p2-add-logging.md",
    "priority": "p2",
    "status": "completed",
    "created_at": "2025-12-26T10:30:15Z",
    "completed_at": "2025-12-26T11:45:00Z"
  }
}
```

## Tips and Best Practices

### 1. Use Batch Creation for Sprint Planning

Create all todos at the start of a sprint, then batch create worktrees for all ready items. Work through them systematically.

### 2. Keep Todos Small and Focused

Each todo should represent 1-4 hours of work. Larger features should be split into multiple todos with dependencies.

### 3. Update Work Logs Regularly

Add work log entries to todos as you progress. This becomes valuable documentation and feeds into lore generation.

### 4. Use Dependencies to Sequence Work

Set `dependencies: ["001", "002"]` in YAML frontmatter to indicate blockers. Only create worktrees for unblocked todos.

### 5. Clean Up Completed Worktrees

Don't accumulate stale worktrees. Always run `complete` when done, which handles cleanup automatically.

### 6. Leverage Lore Documentation

The auto-generated lore entries become searchable knowledge for AI agents. Well-documented commits create better narratives.

### 7. Priority-Based Workflow

Work on p1 todos first. Use `./tools/worktree-todo-manager.sh status` to see priorities at a glance.

## Troubleshooting

### "No ready todos found"

Create todos in `todos/` directory and ensure they're in `ready` status:
```bash
# Check status
ls todos/*-ready-*.md

# Move from pending to ready
mv todos/001-pending-p1-task.md todos/001-ready-p1-task.md
sed -i 's/status: pending/status: ready/' todos/001-ready-p1-task.md
```

### Worktree already exists

If batch creation fails because worktree exists:
```bash
# List existing worktrees
git worktree list

# Remove if needed
git worktree remove todo-001-implement-auth
```

### Mapping out of sync

If mapping doesn't match reality:
```bash
# Delete and rebuild
rm .worktree-todo-mapping.json
./tools/worktree-todo-manager.sh batch
```

### Lore generation skipped

If lore integration isn't working:
```bash
# Check if lore-flow.sh exists
ls integration/lore-flow.sh

# Check if OPENROUTER_API_KEY is set
echo $OPENROUTER_API_KEY

# Manually generate lore
cd .worktrees/todo-001-task
bash ../../integration/lore-flow.sh git-diff HEAD
```

## Advanced Usage

### Custom Completion Hooks

Add your own logic to the completion workflow by editing `worktree-todo-manager.sh`:

```bash
# After step 2 (lore generation), add:
echo -e "${BLUE}[2.5/4] Running custom validation...${NC}"
# Run your custom tests, checks, etc.
```

### Integration with CI/CD

Before merging, verify all acceptance criteria:

```bash
# Check todo acceptance criteria
todo_file=$(jq -r --arg id "001" '.[$id].todo_file' .worktree-todo-mapping.json)
grep -A 10 "## Acceptance Criteria" "$todo_file"

# Ensure all boxes checked
if grep -q "- \[ \]" "$todo_file"; then
    echo "Error: Unchecked acceptance criteria"
    exit 1
fi
```

### Bulk Status Updates

Update multiple todos at once:

```bash
# Mark all p3 todos as ready
for todo in todos/*-pending-p3-*.md; do
    new_name=$(echo "$todo" | sed 's/pending/ready/')
    mv "$todo" "$new_name"
    sed -i 's/status: pending/status: ready/' "$new_name"
done
```

## Command Reference

```bash
# Batch create all worktrees
./tools/worktree-todo-manager.sh batch

# Interactive single creation
./tools/worktree-todo-manager.sh select

# View status
./tools/worktree-todo-manager.sh status

# Complete a todo
./tools/worktree-todo-manager.sh complete <issue_id>

# Help
./tools/worktree-todo-manager.sh help
```

## Next Steps

1. **Create your first todo** using the template
2. **Triage it** (pending → ready)
3. **Run batch creation** to see it in action
4. **Work on the task** in the isolated worktree
5. **Complete it** and watch the full workflow execute

This system transforms how you handle parallel work, turning chaos into organized async productivity!
