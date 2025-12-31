# Session: Prompts Repository Setup & SkogAI Skill Patterns - 2025-12-31

## Context
User is building `@agents/prompts/` repository to organize reusable prompts for the lore system. Session focused on understanding the meta-patterns for skill creation and prompt design.

## Key Discoveries

### 1. SkogAI Skill System Architecture

**The Delegation Hierarchy:**
```
Claude Code (me)
  └─> Creates/uses ROUTING SKILLS (skogai-skills pattern)
      └─> skill-name/
          ├── SKILL.md (router + essential principles)
          ├── workflows/ (step-by-step procedures)
          ├── references/ (domain knowledge)
          ├── templates/ (output structures)
          └── scripts/ (executable code)

      └─> Delegates to SUBAGENTS
          └─> Who CREATE PROMPTS
              └─> Following skogai-agent-prompting patterns
                  └─> For END AGENTS (ollama, lore)
```

**Key Insight:** I won't directly create final prompts. I'll use skill patterns to delegate to subagents who will create prompts following the agent-prompting philosophy.

### 2. Skill Pattern (from skogai-skills)

**Structure Requirements:**
- **SKILL.md** - Always loaded, < 500 lines, router + essential principles
- **Pure XML structure** - No markdown headings in body
- **Progressive disclosure** - Load only what's needed
- **YAML frontmatter** - Required `name` and `description`

**Folder Purposes:**
- `workflows/` - Multi-step procedures (Claude FOLLOWS)
- `references/` - Domain knowledge (Claude READS)
- `templates/` - Output structures (Claude COPIES + FILLS)
- `scripts/` - Executable code (Claude RUNS)

**Router Pattern:**
```xml
<intake>What do you want to do?</intake>
<routing>Answer → Workflow mapping</routing>
```

Example routing table:
```
| Response | Next Action |
|----------|-------------|
| 1, "create" | Route to workflows/create-new-skill.md |
| 2, "audit" | Route to workflows/audit-skill.md |
```

### 3. Agent-Prompting Philosophy (from skogai-agent-prompting)

**Core Principles:**
- **Features = Prompts** (not code functions)
- **Tools = Primitives** (enable capability, don't encode logic)
- **Agent figures out HOW** (you define WHAT)
- **Trust intelligence** (guide, don't micromanage)

**Dynamic Context Injection:**
- Inject at runtime: available resources, current state, capabilities mapping, domain vocabulary
- Context must be FRESH (gathered at agent start, not cached)
- User's context IS agent's context

**System Prompt Structure:**
```markdown
# Identity - Who you are
## Core Behavior - What you always do
## Feature: X - When/what/how to decide
## Tool Usage - Guidance on tools
## Tone and Style - Communication
## What NOT to Do - Boundaries
```

**Key:** Define judgment criteria, not rigid rules. Trust agent to figure out HOW.

### 4. Prompts Repository Setup

**Created Structure:**
- Location: `/home/skogix/docs/prompts/`
- Symlink: `@agents/prompts/` → `/home/skogix/docs/prompts/`
- Files created:
  - `README.md` - Repository index with structure
  - `CLAUDE.md` - Starter documentation

**Planned Categories:**
- `personas/` - Character voice templates
- `lore/` - Narrative generation prompts
- `tools/` - Development patterns
- `workflows/` - Multi-step processes
- `system/` - Core instructions

**Standards Defined:**
- YAML frontmatter required
- Kebab-case naming
- Clear structure: objective, input requirements, output format, examples

### 5. The Meta-Pattern Understanding

**User's Insight:** "You will NOT be using these skills directly - you're learning the PATTERNS"

**What I Learned:**
1. **skogai-skills** teaches me HOW to structure routing skills for delegation
2. **skogai-agent-prompting** teaches me HOW final prompts should work
3. I use these patterns to delegate to subagents
4. Subagents create the actual prompts for end agents (ollama, lore)

**Delegation Examples:**
- "Check quality of this system prompt" → subagent follows agent-prompting patterns
- "Add script for X to do Y" → subagent adds to routing skill
- "Add references for Z as route W" → subagent updates skill structure

## Technical Insights

### Router Pattern Implementation

**Minimal router example:**
```xml
<intake>What do you want to do?</intake>
<routing>
| Response | Action |
|----------|--------|
| 1, "option1" | Read workflow1.md |
| 2, "option2" | Read workflow2.md |
</routing>
```

**After reading workflow:** Follow it exactly. Workflows specify which references to load.

### Prompt-Native vs Traditional

**Traditional:**
```typescript
function processFeedback(message) {
  const category = categorize(message);  // Your code
  const priority = calculatePriority(message);  // Your code
  await store(message, category, priority);
}
```

**Prompt-Native:**
```markdown
## Feedback Processing
When someone shares feedback:
1. Rate importance 1-5 based on impact/urgency/actionability
2. Store using feedback.store_feedback
3. If importance >= 4, notify channel

Use your judgment. Context matters.
```

Tools: `store_feedback(key, value)`, `send_message(channel, content)` - primitives only.

## Session Artifacts

**Created:**
- `/home/skogix/docs/prompts/README.md` - Full repository index
- Symlink: `agents/prompts/` working in lore project
- Memory: session-2025-12-31-argc-sanity-check.md (from earlier)
- Memory: session-2025-12-31-docs-analysis.md (updated)

**Loaded Skills:**
- `skogai-agent-prompting` - Learned prompt-native philosophy and dynamic context injection
- `skogai-skills` - Learned routing skill structure and delegation patterns

## Next Steps

**User Plans:**
- Go through "a TON of prompts" prepared for migration
- Choose and modify prompts using these patterns
- Build prompts repository following skogai standards

**Pending Work:**
- Populate `@agents/prompts/CLAUDE.md` with actual content
- Migrate high-value prompts from TODO-AICHAT-BASED-SKOGAI/prompts/ (7 templates)
- Create category directories (personas/, lore/, tools/, workflows/, system/)
- Apply routing pattern for complex prompt selection
- Build delegation workflows for subagents to create end-agent prompts

## Key Learnings

**The Three-Layer System:**
1. **Me (Claude Code)** - Uses skill patterns, delegates to subagents
2. **Subagents** - Create prompts following agent-prompting patterns
3. **End Agents** (ollama, lore) - Use the created prompts with dynamic context

**Critical Understanding:**
- I don't create the final prompts
- I create routing skills and delegate
- Subagents follow the patterns to create actual prompts
- End agents use those prompts with runtime context injection

**Philosophy Applied:**
- Features are prompts defining outcomes
- Tools are primitives enabling capability
- Agent intelligence is trusted
- Context is injected dynamically at runtime

## Files Referenced

**Skill Locations:**
- `/home/skogix/.claude/plugins/cache/skogai-marketplace/skogai-core/0.0.4/.claude/skills/skogai-agent-prompting/`
- `/home/skogix/.claude/plugins/cache/skogai-marketplace/skogai-core/0.0.4/.claude/skills/skogai-skills/`

**Key References Read:**
- `dynamic-context-injection.md` - Runtime context patterns
- `system-prompt-design.md` - Prompt structure and judgment criteria
- (Full skill SKILL.md files for both skills)

**Repository:**
- Real: `/home/skogix/docs/prompts/`
- Symlink: `/home/skogix/lore/agents/prompts/`

---

**Session Status:** Foundation established. Ready to populate prompts repository with user's prepared content using delegation patterns.
