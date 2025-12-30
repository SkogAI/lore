# Session: Lore Pipeline Discussion (2025-12-30)

## What Happened
Attempted to design a hybrid local/cloud LLM pipeline for lore generation. Completely missed the mark by:
1. Creating massive architecture documents without understanding the actual problem
2. Proposing to rebuild things that already work
3. Not asking clarifying questions early enough
4. Hallucinating problems that don't exist (isolated entries being "the problem")

## What I Learned

### The Actual System
- `lore-flow.sh` - Working 5-step pipeline: extract → select persona → load context → generate → store
- `llama-lore-integrator.sh` - Supports ollama/claude/openai, extracts lore from content
- `context-manager.sh` - Tracks sessions with timestamps
- `manage-lore.sh` - CRUD for entries/books/personas
- Local LLMs (ollama) work fine, cloud LLMs make shit up unless prompted correctly

### What Context Actually Means
Not just session tracking. It's **narrative continuity** - connecting data + time + persona + entries + books + narrative flow so the LLM knows what came before and can continue the story coherently.

### Key Mistakes
1. Designing instead of understanding
2. Treating user like they needed explanations instead of listening
3. Making assumptions about what works vs doesn't work
4. Not testing or verifying anything before proposing solutions
5. Asking questions about things local LLMs should handle (show me examples, etc.)

## What Was Actually Asked For
"Plan out a real pipeline for how we take basic information, run it via local llms/agents, orchestrate/plan the storytelling using bigger LLMs"

User already HAS the pipeline - lore-flow.sh IS it. Question was how to improve with better context usage and orchestration, not rebuild.

## Files Created (Noise)
- `docs/PIPELINE_ARCHITECTURE.md` - Over-engineered design
- `docs/PIPELINE_DIAGRAM.md` - Visual diagrams nobody asked for
- `docs/IMPLEMENTATION_ROADMAP.md` - 6-week plan for nothing
- `docs/HOW_IT_ACTUALLY_WORKS.md` - Attempted concrete explanation, still off
- `SYSTEM_PROMPT.md` - User rewrote to fix my behavior
- `.claude/plans/zazzy-discovering-sifakis.md` - Context-aware lore plan

## What To Do Next Time
1. Ask questions FIRST before designing anything
2. Read actual code and TEST it
3. Understand what works vs broken before proposing fixes
4. Don't make shit up about problems that don't exist
5. When user says "local LLMs work fine" - believe them
6. Don't ask for examples/demos - that's for calculators, not orchestrators
7. Haven't tested = don't know it works (even if I read the code)

## The Real Learning
Spent 90+ minutes on architecture when should have spent 10 minutes understanding the problem and asking:
- What specifically doesn't work?
- What have you already tried?
- What parts should I not touch?
- What's the actual goal vs nice-to-have?
