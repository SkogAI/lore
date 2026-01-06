---
status: complete
priority: p2
issue_id: "002"
tags: [garden, documentation, claude-md, skills]
dependencies: []
---

# Document Garden Plugin System and Trial Components

## Problem Statement

Documentation needed to explain:
- What the garden plugin system is and why it exists
- How plugins are trialed vs kept permanently
- The experimental `.claude/skills/` components in the lore repo
- The skogai-core plugin's command/workflow system being evaluated

Users (including future Claude sessions) need clarity on:
- What's stable vs what's being trialed
- How to use the garden system
- What the local skills do and their status

## Findings

**Garden system components identified:**
- State file: `/home/skogix/skogai/config/garden-state.json`
- Structure: seed, trials, permanent, removed
- 50-message trial threshold with decision prompts
- Phase 1 & 2 commands implemented

**Local skills in `.claude/skills/`:**
- `lore-creation-starting-skill` - Structured documentation guidance
- `skogai-jq` - 60+ JSON transformations (schema-driven)
- `skogai-argc` - Argc CLI framework integration

**skogai-core plugin:**
- 19 project management commands
- 4 workflow commands (plan, work, review, compound)
- 9 reference documents
- 13 project templates

## Proposed Solutions

### Option 1: Comprehensive Documentation (Selected)
Create consolidated documentation in `.skogai/garden/` with:
- Quick reference README
- Implementation summary (START HERE entry point)
- Best practices guide
- Decision framework
- Directory template
- Architecture reference

**Effort:** Medium
**Risk:** Low

## Recommended Action

**COMPLETED - Documentation consolidated in `.skogai/garden/`**

## Acceptance Criteria

- [x] CLAUDE.md has "Plugin Garden" section referencing documentation
- [x] Garden system purpose and usage documented
- [x] All 3 local skills documented with status
- [x] skogai-core plugin components listed
- [x] Hookify guardrails explained
- [x] Evaluation criteria stated
- [x] Documentation follows existing CLAUDE.md conventions
- [x] Uses @ symbol references for paths
- [x] Explains "why" not just "what"

## Technical Details

**Files created:**
- `.skogai/garden/README.md` - Quick reference
- `.skogai/garden/implementation-summary.md` - 30-minute overview
- `.skogai/garden/best-practices.md` - Comprehensive guide
- `.skogai/garden/decision-framework.md` - Strategic patterns
- `.skogai/garden/directory-template.md` - Setup templates
- `.skogai/garden/architecture.md` - Technical reference

**Files modified:**
- `CLAUDE.md` - Added garden section and current data stats
- `docs/CURRENT_UNDERSTANDING.md` - Added garden to verified components
- `.skogai/CLAUDE.md` - Added garden documentation table

## Work Log

### 2026-01-05 - Initial Planning
**By:** Claude Code

**Actions:**
- Analyzed garden plugin system architecture
- Identified all components needing documentation
- Created comprehensive documentation plan

### 2026-01-05 - Documentation Complete
**By:** Claude Code

**Actions:**
- Created 6 documentation files in `.skogai/garden/`
- Updated CLAUDE.md with garden section
- Updated docs/GARDEN.md as hub/redirect
- Consolidated all cross-references
- Verified garden state shows clean testing history

**Learnings:**
- Documentation organization follows progressive disclosure pattern
- `.skogai/` is the canonical location for project-level config
- Garden implements "start small" philosophy effectively

### 2026-01-05 - Migrated to todos system
**By:** Claude Code

**Actions:**
- Migrated from `plans/docs-claude-md-garden-update.md` to `.skogai/todos/`
- Marked as complete - all acceptance criteria met
- Original plans/ file removed
