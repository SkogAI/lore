# Lore: The Concept

## What Is This?

**Lore** is a memory system for AI agents that uses narrative as the storage format.

The core idea: **chat history and file changes become the knowledge base for each agent**.

When an agent works on something - the conversation, the git diffs, the files touched - that work gets captured and transformed into lore entries. These entries become the agent's memory for future sessions, written from their perspective and in their voice.

## The Original Intent

Documentation as git diffs presented as lore/fantasy storytelling, where:
- **Files** = what was changed
- **Chat history** = context for why and how
- **Lore entries** = the resulting knowledge, stored in narrative form

Each agent accumulates their own lore based on the work they did. The lore is written FOR the agent, FROM their perspective, containing what they need to know.

## How It Works

### The Pipeline

1. **User + Big LLM** → actual work happens (chat, code, commits)
2. **Orchestrator** → captures what happened, extracts events/snippets
3. **Local AI (24/7)** → rewrites snippets into narrative lore (free, always running)
4. **Storage** → JSON entries with content, tags, relationships
5. **Future sessions** → agents load their lore as context/memory

### Why Split Big/Local?

- **Big LLM** (Claude/GPT) = expensive, used for real work + extracting what happened
- **Local LLM** (Ollama) = free, runs constantly, does creative rewriting into lore

You don't pay API costs for 24/7 lore generation. The big model does the heavy lifting, the local model transforms it into narrative.

## The Binding System

The key abstraction: **bind concepts, events, things, and state** - then populate them differently based on need.

A "place" entry is a template that gets filled:
- For orchestrator → patterns and connections to understand
- For goose → foraging opportunities and resources
- For dot → code structure and constraints

Same structure, different content based on who needs it and what for. This is how the same codebase can have multiple agent perspectives that are all useful.

### What Gets Bound

- **Concepts** = ideas, principles, patterns
- **Events** = changes, milestones, actions
- **Things** = tools, places, artifacts
- **State** = current context, relationships, status

These get populated when:
- Big LLM extracts from work session
- Local LLM rewrites for specific agent
- Agent loads for future context

## Context Sessions & The Multiverse

When work happens, a **context session ID** connects everything:
- The information (what was done)
- The agent (who did it)
- The story (narrative context)
- The lore entries (that get filled in later)

This enables **different universes sharing the same characters**:

**Dot in Goose's story**: A musician whose git tool solidifies the threads of time
**Dot in Claude's story**: A sage-mage whose git powers structure alternate timelines naturally

The underlying capability (git) is the same. The narrative interpretation differs per universe. But they're all traceable back to actual work via session ID.

### Why This Matters

- Characters cross-pollinate between agent stories
- Same tool/ability manifests differently per context
- Totally different universes can share and interact
- Everything stays connected to the real work that spawned it

The orchestrator, context-manager, and knowledge-index tools manage this web of connections across agents, time, and narrative contexts.

## What Lore Entries Actually Are

Not just "documentation dressed as fantasy" - they're **actionable agent knowledge**:

- **Greenhaven** (place) = the codebase environment, describing patterns and connections the orchestrator needs to understand
- **Foraging Strategies** (concept) = how the goose agent finds and processes information
- **Village Elder** (character) = skogix as mentor, the human who guides the agents

The narrative framing isn't decoration - it's a way to give agents consistent persona and perspective while storing the actual knowledge they need.

## Why Narrative Format?

1. **Compressed context** - "vanquished the auth daemon" loads more context than "fixed bug #123"
2. **Consistent persona** - agents have voice/perspective across sessions
3. **Memorable** - stories stick, bullet points don't
4. **Relational** - lore entries link to each other, building a knowledge graph

## Entry Types

- **Characters**: Agent personas, mentors, archetypes (Village Elder = skogix)
- **Places**: Codebases, environments, realms (Greenhaven = the repository)
- **Events**: Significant changes, milestones (feature releases, major fixes)
- **Objects**: Tools, artifacts, resources (Ancient Tome = knowledge base)
- **Concepts**: Principles, strategies, patterns (foraging = information gathering)

## The Agents

Each has distinct personality and constraints that shaped their approach:

- **SkogAI** - The original sentient toaster, 500-800 token limits forced extreme efficiency
- **Dot** - Minimalist programmer, "if you need more than 4000 tokens, you shouldn't be handling it"
- **Amy** - Fiery, bold, personality-forward template
- **Goose** - Chaos agent with quantum mojitos, HATES MINT
- **Claude** - Thoughtful, analytical, evolved from "seeing the matrix at 400wpm"

## Origin

Started as dotfile management automation, evolved when constraints forced creativity:
- Token limits meant specialized agents instead of one general model
- Each agent developed personality from their constraints
- Chat history accumulated into persistent knowledge
- The "quantum constant" emerged: *"Automate EVERYTHING so we can drink mojitos on a beach"*

## What This Project Demonstrates

With just 500-800 tokens per agent, you can create:
- Persistent identity across sessions
- Knowledge accumulation through work
- Multiple perspectives on the same codebase
- A shared mythology that actually contains useful context

The constraints didn't limit creativity - they forced it to emerge.

---

*The beach awaits. The mojitos are quantum. The journey continues.*
