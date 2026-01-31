# Garden Plugin System: Best Practices and Prevention Strategies

> **Philosophy:** "Start small, add complexity only after testing and seeing actual need."

This document provides comprehensive guidance for implementing and maintaining the Garden Plugin System across projects. It covers project structure, trial evaluation, documentation patterns, and decision-making frameworks.

---

## Part 1: Project Structure for Garden Systems

### 1.1 Directory Organization Pattern

The optimal `.skogai/` structure balances trial management, planning, and task tracking:

```
.skogai/
├── garden/
│   ├── README.md              # Garden system documentation
│   ├── evaluation-criteria.md # How plugins move through states
│   └── trial-log.md           # Decisions and outcomes
├── plan/
│   ├── PROJECT.md             # Project vision and requirements
│   ├── ROADMAP.md             # Milestone phases and timeline
│   ├── phases/                # Phase-specific execution plans
│   │   ├── 01-verify-pipeline/
│   │   │   ├── 1-1-PLAN.md   # Detailed execution steps
│   │   │   └── 1-1-CONTEXT.md # Resources and context
│   │   └── 02-quality-prompts/
│   │       ├── 2-1-PLAN.md
│   │       └── 2-1-CONTEXT.md
│   └── codebase/              # Codebase analysis documents
│       ├── STRUCTURE.md       # Architecture overview
│       ├── CONVENTIONS.md     # Code style and patterns
│       ├── STACK.md           # Technology choices
│       ├── ARCHITECTURE.md    # System design
│       ├── INTEGRATIONS.md    # Component interactions
│       ├── TESTING.md         # Test strategy
│       └── CONCERNS.md        # Known issues and risks
├── todos/
│   └── *.md                   # Individual task files
└── CLAUDE.md                  # This directory overview

.claude/
├── skills/
│   ├── lore-creation-starting-skill/  # Trial skills
│   ├── skogai-argc/
│   └── skogai-jq/
└── *.local.md                 # Hookify guardrails
```

**Key Principles:**
- **Separation of Concerns**: Garden system isolated from planning and task tracking
- **Hierarchical Planning**: Project → Roadmap → Phases → Plans
- **Codebase Documentation**: Separate analysis documents for different aspects
- **Scalability**: Structure supports multiple phases without file proliferation

### 1.2 File Organization Best Practices

#### Planning Documents
- **PROJECT.md**: Single source of truth for vision, requirements, scope
  - Maximum 1-2 pages
  - Link to detailed requirements elsewhere, not inline
  - Include success criteria that are testable
  - Update at project start and major pivots only

- **ROADMAP.md**: Phase-by-phase breakdown
  - One entry per phase with clear dependencies
  - Mark urgent insertions as decimal phases (2.1, 2.2)
  - Update phase completion status here
  - 50-100 lines per major milestone

- **Phase-specific Plans**: Deep dives on execution
  - `<PHASE>-PLAN.md` for step-by-step execution
  - `<PHASE>-CONTEXT.md` for resources, dependencies, external references
  - Keep plans focused on one phase only
  - Archive completed plans (don't delete)

- **Codebase Analysis**: Documentation for understanding
  - STRUCTURE.md: What exists (file tree, modules, components)
  - STACK.md: What technologies are used
  - CONVENTIONS.md: How things are done (patterns, naming, style)
  - ARCHITECTURE.md: How things work together (data flow, integration points)
  - INTEGRATIONS.md: How external systems connect
  - TESTING.md: How quality is ensured
  - CONCERNS.md: Known issues, limitations, risks

#### Avoiding Documentation Bloat
- Don't create a `.skogai/docs/` directory (causes duplication)
- Use dedicated subdirectories for analysis (e.g., `plan/codebase/`)
- Link to main docs from `.skogai/` files, don't duplicate
- Archive old planning documents instead of deleting
- Keep README files small and link-heavy

---

## Part 2: Garden Plugin System Deep Dive

### 2.1 State Machine and Lifecycle

The Garden system uses a clear state machine for plugin evaluation:

```
                     ┌─────────────────┐
                     │   SEED PLUGINS  │  Always active
                     │  (core, docs)   │  Can't be removed
                     └─────────────────┘

                            ↓

         Trial Plugin Added via `/garden:trial`
                            ↓
                   ┌──────────────────┐
                   │   TRIAL STATE    │
                   │  (Message counter│
                   │  tracks usage)   │
                   └─────────────────┘
                   /        |        \
                  /         |         \
            At 50 msgs   Not used   Swap for
            Prompt to    →DropOut  another
            decide
                  \         |         /
                   \        |        /
                    ┌───────┴────────┐
                    ↓                ↓
              `/garden:keep`    `/garden:swap`
                    ↓                ↓
          ┌─────────────────┐  ┌──────────────┐
          │  PERMANENT      │  │  REMOVED     │
          │  (Keeps         │  │  (Tracked    │
          │   supporting)   │  │   with       │
          └─────────────────┘  │   reason)    │
                                └──────────────┘
```

**State Transitions:**
- `SEED` → (immutable, always active)
- `TRIAL` → `PERMANENT` (via `/garden:keep`)
- `TRIAL` → `REMOVED` (via `/garden:swap` or end of life)
- `TRIAL` → `TRIAL` (via `/garden:reset` to extend threshold)
- `PERMANENT` → `REMOVED` (via `/garden:remove` with reason)

**Message Counter Logic:**
- Increments per user prompt (not system messages)
- Threshold: 50 messages (configurable via `default_trial_threshold`)
- Counter resets if plugin is updated or trial extended
- Not time-based—based on actual usage

### 2.2 State File Structure

**Location:** `/home/skogix/skogai/config/garden-state.json`

```json
{
  "version": "1.0.0",
  "seed": ["core", "docs"],
  "trials": {
    "plugin-name": {
      "message_count": 23,
      "started_at": "2026-01-05T10:00:00Z",
      "last_used": "2026-01-05T15:30:00Z",
      "notes": "Testing connection pooling improvements"
    }
  },
  "permanent": ["skogai-jq", "skogai-argc"],
  "removed": {
    "old-plugin": {
      "reason": "better-alternative-found",
      "messages_used": 45,
      "removed_at": "2026-01-04T12:00:00Z"
    }
  },
  "settings": {
    "default_trial_threshold": 50,
    "auto_suggest": true,
    "prompt_style": "session-start"
  }
}
```

**Critical Fields:**
- `version`: Semantic versioning for state schema
- `seed`: Immutable list of always-active plugins
- `trials`: Active trial plugins with usage metadata
- `permanent`: Promoted plugins that stay
- `removed`: Historical record of removed plugins with reasons
- `settings.default_trial_threshold`: When to prompt for decision (50 messages default)

### 2.3 The 50-Message Decision Threshold Philosophy

**Why 50 Messages?**

The 50-message threshold serves multiple purposes:

1. **Sufficient Signal**: 50 prompts provide genuine usage data
   - Enough to encounter edge cases
   - Too few: just scratching the surface
   - Too many: wasting trial time on marginal improvements

2. **Context Window**: Matches typical working session length
   - Single session might be 5-10 messages
   - A day's work: 30-50 messages
   - Enough for multi-phase evaluation

3. **Human Decision Point**: When to make conscious choices
   - After 50 messages, you've invested enough to have an opinion
   - Natural decision moment: keep learning or move on
   - Prevents plugin drift (forgetting to evaluate)

4. **Reversible Decisions**: Can extend with `/garden:reset`
   - Reset adds 50 more messages to threshold
   - Can repeat if still uncertain
   - Prevents premature removal

**Practical Guidance:**

```
Messages 0-15:   "This is new, still figuring it out"
Messages 15-35:  "Getting the hang of it, finding value"
Messages 35-50:  "Ready to decide: is this worth keeping?"
At 50:           PROMPT: Keep? Swap? Reset?
After 50:        If reset: 50-100 messages
At 100+:         If still trialing: explicitly justify delay
```

**Decision Framework at Threshold:**

When prompted at 50 messages, ask:
- **Usefulness**: Did I actually use this? (vs. just present)
- **Friction**: Did it solve problems or create them?
- **Learning Curve**: Am I still learning or comfortable?
- **Alternatives**: Is there a better solution?
- **Uncertainty**: Do I need 50 more messages?

### 2.4 Commands Reference

| Command | Purpose | When to Use | Notes |
|---------|---------|------------|-------|
| `/garden:status` | View current state | Every session start | Shows seed, trials, permanent, removed |
| `/garden:trial <plugin>` | Start trial | Adding new component | Message counter begins at 0 |
| `/garden:keep <plugin>` | Promote to permanent | After positive evaluation | Only from trial state |
| `/garden:swap <old> <new>` | Replace trial plugin | Changing approach mid-trial | Both must exist |
| `/garden:reset <plugin>` | Extend trial period | Need more evaluation time | Resets counter to 0 |
| `/garden:remove <plugin>` | Remove entirely | Plugin didn't work out | Requires reason note |

**Command Patterns:**

```bash
# Evaluation workflow
/garden:trial skogai-new-feature
# ... work for 50 messages ...
/garden:status  # Check counter
# If ready: /garden:keep skogai-new-feature
# If uncertain: /garden:reset skogai-new-feature
# If bad: /garden:swap skogai-new-feature skogai-alternative

# Maintenance
/garden:remove skogai-broken-plugin  # Documents removal with reason
```

---

## Part 3: Best Practices Checklist

### 3.1 Starting a New Trial

**Before Starting Trial:**

- [ ] Plugin has clear purpose and scope
- [ ] You've identified what success looks like (testable criteria)
- [ ] You know what failure looks like (when to remove it)
- [ ] You've chosen a 50-message evaluation period
- [ ] Documentation exists (README or wiki for plugin)
- [ ] No circular dependencies with other trial plugins

**Trial Setup Checklist:**

```bash
# 1. Check current status
/garden:status

# 2. Verify plugin doesn't exist
# (if it does, swap for it instead)

# 3. Start trial
/garden:trial my-new-plugin

# 4. Document decision in .skogai/garden/trial-log.md
# Record:
# - Date started
# - Reason for trial
# - Success criteria (testable)
# - Expected duration estimate

# 5. Begin work
```

**Example Trial Log Entry:**

```markdown
## Trial: skogai-new-query-tool
- **Started:** 2026-01-05
- **Reason:** Prototype new JSON query patterns
- **Success Criteria:**
  - Can replace 80% of manual jq calls
  - Performance within 10% of native jq
  - Documentation complete
- **Estimated Duration:** 1 week (50+ messages)
- **Status:** Active (message count: 12/50)
```

### 3.2 During Trial Period

**Weekly Evaluation:**

- [ ] Plugin in active use (not abandoned)
- [ ] Message counter is incrementing
- [ ] No unexpected errors or friction
- [ ] Still relevant to project goals
- [ ] Documentation is staying current

**Red Flags:**

- Message count hasn't changed in 2+ days
- Plugin causes repeated errors
- Better alternative has appeared
- Scope creep beyond initial purpose
- Lack of documentation/examples

**Response to Red Flags:**

- **No usage**: Consider `/garden:swap` if alternative exists
- **Errors**: Debug issues immediately or remove
- **Scope creep**: Reset scope or remove features
- **Documentation gaps**: Add examples before continuing

### 3.3 Making Keep/Swap/Remove Decisions

**Decision Framework at Threshold:**

**KEEP if:**
- [ ] Actually used in daily work (not just available)
- [ ] Solves a real problem (not nice-to-have)
- [ ] Fits naturally with existing tools
- [ ] Documentation is clear and complete
- [ ] No major friction or errors encountered
- [ ] Counterargument: Why would you remove this?

**SWAP if:**
- [ ] Different approach seems better
- [ ] Current plugin partially works
- [ ] Clearer alternative available
- [ ] Worth pivoting to test the alternative
- [ ] Don't remove the current one yet—swap so you can compare

**REMOVE if:**
- [ ] Barely used or abandoned
- [ ] Causes frequent errors
- [ ] Better alternative exists (and you've moved to it)
- [ ] Scope doesn't match project needs
- [ ] Documentation is too complex for value provided
- [ ] Counterargument: Why would you keep this?

**Decision Tracking:**

Document decisions in `.skogai/garden/trial-log.md`:

```markdown
## Completed Trial: skogai-broken-plugin
- **Evaluated:** 2026-01-05 (47 messages)
- **Decision:** REMOVED
- **Reason:** Plugin generated 14 errors, alternative (skogai-better-plugin) works reliably
- **Messages Used:** 47
- **Outcome:** Will trial replacement next week
```

### 3.4 Preventing Common Mistakes

**Prevention Checklist:**

| Mistake | Prevention | Recovery |
|---------|-----------|----------|
| Too many trials at once | Limit to 1-2 concurrent trials | Stop new trials, finish current ones |
| Trial abandoned mid-way | Set 2-week check-in reminders | Use `/garden:swap` to move on |
| Forgetting to document | Update trial-log.md immediately | Backfill from git logs |
| Threshold never reached | Plugin not actually used | Use `/garden:remove` with reason |
| No clear success criteria | Define before `/garden:trial` | Add criteria to trial-log.md retroactively |
| Plugin removed without reason | Require reason in `/garden:remove` | Document retroactively in removed section |
| Circular dependency between plugins | Map dependencies before trials | Ensure plugins work independently |
| Scope creep during trial | Review scope weekly | Reset scope or split into separate plugins |
| No documentation | Add docs before declaring success | Make docs completion a success criterion |
| Permanent plugin doesn't get used | Periodic audit of permanent plugins | Remove unused ones with honest reason |

**Preventing Plugin Bloat:**

- Audit permanent plugins quarterly
- Remove plugins not used in 3+ months (document reason)
- Don't keep "just in case" plugins
- Prefer consolidating related plugins to adding new ones

---

## Part 4: Documentation Organization Patterns

### 4.1 Garden System Documentation Structure

Within `.skogai/garden/`:

```
garden/
├── README.md
│   └── Quick reference: what is the garden, commands summary
├── evaluation-criteria.md
│   └── How plugins move between states (conceptual)
├── trial-log.md
│   └── Historical record of all trial decisions
└── decision-framework.md (optional)
    └── How to make keep/swap/remove decisions
```

**README.md (100-150 lines)**
- What the garden system is (1-2 paragraphs)
- Quick command reference table
- Link to full documentation
- Current state summary (seed, trials, permanent, removed)

**evaluation-criteria.md (200-300 lines)**
- State machine diagram
- When to use each command
- Message threshold explanation
- Decision framework
- Link back to this best practices document

**trial-log.md (grows over time)**
- Chronological record of all trial decisions
- Searchable by plugin name
- Includes reason for each decision
- Messages used and date completed

**Example trial-log.md:**

```markdown
# Garden Trial Log

## Active Trials

### skogai-new-query (Started 2026-01-05)
- Purpose: Prototype query patterns
- Status: Active
- Messages: 23/50
- Notes: Working well, found 3 edge cases

## Completed Trials

### skogai-test-framework (2025-12-15)
- Decision: KEEP
- Messages Used: 48
- Reason: Improved test reliability by 40%

### skogai-old-tool (2025-12-01)
- Decision: REMOVE
- Messages Used: 12
- Reason: Alternative (skogai-new-tool) better
```

### 4.2 Avoiding Documentation Anti-Patterns

**Anti-Pattern 1: Monolithic GARDEN.md**
```
❌ Bad: Single 2000-line file covering everything
✅ Good: README.md (100 lines) linking to evaluation-criteria.md
```

**Anti-Pattern 2: Duplicate Documentation**
```
❌ Bad: Garden info in CLAUDE.md AND README.md AND docs/GARDEN.md
✅ Good: Single source of truth in .skogai/garden/README.md
```

**Anti-Pattern 3: Outdated Decision Records**
```
❌ Bad: Trial log mentions plugins that don't exist anymore
✅ Good: Trial log is historical—shows removed plugins with reasons
```

**Anti-Pattern 4: Missing Evaluation Outcomes**
```
❌ Bad: Plugin promoted to permanent with no recorded reason
✅ Good: Decision recorded in trial-log.md with explicit criteria met
```

**Anti-Pattern 5: Scope Creep in Documentation**
```
❌ Bad: Garden docs includes general project management guidance
✅ Good: Garden docs focused on plugin trial system only
```

### 4.3 Documentation Templates

**Trial Announcement Template:**

```markdown
## Starting Trial: [plugin-name]

**Date:** YYYY-MM-DD
**Reason:** [One sentence about why we're trying this]
**Success Criteria:**
- [ ] Criterion 1 (testable)
- [ ] Criterion 2 (testable)
- [ ] Criterion 3 (testable)

**Expected Duration:** [Estimate in days/weeks or 50+ messages]
**Initial Assessment:** [Early impressions, if any]
```

**Decision Record Template:**

```markdown
## Decision: [KEEP|REMOVE|SWAP] plugin-name

**Date Decided:** YYYY-MM-DD
**Messages Used:** [number]
**Decision:** [KEEP|REMOVE|SWAP]
**Primary Reason:** [One clear sentence]

**Supporting Evidence:**
- Evidence point 1
- Evidence point 2
- Evidence point 3

**Lessons Learned:**
- What went well
- What could improve
```

---

## Part 5: Structuring .skogai/ for New Projects

### 5.1 Bootstrap Checklist for New Project

**Initial Setup (Day 1):**

```bash
# Create directory structure
mkdir -p .skogai/{garden,plan/{phases,codebase},todos}
mkdir -p .claude/skills

# Create essential files
cat > .skogai/CLAUDE.md << 'EOF'
# .skogai Directory

Project-level configuration and state.

## Contents
- `garden/` — Plugin trial system
- `plan/` — Project planning documents
- `todos/` — Task tracking

## Quick Links
- `@.skogai/garden/README.md` — Garden system docs
- `@.skogai/plan/PROJECT.md` — Project vision
- `@.skogai/plan/ROADMAP.md` — Phase timeline
EOF

cat > .skogai/garden/README.md << 'EOF'
# Plugin Garden

Philosophy: Start small, add complexity only after testing.

## Commands
- `/garden:status` — View state
- `/garden:trial <plugin>` — Start trial
- `/garden:keep <plugin>` — Promote to permanent

See .skogai/garden/evaluation-criteria.md for details.
EOF

cat > .skogai/garden/evaluation-criteria.md << 'EOF'
# Plugin Evaluation Criteria

[Insert state machine diagram and decision framework]
EOF

cat > .skogai/garden/trial-log.md << 'EOF'
# Trial Log

Keep chronological record of all trial decisions.
EOF

cat > .skogai/plan/PROJECT.md << 'EOF'
# Project Name: [Vision]

## Requirements
- [ ] Requirement 1
- [ ] Requirement 2

## Out of Scope
- Non-requirement 1
- Non-requirement 2

## Success Criteria
- Testable criterion 1
- Testable criterion 2
EOF

cat > .skogai/plan/ROADMAP.md << 'EOF'
# Roadmap

## Phases
- [ ] Phase 1: [Goal]
- [ ] Phase 2: [Goal]

See .skogai/plan/phases/ for detailed plans.
EOF
```

**Project Understanding (Days 1-2):**

```bash
# Create codebase analysis
cat > .skogai/plan/codebase/STRUCTURE.md << 'EOF'
# Structure

## Directory Layout
[List main directories and their purposes]

## Key Components
[List major components and files]
EOF

cat > .skogai/plan/codebase/STACK.md << 'EOF'
# Technology Stack

## Languages
- [Language]: [Purpose]

## Frameworks
- [Framework]: [Purpose]

## Tools
- [Tool]: [Purpose]
EOF

cat > .skogai/plan/codebase/CONVENTIONS.md << 'EOF'
# Conventions

## Naming
- [Pattern]: [Examples]

## Structure
- [Pattern]: [Examples]

## Testing
- [Pattern]: [Examples]
EOF
```

**Initial Onboarding:**

```bash
# Make sure structure exists
ls -la .skogai/
# Output should show: CLAUDE.md, garden/, plan/, todos/

# Check garden system works
/garden:status
# Output should show: seed plugins only, no trials yet

# Document first decision
echo "## Project Started" >> .skogai/garden/trial-log.md
```

### 5.2 Scaling .skogai/ as Project Grows

**Phase 1 (Weeks 1-2): Just the Essentials**
```
.skogai/
├── CLAUDE.md
├── garden/
│   ├── README.md
│   ├── evaluation-criteria.md
│   └── trial-log.md
├── plan/
│   ├── PROJECT.md
│   ├── ROADMAP.md
│   └── codebase/
│       └── STRUCTURE.md
└── todos/
```

**Phase 2 (Weeks 3-4): Add Analysis Docs**
```
.skogai/plan/codebase/
├── STRUCTURE.md
├── STACK.md
├── CONVENTIONS.md
├── ARCHITECTURE.md
├── INTEGRATIONS.md
├── TESTING.md
└── CONCERNS.md
```

**Phase 3 (Months 2+): Add Phase Plans**
```
.skogai/plan/phases/
├── 01-foundation/
│   ├── 1-1-PLAN.md
│   └── 1-1-CONTEXT.md
├── 02-features/
│   ├── 2-1-PLAN.md
│   └── 2-1-CONTEXT.md
└── 03-optimization/
    └── 3-1-PLAN.md
```

**Phase 4 (Ongoing): Maintain and Archive**
```
.skogai/
├── archive/           # Completed phases
│   ├── phases/
│   │   ├── 01-foundation.md
│   │   └── 02-features.md
│   └── garden/
│       ├── trial-log-2025.md
│       └── decisions-2025.md
└── [current structure above]
```

**Growth Rule of Thumb:**
- Don't create files until you need them
- Each new file should replace clutter, not add it
- Archive old files instead of deleting
- Link to files rather than duplicating content

---

## Part 6: Prevention Strategies for Common Pitfalls

### 6.1 Plugin Management Pitfalls

**Pitfall 1: Plugin Proliferation**
- **What:** Too many trial plugins, losing track
- **Prevention:**
  - Never more than 2-3 concurrent trials
  - Archive trial-log.md entries when complete
  - Audit permanent plugins monthly
- **Recovery:** Limit new trials for 2 weeks, finish existing ones

**Pitfall 2: Abandoned Trials**
- **What:** Plugin sits in trial for 6+ months unused
- **Prevention:**
  - Check 50-message threshold weekly
  - Set calendar reminder for decision date
  - Remove idle plugins aggressively
- **Recovery:** Use `/garden:remove` with "abandoned" reason

**Pitfall 3: Circular Dependencies**
- **What:** Plugin A depends on Plugin B depends on Plugin A
- **Prevention:**
  - Map dependencies before `/garden:trial`
  - Require plugins to work independently
  - Test without dependent plugins first
- **Recovery:** Remove one, test the other in isolation

**Pitfall 4: Vague Success Criteria**
- **What:** "See if it works" as only evaluation criteria
- **Prevention:**
  - Define testable criteria before trial starts
  - List 2-3 specific, measurable outcomes
  - Make criteria falsifiable (can you prove it failed?)
- **Recovery:** Add explicit criteria to trial-log.md retroactively

**Pitfall 5: "Just in Case" Permanent Plugins**
- **What:** Keep plugins that haven't been used in 3+ months
- **Prevention:**
  - Remove unused plugins immediately upon discovery
  - Quarterly audit of all permanent plugins
  - Track last-used date for each plugin
- **Recovery:** Remove unused plugins, document reason honestly

### 6.2 Documentation Pitfalls

**Pitfall 1: Documentation Bloat**
- **What:** Too many files, unclear hierarchy, hard to find info
- **Prevention:**
  - One file per major topic
  - Clear directory structure
  - Link between files rather than duplicating
  - Archive completed content
- **Recovery:** Consolidate files, create index

**Pitfall 2: Stale Documentation**
- **What:** Docs say X but system does Y
- **Prevention:**
  - Update docs when changing behavior
  - Periodic audit of critical documentation
  - Link from code to docs it's implementing
- **Recovery:** Schedule monthly doc review

**Pitfall 3: Duplicate Documentation**
- **What:** Same info in multiple places diverges
- **Prevention:**
  - Single source of truth principle
  - Link to authoritative version
  - Delete copies when found
- **Recovery:** Identify authoritative version, link to it

**Pitfall 4: Missing Rationale**
- **What:** "Plugin was removed" with no reason why
- **Prevention:**
  - Require reason with every `/garden:remove`
  - Record decision framework in trial-log.md
  - Document what was tried and why it didn't work
- **Recovery:** Interview decision makers, backfill reasons

### 6.3 Planning Pitfalls

**Pitfall 1: Vague Phase Goals**
- **What:** "Improve things" as a phase goal
- **Prevention:**
  - Phase goals must be measurable
  - Success criteria testable before phase starts
  - Breaking down into sub-goals if needed
- **Recovery:** Rewrite phase goal with specific metrics

**Pitfall 2: Scope Creep**
- **What:** Phase grows beyond original scope
- **Prevention:**
  - Weekly scope review during phase
  - Mark new items as "Phase N.1" (decimal phase)
  - Move scope creep to next phase explicitly
- **Recovery:** Create decimal phase for urgent work

**Pitfall 3: Phase Dependencies Unknown**
- **What:** Start Phase 2 only to realize Phase 1 not complete
- **Prevention:**
  - List dependencies for each phase in ROADMAP.md
  - Mark phases blocked if dependencies fail
  - Don't start next phase until dependencies satisfied
- **Recovery:** Insert decimal phase for blocking work

**Pitfall 4: No Archive**
- **What:** Completed phases deleted, lost learnings
- **Prevention:**
  - Archive completed phases to `.skogai/archive/phases/`
  - Keep trial-log.md as permanent record
  - Reference archive when starting similar work
- **Recovery:** Restore from git history, document learnings

---

## Part 7: Integration with Skogai Ecosystem

### 7.1 Garden System + Skogai-Core Plugin

The Garden system works alongside skogai-core plugin commands:

```
Garden System              Skogai-Core Commands
─────────────────────────────────────────────────
Trial/Permanent           `/skogai:new-project`
Status                    `/skogai:progress`
Keep/Swap/Remove          `/skogai:plan-phase`
                          `/skogai:execute-plan`
```

**Relationship:**
- Garden evaluates **plugins/skills** (tools and integrations)
- Skogai-core manages **project workflow** (phases, milestones)
- They complement each other: garden evaluates what tools to use, skogai-core executes using those tools

**Example Workflow:**

```bash
# 1. Start project with skogai-core
/skogai:new-project --name my-project

# 2. Trial new skill
/garden:trial skogai-new-feature

# 3. Use skill in project execution
/skogai:plan-phase --phase 1

# 4. Evaluate skill effectiveness
# (at 50 messages)
/garden:keep skogai-new-feature  # Passed evaluation
```

### 7.2 Garden System + Local Skills

Three local skills being managed through garden system in lore repo:

| Skill | Status | Purpose |
|-------|--------|---------|
| `lore-creation-starting-skill` | Trial | Guidance for documentation |
| `skogai-jq` | Trial | JSON transformations |
| `skogai-argc` | Trial | CLI framework |

**Best Practices for Skills:**

- Each skill has a SKILL.md or README documenting purpose
- Skills in `.claude/skills/` are trialed before wider adoption
- Message counter tracks skill usage across all interactions
- Success criteria: documented, tested, integrated

---

## Part 8: Quick Reference Guides

### 8.1 Decision Tree: Keep, Swap, or Remove

```
Does the plugin solve a real problem?
├─ NO → Use /garden:remove (plugin not applicable)
└─ YES ↓

Has it been tested for 50+ messages?
├─ NO → Wait more or use /garden:reset
└─ YES ↓

Did it work well in actual use?
├─ NO → Use /garden:remove (plugin broken/inadequate)
└─ YES ↓

Is there a better alternative?
├─ NO → Use /garden:keep (no better option)
└─ YES ↓

Is the alternative proven/stable?
├─ NO → Use /garden:keep (don't risk untested)
└─ YES ↓

Use /garden:swap (migrate to better option)
```

### 8.2 Check-In Checklist (Weekly)

Every week during active trials:

- [ ] `/garden:status` shows trials still relevant
- [ ] Message counter increasing (plugin in use)
- [ ] No unexpected errors or friction
- [ ] Documentation staying current
- [ ] Trial deadline approaching? Plan decision
- [ ] Any red flags? Address immediately

### 8.3 Trial Lifecycle Checklist

**Before Trial (Pre):**
- [ ] Clear problem statement
- [ ] Testable success criteria
- [ ] Estimated duration (50+ messages)
- [ ] Plugin scoped appropriately
- [ ] No conflicts with existing tools

**During Trial (In):**
- [ ] Using regularly (message counter active)
- [ ] Taking notes on friction points
- [ ] Documenting issues/discoveries
- [ ] Checking against success criteria weekly
- [ ] Staying within estimated duration

**At Threshold (50 messages):**
- [ ] Review actual usage against criteria
- [ ] Assess friction and friction points
- [ ] Make decision: keep/swap/remove
- [ ] Document decision in trial-log.md
- [ ] Execute decision

**After Decision (Post):**
- [ ] Promote to permanent (move to persistent config)
- [ ] Document lessons learned
- [ ] Archive trial notes if removed
- [ ] Plan next trial if needed

---

## Part 9: Recommended Reading and References

**Internal Documentation:**
- `.skogai/garden/README.md` — Quick reference
- `.skogai/garden/evaluation-criteria.md` — Detailed state machine
- `.skogai/garden/trial-log.md` — Decision history
- `CLAUDE.md` — Project context and philosophy

**Garden System Philosophy:**
- "Start small, add complexity only after testing and seeing actual need"
- Trial-based evaluation before permanent adoption
- Honest decision-making with documented reasoning
- Reversible decisions (can reset or swap trials)

**Related Skogai Systems:**
- Skogai-core plugin: Project lifecycle management
- Skogai-jq: JSON transformation primitives
- Skogai-argc: CLI framework for automation

---

## Part 10: Updating This Document

This best practices guide should be updated when:

1. **New command added to garden system**: Document in reference section
2. **New pitfall discovered**: Add to prevention strategies
3. **Project grows**: Add new project structure examples
4. **Decision patterns emerge**: Add to decision framework
5. **Better practices discovered**: Update checklists and guidelines

**Maintenance Schedule:**
- Quarterly: Review for stale information
- After major project completion: Document lessons learned
- When pitfall occurs: Add prevention strategy immediately
- During garden system updates: Sync with new features

---

**Last Updated:** 2026-01-05
**Document Version:** 1.0.0
**Philosophy Version:** "Start small, add complexity only after testing"
