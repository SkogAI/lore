# SkogAI Active Endpoints & Scripts

## Working Components

### Small Model Agent System
- `skogai-agent-small-service.sh` - **WORKS!** Service that runs Ollama small model agents (llama3)
- `skogai-agent-small-client.sh` - Send requests to the small model service
- `demo/small_model_workflow.py` - Three-phase content workflow using small LLMs
- `agents/implementations/small_model_agents.py` - Implementation for Ollama integration

### Lore & Persona Management
- `agents/api/lore_api.py` - **WORKS!** API for personas, lore entries, and books
- `tools/manage-lore.sh` - CLI tool for lore management
- `tools/create-persona.sh` - CLI tool for persona creation and management
- `tools/llama-lore-creator.sh` - **NEW!** Generate lore and personas using Llama
- `tools/llama-lore-integrator.sh` - **NEW!** Extract lore from existing content
- `demo/lore_demo.py` - Demonstrates persona and lore system functionality

## Using Llama3 for Lore Management

### Creating New Content

```bash
# Pull Llama Model
ollama pull llama3

# Create a persona using Llama
./tools/llama-lore-creator.sh llama3 persona "Elara" "An elven sorceress"

# Generate a lore entry
./tools/llama-lore-creator.sh llama3 entry "The Crystal Forest" "place"

# Generate a complete lorebook with multiple entries
./tools/llama-lore-creator.sh llama3 lorebook "Eldoria" "A magical realm" 5

# Link a persona to lore books
./tools/llama-lore-creator.sh llama3 link persona_1743770116 2
```

### Integrating Existing Content

```bash
# Extract lore from a text file
./tools/llama-lore-integrator.sh llama3 extract-lore story.txt

# Create a persona from character description
./tools/llama-lore-integrator.sh llama3 create-persona character.txt

# Import an entire directory of content into a lorebook
./tools/llama-lore-integrator.sh llama3 import-directory /path/to/world "My Fantasy World" "A rich fantasy setting"

# Find connections between lore entries
./tools/llama-lore-integrator.sh llama3 analyze-connections book_id
```

### Managing Content

```bash
# List all personas
./tools/create-persona.sh list

# View persona details
./tools/create-persona.sh show persona_id

# List all lore books
./tools/manage-lore.sh list-books

# View book content
./tools/manage-lore.sh show-book book_id

# View a specific lore entry
./tools/manage-lore.sh show-entry entry_id
```

## Other Components

### Small Model Workflow
- **Start Service**: `./skogai-agent-small-service.sh llama3`
- **Send Content Requests**: `echo "artificial intelligence ethics" > pipes/small_model_requests`
- **Find Generated Content**: Look in the `demo/small_model_content_*` directories

### Components to Move
The chat-related files should be moved to `../skogchat`:
- `skogai-chat.py`
- `streamlit_chat.py`
- `start-chat-ui.sh`
- `skogai-chat.desktop`

## Not Yet Implemented
- Integration of persona system with agent workflows
- Chat interface for lore/persona interaction
- Knowledge document indexing functionality
- Full orchestrator system