# Garden System Decision Framework

Strategic decision-making for plugin trials and project evolution.

---

## Executive Summary

The Garden system reduces risk through **trial-based evaluation**. This framework provides decision patterns, evaluation criteria, and anti-patterns to help maximize signal from limited trial time.

**Core Philosophy:** "Start small, add complexity only after testing and seeing actual need."

---

## Part 1: Pre-Trial Decision Framework

### Should You Start a Trial?

Before beginning any plugin trial, answer these questions:

#### 1. Problem Clarity

**Question:** Can you articulate the problem this plugin solves in one sentence?

**Good Answers:**
- "Replaces repetitive jq commands with simpler syntax"
- "Provides shell completion for our CLI tools"
- "Reduces context switching between JSON and YAML"

**Bad Answers:**
- "Might be useful someday"
- "Everyone else is using it"
- "Could improve things"

**Decision Rule:**
- [ ] Can I state problem clearly? → Continue
- [ ] Problem feels vague or speculative? → Don't trial, wait for clarity

#### 2. Success Criteria Specificity

**Question:** What would success look like, and can I measure it?

**Testable Criteria:**
- "Reduces jq command length by 30%"
- "Adds shell completion for 5 commands"
- "Eliminates one category of errors we see in logs"

**Untestable Criteria:**
- "Makes development better"
- "Improves productivity"
- "Reduces cognitive load"

**Decision Rule:**
- [ ] Can I create 2-3 testable success criteria? → Continue
- [ ] All criteria are subjective or vague? → Don't trial yet

#### 3. Cost of Trial

**Question:** What's the cost of trialing this plugin?

**Low Cost Trials:**
- Plugin can be removed cleanly without side effects
- Trial doesn't interfere with other work
- No data dependency or system integration
- <5 minutes to set up or remove

**High Cost Trials:**
- Requires changes to multiple systems
- Affects production or critical path
- Has dependencies on other plugins
- Creates technical debt if removed

**Decision Rule:**
- [ ] Cost of trial < cost of not knowing? → Continue
- [ ] Cost of trial is very high for uncertain benefit? → Don't trial now

#### 4. Natural Decision Point

**Question:** Can I reach a clear decision in 50 messages?

**Good Questions for 50-Message Trial:**
- Does this CLI work as advertised?
- Can this replace our current tool?
- Is the learning curve manageable?
- Does this solve 80% of our problem?

**Questions Needing Longer Trials:**
- How does this perform at scale?
- Will this handle production load?
- Can we integrate this across multiple systems?
- How will this evolve over 6 months?

**Decision Rule:**
- [ ] Can I make a keep/swap/remove decision in 50 messages? → Continue
- [ ] Need more time to evaluate properly? → Extend or don't trial

#### 5. Alternative Paths

**Question:** What's the cost of NOT trialing this?

**Worth Trialing Even If Uncertain:**
- Alternative is significantly worse
- Current approach is causing real pain
- No better option available
- Low switching cost

**Not Worth Trialing:**
- Current approach is "good enough"
- Better alternatives exist and are proven
- Switching cost is high
- Just curious, no real need

**Decision Rule:**
- [ ] Cost of staying with current approach > trial cost? → Continue
- [ ] Status quo is fine, just exploring? → Don't trial now

### Pre-Trial Checklist

Before `/garden:trial`, verify:

- [ ] Problem statement written in one sentence
- [ ] 2-3 testable success criteria defined
- [ ] Trial cost estimated and acceptable
- [ ] Decision point clear (what does success look like?)
- [ ] No circular dependencies with other plugins
- [ ] Time budget allocated (50+ messages estimated as N days)
- [ ] Alternative paths identified
- [ ] Documentation started (at least a stub)
- [ ] Removal plan clear (how to back out if needed)
- [ ] No better alternative already exists

If any checkbox fails → **Don't trial yet**, address the issue first.

---

## Part 2: During-Trial Evaluation Framework

### Weekly Assessment Checklist

Every week during active trial, answer:

#### 1. Usage Pattern
- [ ] Using plugin 3+ times per week?
- [ ] Message counter increasing steadily?
- [ ] Natural or forced usage?

**Interpretation:**
- Natural usage + message counter rising = Plugin is truly valuable
- Forced usage + slow counter = Plugin may not match real needs
- No usage + stalled counter = Trial is dead, decision needed

#### 2. Friction Assessment
- [ ] Any errors or unexpected behavior?
- [ ] Learning curve reasonable?
- [ ] Documentation sufficient?
- [ ] Integration with other tools smooth?

**Interpretation:**
- 0 errors, smooth integration = Good trial progress
- 1-2 minor errors = Acceptable, keep going
- 3+ errors or major friction = Stop, swap, or remove

#### 3. Criteria Check
- [ ] Making progress on criterion #1?
- [ ] Making progress on criterion #2?
- [ ] Making progress on criterion #3?

**Interpretation:**
- All 3 criteria progressing = Trial on track
- Some criteria progressing = Still evaluating
- No progress on criteria = Trial may fail

#### 4. Alternative Comparison
- [ ] Still best option we know of?
- [ ] New alternative appeared?
- [ ] Reconsidered before trialing?

**Interpretation:**
- Still best = Trial continues normally
- New alternative = Consider /garden:swap
- Better alternative existed = Learn lesson for next trial

#### 5. Time Budget
- [ ] Messages used: ____ / 50 target
- [ ] Estimated completion: ____ days
- [ ] On track for decision deadline?

**Interpretation:**
- 40+ messages with decision clarity = Next decision at threshold
- 20-30 messages, still evaluating = Continue normally
- <10 messages, stalled = Plugin not being used, decision needed

### Red Flag Decision Tree

If any red flag appears, decide immediately:

```
Plugin causing errors?
├─ YES → /garden:remove
└─ NO ↓

Not being used at all?
├─ YES → /garden:remove
└─ NO ↓

Better alternative available?
├─ YES → /garden:swap
└─ NO ↓

Learning curve too steep?
├─ YES → /garden:remove or /garden:reset for learning
└─ NO ↓

Doesn't integrate with existing tools?
├─ YES → /garden:remove
└─ NO ↓

Continue trial normally
```

### Trial Journal Template

Keep brief notes during trial:

```markdown
## Trial: plugin-name

### Week 1
- Usage pattern: [natural/forced/none]
- Errors encountered: [none/minor/major]
- Progress on success criteria: [criterion 1: progress, criterion 2: progress]
- Notes: [What we learned this week]

### Week 2
- Usage pattern: [...]
- Errors: [...]
- Progress: [...]
- Notes: [...]
```

---

## Part 3: Decision Point Framework (50 Messages)

### The Decision Meeting

When message counter reaches 50, hold a decision meeting (internal or with team):

#### Agenda (15 minutes)

1. **State Success Criteria** (2 minutes)
   - Criterion 1: Expected outcome
   - Criterion 2: Expected outcome
   - Criterion 3: Expected outcome

2. **Review Actual Outcomes** (5 minutes)
   - Criterion 1: Actual outcome vs. expected
   - Criterion 2: Actual outcome vs. expected
   - Criterion 3: Actual outcome vs. expected

3. **Assess Friction** (3 minutes)
   - Errors encountered: List
   - Learning curve: Easy/medium/hard
   - Integration: Smooth/rough/blockers

4. **Make Decision** (3 minutes)
   - KEEP / SWAP / REMOVE
   - Alternative if swapping
   - Action items

5. **Document** (2 minutes)
   - Update trial-log.md immediately
   - Set completion date
   - Record decision rationale

### Quantitative Decision Matrix

Score the plugin across criteria:

| Criterion | Weight | Score 1-5 | Weighted |
|-----------|--------|-----------|----------|
| Usefulness | 30% | 4 | 1.2 |
| Reliability | 25% | 3 | 0.75 |
| Learning Curve | 20% | 4 | 0.8 |
| Documentation | 15% | 5 | 0.75 |
| Integration | 10% | 3 | 0.3 |
| **TOTAL** | **100%** | | **3.8/5** |

**Interpretation:**
- 4.0-5.0: KEEP (strong)
- 3.5-3.9: KEEP (marginal, monitor)
- 3.0-3.4: SWAP (try alternative)
- 2.0-2.9: REMOVE (significant issues)
- <2.0: REMOVE (major problems)

### Qualitative Decision Framework

Ask the hard questions:

**For KEEP:**
1. "Would I introduce this to a new team member?"
2. "Do I miss this when using alternatives?"
3. "Would we be worse off without it?"

If yes to all three → KEEP is right decision

**For SWAP:**
1. "What's specifically better about the alternative?"
2. "Have we verified the alternative works?"
3. "Can we live with current plugin for 1 more week?"

If alternative is proven → SWAP is right decision

**For REMOVE:**
1. "What went wrong?"
2. "Would we ever revisit this?"
3. "What did we learn?"

If problems are fundamental → REMOVE is right decision

### Decision Tracking

Record in trial-log.md:

```markdown
## Decision: plugin-name

**Date Decided:** 2026-01-15
**Messages Used:** 48
**Decision:** KEEP

### Success Criteria Assessment
- Criterion 1: PASSED (Expected X, achieved X)
- Criterion 2: PASSED (Expected X, achieved X)
- Criterion 3: PARTIAL (Expected X, achieved Y)

### Friction Assessment
- Errors: 0 major, 2 minor
- Learning Curve: Medium (took 3 days to master)
- Integration: Smooth with existing tools

### Quantitative Score
- Usefulness: 4/5
- Reliability: 4/5
- Learning Curve: 3/5
- Documentation: 4/5
- Integration: 4/5
- **Average: 3.8/5**

### Decision Rationale
[1-2 paragraphs explaining the decision]

### Action Items
- [ ] If KEEP: Promote to permanent, move to supported config
- [ ] If SWAP: Start new trial with alternative
- [ ] If REMOVE: Document lessons learned
```

---

## Part 4: Post-Decision Framework

### After KEEP Decision

**Immediate Actions:**
- [ ] Move plugin from trial state to permanent
- [ ] Ensure plugin documentation is in supported config
- [ ] Schedule quarterly review (check if still used)
- [ ] Integrate into team onboarding if needed

**Long-term Monitoring:**
- Last-used tracking (detect disuse)
- Performance monitoring (if applicable)
- Update documentation as new use cases appear
- Plan for eventual removal if usage declines

### After SWAP Decision

**Immediate Actions:**
- [ ] Start new trial with identified alternative
- [ ] Set expectation for alternative to be superior
- [ ] Plan removal of old plugin
- [ ] Document migration path

**Evaluation Period:**
- Parallel trial: Run new plugin while old still available
- Direct comparison: Easy switching if alternative doesn't work out
- Decision deadline: 50 messages for new alternative too

### After REMOVE Decision

**Immediate Actions:**
- [ ] Document lessons learned (what went wrong, why)
- [ ] Remove plugin config
- [ ] Verify no dependencies exist
- [ ] Update any documentation mentioning it

**Learning Capture:**
- What problem were we trying to solve?
- Why didn't this solution work?
- What would need to change to make it viable?
- Would we try this again with modifications?

**Archive Pattern:**
Keep removed plugins in removed list with reason. Don't delete—preserve history.

---

## Part 5: Common Decision Scenarios

### Scenario 1: Plugin Works Great, Team Loves It

**Signals:**
- Heavy usage (40+ messages in 40 days)
- Zero major errors
- Positive feedback
- Already in team workflows

**Decision Path:**
```
Excellent trial performance
    ↓
KEEP immediately
    ↓
Move to permanent config
    ↓
Schedule 6-month review
```

**Follow-up:**
- Ensure it stays maintained
- Monitor for deprecation risk
- Plan upgrade path if needed

### Scenario 2: Plugin Works Partially, Not Clear if Worth It

**Signals:**
- Moderate usage (20-30 messages in 40 days)
- Works well when used, but not essential
- 1-2 issues encountered
- Team has mixed opinions

**Decision Path:**
```
Unclear benefit after trial
    ↓
Use QUANTITATIVE matrix
    ↓
If score 3.5-3.9: KEEP (marginal) with 3-month review
If score 3.0-3.4: SWAP if alternative available
If score <3.0: REMOVE
```

**Follow-up if KEEP:**
- Set mandatory 3-month review date
- Assign champion to use actively
- Plan for REMOVE if usage doesn't increase

### Scenario 3: Plugin Has Bugs or Problems

**Signals:**
- Errors encountered (3+ in trial period)
- Workarounds needed
- Learning curve steeper than expected
- Integration issues

**Decision Path:**
```
Significant problems found
    ↓
Better alternative exists?
├─ YES: SWAP immediately
└─ NO: ↓
  Is plugin actively maintained?
  ├─ YES: RESET for bug fix period
  └─ NO: REMOVE
```

**Follow-up if RESET:**
- Set specific bug-fix targets
- Verify issues resolved in new version
- Shorter trial period (25 messages) for validation

### Scenario 4: Plugin Not Being Used

**Signals:**
- Light usage (<10 messages in 40 days)
- Plugin installed but rarely invoked
- More alternatives available
- No emergency need

**Decision Path:**
```
Plugin unused in trial
    ↓
REMOVE (low value, wasted mental load)
    ↓
Document: "Abandoned during trial"
    ↓
Lessons: Why did we think we needed this?
```

**Learn from this:**
- Pre-trial assessment missed something
- Plugin didn't match real needs
- Better alternative should have been clear
- Improve pre-trial decision process

### Scenario 5: New Alternative Appeared Mid-Trial

**Signals:**
- Better plugin discovered after trial started
- Original plugin still adequate, not problematic
- New alternative has strong reputation
- Worth testing the better option

**Decision Path:**
```
Better alternative discovered
    ↓
SWAP to new alternative
    ↓
Evaluate new plugin for 50 messages
    ↓
Compare head-to-head
    ↓
KEEP winner, document lessons
```

**Best Practice:**
- Run both in parallel for 1-2 weeks
- Make direct comparison if possible
- Remove loser after winner validated

---

## Part 6: Avoiding Anti-Patterns

### Anti-Pattern 1: "Forever Trials"

**Problem:** Plugin stays in trial indefinitely, never promoted or removed.

**Prevention:**
- Set hard 50-message decision deadline
- If uncertain at 50: Reset for exactly 50 more (not open-ended)
- Max 2 resets before forced decision
- After 3 resets: Default to REMOVE

**Example Timeline:**
- Days 1-10: Trial active, 20 messages
- Days 10-20: Trial active, 50 messages total → Decision point
- If RESET: Another 50 messages
- Days 20-30: Second trial period, 50 messages total
- If RESET again: Final 50 messages
- Days 30-40: Final trial period, 50 messages total
- At 150 total messages: FORCED decision (keep or remove)

### Anti-Pattern 2: "Just in Case" Permanent Plugins

**Problem:** Plugin promoted to permanent but barely used afterward.

**Prevention:**
- Quarterly audit of permanent plugins
- Track last-used timestamp
- Remove unused plugins after 1 month disuse
- Be aggressive: prefer fewer, focused tools

**Quarterly Audit Template:**
```markdown
## Permanent Plugin Audit (Q1 2026)

- [x] skogai-jq: Last used 2026-01-04 → KEEP
- [ ] skogai-old-tool: Last used 2025-11-15 → REMOVE
- [x] my-favorite-plugin: Used daily → KEEP
- [ ] backup-tool: Never used → REMOVE
```

### Anti-Pattern 3: "Undocumented Decisions"

**Problem:** Plugin removed but no one remembers why, leads to re-trial later.

**Prevention:**
- Every removal must have documented reason
- Trial log is permanent, never deleted
- Reason should be specific enough that future version would address it

**Example Good Reasons:**
- "Better alternative (skogai-new-tool) now exists"
- "Plugin generates 5+ errors per session"
- "Learning curve too steep for team adoption"
- "Scope doesn't match project needs"

**Example Bad Reasons:**
- "Didn't work"
- "Wasn't using it"
- "Seemed unnecessary"

### Anti-Pattern 4: "Criteria Drift"

**Problem:** Success criteria change during trial to justify keeping failing plugin.

**Prevention:**
- Write criteria BEFORE trial starts
- Treat criteria as immutable
- Any criteria changes are REMOVED criteria (tighten, never loosen)
- If criteria change mid-trial → plugin doesn't meet original requirements → REMOVE

### Anti-Pattern 5: "No Data, Just Opinion"

**Problem:** Decision made on gut feeling with no message count or usage data.

**Prevention:**
- Always wait for 50-message threshold (or reset/swap decision)
- Quantitative matrix required for marginal decisions (3.0-3.9 scores)
- Document actual usage patterns in decision record
- Avoid "I think this is good" without data

---

## Part 7: Metrics and Learning

### Success Rate Tracking

Track outcomes to improve pre-trial assessment:

```markdown
## Garden Metrics (2026)

**Total Trials:** 15
**Kept:** 8 (53%)
**Swapped:** 3 (20%)
**Removed:** 4 (27%)

### Success Rate Analysis
- Kept plugins with 4+ criteria met at start: 80% success rate
- Kept plugins with 2 criteria met at start: 40% success rate
- → Stricter pre-trial criteria screening improves outcomes

### Swap Analysis
- Swaps: Plugin worked okay but alternative was better
- Lesson: Earlier identification of alternatives could prevent wasted trial time

### Removal Analysis
- Removals for lack of use: 2 (could have detected earlier)
- Removals for errors: 1 (acceptable risk)
- Removals for scope mismatch: 1 (pre-trial assessment failed)
```

### Retrospective Review

Quarterly, review your trial decisions:

**Questions:**
1. Did decisions hold up over time?
2. Are kept plugins still used?
3. Did removed plugins stay removed?
4. Would you make same decisions again?
5. What's the ratio of good decisions to questionable ones?

**Adjustments:**
- If KEEP plugins aren't used: Tighten success criteria
- If removed plugins are re-trialed: Improve documentation of why
- If low decision confidence: Require quantitative matrix for all decisions
- If good decisions: Keep current process

---

## Part 8: Decision Framework Quick Reference

### Decision Tree (Ultra-Condensed)

```
Used in 50+ messages?
├─ NO → REMOVE
└─ YES ↓

Zero major errors?
├─ NO → SWAP or REMOVE
└─ YES ↓

Meets 2+ success criteria?
├─ NO → REMOVE
└─ YES ↓

Worth keeping vs alternative?
├─ NO → SWAP
└─ YES ↓

KEEP
```

### Decision Scoring (1-Minute Method)

Rate 1-5 on:
- Usefulness (is it actually used?)
- Reliability (does it work?)
- Integration (fits with other tools?)

**Sum score:**
- 13-15: KEEP strong
- 10-12: KEEP marginal (3-month review)
- 7-9: SWAP (try alternative)
- <7: REMOVE

### Decision Prompts (When Unsure)

Ask yourself:
1. "Would I choose this again if starting over?" → KEEP if yes
2. "Is this better than what we had before?" → KEEP if significantly
3. "Would the project suffer without this?" → KEEP if definitely
4. "Are we stuck with this forever if we keep it?" → REMOVE if yes

---

**Last Updated:** 2026-01-05
**Document Version:** 1.0.0
**Companion Documents:**
- `@.skogai/garden/best-practices.md` — Comprehensive best practices
- `@.skogai/garden/architecture.md` — Technical architecture reference
- `@.skogai/garden/implementation-summary.md` — 30-minute overview
