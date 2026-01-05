# feat: Document Garden Plugin System and Trial Components

## Overview

Update CLAUDE.md and related documentation to explain:
1. The **Garden Plugin System** - plugin trial management for Claude Code
2. **Local Skills** being trialed in `.claude/skills/`
3. **skogai-core plugin components** being evaluated (commands, references, templates, workflows)

Philosophy: **Start small, add complexity only after testing and proven need.**

## Problem Statement / Motivation

Current documentation doesn't explain:
- What the garden plugin system is and why it exists
- How plugins are trialed vs kept permanently
- The experimental `.claude/skills/` components in the lore repo
- The skogai-core plugin's command/workflow system being evaluated

Users (including future Claude sessions) need clarity on:
- What's stable vs what's being trialed
- How to use the garden system
- What the local skills do and their status

## Proposed Solution

Add a new "Plugin Garden & Experimental Components" section to CLAUDE.md that documents:

1. **Garden Plugin System** (MVP - currently implemented)
   - Purpose: Trial plugins before committing permanently
   - State file: `/home/skogix/skogai/config/garden-state.json`
   - Commands: `/garden:status`
   - Philosophy: 50-message trial threshold, then decide

2. **Local Skills** (being trialed in this repo)
   - `lore-creation-starting-skill` - Guidance for structured documentation
   - `skogai-jq` - 60+ JSON transformations for AI agents
   - `skogai-argc` - Argc CLI framework integration

3. **skogai-core Plugin Components** (being evaluated)
   - `commands/skogai/` - 19 project management commands
   - `commands/workflows/` - 4 workflow commands (plan, work, review, compound)
   - `references/` - 9 reference documents
   - `templates/` - 13 project templates
   - `workflows/` - 13 workflow definitions

4. **Hookify Guardrails** (active safety measures)
   - Block: git push --force, git reset --hard
   - Warn: git commit without diff review, git reset

## Technical Approach

### Phase 1: CLAUDE.md Update

Add new section after "Session Memories" (around line 810):

```markdown
## Plugin Garden & Experimental Components

**Philosophy:** Start small, add complexity only after testing and seeing actual need.

### Garden Plugin System

The garden plugin manages plugin trials - test plugins before permanently adding them.

**State File:** `/home/skogix/skogai/config/garden-state.json`

**Structure:**
- `seed` - Plugins always active (core, docs)
- `trials` - Plugins being tested (message counter tracks usage)
- `permanent` - Promoted plugins (kept after trial)
- `removed` - Dropped plugins (tracked with reason)

**Commands:**
- `/garden:status` - View current garden state
- `/garden:status --json` - Raw JSON output

**Trial Flow:**
1. Add plugin to trial
2. Each message increments counter
3. After 50 messages, prompted to decide: keep/swap/reset
4. Decisions tracked for learning

### Local Skills (`.claude/skills/`)

Three skills being trialed in this repository:

| Skill | Purpose | Status |
|-------|---------|--------|
| `lore-creation-starting-skill` | Guidance for structured knowledge documentation | Trial |
| `skogai-jq` | 60+ JSON transformations optimized for AI agents | Trial |
| `skogai-argc` | Argc CLI framework integration | Trial |

**skogai-jq highlights:**
- Schema-driven discovery (AI finds transformations via schemas)
- CRUD, array, string, validation, extraction operations
- Each transformation: `transform.jq` + `schema.json` + `test.sh`

**skogai-argc highlights:**
- Converts bash comments to CLI argument parsing
- 14 example scripts demonstrating features
- Critical: Use `argc --argc-eval` to understand generated code

### skogai-core Plugin (Evaluating)

The skogai-core plugin provides project management workflows. Being evaluated for adoption.

**Commands (`commands/skogai/`):**
- Project lifecycle: `new-project`, `create-roadmap`, `map-codebase`
- Phase management: `plan-phase`, `execute-plan`, `research-phase`
- Milestone tracking: `new-milestone`, `complete-milestone`, `progress`
- Workflow helpers: `pause-work`, `resume-work`, `auto`

**Workflows (`commands/workflows/`):**
- `/workflows:plan` - Transform feature descriptions into structured plans
- `/workflows:work` - Execute work plans efficiently
- `/workflows:review` - Multi-agent code review
- `/workflows:compound` - Document solved problems

**References (`references/`):**
- `plan-format.md` - Plan document structure
- `research-pitfalls.md` - Common research mistakes
- `tdd.md` - Test-driven development guidance
- `principles.md` - Core working principles

**Templates (`templates/`):**
- `project.md`, `roadmap.md`, `milestone.md` - Project planning
- `research.md`, `discovery.md` - Investigation templates
- `state.md`, `context.md` - Session continuity

### Hookify Guardrails (`.claude/*.local.md`)

Safety guardrails learned from previous sessions:

| File | Action | Purpose |
|------|--------|---------|
| `hookify.block-git-push-force.local.md` | Block | Prevent history rewriting |
| `hookify.block-git-reset-hard.local.md` | Block | Prevent data loss |
| `hookify.warn-diff-before-commit.local.md` | Warn | Ensure diff review |
| `hookify.warn-git-reset.local.md` | Warn | Confirm reset intent |

### Evaluation Criteria

Components move from "trial" to "permanent" when:
1. **Proven useful** - Actually used in daily work
2. **Well understood** - Documentation explains purpose
3. **Tested** - Edge cases handled, bugs fixed
4. **Integrated** - Works with existing tools

Components get removed when:
- Not used after trial period
- Causes friction/complexity
- Better alternative exists
```

### Phase 2: Update Current Data Stats

Update the statistics in CLAUDE.md (line ~95-101) to reflect current counts and add garden state:

```markdown
**Current Data:**

- 88 books
- 368 entries
- 53 personas

**Garden State:**
- Seed plugins: core, docs
- Trial plugins: 0
- Permanent plugins: 0

*(Last updated: 2026-01-05)*
```

### Phase 3: Create Garden README

Create `/home/skogix/lore/docs/GARDEN.md` with detailed garden documentation:

```markdown
# Plugin Garden System

The garden manages plugin lifecycle through trial-based evaluation.

## Philosophy

> "Start small, add complexity only after testing and seeing actual need."

## Quick Start

```bash
# Check garden status
/garden:status

# View raw state
/garden:status --json
```

## State Structure

Location: `/home/skogix/skogai/config/garden-state.json`

```json
{
  "version": "1.0.0",
  "seed": ["core", "docs"],
  "trials": {},
  "permanent": [],
  "removed": {},
  "settings": {
    "default_trial_threshold": 50,
    "auto_suggest": true,
    "prompt_style": "session-start"
  }
}
```

## Lifecycle

1. **Seed** - Always active (never removed)
2. **Trial** - Being tested (50-message default threshold)
3. **Permanent** - Promoted after successful trial
4. **Removed** - Dropped with tracked reason

## Future Commands (Planned)

- `/garden:trial <plugin>` - Start trialing a plugin
- `/garden:keep <plugin>` - Promote to permanent
- `/garden:swap <old> <new>` - Replace trial plugin
- `/garden:reset <plugin>` - Extend trial period
```

## Acceptance Criteria

### Functional Requirements
- [ ] CLAUDE.md has new "Plugin Garden & Experimental Components" section
- [ ] Garden system purpose and usage documented
- [ ] All 3 local skills documented with status
- [ ] skogai-core plugin components listed
- [ ] Hookify guardrails explained
- [ ] Evaluation criteria stated

### Documentation Quality
- [ ] Follows existing CLAUDE.md conventions (warning blocks, tables, code examples)
- [ ] Uses @ symbol references for paths
- [ ] Includes timestamps for versioning
- [ ] Explains "why" not just "what"

## Files to Modify

1. **`CLAUDE.md`** (primary)
   - Add new section after "Session Memories" (~line 810)
   - Update "Current Data" stats (~line 95)

2. **`docs/GARDEN.md`** (new file)
   - Detailed garden documentation
   - Future command reference

3. **`docs/CURRENT_UNDERSTANDING.md`** (update)
   - Add garden system to "What Has Been Verified" section

## Success Metrics

- Future Claude sessions understand garden without asking
- Plugin trial decisions get documented
- Local skills have clear status (trial vs permanent)
- Hookify guardrails prevent repeated mistakes

## References

### Internal
- Garden state: `/home/skogix/skogai/config/garden-state.json`
- Garden scripts: `~/.claude/plugins/cache/skogai-marketplace/garden/0.0.1/scripts/`
- Local skills: `/home/skogix/lore/.claude/skills/`
- skogai-core: `~/.claude/plugins/cache/skogai-marketplace/skogai-core/0.0.2/.claude/`

### External
- Garden plugin source: skogai-marketplace/plugins/garden/
- skogai-core source: skogai-marketplace/plugins/skogai-core/
