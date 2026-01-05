# Lore Project - Current Understanding

## Core Concept

Lore is an agent memory system that uses narrative as the storage format. It transforms work sessions (code changes, commits, chat logs) into mythological narrative entries that become
persistent memory for AI agents across sessions.

## The System Architecture

### Data Model

Three atomic units, each with JSON Schema contracts:

1. Entry (@knowledge/core/lore/schema.json) - Atomic narrative unit

- Categories: character, place, event, object, concept
- Storage: knowledge/expanded/lore/entries/entry*<timestamp>[*<hash>].json
- Contains content field with markdown narrative

2. Book (@knowledge/core/book-schema.json) - Collection of entries

- Storage: knowledge/expanded/lore/books/book\_<timestamp>.json
- Access control: readers (view), owners (modify)
- Status: draft, active, archived, deprecated

3. Persona (@knowledge/core/persona/schema.json) - AI character profile

- Storage: knowledge/expanded/personas/persona\_<timestamp>.json
- Defines: voice.tone, core_traits (values/motivations), interaction_style
- Links to lore books via knowledge.lore_books

### APIs and Tools

agents/api/lore_api.py - Simple CRUD for JSON files:

- create_lore_entry(), create_lore_book(), create_persona()
- add_entry_to_book(), link_book_to_persona()
- Just ID generation (timestamp) + JSON writing with json.dump()

agents/api/agent_api.py - LLM API wrapper:

- Calls OpenRouter API (GPT-4, Claude, etc.)
- Saves to demo/content*creation*<session>/ (temporary)
- Generates content (text), doesn't create lore data

scripts/jq/ - Standard CRUD operations across all skogai projects:

- crud-get/, crud-set/, crud-delete/ for JSON manipulation

Argcfile.sh - CLI interface:

- argc list-books, argc show-book, argc read-book-entries
- Self-validating, reads actual data files

tools/context-manager.sh - Session lifecycle:

- create <template> - Generate session context
- update <session_id> <key> <value> - Track state
- archive <session_id> - Store completed sessions

## The Binding Mechanism

Context is the glue connecting data + agent + time + history.

### Session ID Binding

A session_id (timestamp) ties together:

- Data: Which personas, books, entries are active
- Agent: Which agent is running, orchestrator mode
- Time: Session timeline and timestamps
- History: What knowledge was loaded, what actions occurred

### Entry ID Format as Quantum Entanglement

Pattern 1: entry\_<timestamp> - Individual entry (personal timeline)

Pattern 2: entry*<timestamp>*<hash> - Batch entry (shared mythology)

- Same timestamp = quantum entangled concept batch
- Different hash = differentiated members of the batch
- Example: entry*1759487978*\* (12 entries) created together as system architecture mythology

### Template Mappings

@context/templates/persona-context.json shows the interface adapter:
"template_mappings": {
"{{name}}": "persona.name",
"{{voice_tone}}": "persona.voice.tone",
"{{personality_traits}}": "persona.core_traits.values",
"{{lore_books}}": "persona.knowledge.lore_books"
}

This transforms persona JSON → agent prompt parameters.

## Why Narrative Format?

1. Compressed context: "vanquished the auth daemon" loads more meaning than "fixed bug #123"
2. Consistent persona: Agents maintain voice/perspective across sessions
3. Memorable: Stories stick, bullet points don't
4. Relational: Entries link to each other, building a knowledge graph

### Mythology as Technical Documentation

Real examples from book_1759486042:

"Quantum Birds"

- Content: "Chirp in programming languages, nest in directory trees. Migration patterns follow git branches."
- Meaning: Directory navigation and git workflow compressed into metaphor

"The PATCH TOOL"

- Content: "Creator: Dot. Uses: Rewrite history, Fix timeline paradoxes."
- Meaning: Git operations (rebase, amend, etc.)

"Two-Number Entry Bridges"

- Content: "Allow quantum entanglement of ideas across universes."
- Summary: "Pattern: entry*[timestamp1][hash1] ↔ entry[timestamp2]*[hash2]"
- Meaning: The entry describes its own ID format - meta-documentation

### The Multiverse

Same concepts appear across different agent books with different narrative interpretations.

Example:

- Book 1744512793 (Orchestrator): "Greenhaven" - medieval village with Village Elder
- Book 1759486042 (Lore-Collector): "The Village (Goose's Domain)" - same place, Goose perspective

Cross-book references create a shared mythology where each agent has their own story about the same underlying system concepts.

## Current State (Updated 2026-01-05)

- **107 books** (up from 102)
- **1202 entries** (up from 728)
- **92 personas** (up from 89)

### Verified Working Components

**Core Infrastructure:**

- ✅ Python LoreAPI - Full CRUD operations for entries/books/personas
- ✅ manage-lore.sh - Fixed and working (now writes JSON files correctly)
- ✅ All three LLM providers tested: Claude, OpenAI (via OpenRouter), Ollama (local)

**Lore Generation Tools:**

- ✅ llama-lore-creator.sh - Creates entries with LLM content (all providers)
- ✅ llama-lore-integrator.sh - Extracts lore from documents
- ✅ integration/lore-flow.sh - Full 5-step pipeline operational

**Known Issues:**

- ⚠️ [Issue #5](https://github.com/SkogAI/lore/issues/5): LLM meta-commentary in content
- ⚠️ [Issue #6](https://github.com/SkogAI/lore/issues/6): Pipeline content update bug

Recent test additions (2025-12-12):

- Multiple test entries created during comprehensive provider testing
- Verified end-to-end workflow from entry creation to book linking
- Confirmed all providers generate valid JSON entries

## Numbered Knowledge System

Core knowledge files organized by ID ranges:

- 00-09: Core/Emergency (load FIRST)
- 10-19: Navigation
- 20-29: Identity
- 30-99: Operational
- 100-199: Standards
- 200-299: Project-specific
- 300-399: Tools/Docs
- 1000+: Frameworks

Generated index at @knowledge/INDEX.md via @tools/index-knowledge.sh

## The Pipeline (Conceptual)

From @docs/CONCEPT.md:

1. User + Big LLM → Actual work happens (chat, code, commits)
2. Orchestrator → Captures what happened, extracts events/snippets
3. Local AI (24/7) → Rewrites snippets into narrative lore (free, always running)
4. Storage → JSON entries with content, tags, relationships
5. Future sessions → Agents load their lore as context/memory

### What Has Been Verified (2025-12-12)

- [x] Integration workflows - The pipeline connecting git commits → lore generation **works end-to-end**
  - Tested manual input and git-diff modes
  - All 5 steps complete: extract → select persona → load context → generate narrative → create entry
  - Known issue: content field empty (Issue #6), but entry creation works

- [x] LLM provider integration - All three providers confirmed working
  - Claude (via OpenRouter API)
  - OpenAI (via OpenRouter API)
  - Ollama (local models like llama3)

### What Needs Further Exploration

- [x] Orchestrator implementation details - Documented in `orchestrator/orchestrator.py` and `docs/SYSTEM_MAP.md`
- [x] Knowledge Router logic - Documented in `docs/SYSTEM_MAP.md` (selects numbered modules 00-99 based on task type)
- [x] Context State Machine - Documented in `docs/SYSTEM_MAP.md` (tracks active task, pipeline progress)
- [ ] Persona-bridge integration - Code exists at `integration/persona-bridge/`, needs end-to-end testing and verification

---

Key insight: This isn't a content generation system. It's a memory persistence system using narrative compression to store technical knowledge in a format that AI agents can load as
context across sessions, maintaining consistent personality and building a shared mythological knowledge graph.

## Recent Session Learnings (2025-12-30 to 2026-01-04)

### Session Memory System

**Location:** `.serena/memories/`

Claude Code now maintains session memories documenting learnings across sessions. Key discoveries:

### 1. Pipeline Architecture Reality (2025-12-30)

**What We Learned:**
- `lore-flow.sh` IS the working pipeline - 5 steps: extract → select persona → load context → generate → store
- Context = **narrative continuity** (not just session tracking) - connects data + time + persona + flow
- Local LLMs (ollama) work fine, cloud LLMs require correct prompting
- `llama-lore-integrator.sh` supports ollama/claude/openai

**Key Mistakes to Avoid:**
- Over-designing before understanding the actual system
- Proposing to rebuild things that already work
- Not asking clarifying questions early enough
- Hallucinating problems that don't exist

### 2. Tool Status Clarification (2025-12-30)

**Critical Discovery:**
- Shell tools (manage-lore.sh, llama-*.sh) are PRIMARY, stable implementation
- Python API (lore_api.py) is "broken as fudge" - NOT the shell tools
- All shell tools support 3 LLM providers (ollama, claude, openai)

**Documentation Created:**
- `docs/api/generation-tools.md` (1078 lines) - Complete reference for all 6 generation tools
- Corrected incorrect deprecation notices

### 3. Skill Routing Patterns (2025-12-31)

**Architecture Learned:**
```
Claude Code (me)
  └─> Creates ROUTING SKILLS (skogai-skills pattern)
      └─> Delegates to SUBAGENTS
          └─> Who CREATE PROMPTS (skogai-agent-prompting patterns)
              └─> For END AGENTS (ollama, lore)
```

**Key Concepts:**
- **Features = Prompts** (not code functions)
- **Tools = Primitives** (enable capability, don't encode logic)
- **Dynamic Context Injection** - Runtime state, not cached
- **Progressive Disclosure** - Load only what's needed

### 4. Repository Index & Token Savings (2025-12-31)

**Achievement:**
- Created PROJECT_INDEX.md covering 204 files (~30K lines)
- Index size: ~3KB = **94% token reduction** per session
- ROI: 10 sessions = 550K tokens saved, 100 sessions = 5.5M tokens saved

**Discovered:**
- TODO-AICHAT-BASED-SKOGAI legacy docs (63 files)
- Prompts repository setup at `agents/prompts/`

### 5. CLI Coverage Verification (2025-12-31)

**Verified:**
- argc provides **100% coverage** of lore API
- All CRUD operations working (create, read, list, link, validate)
- End-to-end flow tested successfully
- Critical: `LLM_OUTPUT` env var required for argc commands

**Current Data Volume (verified 2026-01-05):**
- 1,202 lore entries (up from 728)
- 107 books (up from 102)
- 92 personas (up from 89)

### What Changed Our Understanding

**Context is not just session tracking** - it's the glue connecting:
- Data (which personas/books/entries are active)
- Agent (which agent is running, what mode)
- Time (session timeline and timestamps)
- History (what knowledge was loaded, what actions occurred)
- **Narrative Flow** (continuity of storytelling across entries)

**The System Works** - verified components:
- ✅ lore-flow.sh pipeline (all 5 steps)
- ✅ All 3 LLM providers (claude, openai, ollama)
- ✅ Shell tool CRUD operations
- ✅ argc CLI coverage
- ✅ Session context tracking

**Known Issues Still Present:**
- Issue #5: LLM generates meta-commentary instead of lore content
- Issue #6: Pipeline creates entries with empty content field

### Next Steps and Current Priorities

**See GitHub Issues for up-to-date task list:** https://github.com/SkogAI/lore/issues

Priority areas based on open issues:

1. **Bug Fixes:**
   - Issue #31: Pipeline creates entries with empty content field (Issue #6 investigation)
   - Issue #32: Improve prompt to reduce LLM meta-commentary (Issue #5)

2. **Documentation:**
   - Issue #25: Deprecate Python lore_api.py - document shell tools as canonical
   - Issue #33: Update CLAUDE.md to reflect current system state
   - Issue #22-24: Fix broken documentation links across multiple files

3. **Code Refactoring:**
   - Issue #26-28: Migrate Python tools from LoreAPI to shell tools
   - Issue #37: Clean up unused Python API references in lore-flow.sh

4. **Feature Enhancements:**
   - Issue #29: Extract inline LLM prompts to offloadable prompt+data format
   - Issue #30: Add generation queue for offline/batch lore processing

**Note:** The GitHub issues tracker is the single source of truth for current tasks and priorities.

---

**Last Updated:** 2026-01-05  
**Session Memories:** 5 sessions documented in `.serena/memories/` directory  
**GitHub Issues:** https://github.com/SkogAI/lore/issues (18 open issues as of 2026-01-05)
