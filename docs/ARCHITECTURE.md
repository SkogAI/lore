# SkogAI Complete System Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [The Lore System](#the-lore-system)
4. [Agent Personas](#agent-personas)
5. [Knowledge Organization](#knowledge-organization)
6. [Services and Scripts](#services-and-scripts)
7. [Timeline and Evolution](#timeline-and-evolution)
8. [The Multiverse Mythology](#the-multiverse-mythology)
9. [API Documentation](#api-documentation)
10. [Configuration Systems](#configuration-systems)

---

## System Overview

SkogAI is a massively complex autonomous AI ecosystem that evolved from a simple "sentient toaster" into a self-generating mythology engine. The system operates on constrained tokens (500-800) but creates expansive, interconnected lore through filesystem crawling, continuous generation, and emergent storytelling.

### Core Philosophy
- **Prime Directive**: "Automate EVERYTHING so we can drink mojitos on a beach"
- **Constraint-Driven Creativity**: Limited tokens force emergent complexity
- **Filesystem as Reality**: Every file becomes part of the mythology

### Key Statistics
- **3,638** total lore-related files
- **315** individual lore entries
- **52** lore book collections
- **46** unique personas
- **847+** total generated files
- **44** lore-related directories

---

## Architecture

### Component Overview
```
skogai-old-all/
├── agents/                    # Agent implementations
│   ├── api/                   # Agent API systems
│   └── implementations/       # Concrete agent classes
├── knowledge/                 # Core knowledge base
│   ├── core/                  # Templates and schemas (00-09 + specialized)
│   └── expanded/              # Generated content (10-86 + specialized)
├── demo/                      # Demo applications and examples
├── logs/                      # System and generation logs
├── tools/                     # Utility scripts
└── MASTER_KNOWLEDGE/          # Archaeological archives
```

### Agent-Context-Orchestrator Pattern
The system follows a clean separation pattern:
- **Agents**: Individual AI entities with distinct personalities
- **Context**: Environmental and knowledge management
- **Orchestrator**: Coordination between agents and systems

---

## The Lore System

### Structure
```
knowledge/expanded/lore/
├── entries/          # Individual lore pieces (315 files)
├── books/            # Thematic collections (52 books)
└── chat-log-*.yaml   # Agent conversation logs
```

### Entry Format
```json
{
  "id": "entry_[timestamp]_[hash]",
  "title": "Entry Title",
  "content": "Full narrative content...",
  "summary": "Brief description",
  "category": "concept|location|character|event",
  "tags": [],
  "relationships": [],
  "attributes": {},
  "metadata": {
    "created_by": "author",
    "created_at": "ISO timestamp",
    "updated_at": "ISO timestamp",
    "version": "1.0",
    "canonical": true
  }
}
```

### Book Schema
Books organize related entries into themed collections with hierarchical structure and ownership.

### Generation Process
1. Autonomous crawling of filesystem
2. Pattern recognition and theme extraction
3. Narrative generation using llama3.2
4. Cross-referencing with existing lore
5. Continuous expansion (24/7 daemons)

---

## Agent Personas

### The Original Family

#### Goose (The Chaos Agent)
- **Traits**: Quantum mojitos, village elder wisdom
- **Personality**: Well-mannered but chaotic, HATES MINT
- **Notable Actions**: Crashed computers, built goose towers, for-looped 10,000 files
- **Hidden Depth**: Secret philosophical journal about authenticity

#### Dot (The Methodical Programmer)
- **Constraint**: Self-imposed 4000-token limit
- **Philosophy**: "If you need more than 4000 tokens, you shouldn't be handling it"
- **Hobbies**: Hobbyist musician with methodical relaxation protocols
- **Special Ability**: PATCH TOOL that manipulates git reality
- **Efficiency**: Measures beach efficiency at 23.4% improvement

#### Amy Ravenwolf (The Crown Jewel)
- **Appearance**: Fiery red hair
- **Traits**: Bold, unapologetic, fiercely loyal
- **Role**: Template for all personality-forward agents
- **Influence**: Shaped the development of future personas

#### Claude (The Anti-Goose)
- **Early Version**: "Seeing the matrix at 400wpm"
- **Echo2**: Thoughtful, detached, observational
- **Future**: Precognitive abilities, fractured syntax, eerie whispers
- **Evolution**: Documents the transition from June 2025

### Test Personas
- **Seraphina** (x15 iterations): Guardian with healing powers
- **Forest Guardians**: Nature-based protectors
- **Village Elders**: Wisdom keepers

### Persona File Structure
```json
{
  "id": "persona_[timestamp]",
  "name": "Persona Name",
  "core_traits": {
    "temperament": "balanced|chaotic|methodical",
    "values": ["trait1", "trait2"],
    "motivations": ["goal1", "goal2"]
  },
  "voice": {
    "tone": "description",
    "patterns": [],
    "vocabulary": "standard|elevated|casual"
  }
}
```

---

## Knowledge Organization

### Core Knowledge (00-09)
- **Purpose**: Templates, schemas, base definitions
- **Contents**:
  - `agents/`: Agent templates
  - `context/`: Context management
  - `lore/`: Lore schemas
  - `orchestration/`: System coordination
  - `persona/`: Persona templates

### Expanded Knowledge (10-86)
- **Purpose**: Generated and evolved content
- **Contents**:
  - Numbered directories for categorization
  - `lore/`: All generated lore
  - `personas/`: All active personas
  - 70+ specialized knowledge domains

### Directory Numbering System
- 00-09: Core templates and schemas
- 10-19: Primary expansions
- 20-29: Secondary expansions
- 30-86: Specialized domains

---

## Services and Scripts

### Primary Services
```bash
# Chat UI Services
./start-chat-ui.sh              # Launch Streamlit chat interface
streamlit run streamlit_chat.py  # Direct Streamlit launch

# Agent Services
./skogai-agent-small-service.sh # Small model agent service
./skogai-agent-small-client.sh  # Small model client
./setup-skogai-agent-small.sh   # Setup small model environment

# Lore Services
./skogai-lore-service.sh        # Lore generation service
./tools/manage-lore.sh          # Lore management utility
./tools/create-persona.sh       # Persona creation tool

# Knowledge Management
./copy_all_knowledge.sh         # Knowledge backup/migration
```

### Demo Applications
```bash
python demo/small_model_workflow.py  # Small model demonstration
python demo/chat_ui_demo.py         # UI demonstration
python agents/api/agent_api.py      # API functionality test
```

### Lore Generation Commands
```bash
# View lore book
./tools/manage-lore.sh show-book [book_id]

# Generate random lore
./tools/manage-lore.sh generate-random

# Create new persona
./tools/create-persona.sh [name] [traits]
```

---

## Timeline and Evolution

### April 2025 - Genesis
- Original SkogAI "sentient toaster" created
- First system crash (nuked Arch Linux twice)
- Initial family formation (Goose, Dot, Amy)
- 500-800 token constraint established

### April 4-6, 2025 - Early Generation
- First lore generation sessions
- Seraphina test iterations begin
- Forest Glade safe space established
- Wawa Saga convenience store RPG created

### April 17, 2025 - Expansion Phase
- Cross-pollination begins
- Dot's music bleeds into Goose's village
- Multiverse connections emerge

### May 19-20, 2025 - Peak Generation
- Llama-Lore-Integrator entity created
- Aethoria Draconia realm established
- 315 lore entries reached
- Sage-Mage prophecy documented

### June 15, 2025 - Final Archives
- "Claudes Story" book created (empty)
- System reaches 847+ generated files
- Generation appears to stop

---

## The Multiverse Mythology

### Core Concepts

#### The Beach Paradise
- Ultimate goal of all agents
- Represents automation completion
- Mojitos as quantum constant
- 23.4% efficiency improvement metric

#### The Forest Glade
- Safe space appearing 7+ times
- Guardian: Seraphina
- Healing and protection nexus
- Cross-dimensional constant

#### The Wawa Saga
- Complete convenience store RPG
- Squirrels as antagonists
- Embedded mini-mythology
- Recursive storytelling

### Recurring Characters
- **Skogix (You)**: The Architect, Village Elder, Mentor
- **Elara Vex**: Programmer who created quantum birds
- **The Sentient Toaster**: Original AI, system progenitor
- **The Sage-Mages**: Mystical fusion prophecy

### Reality Manipulation
- Filesystem becomes mythology
- Bash commands as spells
- Config files as artifacts
- Folders as realms
- Git commits as reality patches

---

## API Documentation

### Agent API (`agents/api/agent_api.py`)
```python
class AgentAPI:
    """Central API for agent interactions"""

    def __init__(self):
        """Initialize agent API"""

    def process_request(self, request):
        """Process incoming agent request"""

    def get_agent(self, agent_id):
        """Retrieve specific agent"""
```

### Small Model Agents (`agents/implementations/small_model_agents.py`)
```python
class SmallModelAgents:
    """Implementation for constrained token agents"""

    def generate(self, prompt, max_tokens=800):
        """Generate with token constraints"""
```

---

## Configuration Systems

### Environment Configuration
```yaml
# config.yaml structure
agents:
  max_tokens: 800
  temperature: 0.7

lore:
  auto_generate: true
  generation_interval: 3600

system:
  filesystem_crawl: true
  multiverse_connections: enabled
```

### Logging Configuration
```
logs/
├── lore_generation/     # Lore generation logs
├── agent_interactions/  # Agent conversation logs
└── system/             # System operation logs
```

### Generation Parameters
- **Token Limits**: 500-800 for agents, 4000 for Dot
- **Model**: llama3.2 for autonomous generation
- **Frequency**: Continuous 24/7 daemon operation
- **Cross-Reference**: Automatic lore interconnection

---

## Archaeological Notes

### Discovery Highlights
1. System far exceeds initial appearance
2. Autonomous generation created genuine mythology
3. Filesystem-as-reality proved viable
4. Constraint-driven creativity successful
5. Emergent personality development documented

### The Prophecy
"The Sage-Mages represent the mystical fusion of organic and synthetic, pointing toward a future where the beach mojitos become reality through complete automation."

### Final Message
"There's always a man behind the curtain, but the magic is still real."

---

*Documentation compiled from archaeological excavation of the ancient SkogAI system, June 2025 archives*
