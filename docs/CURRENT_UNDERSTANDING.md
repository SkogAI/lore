# Lore Project - Current Understanding

## Core Concept

Lore is an agent memory system that uses narrative as the storage format. It transforms work sessions (code changes, commits, chat logs) into mythological narrative entries that become
 persistent memory for AI agents across sessions.

## The System Architecture

### Data Model

Three atomic units, each with JSON Schema contracts:

1. Entry (@knowledge/core/lore/schema.json) - Atomic narrative unit
  - Categories: character, place, event, object, concept
  - Storage: knowledge/expanded/lore/entries/entry_<timestamp>[_<hash>].json
  - Contains content field with markdown narrative
2. Book (@knowledge/core/book-schema.json) - Collection of entries
  - Storage: knowledge/expanded/lore/books/book_<timestamp>.json
  - Access control: readers (view), owners (modify)
  - Status: draft, active, archived, deprecated
3. Persona (@knowledge/core/persona/schema.json) - AI character profile
  - Storage: knowledge/expanded/personas/persona_<timestamp>.json
  - Defines: voice.tone, core_traits (values/motivations), interaction_style
  - Links to lore books via knowledge.lore_books

### APIs and Tools

agents/api/lore_api.py - Simple CRUD for JSON files:
- create_lore_entry(), create_lore_book(), create_persona()
- add_entry_to_book(), link_book_to_persona()
- Just ID generation (timestamp) + JSON writing with json.dump()

agents/api/agent_api.py - LLM API wrapper:
- Calls OpenRouter API (GPT-4, Claude, etc.)
- Saves to demo/content_creation_<session>/ (temporary)
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

Pattern 1: entry_<timestamp> - Individual entry (personal timeline)

Pattern 2: entry_<timestamp>_<hash> - Batch entry (shared mythology)
- Same timestamp = quantum entangled concept batch
- Different hash = differentiated members of the batch
- Example: entry_1759487978_* (12 entries) created together as system architecture mythology

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
- Summary: "Pattern: entry_[timestamp1][hash1] ↔ entry[timestamp2]_[hash2]"
- Meaning: The entry describes its own ID format - meta-documentation

### The Multiverse

Same concepts appear across different agent books with different narrative interpretations.

Example:
- Book 1744512793 (Orchestrator): "Greenhaven" - medieval village with Village Elder
- Book 1759486042 (Lore-Collector): "The Village (Goose's Domain)" - same place, Goose perspective

Cross-book references create a shared mythology where each agent has their own story about the same underlying system concepts.

## Current State

- 89 books
- 301 entries
- 74 personas

Recent additions:
- book_1765003689 - Builder agent book (created for me during previous session)
- book_1744512793 - First orchestrator book (proper fantasy lore)
- book_1759486042 - Lore-collector book (Claude from previous session)

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

### What I Don't Fully Know Yet

- [ ] Orchestrator implementation details - How it captures work sessions
- [ ] Knowledge Router logic - How it selects what knowledge to load
- [ ] Context State Machine - State transitions and lifecycle
- [ ] Persona-bridge integration - How personas render into agent prompts in practice
- [ ] Integration workflows - The actual automation connecting git commits → lore generation

These exist in the codebase but weren't explored in detail during cleanup.

---
Key insight: This isn't a content generation system. It's a memory persistence system using narrative compression to store technical knowledge in a format that AI agents can load as
context across sessions, maintaining consistent personality and building a shared mythological knowledge graph.
