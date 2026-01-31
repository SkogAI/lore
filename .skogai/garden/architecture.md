---
title: "Garden Plugin System: Trial-Based Plugin Evaluation Framework"
problem_type: architecture
solution_category: plugin-lifecycle-management
created_date: "2026-01-05"
session_context: "Phase 1 Planning - Lore Integration Project"
author: "SkogAI Agent System"
tags:
  - plugin-lifecycle
  - trial-system
  - experimental-features
  - state-management
  - decision-tracking
  - phase-gates
  - skogai-architecture
  - claude-code
  - feature-evaluation
  - plugin-discovery
---

# Garden Plugin System: Trial-Based Plugin Evaluation Framework

> **Philosophy:** "Start small, add complexity only after testing and seeing actual need."

The Garden Plugin System is a trial-based evaluation framework that manages the lifecycle of experimental components (skills, plugins, guardrails) through evidence-based promotion to permanent status.

## Problem Statement

Claude Code projects need a systematic way to test experimental features and plugins before committing them permanently. Without a trial framework, adding plugins creates friction:
- Always-on plugins become hard to remove when not useful
- Always-off plugins never get tested long enough for proper evaluation
- No structured decision points leads to plugin drift

## Solution Overview

Garden implements a state-machine approach to plugin evaluation:

```
┌─────────────────────────────────────────────────────────┐
│                    SEED PLUGINS                         │
│              (Always Active - Core, Docs)               │
│                                                         │
│  No decision required. These form the project baseline. │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│                   TRIAL PLUGINS                         │
│            (Under Evaluation - Message Counter)         │
│                                                         │
│  • Added with `/garden:trial <plugin>`                  │
│  • Message counter tracks usage (0-50)                  │
│  • At 50 messages: prompted to KEEP/SWAP/RESET          │
│  • Each decision tracked for learning                   │
└─────────────────────────────────────────────────────────┘
                    ↙          ↓          ↖
              KEEP         RESET         SWAP
               ↓             ↓             ↓
        ┌─────────┐   ┌─────────┐   ┌─────────┐
        │PERMANENT│   │RE-TRIAL │   │REMOVED  │
        │(Promoted│   │(Counter │   │(Tracked │
        │ to stay)│   │  Reset) │   │w/reason)│
        └─────────┘   └─────────┘   └─────────┘
```

## State File Structure

**Location:** `/home/skogix/skogai/config/garden-state.json`

```json
{
  "version": "1.0.0",
  "seed": ["core", "docs"],
  "trials": {
    "plugin-name": {
      "message_count": 23,
      "threshold": 50,
      "started_at": "2026-01-05T15:30:00Z",
      "source": "manual",
      "added_by": "user"
    }
  },
  "permanent": [],
  "removed": {
    "test-plugin": {
      "reason": "testing-cleanup",
      "messages_used": "permanent",
      "removed_at": "2026-01-05T15:51:11Z"
    }
  },
  "settings": {
    "default_trial_threshold": 50,
    "auto_suggest": true,
    "prompt_style": "session-start"
  }
}
```

### Key Fields

| Field | Purpose |
|-------|---------|
| `version` | Schema version for state file |
| `seed` | Immutable, always-active plugins |
| `trials` | Active trial plugins with message counters |
| `permanent` | Promoted plugins that stay |
| `removed` | Historical record with reasons |
| `settings.default_trial_threshold` | Messages before decision prompt (50) |

## Commands Reference

| Command | Effect | Example |
|---------|--------|---------|
| `/garden:status` | Display current state | View seed/trial/permanent/removed |
| `/garden:trial <plugin>` | Move plugin to trial | Start testing new component |
| `/garden:keep <plugin>` | Move from trial to permanent | Plugin proved useful |
| `/garden:swap <old> <new>` | Replace one trial with another | Pivot mid-trial |
| `/garden:reset <plugin>` | Reset message counter | Extend trial period |
| `/garden:remove <plugin>` | Move to removed | Stop using plugin |

## The 50-Message Threshold Philosophy

### Why 50 Messages?

1. **Sufficient Signal**: 50 prompts provide genuine usage data
   - Enough to encounter edge cases
   - Too few: just scratching the surface
   - Too many: wasting trial time

2. **Natural Decision Point**: When to make conscious choices
   - After 50 messages, you've invested enough to have an opinion
   - Prevents plugin drift (forgetting to evaluate)

3. **Reversible**: Can extend with `/garden:reset`
   - Reset adds 50 more messages to threshold
   - Can repeat if still uncertain

### Decision Framework at Threshold

```
Messages 0-15:   "This is new, still figuring it out"
Messages 15-35:  "Getting the hang of it, finding value"
Messages 35-50:  "Ready to decide: is this worth keeping?"
At 50:           PROMPT: Keep? Swap? Reset?
```

## The .skogai Directory Pattern

Garden documentation lives in `.skogai/garden/` following the **meta-project configuration** pattern:

```
.skogai/
├── CLAUDE.md           # Directory index
├── garden/             # Plugin trial system
│   └── README.md       # Quick reference
├── plan/               # Project planning
│   ├── PROJECT.md
│   ├── ROADMAP.md
│   ├── STATE.md
│   └── codebase/       # Codebase analysis
└── todos/              # Task tracking
```

### Pattern Benefits

- **Separation of concerns**: Main codebase vs project metadata
- **Scalable**: New meta-projects don't pollute project root
- **Discoverable**: `.skogai/CLAUDE.md` acts as portal
- **Maintainable**: Each document has clear audience and scope

## Component Ecosystem Being Managed

### Local Skills (`.claude/skills/`)

| Skill | Purpose | Status |
|-------|---------|--------|
| `lore-creation-starting-skill` | Structured knowledge documentation | Trial |
| `skogai-jq` | 60+ JSON transformations | Trial |
| `skogai-argc` | CLI framework integration | Trial |

### skogai-core Plugin

**19 commands** across categories:
- Project lifecycle: `new-project`, `create-roadmap`, `map-codebase`
- Phase management: `plan-phase`, `execute-plan`, `research-phase`
- Milestone tracking: `new-milestone`, `complete-milestone`, `progress`
- Workflow helpers: `pause-work`, `resume-work`

**4 workflows**: `/workflows:plan`, `/workflows:work`, `/workflows:review`, `/workflows:compound`

### Hookify Guardrails (`.claude/*.local.md`)

| Guard | Action | Protects Against |
|-------|--------|------------------|
| `block-git-push-force` | Block | Remote history rewriting |
| `block-git-reset-hard` | Block | Data loss from hard reset |
| `warn-diff-before-commit` | Warn | Committing without review |
| `warn-git-reset` | Warn | Accidental reset |

## Evaluation Criteria

### When to KEEP (Promote to Permanent)

- [ ] Actually used in daily work (not just available)
- [ ] Solves a real problem (not nice-to-have)
- [ ] Fits naturally with existing tools
- [ ] Documentation is clear and complete
- [ ] No major friction or errors encountered

### When to SWAP

- [ ] Different approach seems better
- [ ] Current plugin partially works
- [ ] Clearer alternative available
- [ ] Worth pivoting to compare

### When to REMOVE

- [ ] Barely used or abandoned
- [ ] Causes frequent errors
- [ ] Better alternative exists
- [ ] Scope doesn't match project needs

## Implementation Details

### Message Counting

The `UserPromptSubmit` hook increments trial counters:

```bash
# Hook triggered on each user message
# Increments message_count for all active trials
```

### Expiration Detection

The `SessionStart` hook checks for expired trials:

```bash
# On session start, checks trials at or above threshold
# Prompts user for keep/swap/reset decision
```

### Atomic State Updates

All state changes use temp file + mv pattern for atomicity:

```bash
# Write to temp file
echo "$new_state" > /tmp/garden-state.tmp
# Atomic move
mv /tmp/garden-state.tmp "$STATE_FILE"
```

## Related Documentation

- **Quick reference**: `@.skogai/garden/README.md`
- **Directory overview**: `@.skogai/CLAUDE.md`
- **Current understanding**: `@docs/CURRENT_UNDERSTANDING.md` (Section 6)
- **Best practices**: `@.skogai/garden/best-practices.md`
- **Decision framework**: `@.skogai/garden/decision-framework.md`

## Verification Status

- [x] `/garden:status` command displays formatted state
- [x] State file initialization via `init-garden.sh`
- [x] Message counting via `UserPromptSubmit` hook
- [x] Expiration detection via `SessionStart` hook
- [x] Trial management commands (trial, keep, swap, reset, remove)
- [x] Decision tracking persists across sessions

## Known Limitations

- Phase 3 (auto-decisions, analytics) not yet implemented
- Learning patterns from decision history not yet extracted
- Cross-project garden state sharing not yet designed

---

**Last Updated:** 2026-01-05
**Garden Plugin Version:** 0.0.3
