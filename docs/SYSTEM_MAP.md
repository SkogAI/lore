# SkogAI Complete System Maip

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER / EXTERNAL INPUT                       │
│   (Tasks, Topics, Commands)                                     │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR DAEMON                          │
│   Pipe: /tmp/skogai-orchestrator                                │
│   - Parse task type                                             │
│   - Load numbered knowledge (00-99)                             │
│   - Select persona via PersonaManager                           │
│   - Route to service pipes                                      │
│   - Manage context state                                        │
└───────┬───────────────┬───────────────┬─────────────────────────┘
        │               │               │
        ▼               ▼               ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│ PersonaManager│ │ Context       │ │ Knowledge     │
│ (Integration) │ │ Manager       │ │ Base          │
└───────┬───────┘ └───────┬───────┘ └───────┬───────┘
        │               │               │
        └───────────────┴───────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SERVICE DAEMONS                              │
├─────────────────────────────┬───────────────────────────────────┤
│ skogai-lore-service.sh      │ skogai-agent-small-service.sh     │
│ /tmp/skogai-lore-generator  │ ./pipes/skogai-agent-small        │
│                             │                                   │
│ Commands:                   │ Input: Topic string               │
│ - generate-entry            │ Output: Content via pipeline      │
│ - generate-book             │ (research→outline→writing)        │
│ - generate-persona          │                                   │
│ - set-interval              │                                   │
│ - set-weights               │                                   │
└─────────────────────────────┴───────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                    STORAGE LAYER                                │
│   knowledge/expanded/lore/entries/*.json                        │
│   knowledge/expanded/lore/books/*.json                          │
│   knowledge/expanded/personas/*.json                            │
│   context/current/*.json                                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. Knowledge Base (Numbered System)

### Structure
```
knowledge/
├── core/                            # Core schemas and templates
├── expanded/
│   └── 20/                          # Priority 10-89: Domain
│       └── content-creation-workflow.md
└── archived/                        # Historical knowledge
```

### Access Protocol (from core-v0.md)
1. **First** check core components (00-09)
2. **Then** expand to domain knowledge (10-89)
3. **Finally** reference implementation (90-99) only when needed

### Knowledge Organization (from system-principles.md)
- **Three-tier structure**: Essential, Expanded, Implementation
- **Numbering system**: Priority and relationship mapping
- **Cross-referencing**: Via consistent tags and IDs

---

## 2. Context Manager

### Templates

**base-context.json**
```json
{
  "session_id": "",
  "context_type": "base",
  "active_knowledge": [],
  "system_state": {
    "orchestrator_mode": "standard",
    "active_agents": [],
    "memory_priority": "core"
  },
  "interaction_state": {
    "current_task": "",
    "task_progress": 0,
    "pending_actions": []
  }
}
```

**persona-context.json** (extended schema)
```json
{
  "schema": {
    "persona": { "id", "name", "core_description" },
    "traits": { "personality", "values", "motivations", "temperament" },
    "voice": { "tone", "patterns", "vocabulary", "formality_level" },
    "knowledge": { "expertise", "limitations", "lore_access" },
    "lore_books": { "ids", "access_level" }
  },
  "integration": {
    "agent_compatibility": ["base-agent", "implementation-agent", "planner-agent"],
    "context_priority": 10,
    "activation_mode": "explicit",
    "persistence": true
  },
  "template_mappings": {
    "base-persona": {
      "name": "persona.name",
      "expertise_list": "knowledge.expertise",
      "lore_books": "lore_books.ids"
    }
  }
}
```

### Storage
- `context/current/` - Active session contexts
- `context/archive/` - Historical contexts
- `context/templates/` - Schema definitions

---

## 3. PersonaManager (Integration Bridge)

**Location**: `integration/persona-bridge/persona-manager.py`

### Key Methods
```python
class PersonaManager:
    def activate_persona(persona_id) -> bool
    def get_active_persona() -> Dict
    def get_persona_context(persona_id) -> Dict
    def format_persona_for_agent(persona_id) -> Dict
    def render_persona_prompt(persona_id) -> str
```

### Output Format (format_persona_for_agent)
```python
{
    "persona": {"id", "name", "description"},
    "traits": {"values", "temperament"},
    "voice": {"tone", "patterns"},
    "lore": [{"title", "content", "category", "tags"}],
    "prompt": "# Rendered persona prompt..."
}
```

### Integration Flow
1. Load persona from `knowledge/expanded/personas/`
2. Get linked lore books from persona's `knowledge.lore_books`
3. Fetch all entries from those books
4. Format for agent consumption
5. Render prompt from template

---

## 4. Agent System

### Agent Templates

**Location**: `agents/implementations/content/`

| Agent | Purpose | Knowledge Access | Output |
|-------|---------|------------------|--------|
| research-agent.md | Gather facts | 00-09, 20-29 | JSON with key_facts, main_concepts |
| outline-agent.md | Structure content | 00-09, 30-39 | JSON with sections, hierarchy |
| writing-agent.md | Generate content | 00-09, 40-49 | JSON with content_sections |

### Agent Protocol
- Direct output to orchestrator (not end user)
- Use specified JSON output format
- Include confidence levels
- Flag requests exceeding specialization

### Pipeline Flow
```
Topic → Research Agent → Outline Agent → Writing Agent → Final Content
         (temp: 0.2)      (temp: 0.4)     (temp: 0.7)
```

---

## 5. Service Daemons

### skogai-lore-service.sh
```bash
# Continuous lore generation
Pipe: /tmp/skogai-lore-generator
Model: llama3.2 (configurable)
Interval: 600s (configurable)

Commands:
  generate-entry              # Random lore entry
  generate-book               # Random lorebook with 3-7 entries
  generate-persona            # Random persona with linked lore
  set-interval <seconds>      # Minimum 60s
  set-weights <E> <B> <P>     # Entry/Book/Persona weights
  stop                        # Graceful shutdown

Features:
- Weighted random generation
- History logging to logs/lore_generation/
- Automatic model pulling
```

### skogai-agent-small-service.sh
```bash
# Content creation workflows
Pipe: ./pipes/skogai-agent-small-requests
Model: llama3.2 (configurable)

Usage:
  echo "AI ethics" > ./pipes/skogai-agent-small-requests

Flow:
  1. Receive topic from pipe
  2. Run small_model_workflow.py
  3. Execute research → outline → writing
  4. Log results to logs/skogai-agent-small.log

Features:
- Background processing
- Automatic model pulling
- Session logging
```

---

## 6. LLM Provider System

### Multi-Provider Support (added this session)

**Python** (`generate-agent-lore.py`):
```bash
python generate-agent-lore.py --agent-type writer --provider claude
python generate-agent-lore.py --agent-type writer --provider openai --model gpt-4
```

**Bash** (`llama-lore-creator.sh`, `llama-lore-integrator.sh`):
```bash
LLM_PROVIDER=claude ./tools/llama-lore-creator.sh - entry "Title" "place"
LLM_PROVIDER=openai ./tools/llama-lore-integrator.sh gpt-4 extract-lore story.txt
```

### Environment Variables
- `LLM_PROVIDER`: ollama (default), claude, openai
- `OPENAI_API_KEY` / `OPENROUTER_API_KEY`: API authentication
- `OPENAI_BASE_URL`: API endpoint (default: OpenRouter)

---

## 7. Agent-Specific Knowledge

### Per-Agent Knowledge

| Agent | Specialization | Key Files |
|-------|----------------|-----------|
| **SkogAI** | Core system, content workflows | docs/AGENTS.md, knowledge/expanded/20/content-creation-workflow.md |
| **Claude** | Workflow orchestration, MCP | docs/AGENTS.md, docs/ARCHITECTURE.md |
| **Dot** | Minimalist programming | docs/AGENTS.md |
| **Goose** | Chaos agent, quantum mojitos | docs/AGENTS.md |
| **Amy** | Personality template | docs/AGENTS.md |

---

## 8. Data Flow Examples

### Example 1: Generate Agent Lore
```
User: python generate-agent-lore.py --agent-type researcher --provider claude

1. determine_agent_needs() → Claude CLI → JSON of needed categories
2. For each entry:
   - generate_lore_entry() → Claude CLI → Rich content
   - LoreAPI.create_lore_entry() → knowledge/expanded/lore/entries/
3. LoreAPI.create_lore_book() → knowledge/expanded/lore/books/
4. Link entries to book
5. Optionally create persona and link
```

### Example 2: Content Pipeline
```
User: echo "AI ethics" > ./pipes/skogai-agent-small-requests

1. Service reads from pipe
2. small_model_workflow.py executes:
   - Research phase → research_output.json
   - Outline phase → outline_output.json (receives research)
   - Writing phase → final_article.md (receives outline)
3. Results logged
```

### Example 3: Orchestrator Flow (TO BE IMPLEMENTED)
```
User: {"type": "content", "topic": "AI ethics", "persona": "persona_123"}
      → /tmp/skogai-orchestrator

1. Parse task, determine type = "content"
2. Load knowledge 00/system-principles.md, 20/content-creation-workflow.md
3. PersonaManager.activate_persona("persona_123")
4. Update context/current/ with active task
5. Route to ./pipes/skogai-agent-small-requests
6. Receive result
7. Store in lore system
8. Update context with completion
```

---

## 9. Missing Components

### Orchestrator Daemon
Central coordinator that:
- Listens on `/tmp/skogai-orchestrator`
- Routes tasks based on type
- Manages persona activation
- Chains service outputs
- Maintains context state

### Knowledge Router
Logic to:
- Determine which numbered modules (00-99) are needed
- Load and merge knowledge for agent context
- Respect priority ordering

### Context State Machine
Track:
- Current active task
- Pipeline progress
- Pending actions
- Agent handoffs

---

## 10. File Reference

### Core APIs
- `agents/api/lore_api.py` - Lore CRUD operations
- `agents/api/agent_api.py` - LLM workflow execution
- `integration/persona-bridge/persona-manager.py` - Persona management

### Service Scripts
- `skogai-lore-service.sh` - Lore generation daemon
- `skogai-agent-small-service.sh` - Content workflow daemon
- `skogai-agent-small-client.sh` - Client for content service

### Tools
- `tools/llama-lore-creator.sh` - Create lore entries/books/personas
- `tools/llama-lore-integrator.sh` - Extract lore from files
- `generate-agent-lore.py` - Generate specialized agent lore

### Knowledge
- `docs/AGENTS.md` - Agent-specific profiles and documentation
- `knowledge/core/` - Schemas and templates
- `knowledge/expanded/` - Lore entries, books, and personas
- `knowledge/archived/` - Historical knowledge

### Context
- `context/templates/` - Context schemas
- `context/current/` - Active sessions
- `orchestrator/identity/core-v0.md` - Orchestrator behavior
