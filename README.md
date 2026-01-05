# Lore - Digital Mythology Generation System

Multi-agent system that transforms technical changes (git commits, code changes, chat logs) into narrative lore entries. Acts as persistent memory for AI agents using narrative compression.

## Quick Start

```bash
# View stats
argc list-books
argc list-entries

# Create lore from git commit
./integration/lore-flow.sh git-diff HEAD

# Manual lore creation
./integration/lore-flow.sh manual "Fixed quantum mojito mixer bug"

# Create entry directly
tools/manage-lore.sh create-entry "The Discovery" "lore"
```

## Key Documentation

- **[AGENTS.md](AGENTS.md)** - Quick reference for developers
- **[CLAUDE.md](CLAUDE.md)** - Complete system documentation
- **[PROJECT_INDEX.md](PROJECT_INDEX.md)** - Repository overview and navigation
- **[STATS.md](STATS.md)** - Current repository statistics
- **[docs/CURRENT_UNDERSTANDING.md](docs/CURRENT_UNDERSTANDING.md)** - Latest system understanding

## Core Concepts

- **Entry** - Atomic unit of lore (character, place, event, object, concept)
- **Book** - Collection of entries organized by theme/persona
- **Persona** - AI character profile with unique voice and traits
- **Context** - Session state binding data+agent+time+history

## Architecture

```
Git Commit → Extract → Persona Selection → LLM Generation → Store as JSON
```

Files stored in `knowledge/expanded/lore/` as JSON with schema validation.

## Current Scale

- **1206 lore entries** - Narrative units
- **107 books** - Collections
- **92 personas** - AI characters

## The Prime Directive

"Automate EVERYTHING so we can drink mojitos on a beach"

---

For detailed documentation, see [CLAUDE.md](CLAUDE.md)
