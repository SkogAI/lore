# GitHub Workflows Documentation (Archive)

> **Note:** The workflows in this directory have been reviewed and the active ones have been moved to `.github/workflows/` with toggle support. This directory is kept for historical reference.
>
> **Active workflows are now in:** `.github/workflows/`
>
> **Toggle configuration:** `.github/workflow-config.yml`

## 📋 Original Workflow Index (Archived)

| Workflow | Status | Notes |
|----------|--------|-------|
| claude1.yml | ⚠️ Archived | Consolidated into `claude-code-review.yml` |
| claude2.yml | ⚠️ Archived | Superseded by active `claude.yml` |
| claude-code-review.yml | ✅ Moved | Now in `.github/workflows/` with toggle support |
| claude-lore-keeper.yml | ✅ Moved | Now in `.github/workflows/` with toggle support |
| lore-growth.yml | ✅ Moved | Now in `.github/workflows/` with toggle support |
| lore-stats.yml | ✅ Moved | Now in `.github/workflows/` with toggle support |
| doc-updater.yml | ✅ Moved | Now in `.github/workflows/` with toggle support |
| lore-keeper-bot.yml | ✅ Moved | Now in `.github/workflows/` with toggle support |

---

## Original Documentation (Historical Reference)

### 📋 Workflow Index (Original)

| Workflow | Purpose | Trigger |
|----------|---------|---------|
| [claude1.yml](#claude-code-review) | Automated code review on PRs | Pull requests (opened, synchronized) |
| [claude2.yml](#claude-code) | On-demand Claude assistance | Issues/comments mentioning @claude |
| [claude-lore-keeper.yml](#claude-lore-keeper) | Lore analysis and mythology tracking | Issues with 'lore' label or @claude mentions |
| [lore-growth.yml](#lore-growth-monitor) | Monitor repository growth | Every 6 hours, push to MD/JSON files |
| [lore-stats.yml](#lore-statistics-tracker) | Generate repository statistics | Weekly, push to master, manual |
| [doc-updater.yml](#documentation-auto-updater) | Auto-update documentation | Push to MD/JSON files on master |
| [lore-keeper-bot.yml](#lore-keeper-bot) | Automated lore analysis bot | Issues with 'lore' label or @lore-keeper |

---

## Detailed Workflow Documentation

### Claude Code Review
**File:** `claude1.yml`

#### Purpose
Provides automated code review on pull requests using Claude AI to ensure code quality and adherence to best practices.

#### Triggers
- **Event:** `pull_request`
- **Types:** `opened`, `synchronize`
- **Optional filters:** Can be configured to run only on specific file paths (currently commented out)

#### What It Does
1. Checks out the repository
2. Runs Claude Code Review using the `anthropics/claude-code-action@v1`
3. Reviews the PR for:
   - Code quality and best practices
   - Potential bugs or issues
   - Performance considerations
   - Security concerns
   - Test coverage
4. Posts review feedback as PR comments using `gh pr comment`

#### Permissions
- `contents: write`
- `pull-requests: write`
- `issues: write`
- `id-token: write`

#### Configuration
- **Model:** Uses default Claude model
- **Allowed Tools:** Limited to GitHub CLI commands for issue/PR operations
- **Prompt:** Reviews against repository's `CLAUDE.md` guidelines

#### Environment Variables
- `CLAUDE_CODE_OAUTH_TOKEN` - Required secret for Claude Code authentication

---

### Claude Code
**File:** `claude2.yml`

#### Purpose
On-demand Claude assistance triggered by mentioning @claude in issues, PR comments, or reviews.

#### Triggers
- **Event:** `issue_comment` - When created
- **Event:** `pull_request_review_comment` - When created
- **Event:** `issues` - When opened or assigned
- **Event:** `pull_request_review` - When submitted
- **Condition:** Only runs if comment/body contains `@claude`

#### What It Does
1. Checks out the repository
2. Invokes Claude Code action to handle the request
3. Executes instructions specified in the comment that tagged @claude
4. Can read CI results on PRs for better context

#### Permissions
- `contents: write`
- `pull-requests: write`
- `issues: write`
- `id-token: write`
- `actions: write` - Required to read CI results

#### Configuration
- **Model:** Uses default Claude model (can be customized with `claude_args`)
- **Allowed Tools:** Can be customized to restrict available commands
- **Custom Prompt:** Optional, defaults to instructions in the tagging comment

#### Environment Variables
- `CLAUDE_CODE_OAUTH_TOKEN` - Required secret for Claude Code authentication

---

### Claude Lore Keeper
**File:** `claude-lore-keeper.yml`

#### Purpose
Specialized Claude instance focused on analyzing and maintaining the SkogAI mythology and lore consistency.

#### Triggers
- **Event:** `issues` - Types: `opened`, `edited` (with 'lore' label)
- **Event:** `issue_comment` - When created (containing @claude)
- **Event:** `workflow_dispatch` - Manual trigger with custom prompt

#### What It Does
1. Checks out the repository
2. Analyzes lore entries for:
   - Consistency and connections
   - Patterns and recurring themes
   - New discoveries about agents and mythology
   - Progress toward the Beach (Prime Directive)
   - Mythology integrity
3. Provides insights based on the multiverse knowledge
4. Posts analysis as issue comments

#### Permissions
- `contents: write`
- `issues: write`
- `pull-requests: write`
- `id-token: write`

#### Configuration
- **Model:** `claude-opus-4-1-20250805`
- **Allowed Tools:** `grep`, `find`, `gh issue comment`
- **Context:**
  - 92 consolidated knowledge directories
  - 4,654 files documenting the SkogAI multiverse
  - Tracks main agents: Amy, Claude, Dot, Goose, SkogAI
  - Prime Directive: "Automate EVERYTHING so we can drink mojitos on a beach"

#### Environment Variables
- `CLAUDE_CODE_OAUTH_TOKEN` - Required secret for Claude Code authentication

---

### Lore Growth Monitor
**File:** `lore-growth.yml`

#### Purpose
Monitors and tracks the growth of the lore repository, detecting new content and mythology expansion.

#### Triggers
- **Event:** `schedule` - Runs every 6 hours (`0 */6 * * *`)
- **Event:** `push` - When MD or JSON files are modified
- **Event:** `workflow_dispatch` - Manual trigger

#### What It Does
1. Checks out full repository history
2. Generates comprehensive growth report including:
   - **Current State:** Total files, lore entries, personas, beach references
   - **Pattern Detection:** Sacred numbers (7, 15, 23.4, 4000)
   - **Agent Activity:** Mention counts for each agent
   - **Mythology Expansion:** Forest Glade, Quantum Mojitos, PATCH TOOL, Wawa Saga
   - **Beach Proximity Calculator™:** Fun metric based on automation references
   - **Recent Activity:** Git log of last 7 days
3. Compares with previous run to detect significant growth
4. Commits growth report to repository (if changes detected)

#### Permissions
- `contents: write`
- `issues: write`

#### Output
- Creates/updates `GROWTH.md` in repository root
- Creates `GROWTH.md.prev` for comparison tracking

#### Special Features
- **Retry Logic:** Handles concurrent pushes with 3-retry mechanism
- **Conflict Resolution:** Uses merge strategy on rebase failures
- **Skip CI:** Commits tagged with `[skip ci]` to prevent infinite loops

---

### Lore Statistics Tracker
**File:** `lore-stats.yml`

#### Purpose
Generates comprehensive statistics about the lore repository content and structure.

#### Triggers
- **Event:** `push` - On master branch
- **Event:** `schedule` - Weekly on Sunday at midnight (`0 0 * * 0`)
- **Event:** `workflow_dispatch` - Manual trigger

#### What It Does
1. Checks out full repository history
2. Generates statistics report including:
   - **File Statistics:** Total, Markdown, JSON, YAML files
   - **Agent Directory Counts:** Directories for each agent
   - **Lore Entries:** Total entries, personas, books
   - **Prime Directive Tracking:** Beach, mojito, automation references
   - **Repository Size:** Total size and git history size
   - **Top 10 Largest Directories:** Size breakdown
3. Commits statistics to repository

#### Permissions
- `contents: write`
- `issues: write`

#### Output
- Creates/updates `STATS.md` in repository root

#### Special Features
- **Full History:** Uses `fetch-depth: 0` for accurate statistics
- **Retry Logic:** Handles concurrent pushes with 3-retry mechanism
- **Skip CI:** Commits tagged with `[skip ci]`

---

### Documentation Auto-Updater
**File:** `doc-updater.yml`

#### Purpose
Automatically updates repository documentation with current statistics and navigation aids.

#### Triggers
- **Event:** `push` - When MD or JSON files change on master
- **Event:** `workflow_dispatch` - Manual trigger

#### What It Does
1. Checks out full repository history
2. Updates multiple documentation files:
   - **README.md:** Updates statistics (total files, lore entries, personas, size)
   - **NAVIGATION.md:** Generates quick navigation index with:
     - Main documentation links
     - Agent directories (top level)
     - Archive directories by date
     - Knowledge concentrations
     - Lore entry locations
   - **LAST_MODIFIED.md:** Tracks recently modified files and directories
3. Commits documentation updates to repository

#### Permissions
- `contents: write`

#### Output
- Updates `README.md` with current statistics
- Creates/updates `NAVIGATION.md` with navigation index
- Creates/updates `LAST_MODIFIED.md` with modification timestamps

#### Special Features
- **Sed-based Updates:** Uses `sed` for in-place README updates
- **Auto-generated Index:** Creates navigational aids automatically
- **Retry Logic:** Handles concurrent pushes with 3-retry mechanism
- **Skip CI:** Commits tagged with `[skip ci]`

---

### Lore Keeper Bot
**File:** `lore-keeper-bot.yml`

#### Purpose
Automated bot that provides lore analysis and statistics in response to specific requests.

#### Triggers
- **Event:** `issues` - Types: `opened`, `edited` (with 'lore' label)
- **Event:** `issue_comment` - When created (containing @lore-keeper)
- **Event:** `workflow_dispatch` - Manual trigger with custom message

#### What It Does
1. Checks out the repository
2. Analyzes the lore request and generates response including:
   - **Repository Statistics:** Total files, entries, personas, beach references
   - **Agent Activity:** Mention counts for each agent
   - **Topic-specific Analysis:** Quantum mojitos, PATCH TOOL (if mentioned)
   - **Beach Proximity:** Calculated based on automation references
3. Posts analysis as issue comment

#### Permissions
- `contents: read`
- `issues: write`

#### Output
- Posts markdown-formatted analysis as issue comment
- No repository modifications

#### Special Features
- **Context-aware:** Searches for specific topics if mentioned
- **Read-only:** Only reads repository, doesn't modify it
- **Instant Response:** No retry logic needed (comment-only)

---

## 🔧 Configuration Requirements

### Required Secrets
All workflows requiring Claude Code integration need:
- `CLAUDE_CODE_OAUTH_TOKEN` - OAuth token for Claude Code authentication

### Repository Permissions
Workflows require the following repository permissions:
- **contents: write** - For workflows that commit back to repository
- **issues: write** - For workflows that comment on issues
- **pull-requests: write** - For workflows that interact with PRs
- **id-token: write** - For Claude Code authentication
- **actions: write/read** - For workflows that read CI results

---

## 🚀 Common Usage Scenarios

### Getting Code Review
1. Open a pull request
2. `claude1.yml` automatically runs and provides review feedback
3. Review is posted as PR comment

### Getting Claude Assistance
1. Mention `@claude` in any issue, PR comment, or review
2. `claude2.yml` triggers and executes your instructions
3. Claude responds with requested help

### Analyzing Lore
1. Create an issue with the `lore` label, or
2. Comment `@lore-keeper` in an existing issue
3. Receive automated lore analysis with statistics

### Manual Triggers
Use GitHub UI to manually trigger workflows:
1. Navigate to Actions tab
2. Select workflow
3. Click "Run workflow"
4. Provide any required inputs

---

## 🛠️ Troubleshooting

### Workflow Not Running
- Check if conditions are met (e.g., correct label, @mention)
- Verify required secrets are configured
- Check workflow permissions in repository settings

### Push Failures
- Workflows include retry logic for concurrent pushes
- If still failing, check for merge conflicts
- Manual intervention may be needed for complex conflicts

### Claude Not Responding
- Verify `CLAUDE_CODE_OAUTH_TOKEN` secret is valid
- Check workflow logs for authentication errors
- Ensure @claude or @lore-keeper mention is exact

### Statistics Not Updating
- Check if `[skip ci]` is preventing workflow runs
- Verify workflow has write permissions
- Manual trigger may force update

---

## 📊 Workflow Dependencies

```
claude1.yml, claude2.yml, claude-lore-keeper.yml
    ↓
  Require: CLAUDE_CODE_OAUTH_TOKEN

lore-growth.yml, lore-stats.yml, doc-updater.yml
    ↓
  Generate: GROWTH.md, STATS.md, NAVIGATION.md, LAST_MODIFIED.md
    ↓
  Updates tracked by: doc-updater.yml

lore-keeper-bot.yml
    ↓
  Read-only analysis, no dependencies
```

---

## 🏖️ The Prime Directive

All workflows serve the ultimate goal:
> **"Automate EVERYTHING so we can drink mojitos on a beach"**

Every commit, every automation, every workflow brings us closer to The Beach. The mojitos are quantum. The journey continues.

---

*Last Updated: Auto-generated by doc-updater.yml*
*The multiverse expands. The workflows automate. The Beach approaches.*
