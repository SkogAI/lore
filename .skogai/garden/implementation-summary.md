# Garden Plugin System: Implementation Summary

Complete overview of the Garden Plugin System pattern for project teams implementing plugin trial systems.

---

## What This Pattern Solves

**The Problem:**
- New tools and plugins add up
- Hard to decide: keep or remove?
- No systematic evaluation process
- "Just in case" plugins accumulate
- Unclear when to promote from trial to permanent

**The Solution:**
The Garden Plugin System provides a **structured trial-based evaluation** framework that:
- Tests plugins systematically before permanent adoption
- Uses message counts to detect when evaluation is complete
- Requires documented decisions with clear rationale
- Prevents plugin bloat through honest assessment
- Creates historical record of decisions for learning

---

## Documentation Map

This pattern is documented across four comprehensive guides:

### 1. **best-practices.md** (Primary Reference)
**For:** Project teams implementing the garden system

**Contains:**
- Part 1: Project structure (.skogai/ organization)
- Part 2: Garden system deep dive (state machine, commands, philosophy)
- Part 3: Best practices checklist (what to do and avoid)
- Part 4: Documentation patterns (what to write, how to organize)
- Part 5: New project bootstrap (day-1 setup)
- Part 6: Prevention strategies (common pitfalls and fixes)
- Part 7: Integration with skogai ecosystem
- Part 8: Quick reference guides
- Part 9: Update and maintenance schedule
- Part 10: Document maintenance

**Use this when:**
- Setting up garden system in new project
- Need complete implementation guidance
- Want to avoid common mistakes
- Establishing team practices
- Evaluating project structure

**Key sections:**
- Pre-trial checklist (page X)
- Decision checklists (page Y)
- Prevention strategies table (page Z)
- Template for `.skogai/` structure (easy copy-paste)

### 2. **decision-framework.md** (Strategic Guide)
**For:** Teams making evaluation decisions

**Contains:**
- Part 1: Pre-trial decision framework (should we trial this?)
- Part 2: During-trial evaluation (weekly assessment)
- Part 3: Decision point framework (50-message threshold)
- Part 4: Post-decision actions (KEEP/SWAP/REMOVE follow-up)
- Part 5: Common decision scenarios (with decision trees)
- Part 6: Anti-patterns to avoid
- Part 7: Metrics and learning (track outcomes)
- Part 8: Decision quick references

**Use this when:**
- Deciding whether to start a trial
- Need framework for weekly evaluation
- At the 50-message decision point
- Making marginal decisions (uncertain about keep/swap)
- Learning from past decisions
- Training team on decision process

**Key tools:**
- Pre-trial checklist (5 questions)
- Weekly assessment checklist
- Quantitative decision matrix
- Decision tree diagrams
- Scenario-based decision paths
- Anti-pattern identification

### 3. **directory-template.md** (Setup Guide)
**For:** Setting up `.skogai/` structure in new projects

**Contains:**
- Bootstrap script (complete setup automation)
- Manual setup instructions (file-by-file)
- File organization patterns
- Progression examples (small → medium → large projects)
- Customization patterns (data projects, DevOps, etc.)
- Maintenance calendar

**Use this when:**
- Creating new project with garden system
- Need `.skogai/` directory structure
- Want copy-paste templates
- Setting up for first time
- Scaling structure as project grows

**Quick start:**
- Run bootstrap script (5 minutes)
- Or follow manual setup (15 minutes)
- 22 template files ready to use
- Comments show what to fill in

### 4. **This Document: implementation-summary.md**
**For:** Understanding the complete system at a glance

**Use this as:**
- Navigation guide to other documents
- Quick orientation for new team members
- Decision point for which doc to read
- Reference for integration points
- Learning outcomes checklist

---

## Core Concepts at a Glance

### The State Machine

```
SEED (core, docs)      Always active, can't remove
    ↓
    Start Trial
    ↓
TRIAL (message counter)
    ├─ 0-50 messages: Evaluation period
    ├─ At 50: Decision point
    ├─ /garden:keep → PERMANENT
    ├─ /garden:swap → Try alternative
    └─ /garden:remove → REMOVED
    ↓
PERMANENT or REMOVED
    (Historical record kept forever)
```

### The 50-Message Threshold

**Why 50?**
- Sufficient signal for genuine evaluation
- Typical working session = 5-10 messages
- A week of work = 40-50 messages
- Natural decision point before wasting more time

**Message counter:**
- Increments per user prompt (not system)
- Not time-based, usage-based
- Can reset with `/garden:reset` for more time
- Max 3 resets before forced decision

### Three Key Commands

| Phase | Command | Meaning |
|-------|---------|---------|
| Setup | `/garden:trial <plugin>` | Start evaluating |
| Evaluate | `/garden:status` | Check counter and status |
| Decision | `/garden:keep` OR `/garden:swap` OR `/garden:remove` | Make decision |

---

## Implementation Roadmap

### Week 1: Setup
- [ ] Read `best-practices.md` Part 1-2 (understand system)
- [ ] Read `directory-template.md` (how to structure)
- [ ] Run bootstrap script or manual setup
- [ ] Create `.skogai/CLAUDE.md` and `garden/README.md`
- [ ] Verify `/garden:status` command works
- [ ] Document project in `plan/PROJECT.md` and `plan/ROADMAP.md`

**Success Criteria:**
- [ ] `.skogai/` directory exists with all subdirectories
- [ ] Garden system initialized (state file exists)
- [ ] `/garden:status` shows seed plugins
- [ ] Team can see project structure and vision

### Week 2-3: First Trial
- [ ] Read `decision-framework.md` Part 1 (pre-trial)
- [ ] Complete pre-trial checklist (5 questions)
- [ ] Start first plugin trial with `/garden:trial`
- [ ] Document trial in `.skogai/garden/trial-log.md`
- [ ] Daily standup: Check `/garden:status` and message counter

**Success Criteria:**
- [ ] Trial started with clear problem statement
- [ ] 2-3 testable success criteria defined
- [ ] Team using plugin in daily work
- [ ] Message counter incrementing steadily

### Week 4-5: Evaluation Period
- [ ] Read `decision-framework.md` Part 2 (during-trial)
- [ ] Weekly assessment checklist (every 7 days)
- [ ] Monitor for red flags (errors, disuse, alternatives)
- [ ] Refine success criteria based on reality
- [ ] Prepare decision framework

**Success Criteria:**
- [ ] Weekly check-ins recorded
- [ ] Usage patterns clear
- [ ] Problems identified and addressed
- [ ] Ready for decision at 50 messages

### Week 6: Decision Point
- [ ] Read `decision-framework.md` Part 3 (decision framework)
- [ ] Review success criteria vs. actual outcomes
- [ ] Complete quantitative decision matrix
- [ ] Make KEEP / SWAP / REMOVE decision
- [ ] Document decision in trial-log.md

**Success Criteria:**
- [ ] Decision made with documented reasoning
- [ ] Trial-log.md updated
- [ ] Team aligned on outcome
- [ ] Action items assigned

### Ongoing: Maintenance
- [ ] Read `best-practices.md` Part 6 (prevention strategies)
- [ ] Weekly: Check `/garden:status`
- [ ] Monthly: Audit trial progress, permanent plugins
- [ ] Quarterly: Full system review
- [ ] When new plugin appears: Apply pre-trial framework

**Success Criteria:**
- [ ] No "forever trials" (decisions made within reasonable time)
- [ ] No "just in case" permanent plugins (removing unused)
- [ ] Decision history documented and learned from
- [ ] Team confident in tool selections

---

## Integration with Larger Systems

### Garden + Skogai-Core

The Garden system **evaluates tools and plugins**.
Skogai-core **executes projects using those tools**.

**Workflow:**
```
1. Garden: Decide which tools to use (trial/keep/remove)
2. Skogai-core: Plan and execute project phases
3. Garden: Evaluate new tools if needed
4. Skogai-core: Use proven tools efficiently
```

**Example:**
```bash
# Week 1: Decide tools
/garden:trial skogai-jq
/garden:trial skogai-argc

# Week 2-4: Evaluate (50 messages each)
/garden:status  # Track usage

# Week 5: Make decisions
/garden:keep skogai-jq      # Passed evaluation
/garden:remove skogai-old   # Didn't work out

# Week 6+: Use tools in project work
/skogai:new-project --name my-project
/skogai:plan-phase --phase 1
# Use kept plugins during execution
```

### Garden + Local Skills

Three local skills in `.claude/skills/` managed through garden:

1. **lore-creation-starting-skill** - Documentation guidance (trial)
2. **skogai-jq** - JSON transformations (trial)
3. **skogai-argc** - CLI framework (trial)

Each skill has:
- Clear purpose and scope
- Success criteria for promotion
- Message counter tracking usage
- Documentation for team

**Best practice:** Skills stay in trial until proven useful, then promoted to permanent.

---

## Key Principles to Remember

### 1. Start Small

Don't add complexity upfront. Begin with:
- Minimal `.skogai/` structure
- Just `garden/README.md`, `PROJECT.md`, `ROADMAP.md`
- Expand as project grows

### 2. Add Complexity Only After Testing

- Try plugin before adopting
- Make decision before moving on
- Don't accumulate "maybe" tools

### 3. Measure Actual Usage

- Message counter shows real usage
- Subjective feelings are unreliable
- Data drives decisions

### 4. Make Decisions Explicitly

- No "forever trials"
- Document KEEP/SWAP/REMOVE reasoning
- Create history for learning

### 5. Prefer Removal to Accumulation

- "Just in case" plugins harm focus
- Aggressive removal > reluctant keeping
- Can always add back if needed

---

## Common Decisions and When to Make Them

| Situation | When to Decide | Decision Method | Document |
|-----------|---------------|-----------------|----------|
| Plugin barely used | At 30 messages | Quick assessment | Trial-log |
| Plugin has major bugs | Immediately | No threshold needed | Trial-log |
| Good plugin, good alternative | At 50 messages | Head-to-head comparison | Trial-log |
| Working well, no concerns | At 50 messages | Confirm criteria met | Trial-log |
| Unclear benefit | At 50 messages | Quantitative matrix | Trial-log |
| Excellent performance | As soon as clear | Fast-track keep | Trial-log |

---

## Team Roles and Responsibilities

### Plugin Evaluator
- Starts trials with clear problem statement
- Performs weekly assessments
- Leads decision discussion at 50 messages
- Documents outcome in trial-log.md

### Project Lead
- Reviews pre-trial checklist
- Approves decision rationale
- Ensures action items assigned
- Audits garden system quarterly

### Team Member Using Plugin
- Uses plugin in actual work
- Reports friction/errors immediately
- Provides feedback on usability
- Votes in decision discussion

### Gardener (Quarterly)
- Audits permanent plugins for usage
- Removes unused plugins
- Archives old trial decisions
- Updates prevention strategies

---

## Success Metrics

### System Health

- **Trial Velocity:** Plugins move from trial to decision in <6 weeks
- **Decision Quality:** Plugins kept for 3+ months have high satisfaction
- **Error Rate:** <5% of decisions regretted later
- **Bloat Prevention:** Permanent plugins actively used

### Team Adoption

- **Participation:** 80%+ of team use garden commands correctly
- **Documentation:** Trial-log.md updated within 24 hours of decision
- **Communication:** Decision rationale understood by team
- **Learning:** Lessons from past trials inform future decisions

### Project Impact

- **Tool Clarity:** Team knows which tools are "canonical"
- **Decision Confidence:** More confident choices over time
- **Reduced Waste:** Fewer abandoned tools, plugins
- **Knowledge Preservation:** History available for future projects

---

## Troubleshooting

### Problem: Trial Abandoned (Unused)

**Symptoms:**
- Plugin in trial but message count stalled
- Team not using it
- Getting forgotten

**Solutions:**
1. Immediate: Move to daily standup, force status checks
2. Short-term: Use `/garden:swap` for alternative or `/garden:remove`
3. Long-term: Improve pre-trial assessment to catch early

**Prevention:**
- Set explicit usage expectations
- Weekly status checks on message count
- Set decision deadline calendar reminder

### Problem: Decision Too Hard (Uncertain at 50)

**Symptoms:**
- Quantitative matrix score 3.5-3.9 (marginal)
- Can't decide keep vs. remove
- Would like more evaluation time

**Solutions:**
1. Use `/garden:reset <plugin>` for 50 more messages
2. Run `/garden:swap` to try alternative in parallel
3. Set specific experiments for next 50 messages

**Prevent:**
- Better pre-trial criteria
- Clear decision framework before trial starts
- Quantitative matrix to break ties

### Problem: No Documentation (Lost History)

**Symptoms:**
- Can't remember why plugin was removed
- No reason recorded in removed section
- Re-trial same plugin later

**Solutions:**
1. Update trial-log.md immediately with decision
2. Interview decision-makers if history lost
3. Archive decision in `.skogai/archive/`

**Prevent:**
- Require reason in every `/garden:remove`
- Weekly documentation checks
- Copy decision immediately after making it

### Problem: Scope Creep in Project

**Symptoms:**
- New work discovered mid-phase
- Phase growing beyond original scope
- Timeline slipping

**Solutions:**
1. Create decimal phase (e.g., 2.1) for urgent work
2. Keep original phase scope unchanged
3. Decide after decimal: merge into next phase or keep separate

**Prevent:**
- Weekly scope review during phase
- Move unexpected work to explicit backlog
- Communicate scope changes to team

---

## Learning Path (Recommended Reading Order)

**If you have 1 hour:**
1. This document (10 minutes) - Orientation
2. `best-practices.md` Part 1-3 (30 minutes) - System overview
3. `directory-template.md` quick start (15 minutes) - Setup
4. Run bootstrap script (5 minutes) - Get started

**If you have 3 hours:**
1. All sections of `best-practices.md` (90 minutes)
2. `decision-framework.md` Part 1-3 (60 minutes)
3. `directory-template.md` detailed read (20 minutes)
4. Plan first trial with checklist (10 minutes)

**If you have 1 day:**
1. Complete `best-practices.md` (2 hours)
2. Complete `decision-framework.md` (2 hours)
3. Complete `directory-template.md` (1 hour)
4. Set up project structure (1 hour)
5. Plan first 3 trials with team (1 hour)
6. Start first trial with full team (1 hour)

---

## Document Update History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-05 | Initial release: 4-document garden system pattern |

---

## Quick Links to Documents

- **Full Best Practices:** `.skogai/garden/best-practices.md`
- **Decision Framework:** `.skogai/garden/decision-framework.md`
- **Directory Template:** `.skogai/garden/directory-template.md`
- **Implementation (this file):** `.skogai/garden/implementation-summary.md`

---

## Next Steps

1. **Read** `best-practices.md` introduction to understand the system
2. **Understand** the 50-message threshold philosophy and state machine
3. **Use** `directory-template.md` to set up your project
4. **Reference** `decision-framework.md` for first trial decisions
5. **Return to this document** as navigation guide during implementation

---

**Created:** 2026-01-05
**Companion Documentation:** 3 detailed guides (total 25,000+ words)
**Philosophy:** "Start small, add complexity only after testing and seeing actual need"
