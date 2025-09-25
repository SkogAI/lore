# SkogCLI-Docs Integration - Official Documentation

## Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Installation & Setup](#installation--setup)
4. [Command Reference](#command-reference)
5. [Voting System](#voting-system)
6. [Document Discovery](#document-discovery)
7. [Usage Examples](#usage-examples)
8. [Configuration Files](#configuration-files)
9. [Troubleshooting](#troubleshooting)

## Overview

The SkogCLI-Docs Integration is a comprehensive bidirectional bridge system that enables seamless interaction between the SkogCLI framework and the SkogAI docs repository management tools. This integration fulfills Amy Ravenwolf's motion for unified command-line access to documentation workflows.

### Key Features
- **Bidirectional Command Access**: Run docs-cli from SkogCLI and vice versa
- **Integrated Voting System**: Democratic proposal voting with persistent storage
- **Context Generation**: Automated repository context creation
- **Document Discovery**: Cross-branch content discovery and summarization
- **Repository Operations**: Full git workflow management through unified interface

### Core Philosophy
- **Unified Interface**: Single command-line entry point for all documentation operations
- **Democratic Workflow**: Built-in voting system for proposal management
- **Cross-Branch Intelligence**: Automated discovery of content across all branches
- **Seamless Integration**: Transparent forwarding between command systems

## Architecture

### System Components

The integration consists of four main components working together:

```
┌─────────────────┐    ┌─────────────────┐
│    SkogCLI      │◄──►│    docs-cli     │
│   Framework     │    │   Repository    │
└─────────────────┘    └─────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│  Integration    │    │  Extension      │
│     Layer       │    │    System       │
└─────────────────┘    └─────────────────┘
```

#### 1. Main Integration Script (`/home/skogix/.config/skogcli/misc/docs.py`)
- **Core Functionality**: Primary integration logic and command routing
- **Voting System**: Democratic proposal voting with JSON persistence
- **Document Discovery**: Cross-branch content analysis and summarization
- **Command Forwarding**: Transparent routing to docs-cli and docs-context

#### 2. SkogCLI Wrapper (`/home/skogix/.config/skogcli/scripts/docs.py`)
- **Purpose**: SkogCLI script interface registration
- **Function**: Bridges SkogCLI script system to main integration
- **Invocation**: `skogcli script run docs [commands]`

#### 3. docs-cli Extension (`/home/skogix/SkogAI/docs/democracy/scripts/extensions/skogcli.sh`)
- **Purpose**: Enables SkogCLI commands from docs-cli
- **Function**: Reverse integration for bidirectional access
- **Invocation**: `docs-cli skogcli [commands]`

#### 4. Repository Management (`/home/skogix/SkogAI/docs/democracy/scripts/docs-cli`)
- **Purpose**: Core git repository operations
- **Features**: Branch management, commits, history, file operations
- **Integration**: Seamlessly accessed through SkogCLI interface

### Data Flow

```
User Command → SkogCLI → Integration Layer → Target System
     ↑              ↓         ↓                ↓
   Output ←    Processing ← Response ←   docs-cli/context
```

### File Structure
```
/home/skogix/.config/skogcli/
├── misc/
│   ├── docs.py                    # Main integration script
│   ├── docs_votes.json           # Voting system data
│   └── docs-integration-README.md # Setup documentation
├── scripts/
│   └── docs.py                   # SkogCLI wrapper script
└── [other SkogCLI files]

/home/skogix/SkogAI/docs/democracy/scripts/
├── docs-cli                      # Core repository management
├── docs-context                  # Context generation tool
├── extensions/
│   └── skogcli.sh               # Reverse integration
└── README.md
```

## Installation & Setup

### Prerequisites
- SkogCLI framework installed and configured
- Access to SkogAI docs repository at `~/SkogAI/docs/democracy/`
- Python 3.8+ for integration scripts
- Git for repository operations

### Current Installation Status
The integration is **already installed** and configured. All components are in place:

✅ Main integration script: `/home/skogix/.config/skogcli/misc/docs.py`
✅ SkogCLI wrapper: `/home/skogix/.config/skogcli/scripts/docs.py`
✅ Extension system: `/home/skogix/SkogAI/docs/democracy/scripts/extensions/skogcli.sh`
✅ Voting system: `/home/skogix/.config/skogcli/misc/docs_votes.json`

### Verification
Test the installation:

```bash
# Test SkogCLI to docs-cli direction
skogcli script run docs help
skogcli script run docs status

# Test docs-cli to SkogCLI direction (if fully configured)
cd ~/SkogAI/docs/democracy
./scripts/docs-cli skogcli help
```

### Optional: Complete Bidirectional Setup
To enable full bidirectional integration, add this to `/home/skogix/SkogAI/docs/democracy/scripts/docs-cli`:

```bash
skogcli)
  if [ -f "$REPO_ROOT/scripts/extensions/skogcli.sh" ]; then
    "$REPO_ROOT/scripts/extensions/skogcli.sh" "${@:2}"
  else
    echo "Error: skogcli extension not found"
  fi
  ;;
```

## Command Reference

### Primary Access Methods

#### Via SkogCLI (Recommended)
```bash
skogcli script run docs [command] [arguments]
```

#### Via docs-cli (If bidirectional setup complete)
```bash
cd ~/SkogAI/docs/democracy
./scripts/docs-cli skogcli [command] [arguments]
```

### Core Repository Commands

#### `status`
Shows git status of the docs repository.
```bash
skogcli script run docs status
```
**Output**: Concise git status with modified, added, and untracked files.

#### `last`
Displays the most recent commit information.
```bash
skogcli script run docs last
```
**Output**: Commit hash, author, timestamp, and message.

#### `branches`
Lists all available branches with current branch indicator.
```bash
skogcli script run docs branches
```
**Output**: Branch list with `*` marking current branch.

#### `branch`
Shows only the current branch name.
```bash
skogcli script run docs branch
```

#### `checkout <branch>`
Switches to specified branch.
```bash
skogcli script run docs checkout feature-branch
skogcli script run docs checkout main
```

#### `history [N]`
Shows last N commits (default: 5).
```bash
skogcli script run docs history        # Last 5 commits
skogcli script run docs history 10     # Last 10 commits
```

#### `diff [file]`
Shows changes in repository or specific file.
```bash
skogcli script run docs diff                    # All changes
skogcli script run docs diff README.md          # Specific file
```

#### `show <commit> [file]`
Displays file contents at specific commit.
```bash
skogcli script run docs show abc123f            # Entire commit
skogcli script run docs show abc123f README.md  # Specific file at commit
```

#### `view <file>`
Views current content of a file.
```bash
skogcli script run docs view workflows/pr-process.md
```

#### `ls [directory]`
Lists files in repository directory.
```bash
skogcli script run docs ls                      # Root directory
skogcli script run docs ls workflows            # Specific directory
```

### Proposal Management Commands

#### `create-proposal <name>`
Creates new proposal branch with standardized naming.
```bash
skogcli script run docs create-proposal context-system
skogcli script run docs create-proposal voting-reform
```

#### `create-draft <name>`
Creates new draft branch for work-in-progress.
```bash
skogcli script run docs create-draft experimental-feature
```

#### `commit [message]`
Adds all files and commits with message.
```bash
skogcli script run docs commit                                    # Default message
skogcli script run docs commit "Add documentation for context system"
```

### Meta Commands

#### `summarize`
Provides comprehensive repository state summary.
```bash
skogcli script run docs summarize
```

#### `quickstart`
Shows quickstart guide for new or reset agents.
```bash
skogcli script run docs quickstart
```

#### `context`
Generates repository context using docs-context tool.
```bash
skogcli script run docs context
```

#### `help`
Shows complete command reference.
```bash
skogcli script run docs help
```

## Voting System

The integration includes a sophisticated democratic voting system for proposal management.

### Voting Data Structure
Votes are stored in `/home/skogix/.config/skogcli/misc/docs_votes.json`:

```json
{
  "votes": {
    "proposal-name": {
      "upvotes": 2,
      "downvotes": 0,
      "history": [
        {
          "timestamp": "2025-04-14T11:51:53.460310",
          "user": "skogix",
          "vote": "+1"
        }
      ]
    }
  }
}
```

### Voting Commands

#### `vote <proposal-name>`
Records a positive vote (+1) for a proposal.
```bash
skogcli script run docs vote cli-integration
skogcli script run docs vote context-system
```

**Features**:
- Automatic proposal initialization if doesn't exist
- Timestamp and user tracking
- Immediate score display

#### `novote <proposal-name>`
Records a negative vote (-1) against a proposal.
```bash
skogcli script run docs novote problematic-proposal
```

#### `votes [proposal-name]`
Displays voting results.
```bash
skogcli script run docs votes                    # All proposals
skogcli script run docs votes cli-integration    # Specific proposal
```

**Output Examples**:
```
# All proposals view
Votes for all proposals:
  cli-integration: 2 (+2 / -0)
  Persona-Consistency: 1 (+1 / -0)
  Capability-Markers: 1 (+1 / -0)

# Specific proposal view
Votes for proposal 'cli-integration':
Upvotes: 2
Downvotes: 0
Vote history:
  2025-04-14T11:51:53.460310 - skogix: +1
  2025-04-14T12:31:56.235980 - skogix: +1
```

### Current Voting Status
Based on existing data:
- **cli-integration**: 2 upvotes, 0 downvotes ✅
- **Persona-Consistency**: 1 upvote, 0 downvotes ✅
- **Capability-Markers**: 1 upvote, 0 downvotes ✅

## Document Discovery

The integration provides powerful cross-branch document discovery capabilities.

### Discovery Commands

#### `motions`
Finds and summarizes all motion documents across all branches.
```bash
skogcli script run docs motions
```

**Features**:
- Searches for files matching `*motion*.md` pattern
- Extracts document titles and summaries
- Shows branch, path, and content preview
- Automatically restores original branch

#### `proposals`
Discovers all proposal documents across branches.
```bash
skogcli script run docs proposals
```

**Features**:
- Identifies files in proposal branches or with "proposal" in path
- Filters for `/draft/` directories
- Provides content summaries

#### `markdown`
Lists all significant markdown files across all branches.
```bash
skogcli script run docs markdown
```

**Features**:
- Discovers all `.md` files across branches
- Excludes noise files (README.md, quickstart.md, cache files)
- Extracts titles from `# Heading` syntax
- Provides first paragraph summaries

### Discovery Output Format
```
=== Motion Documents Across All Branches ===

Branch: feature-context
  - Context System Motion
    A motion to implement a unified context generation system for documentation workflows.
    Path: /home/skogix/SkogAI/docs/democracy/motions/context-system-motion.md

Branch: proposal-voting
  - Democratic Voting Motion
    Establishes voting procedures for proposal acceptance and rejection.
    Path: /home/skogix/SkogAI/docs/democracy/motions/voting-motion.md
```

### Discovery Algorithm
1. **Branch Enumeration**: Gets all branches using `docs-cli branches`
2. **Sequential Checkout**: Safely switches to each branch
3. **File Discovery**: Uses `find` with pattern matching and exclusions
4. **Content Analysis**: Extracts titles and summaries from markdown
5. **Result Aggregation**: Organizes by branch with title/summary/path
6. **Branch Restoration**: Returns to original branch

## Usage Examples

### Daily Workflow Examples

#### Check Repository Status
```bash
# Quick status check
skogcli script run docs status

# Detailed history review
skogcli script run docs history 10

# Current branch confirmation
skogcli script run docs branch
```

#### Proposal Workflow
```bash
# Create new proposal
skogcli script run docs create-proposal agent-coordination

# Work on files, then commit
skogcli script run docs commit "Add agent coordination proposal"

# Vote on the proposal
skogcli script run docs vote agent-coordination

# Check voting status
skogcli script run docs votes agent-coordination
```

#### Content Discovery
```bash
# Find all existing proposals
skogcli script run docs proposals

# Look for motion documents
skogcli script run docs motions

# General content overview
skogcli script run docs markdown
```

#### Context Generation
```bash
# Generate current context
skogcli script run docs context

# Get repository summary
skogcli script run docs summarize
```

### Advanced Workflows

#### Cross-Branch Analysis
```bash
# Discover content across all branches
skogcli script run docs markdown

# Find specific motion documents
skogcli script run docs motions

# Review voting patterns
skogcli script run docs votes
```

#### Repository Maintenance
```bash
# Check all branches
skogcli script run docs branches

# Review recent activity
skogcli script run docs history 20

# Check for uncommitted changes
skogcli script run docs status
```

## Configuration Files

### Primary Configuration Files

#### `/home/skogix/.config/skogcli/misc/docs_votes.json`
**Purpose**: Persistent voting data storage
**Format**: JSON with votes, history, and metadata
**Auto-created**: Yes, on first vote

**Structure**:
```json
{
  "votes": {
    "proposal-name": {
      "upvotes": 0,
      "downvotes": 0,
      "history": [
        {
          "timestamp": "ISO-8601-timestamp",
          "user": "username",
          "vote": "+1|-1"
        }
      ]
    }
  }
}
```

#### `/home/skogix/.config/skogcli/misc/docs-integration-README.md`
**Purpose**: Setup and maintenance documentation
**Content**: Installation instructions, usage examples, maintenance procedures

### Path Configuration

#### Repository Paths
```python
# Main integration script paths
DOCS_CLI_PATH = "~/SkogAI/docs/democracy/scripts/docs-cli"
DOCS_CONTEXT_PATH = "~/SkogAI/docs/democracy/scripts/docs-context"
VOTES_PATH = "~/.config/skogcli/misc/docs_votes.json"
```

#### Repository Root
```bash
# docs-cli script configuration
REPO_ROOT="$HOME/SkogAI/docs/democracy/"
```

### Integration Points

#### SkogCLI Script Registration
Location: `/home/skogix/.config/skogcli/scripts/docs.py`
Accessible via: `skogcli script run docs [command]`

#### Extension Registration
Location: `/home/skogix/SkogAI/docs/democracy/scripts/extensions/skogcli.sh`
Accessible via: `docs-cli skogcli [command]` (when configured)

## Troubleshooting

### Common Issues

#### 1. Command Not Found
**Problem**: `skogcli script run docs` returns "script not found"
**Solution**:
```bash
# Verify script exists
ls -la /home/skogix/.config/skogcli/scripts/docs.py

# Check permissions
chmod +x /home/skogix/.config/skogcli/scripts/docs.py
```

#### 2. Repository Access Issues
**Problem**: "Could not change to repository directory"
**Solution**:
```bash
# Verify repository path
ls -la ~/SkogAI/docs/democracy/

# Check git repository status
cd ~/SkogAI/docs/democracy && git status
```

#### 3. Voting System Issues
**Problem**: Votes not persisting or JSON errors
**Solution**:
```bash
# Check votes file
cat /home/skogix/.config/skogcli/misc/docs_votes.json

# Reset votes file if corrupted
echo '{"votes": {}}' > /home/skogix/.config/skogcli/misc/docs_votes.json
```

#### 4. Permission Errors
**Problem**: Permission denied when accessing files
**Solution**:
```bash
# Fix script permissions
chmod +x /home/skogix/.config/skogcli/scripts/docs.py
chmod +x /home/skogix/.config/skogcli/misc/docs.py

# Fix directory permissions
chmod 755 /home/skogix/.config/skogcli/misc/
```

### Debug Commands

#### Test Integration Components
```bash
# Test main integration script directly
python3 /home/skogix/.config/skogcli/misc/docs.py help

# Test SkogCLI wrapper
skogcli script run docs help

# Test docs-cli access
cd ~/SkogAI/docs/democracy && ./scripts/docs-cli help
```

#### Verify File Paths
```bash
# Check all integration files exist
ls -la /home/skogix/.config/skogcli/misc/docs.py
ls -la /home/skogix/.config/skogcli/scripts/docs.py
ls -la /home/skogix/SkogAI/docs/democracy/scripts/docs-cli
ls -la /home/skogix/SkogAI/docs/democracy/scripts/extensions/skogcli.sh
```

#### Validate JSON Data
```bash
# Check votes file syntax
python3 -m json.tool /home/skogix/.config/skogcli/misc/docs_votes.json
```

### Recovery Procedures

#### Reset Voting System
```bash
# Backup existing votes
cp /home/skogix/.config/skogcli/misc/docs_votes.json \
   /home/skogix/.config/skogcli/misc/docs_votes.json.backup

# Reset to clean state
echo '{"votes": {}}' > /home/skogix/.config/skogcli/misc/docs_votes.json
```

#### Reinstall Integration
```bash
# Navigate to integration directory
cd /home/skogix/.config/skogcli/misc/

# Verify main integration script
python3 docs.py help

# Verify wrapper script
cd ../scripts/
python3 docs.py help
```

---

## Conclusion

The SkogCLI-Docs Integration provides a comprehensive, bidirectional bridge between SkogCLI and the SkogAI documentation repository management system. With its unified command interface, democratic voting system, and powerful document discovery capabilities, it enables efficient collaboration and content management across the entire SkogAI documentation ecosystem.

### Key Benefits
- **Unified Interface**: Single command-line access point for all documentation operations
- **Democratic Process**: Built-in voting system for transparent proposal management
- **Cross-Branch Intelligence**: Automated content discovery across all repository branches
- **Seamless Integration**: Transparent command forwarding between systems
- **Persistent State**: Reliable voting and configuration persistence

### Current Status
- ✅ **Fully Installed**: All components operational
- ✅ **Voting System Active**: 3 proposals with recorded votes
- ✅ **Document Discovery**: Cross-branch analysis ready
- ✅ **Repository Operations**: Full git workflow support

The integration successfully fulfills Amy Ravenwolf's motion requirements and provides a robust foundation for collaborative documentation management within the SkogAI ecosystem.
