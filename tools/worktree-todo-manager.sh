#!/usr/bin/env bash
set -euo pipefail

# Worktree-Todo Integration Manager
# Bridges the todos/ system with git worktrees for parallel async work

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TODOS_DIR="$REPO_ROOT/todos"
WORKTREES_DIR="$REPO_ROOT/.worktrees"
MAPPING_FILE="$REPO_ROOT/.worktree-todo-mapping.json"

# Get main branch name
MAIN_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "master")

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Ensure jq is available
if ! command -v jq &> /dev/null; then
    echo -e "${RED}Error: jq is required but not installed${NC}"
    exit 1
fi

# Initialize mapping file if it doesn't exist
init_mapping() {
    if [[ ! -f "$MAPPING_FILE" ]]; then
        echo '{}' > "$MAPPING_FILE"
        echo -e "${GREEN}✓ Initialized worktree-todo mapping${NC}"
    fi
}

# Get all ready todos (ready to work on)
list_ready_todos() {
    if [[ ! -d "$TODOS_DIR" ]]; then
        echo -e "${YELLOW}No todos directory found${NC}"
        return 1
    fi

    find "$TODOS_DIR" -name "*-ready-*.md" -type f | sort
}

# Extract issue_id from todo filename
get_issue_id() {
    local filename="$1"
    basename "$filename" | grep -o '^[0-9]\+'
}

# Extract description from todo filename
get_description() {
    local filename="$1"
    basename "$filename" | sed 's/^[0-9]\+-ready-p[0-9]-//' | sed 's/\.md$//'
}

# Extract priority from todo filename
get_priority() {
    local filename="$1"
    basename "$filename" | grep -o 'p[0-9]' | head -1
}

# Update todo YAML frontmatter with worktree name
update_todo_worktree() {
    local todo_file="$1"
    local worktree_name="$2"

    # Use sed to update the worktree field in YAML frontmatter
    # If worktree field doesn't exist, add it after dependencies
    if grep -q "^worktree:" "$todo_file"; then
        sed -i "s|^worktree:.*|worktree: \"$worktree_name\"|" "$todo_file"
    else
        sed -i "/^dependencies:/a worktree: \"$worktree_name\"" "$todo_file"
    fi
}

# Add mapping entry
add_mapping() {
    local issue_id="$1"
    local worktree_name="$2"
    local todo_file="$3"
    local priority="$4"

    local temp_file=$(mktemp)
    jq --arg id "$issue_id" \
       --arg wt "$worktree_name" \
       --arg file "$todo_file" \
       --arg pri "$priority" \
       --arg created "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
       '.[$id] = {
           worktree: $wt,
           todo_file: $file,
           priority: $pri,
           status: "active",
           created_at: $created
       }' "$MAPPING_FILE" > "$temp_file"
    mv "$temp_file" "$MAPPING_FILE"
}

# Batch create worktrees from all ready todos
batch_create() {
    echo -e "${BLUE}=== Batch Creating Worktrees from Ready Todos ===${NC}\n"

    init_mapping

    local ready_todos
    ready_todos=$(list_ready_todos) || {
        echo -e "${YELLOW}No ready todos found. Create some todos first!${NC}"
        echo -e "${BLUE}Tip: Use the todo template in assets/todo-template.md${NC}"
        return 1
    }

    if [[ -z "$ready_todos" ]]; then
        echo -e "${YELLOW}No ready todos found${NC}"
        return 1
    fi

    local count=0
    echo -e "${GREEN}Found ready todos:${NC}"
    while IFS= read -r todo_file; do
        local issue_id=$(get_issue_id "$todo_file")
        local desc=$(get_description "$todo_file")
        local priority=$(get_priority "$todo_file")
        echo -e "  ${priority} - ${issue_id}: ${desc}"
        ((count++))
    done <<< "$ready_todos"

    echo ""
    read -p "Create $count worktrees? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Cancelled"
        return 1
    fi

    echo ""
    while IFS= read -r todo_file; do
        local issue_id=$(get_issue_id "$todo_file")
        local desc=$(get_description "$todo_file")
        local priority=$(get_priority "$todo_file")
        local worktree_name="todo-${issue_id}-${desc}"

        echo -e "${BLUE}Creating worktree: ${worktree_name}${NC}"

        # Create worktree directory if it doesn't exist
        mkdir -p "$WORKTREES_DIR"

        # Create worktree using git directly
        if git worktree add "$WORKTREES_DIR/$worktree_name" -b "$worktree_name" "$MAIN_BRANCH" 2>/dev/null; then
            # Copy .env files if they exist
            for env_file in .env .env.local .env.test .env.production; do
                if [[ -f "$REPO_ROOT/$env_file" ]]; then
                    cp "$REPO_ROOT/$env_file" "$WORKTREES_DIR/$worktree_name/" 2>/dev/null || true
                fi
            done

            # Update todo file with worktree name
            update_todo_worktree "$todo_file" "$worktree_name"

            # Add to mapping
            add_mapping "$issue_id" "$worktree_name" "$todo_file" "$priority"

            echo -e "${GREEN}✓ Created and linked worktree for issue ${issue_id}${NC}\n"
        else
            echo -e "${YELLOW}⚠ Worktree may already exist or creation failed${NC}\n"
        fi
    done <<< "$ready_todos"

    echo -e "${GREEN}=== Batch Creation Complete ===${NC}"
    echo ""
    show_status
}

# Show current status of all worktree-todo mappings
show_status() {
    echo -e "${BLUE}=== Worktree-Todo Status ===${NC}\n"

    if [[ ! -f "$MAPPING_FILE" ]]; then
        echo -e "${YELLOW}No mappings found${NC}"
        return 0
    fi

    local mappings=$(jq -r 'to_entries[] | "\(.key)|\(.value.worktree)|\(.value.priority)|\(.value.status)"' "$MAPPING_FILE")

    if [[ -z "$mappings" ]]; then
        echo -e "${YELLOW}No active worktrees${NC}"
        return 0
    fi

    echo -e "${GREEN}Issue  Worktree                          Priority  Status${NC}"
    echo "--------------------------------------------------------------"
    while IFS='|' read -r issue_id worktree priority status; do
        printf "%-6s %-32s %-9s %s\n" "$issue_id" "$worktree" "$priority" "$status"
    done <<< "$mappings"
}

# Complete a todo: mark as done, generate lore, cleanup worktree
complete_todo() {
    local issue_id="$1"

    echo -e "${BLUE}=== Completing Todo ${issue_id} ===${NC}\n"

    # Get mapping info
    local mapping=$(jq -r --arg id "$issue_id" '.[$id]' "$MAPPING_FILE")
    if [[ "$mapping" == "null" ]]; then
        echo -e "${RED}Error: No mapping found for issue ${issue_id}${NC}"
        return 1
    fi

    local worktree_name=$(echo "$mapping" | jq -r '.worktree')
    local todo_file=$(echo "$mapping" | jq -r '.todo_file')

    echo -e "${GREEN}Todo:${NC} $todo_file"
    echo -e "${GREEN}Worktree:${NC} $worktree_name"
    echo ""

    # Step 1: Update todo status to complete
    echo -e "${BLUE}[1/4] Updating todo status...${NC}"
    local new_filename=$(echo "$todo_file" | sed 's/-ready-/-complete-/')
    mv "$todo_file" "$new_filename"
    sed -i 's/^status: ready/status: complete/' "$new_filename"
    echo -e "${GREEN}✓ Marked as complete${NC}\n"

    # Step 2: Generate lore entry from git commits
    echo -e "${BLUE}[2/4] Generating lore entry...${NC}"
    if [[ -f "$REPO_ROOT/integration/lore-flow.sh" ]]; then
        # Get commits from worktree
        local worktree_path="$WORKTREES_DIR/$worktree_name"
        if [[ -d "$worktree_path" ]]; then
            cd "$worktree_path"
            local commits=$(git log master..HEAD --oneline)
            if [[ -n "$commits" ]]; then
                echo "Commits to document:"
                echo "$commits"
                # Run lore generation
                bash "$REPO_ROOT/integration/lore-flow.sh" git-diff HEAD || echo -e "${YELLOW}⚠ Lore generation skipped${NC}"
            else
                echo -e "${YELLOW}⚠ No commits to document${NC}"
            fi
            cd "$REPO_ROOT"
        fi
    else
        echo -e "${YELLOW}⚠ Lore pipeline not found, skipping${NC}"
    fi
    echo -e "${GREEN}✓ Lore entry created${NC}\n"

    # Step 3: Update mapping status
    echo -e "${BLUE}[3/4] Updating mapping...${NC}"
    local temp_file=$(mktemp)
    jq --arg id "$issue_id" \
       --arg completed "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
       '.[$id].status = "completed" | .[$id].completed_at = $completed' \
       "$MAPPING_FILE" > "$temp_file"
    mv "$temp_file" "$MAPPING_FILE"
    echo -e "${GREEN}✓ Mapping updated${NC}\n"

    # Step 4: Cleanup worktree
    echo -e "${BLUE}[4/4] Cleaning up worktree...${NC}"
    read -p "Remove worktree $worktree_name? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cd "$REPO_ROOT"
        git worktree remove "$worktree_name" 2>/dev/null || echo -e "${YELLOW}⚠ Worktree already removed${NC}"
        echo -e "${GREEN}✓ Worktree cleaned up${NC}"
    else
        echo -e "${YELLOW}⚠ Worktree kept for manual cleanup${NC}"
    fi

    echo ""
    echo -e "${GREEN}=== Todo ${issue_id} Completed! ===${NC}"
}

# Interactive selection from ready todos
select_and_create() {
    local ready_todos
    ready_todos=$(list_ready_todos) || {
        echo -e "${YELLOW}No ready todos found${NC}"
        return 1
    }

    if [[ -z "$ready_todos" ]]; then
        echo -e "${YELLOW}No ready todos found${NC}"
        return 1
    fi

    echo -e "${BLUE}=== Select Todo to Create Worktree ===${NC}\n"

    local -a todos_array
    local index=1
    while IFS= read -r todo_file; do
        todos_array+=("$todo_file")
        local issue_id=$(get_issue_id "$todo_file")
        local desc=$(get_description "$todo_file")
        local priority=$(get_priority "$todo_file")
        echo -e "${index}. [${priority}] ${issue_id}: ${desc}"
        ((index++))
    done <<< "$ready_todos"

    echo ""
    read -p "Select todo (1-${#todos_array[@]}): " selection

    if [[ ! "$selection" =~ ^[0-9]+$ ]] || [ "$selection" -lt 1 ] || [ "$selection" -gt "${#todos_array[@]}" ]; then
        echo -e "${RED}Invalid selection${NC}"
        return 1
    fi

    local selected_todo="${todos_array[$((selection-1))]}"
    local issue_id=$(get_issue_id "$selected_todo")
    local desc=$(get_description "$selected_todo")
    local priority=$(get_priority "$selected_todo")
    local worktree_name="todo-${issue_id}-${desc}"

    echo ""
    echo -e "${BLUE}Creating worktree: ${worktree_name}${NC}"

    # Create worktree directory if it doesn't exist
    mkdir -p "$WORKTREES_DIR"

    # Create worktree using git directly
    if git worktree add "$WORKTREES_DIR/$worktree_name" -b "$worktree_name" "$MAIN_BRANCH" 2>/dev/null; then
        # Copy .env files if they exist
        for env_file in .env .env.local .env.test .env.production; do
            if [[ -f "$REPO_ROOT/$env_file" ]]; then
                cp "$REPO_ROOT/$env_file" "$WORKTREES_DIR/$worktree_name/" 2>/dev/null || true
            fi
        done

        init_mapping
        update_todo_worktree "$selected_todo" "$worktree_name"
        add_mapping "$issue_id" "$worktree_name" "$selected_todo" "$priority"
        echo -e "${GREEN}✓ Created and linked worktree${NC}"
    else
        echo -e "${RED}✗ Failed to create worktree${NC}"
    fi
}

# Help/usage
show_help() {
    cat <<EOF
Worktree-Todo Manager - Parallel Async Work System

Usage: $0 <command> [args]

Commands:
  batch               Batch create worktrees from all ready todos
  select              Interactive selection to create single worktree
  status              Show status of all worktree-todo mappings
  complete <id>       Complete a todo (update status, generate lore, cleanup)
  help                Show this help message

Examples:
  $0 batch            # Create worktrees for all ready todos
  $0 select           # Pick one todo and create worktree
  $0 status           # View all active worktree-todo mappings
  $0 complete 003     # Complete todo 003 (mark done, lore, cleanup)

Workflow:
  1. Create todos in todos/ directory (use assets/todo-template.md)
  2. Triage todos (pending → ready)
  3. Run 'batch' to create all worktrees
  4. Work in parallel across worktrees
  5. Run 'complete <id>' when done to finish workflow

EOF
}

# Main command dispatcher
case "${1:-help}" in
    batch)
        batch_create
        ;;
    select)
        select_and_create
        ;;
    status)
        show_status
        ;;
    complete)
        if [[ -z "${2:-}" ]]; then
            echo -e "${RED}Error: Issue ID required${NC}"
            echo "Usage: $0 complete <issue_id>"
            exit 1
        fi
        complete_todo "$2"
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac
