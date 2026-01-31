# Plugin Garden & Experimental Components

**Philosophy:** Start small, add complexity only after testing and seeing actual need.

## Garden Plugin System

The garden plugin manages plugin trials - test plugins before permanently adding them.

**State File:** `/home/skogix/skogai/config/garden-state.json`

**Structure:**
- `seed` - Plugins always active (core, docs)
- `trials` - Plugins being tested (message counter tracks usage)
- `permanent` - Promoted plugins (kept after trial)
- `removed` - Dropped plugins (tracked with reason)

### Commands (Phase 1 & 2)

| Command | Purpose |
|---------|---------|
| `/garden:status` | View current garden state |
| `/garden:status --json` | Raw JSON output |
| `/garden:trial <plugin>` | Start trialing a plugin |
| `/garden:keep <plugin>` | Promote trial to permanent |
| `/garden:swap <old> <new>` | Replace one trial with another |
| `/garden:reset <plugin>` | Extend trial (reset counter) |
| `/garden:remove <plugin>` | Remove from trial/permanent |

### Trial Flow

1. Add plugin to trial
2. Each message increments counter
3. After 50 messages, prompted to decide: keep/swap/reset
4. Decisions tracked for learning

## Local Skills (`.claude/skills/`)

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

## skogai-core Plugin (Evaluating)

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

## Hookify Guardrails (`.claude/*.local.md`)

Safety guardrails learned from previous sessions:

| File | Action | Purpose |
|------|--------|---------|
| `hookify.block-git-push-force.local.md` | Block | Prevent history rewriting |
| `hookify.block-git-reset-hard.local.md` | Block | Prevent data loss |
| `hookify.warn-diff-before-commit.local.md` | Warn | Ensure diff review |
| `hookify.warn-git-reset.local.md` | Warn | Confirm reset intent |

## Evaluation Criteria

Components move from "trial" to "permanent" when:
1. **Proven useful** - Actually used in daily work
2. **Well understood** - Documentation explains purpose
3. **Tested** - Edge cases handled, bugs fixed
4. **Integrated** - Works with existing tools

Components get removed when:
- Not used after trial period
- Causes friction/complexity
- Better alternative exists

## Related Files

- **Architecture docs**: `@.skogai/garden/architecture.md`
- **Best practices**: `@.skogai/garden/best-practices.md`
- **Decision framework**: `@.skogai/garden/decision-framework.md`
- **Implementation summary**: `@.skogai/garden/implementation-summary.md`
- **Directory template**: `@.skogai/garden/directory-template.md`
- **State**: `/home/skogix/skogai/config/garden-state.json`
- **Scripts**: `~/.claude/plugins/cache/skogai-marketplace/garden/*/scripts/`
- **Plugin Source**: skogai-marketplace/plugins/garden/
