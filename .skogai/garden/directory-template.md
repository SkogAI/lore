# .skogai/ Directory Template for New Projects

A ready-to-use template structure for implementing the Garden Plugin System in new projects.

---

## Quick Start Bootstrap Script

Use this script to initialize `.skogai/` in a new project:

```bash
#!/bin/bash
# Initialize .skogai/ directory structure

set -e

project_name="${1:?Usage: bootstrap-skogai.sh <project-name>}"
mkdir -p .skogai/{garden,plan/{phases,codebase},todos}
mkdir -p .claude/skills

echo "✓ Created .skogai/ directory structure"

# Create CLAUDE.md
cat > .skogai/CLAUDE.md << 'EOF'
# .skogai Directory

Project-level skogai configuration and state management.

## Contents

| Directory | Purpose |
|-----------|---------|
| `garden/` | Plugin trial system - test plugins before permanent adoption |
| `plan/` | Project planning and analysis documents |
| `todos/` | Task tracking and work items |

## Garden System

Trial-based plugin evaluation. Test plugins safely before committing.

**Quick Commands:**
- `/garden:status` - View current state (seed, trials, permanent, removed)
- `/garden:trial <plugin>` - Start trialing a new plugin
- `/garden:keep <plugin>` - Promote trial plugin to permanent
- `/garden:swap <old> <new>` - Replace one trial with another
- `/garden:reset <plugin>` - Extend trial period (reset message counter)
- `/garden:remove <plugin>` - Remove plugin (requires reason)

See `@.skogai/garden/README.md` for full documentation.

## Planning

Structured approach to project planning and execution.

- `PROJECT.md` - Project vision, requirements, and success criteria
- `ROADMAP.md` - High-level phase timeline and dependencies
- `phases/` - Detailed execution plans for each phase
- `codebase/` - Architecture and design documentation

## Task Tracking

Individual task files for work items, PRs, and decisions.

See `@.skogai/todos/` for current work.
EOF

echo "✓ Created .skogai/CLAUDE.md"

# Create garden/README.md
cat > .skogai/garden/README.md << 'EOF'
# Plugin Garden & Experimental Components

**Philosophy:** Start small, add complexity only after testing and seeing actual need.

## What is the Garden?

A plugin trial system that evaluates new tools, skills, and integrations before permanent adoption.

- **Seed Plugins**: Always active (core, docs)
- **Trial Plugins**: Being evaluated (message counter tracks usage)
- **Permanent Plugins**: Promoted after successful trial
- **Removed Plugins**: Historical record of plugins that didn't work out

## State Machine

```
Trial Started → (50 messages) → Decision Point
                                 ├─ KEEP → Permanent
                                 ├─ SWAP → Try alternative
                                 └─ REMOVE → End trial
```

## Commands

| Command | Purpose |
|---------|---------|
| `/garden:status` | View current state |
| `/garden:trial <plugin>` | Start new trial |
| `/garden:keep <plugin>` | Promote to permanent |
| `/garden:swap <old> <new>` | Change approach |
| `/garden:reset <plugin>` | Extend evaluation period |
| `/garden:remove <plugin>` | Remove plugin |

## The 50-Message Threshold

Trial plugins are evaluated after 50 messages of actual use:

- 0-15 messages: "Getting the hang of it"
- 15-35 messages: "Finding value or friction"
- 35-50 messages: "Ready to decide"
- At 50: Prompted to keep/swap/remove
- Can reset for 50 more messages if uncertain

## Evaluation Criteria

**KEEP if:**
- Actually used in daily work
- Solves real problem
- No friction or errors
- Documentation complete

**SWAP if:**
- Better alternative available
- Current plugin partially works
- Worth trying different approach

**REMOVE if:**
- Not used after trial
- Causes errors
- Better solution exists elsewhere
- Scope doesn't match needs

## Files

- `README.md` - This file (overview and commands)
- `evaluation-criteria.md` - Detailed decision framework
- `trial-log.md` - Historical record of all trials and decisions

See `@.skogai/garden/best-practices.md` for comprehensive guidance.
EOF

echo "✓ Created .skogai/garden/README.md"

# Create garden/evaluation-criteria.md
cat > .skogai/garden/evaluation-criteria.md << 'EOF'
# Plugin Evaluation Criteria

## State Machine Diagram

```
                   ┌─────────────────┐
                   │   SEED PLUGINS  │  Always active
                   │  (core, docs)   │  Can't be removed
                   └─────────────────┘
                          ↓
              Trial Plugin Added
                          ↓
                   ┌──────────────────┐
                   │   TRIAL STATE    │
                   │  (50 msg counter)│
                   └─────────────────┘
                   /         |         \
                  /          |          \
            /garden:keep  /garden:  /garden:
            KEEP          swap      REMOVE
                  \          |          /
                   \         |         /
                    ┌────────┴────────┐
                    ↓                 ↓
              ┌──────────┐      ┌──────────┐
              │ PERMANENT│      │ REMOVED  │
              │ (stays)  │      │(history) │
              └──────────┘      └──────────┘
```

## Evaluation Timeline

### Weeks 1-2: Initial Trial
- Plugin added via `/garden:trial`
- Message counter starts at 0
- Documentation created/updated
- Early feedback collected

### Week 2-3: Active Use
- Plugin in regular use
- Message counter increasing
- Friction points identified
- Success criteria assessed

### Approaching 50 Messages
- Review actual usage patterns
- Assess against success criteria
- Prepare decision framework
- Document findings

### Decision Point (50 Messages)
- KEEP: Plugin meets criteria, stays permanently
- SWAP: Try different approach, remove current
- REMOVE: Didn't work, abandon
- RESET: Need more evaluation, extend 50 messages

## Decision Framework

### KEEP Decision

**Qualifiers:**
- [ ] Plugin used 3+ times per week in actual work
- [ ] Solves documented problem or improves workflow
- [ ] 0-2 issues encountered in 50 messages
- [ ] Documentation is clear and complete
- [ ] No better alternative exists
- [ ] Integrates well with existing tools

**Questions to Ask:**
- Would you feel lost without this plugin?
- Would you choose this again if starting over?
- Can you teach someone else how to use it quickly?

**Record Decision:**
```markdown
## KEEP: plugin-name
- **Date:** YYYY-MM-DD
- **Messages Used:** [number]
- **Primary Reason:** [One sentence]
- **Criteria Met:** [List 3-4 criteria]
```

### SWAP Decision

**Qualifiers:**
- [ ] Better alternative identified
- [ ] Current plugin has fundamental limitation
- [ ] Alternative worth evaluating
- [ ] Don't burn bridge with current plugin
- [ ] Clear switching path identified

**Questions to Ask:**
- Is the alternative proven/tested?
- What specifically is better?
- Can you test alternative in isolation?

**Record Decision:**
```markdown
## SWAP: old-plugin → new-plugin
- **Date:** YYYY-MM-DD
- **Messages Used:** [number]
- **Reason for Swap:** [One sentence]
- **What's Better:** [Specific improvement]
```

### REMOVE Decision

**Qualifiers:**
- [ ] Plugin barely used (< 10% of work)
- [ ] Better alternative already in place
- [ ] Causes friction or errors
- [ ] Scope doesn't match project needs
- [ ] Documentation too complex for value

**Questions to Ask:**
- Why wasn't this used more?
- What's the replacement?
- Would you ever pick this again?
- What would need to change to keep it?

**Record Decision:**
```markdown
## REMOVE: plugin-name
- **Date:** YYYY-MM-DD
- **Messages Used:** [number]
- **Reason:** [One sentence]
- **Lessons Learned:** [What we discovered]
```

## Message Counter Behavior

**Increment Logic:**
- +1 for each user prompt (not system messages)
- Counter shared across all interactions
- Resets if plugin updated or trial explicitly extended

**Tracking:**
- Visible in `/garden:status` output
- Threshold: 50 messages (configurable)
- Goal: Sufficient signal to make decision

**When to Reset:**
- Need more evaluation time
- Plugin just updated with bug fixes
- Significant scope change discovered
- Evaluator wants to be thorough

## Preventing Common Mistakes

| Mistake | Prevention | Recovery |
|---------|-----------|----------|
| Vague success criteria | Define before trial | Add retroactively to trial-log.md |
| Abandoned trial | Set decision deadline | Use /garden:swap or /garden:remove |
| No documentation | Add before declaration complete | Create docs immediately |
| Circular dependencies | Check before trial | Remove one, test other alone |
| Too many trials | Limit to 2 concurrent | Finish current, start new |

## Related Documentation

- `README.md` - Quick reference and commands
- `trial-log.md` - Historical decisions
- `@.skogai/garden/best-practices.md` - Comprehensive guidance
EOF

echo "✓ Created .skogai/garden/evaluation-criteria.md"

# Create garden/trial-log.md
cat > .skogai/garden/trial-log.md << 'EOF'
# Garden Trial Log

Chronological record of all plugin trials and decisions.

## Active Trials

(None yet - add trials with `/garden:trial <plugin>`)

## Completed Trials

(Decisions will be recorded here as trials conclude)

## Decisions Format

When concluding a trial, record decision as:

```markdown
## [DECISION]: plugin-name
- **Date Decided:** YYYY-MM-DD
- **Messages Used:** [number]
- **Decision:** [KEEP|SWAP|REMOVE]
- **Reason:** [One sentence]

**Supporting Evidence:**
- Evidence point 1
- Evidence point 2
- Evidence point 3

**Lessons Learned:**
- Learning 1
- Learning 2
```

## Removed Plugins Archive

Plugins removed during trials are tracked with reasons:

| Plugin | Reason | Messages | Date |
|--------|--------|----------|------|
| (none yet) | | | |

---

Use this log to:
1. Track trial progress
2. Make informed decisions
3. Learn from past choices
4. Avoid repeating mistakes
EOF

echo "✓ Created .skogai/garden/trial-log.md"

# Create plan/PROJECT.md
cat > .skogai/plan/PROJECT.md << 'EOF'
# $project_name: Project Overview

**Status:** Just initialized
**Last Updated:** $(date -u +%Y-%m-%d)

## Vision

[One paragraph describing the project's ultimate goal]

## Core Requirements

- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3

## Out of Scope

Items explicitly NOT being addressed in this project:

- Non-requirement 1
- Non-requirement 2
- Non-requirement 3

## Success Criteria

How we know we've succeeded (testable, measurable):

1. **Criterion 1:** [Specific, measurable outcome]
2. **Criterion 2:** [Specific, measurable outcome]
3. **Criterion 3:** [Specific, measurable outcome]

## Key Assumptions

What we're assuming to be true:

- Assumption 1: [What we're assuming]
- Assumption 2: [What we're assuming]

## Domain Expertise Required

Knowledge areas needed to execute:

- Expertise area 1
- Expertise area 2
- Expertise area 3

---

See `ROADMAP.md` for phase-by-phase breakdown.
EOF

echo "✓ Created .skogai/plan/PROJECT.md"

# Create plan/ROADMAP.md
cat > .skogai/plan/ROADMAP.md << 'EOF'
# Roadmap: $project_name

## Milestone Overview

| Phase | Goal | Status | Depends On |
|-------|------|--------|-----------|
| 1 | [Phase 1 goal] | Planned | Nothing |
| 2 | [Phase 2 goal] | Not started | Phase 1 |
| 3 | [Phase 3 goal] | Not started | Phase 2 |

## Phase Details

### Phase 1: [Phase 1 Title]

**Goal:** [One sentence describing what this phase accomplishes]

**Depends on:** Nothing (first phase)

**Success Criteria:**
- [ ] Success criterion 1
- [ ] Success criterion 2
- [ ] Success criterion 3

**Key Activities:**
- Activity 1
- Activity 2
- Activity 3

### Phase 2: [Phase 2 Title]

**Goal:** [One sentence]

**Depends on:** Phase 1 completion

**Success Criteria:**
- [ ] Success criterion 1
- [ ] Success criterion 2

**Key Activities:**
- Activity 1
- Activity 2

### Phase 3: [Phase 3 Title]

**Goal:** [One sentence]

**Depends on:** Phase 2 completion

**Success Criteria:**
- [ ] Success criterion 1
- [ ] Success criterion 2

---

## Decimal Phase Notation

Urgent work discovered during execution uses decimal phases:

- **2.1 - [Urgent Work]**: [Description]
  - Inserted between Phase 2 and Phase 3
  - Doesn't delay Phase 2 completion
  - Can be parallel or sequential

See `.skogai/plan/phases/` for detailed execution plans.
EOF

echo "✓ Created .skogai/plan/ROADMAP.md"

# Create plan/codebase structure files
cat > .skogai/plan/codebase/STRUCTURE.md << 'EOF'
# Codebase Structure

## Directory Layout

[Document main directories and their purposes]

```
project/
├── src/        [Source code]
├── tests/      [Test files]
├── docs/       [Documentation]
└── tools/      [Scripts and utilities]
```

## Key Files and Modules

[List important files and modules]

## Component Overview

[Describe major components and their relationships]
EOF

echo "✓ Created .skogai/plan/codebase/STRUCTURE.md"

cat > .skogai/plan/codebase/STACK.md << 'EOF'
# Technology Stack

## Languages

| Language | Purpose | Version |
|----------|---------|---------|
| [Language] | [What for] | [Version] |

## Frameworks & Libraries

| Framework | Purpose | Version |
|-----------|---------|---------|
| [Framework] | [What for] | [Version] |

## Tools

| Tool | Purpose | Status |
|------|---------|--------|
| [Tool] | [What for] | Configured |

## Development Environment

[Local setup requirements]
EOF

echo "✓ Created .skogai/plan/codebase/STACK.md"

cat > .skogai/plan/codebase/CONVENTIONS.md << 'EOF'
# Code Conventions

## Naming Conventions

[Document how things are named]

### Files
[File naming pattern]

### Variables
[Variable naming pattern]

### Functions
[Function naming pattern]

## Code Organization

[How code is organized within files]

## Testing Conventions

[How tests are structured and named]

## Documentation Standards

[How code is documented]
EOF

echo "✓ Created .skogai/plan/codebase/CONVENTIONS.md"

cat > .skogai/plan/codebase/ARCHITECTURE.md << 'EOF'
# Architecture

## System Design

[High-level overview of how components fit together]

## Data Flow

[How data flows through the system]

## Component Relationships

[How different components interact]

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| [Decision] | [Why we chose this] |

## Integration Points

[Where external systems connect]
EOF

echo "✓ Created .skogai/plan/codebase/ARCHITECTURE.md"

cat > .skogai/plan/codebase/INTEGRATIONS.md << 'EOF'
# External Integrations

## Services

[External services the system uses]

## APIs

[External APIs consumed]

## Dependencies

[Key external dependencies and versions]
EOF

echo "✓ Created .skogai/plan/codebase/TESTING.md << 'EOF'
# Testing Strategy

## Test Types

[What types of tests are used]

## Coverage Goals

[What level of coverage is target]

## Running Tests

[How to run the test suite]

## Known Issues

[Known test failures or limitations]
EOF

echo "✓ Created .skogai/plan/codebase/TESTING.md"

cat > .skogai/plan/codebase/CONCERNS.md << 'EOF'
# Known Concerns

## Technical Debt

[Known technical limitations or debt]

## Performance Issues

[Known performance problems]

## Security Concerns

[Any security-related concerns]

## Limitations

[Fundamental limitations of current design]
EOF

echo "✓ Created .skogai/plan/codebase/CONCERNS.md"

# Create .gitkeep in todos
touch .skogai/todos/.gitkeep

echo ""
echo "✓ Bootstrap complete!"
echo ""
echo "Next steps:"
echo "1. Update .skogai/plan/PROJECT.md with your project details"
echo "2. Update .skogai/plan/ROADMAP.md with your phases"
echo "3. Fill in codebase documentation as you learn the system"
echo "4. Use /garden:trial to evaluate new plugins"
echo "5. Check /garden:status regularly to track trials"
EOF
```

---

## Manual File-by-File Setup

If you prefer manual setup, create files in this order:

### Step 1: Core Structure (5 minutes)

```bash
mkdir -p .skogai/{garden,plan/{phases,codebase},todos}
mkdir -p .claude/skills
touch .skogai/todos/.gitkeep
```

### Step 2: Garden System (10 minutes)

Create these three files in `.skogai/garden/`:
1. `README.md` - Overview and quick commands
2. `evaluation-criteria.md` - Decision framework
3. `trial-log.md` - Empty log file for decisions

### Step 3: Project Planning (10 minutes)

Create these files in `.skogai/plan/`:
1. `PROJECT.md` - Vision and requirements
2. `ROADMAP.md` - Phase timeline

Create subdirectory `.skogai/plan/codebase/` with analysis files:
1. `STRUCTURE.md` - Directory layout
2. `STACK.md` - Technology choices
3. `CONVENTIONS.md` - Code standards
4. `ARCHITECTURE.md` - System design
5. `INTEGRATIONS.md` - External connections
6. `TESTING.md` - Test strategy
7. `CONCERNS.md` - Known issues

### Step 4: Scaffold Phase Plans (5 minutes per phase)

For each phase in ROADMAP, create:

```
.skogai/plan/phases/01-phase-name/
├── 1-1-PLAN.md        # Execution steps
└── 1-1-CONTEXT.md     # Resources and context
```

### Step 5: Initialize Git (2 minutes)

```bash
git add .skogai/
git commit -m "Initialize .skogai/ project structure with garden system"
```

---

## Progression Examples

### Small Project Example

For a 2-week project:

```
.skogai/
├── CLAUDE.md
├── garden/
│   ├── README.md
│   ├── evaluation-criteria.md
│   └── trial-log.md
├── plan/
│   ├── PROJECT.md
│   ├── ROADMAP.md         # Just 2-3 phases
│   └── codebase/
│       ├── STRUCTURE.md
│       ├── STACK.md
│       └── CONVENTIONS.md
└── todos/
```

### Medium Project Example

For a 2-3 month project:

```
.skogai/
├── CLAUDE.md
├── garden/
│   ├── README.md
│   ├── evaluation-criteria.md
│   └── trial-log.md        # Multiple trials completed
├── plan/
│   ├── PROJECT.md
│   ├── ROADMAP.md          # 4-5 phases
│   ├── phases/
│   │   ├── 01-foundation/
│   │   │   ├── 1-1-PLAN.md
│   │   │   └── 1-1-CONTEXT.md
│   │   └── 02-core/
│   │       ├── 2-1-PLAN.md
│   │       └── 2-1-CONTEXT.md
│   └── codebase/           # Full analysis docs
└── todos/                  # Multiple task files
```

### Large Project Example

For a 6+ month project:

```
.skogai/
├── CLAUDE.md
├── garden/
│   ├── README.md
│   ├── evaluation-criteria.md
│   ├── trial-log.md        # Extensive history
│   └── decision-framework.md
├── plan/
│   ├── PROJECT.md
│   ├── ROADMAP.md          # 6+ phases
│   ├── phases/             # Detailed plans for each
│   │   ├── 01-*/
│   │   ├── 02-*/
│   │   ├── 03-*/
│   │   └── ...
│   ├── archive/            # Completed phases
│   │   ├── phases-2025/
│   │   └── decisions-2025/
│   └── codebase/           # Comprehensive docs
└── todos/                  # Many task files
```

---

## Customization Guide

### For Data Projects

Add to `.skogai/plan/codebase/`:
- `DATA_MODEL.md` - Entity relationships
- `PIPELINES.md` - Data processing flows
- `QUALITY.md` - Data quality standards

### For DevOps Projects

Add to `.skogai/plan/codebase/`:
- `INFRASTRUCTURE.md` - Cloud/server setup
- `MONITORING.md` - Health checks
- `INCIDENT_RESPONSE.md` - Playbooks

### For API Projects

Add to `.skogai/plan/codebase/`:
- `API_DESIGN.md` - REST/GraphQL design
- `AUTHENTICATION.md` - Auth mechanisms
- `RATE_LIMITING.md` - Quotas and limits

### For Frontend Projects

Add to `.skogai/plan/codebase/`:
- `COMPONENT_LIBRARY.md` - Reusable components
- `STYLING.md` - Theme and CSS standards
- `ACCESSIBILITY.md` - A11y standards

---

## Maintenance Calendar

### Weekly
- Check `/garden:status`
- Review active trials progress
- Update trial-log.md if decisions needed

### Monthly
- Audit codebase docs for accuracy
- Review plan phases for scope creep
- Archive completed trials

### Quarterly
- Full garden system audit
- Permanent plugin review (remove unused)
- Codebase analysis refresh

### Yearly
- Archive completed milestones
- Update project overview docs
- Plan major direction changes

---

**Last Updated:** 2026-01-05
**Template Version:** 1.0.0
**For Guidance:** See `@.skogai/garden/best-practices.md`
