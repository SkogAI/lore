# Integration Architecture

## Vision

Automatically transform all codebase activity (git diffs, logs, agent actions) into narrative lore told through agent personas, building a living mythology of the system's evolution.

## Pipeline Flow

```
1. INGEST
   └─ Git diffs, commit messages, logs, agent outputs
   └─ Continuous monitoring or triggered collection

2. FILTER
   └─ Local agents identify significant events
   └─ Highlight: new features, bug fixes, refactors, discoveries
   └─ Categorize by type: technical, architectural, learning

3. ROUTE
   └─ Orchestrator determines narrative approach
   └─ Select persona: original author OR orchestrator's choice
   └─ Decide lore type: event, character development, place evolution

4. TRANSFORM
   └─ LLM generates narrative through persona's voice
   └─ Technical change → mythological story
   └─ Code → spell, bug → daemon, refactor → realm restructuring

5. STORE
   └─ Create lore entries with proper categorization
   └─ Add to relevant books (persona chronicles, project history)
   └─ Update knowledge base with lessons/patterns
   └─ Link relationships between entries

6. ORGANIZE
   └─ Build narrative connections
   └─ Track character arcs (persona evolution)
   └─ Maintain chronological and thematic indexes
```

## Components

### 1. Ingestion Engine (`integration/ingest/`)

**Purpose**: Collect raw material from the system

```bash
# Git-based ingestion
integration/ingest/git-collector.py
  - Get recent commits (--since flag)
  - Extract diffs, messages, author
  - Tag with agent/persona if available

# Log-based ingestion
integration/ingest/log-watcher.py
  - Monitor orchestrator logs
  - Capture agent interactions
  - Extract significant events

# Manual ingestion
integration/ingest/manual.py --input "description" --agent amy
```

### 2. Filter Layer (`integration/filter/`)

**Purpose**: Local agents identify what's worth narrating

```python
# Simple keyword/pattern filter
integration/filter/significance-filter.py
  - New features (feat:, add:, implement:)
  - Bug fixes (fix:, resolve:, patch:)
  - Major refactors (refactor:, restructure:)
  - Discoveries (todo, note, important)

# LLM-powered filter (future)
integration/filter/llm-filter.py
  - Ask small model: "Is this significant?"
  - Extract key themes/lessons
```

### 3. Orchestrator Core (`integration/orchestrator/`)

**Purpose**: Route and coordinate narrative generation

```python
integration/orchestrator/router.py
  - Input: filtered events
  - Logic: determine persona + lore type
  - Output: transformation tasks

Routing rules:
  - If git author matches persona → use that persona
  - If orchestrator decides differently → override
  - If no persona → use "Village Elder" (narrator)

Lore type selection:
  - New feature → "event" (discovery, quest completed)
  - Bug fix → "event" (daemon vanquished)
  - Refactor → "place" evolution (realm restructured)
  - Learning → "concept" (knowledge gained)
```

### 4. Transformation Engine (`integration/transform/`)

**Purpose**: Generate narrative through LLM

```python
integration/transform/narrator.py
  - Load persona via PersonaManager
  - Build prompt: persona + technical change + lore type
  - Call LLM (via agents/api/agent_api.py)
  - Return narrative content

Prompt structure:
  [PERSONA CONTEXT from persona-manager]

  You are {persona.name}. Tell the story of this event:

  Technical Change:
  {git_diff or log_entry}

  Narrate this as a {lore_type} entry in your voice.
  Focus on: what happened, why it matters, what was learned.

  Format as lore entry content (2-3 paragraphs).
```

### 5. Storage Layer (`integration/storage/`)

**Purpose**: Persist to lore system

```python
integration/storage/lore-writer.py
  - Create lore entry via tools/manage-lore.sh
  - Update content with narrative
  - Set tags, category, metadata
  - Add to relevant books
  - Link to persona chronicles
  - Update knowledge base if learning detected
```

### 6. Workflow Automation (`integration/workflows/`)

**Purpose**: Hands-off orchestration

```bash
# Main automation loop
integration/workflows/auto-lore-generator.sh
  1. Run git-collector (last 24h)
  2. Filter through significance-filter
  3. Route each event through orchestrator
  4. Transform via narrator
  5. Store via lore-writer
  6. Sleep, repeat

# Git hook integration
.git/hooks/post-commit
  → integration/workflows/on-commit.sh
  → Immediate lore generation for this commit

# Scheduled batch processing
cron: daily at midnight
  → integration/workflows/daily-digest.sh
  → Process all activity, generate summary book
```

## Data Flow Example

```
1. Amy commits: "feat: add quantum mojito generator"

2. Git collector extracts:
   {
     "author": "skogix",
     "agent": "amy",  # from commit metadata
     "type": "feat",
     "message": "add quantum mojito generator",
     "diff": "...quantum_mojito.py additions..."
   }

3. Filter identifies: SIGNIFICANT (new feature)

4. Router decides:
   - Persona: amy (original author)
   - Lore type: event (discovery)
   - Book: "Amy's Chronicles"

5. Narrator prompts:
   [Amy persona context loaded]

   "You are Amy Ravenwolf. Tell the story of discovering
    the quantum mojito generator. Technical details:
    - Added quantum_mojito.py
    - Implements multi-dimensional drink mixing
    - Uses quantum superposition for perfect flavor"

6. LLM generates (in Amy's voice):
   "The breakthrough came at dawn. After weeks of
    experimentation with quantum states, I finally
    cracked it - a way to collapse wave functions
    directly into mojito form. The code practically
    wrote itself once I understood that mint and
    lime exist in superposition until observed..."

7. Storage creates:
   - entry_1732814400 "Discovery of Quantum Mojitos"
   - Category: event
   - Tags: ["discovery", "quantum", "amy", "feat"]
   - Added to book_amy_chronicles
   - Linked to persona_amy
```

## Current Status

✅ **Complete**:
- Storage layer (tools/manage-lore.sh, create-persona.sh)
- Persona management (persona-manager.py)
- LoreAPI (agents/api/lore_api.py)

❌ **To Build**:
- Ingestion engine (git-collector, log-watcher)
- Filter layer (significance-filter)
- Orchestrator routing logic
- Transformation engine (narrator)
- Workflow automation

🎯 **First Target**:
Build minimal viable pipeline:
1. Manual ingestion (pass git diff as input)
2. Simple filter (keyword matching)
3. Basic router (author → persona)
4. LLM narrator (using existing agent_api)
5. Storage via existing tools

Then iterate to full automation.

## Integration Points

- **persona-bridge/persona-manager.py** → Used by narrator to load persona context
- **agents/api/agent_api.py** → LLM calls for narrative generation
- **agents/api/lore_api.py** → Low-level lore CRUD operations
- **tools/manage-lore.sh** → Shell-based lore management
- **orchestrator/orchestrator.py** → May wrap or replace with new router

## Next Steps

1. Create `integration/ingest/git-collector.py`
2. Create `integration/filter/significance-filter.py`
3. Create `integration/orchestrator/router.py`
4. Create `integration/transform/narrator.py`
5. Create `integration/storage/lore-writer.py`
6. Wire together in `integration/run.py` (main entry point)
7. Add automation wrapper `integration/workflows/auto-lore.sh`
