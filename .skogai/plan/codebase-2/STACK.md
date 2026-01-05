# Technology Stack

*Generated: 2026-01-05*
*Focus: Lore generation and connections created with context and lore-integrator*

## Languages & Runtime

### Primary Languages
- **Python 3.12+** - API layer, orchestration, persona management
- **Bash** - Primary orchestration layer, tool interfaces
- **jq** - JSON manipulation and CRUD operations

### Core Runtime
- Python runtime with pyproject.toml configuration
- Bash shell environment
- jq for all JSON transformations

## Key Dependencies

### Python Packages (pyproject.toml)

**LLM Integration:**
```
anthropic>=0.68.0          # Claude API integration
openai>=1.109.1            # OpenAI API client
requests>=2.31.0           # HTTP client for OpenRouter
```

**CLI & Configuration:**
```
click>=8.1.0               # CLI framework
pyyaml>=6.0                # YAML configuration parsing
rich>=13.7.0               # Rich terminal output
```

**UI Frameworks (Optional):**
```
streamlit>=1.50.0          # Web UI for content creation
gradio>=5.48.0             # Alternative UI framework
textual>=1.0.0             # TUI (terminal UI) framework
numpy>=2.3.3               # Numerical operations
```

## LLM Provider Integrations

### 1. OpenRouter API (Universal Provider)
**Primary Integration:** `agents/api/agent_api.py`

**Configuration:**
```python
{
    "api_key": os.environ.get("OPENROUTER_API_KEY"),
    "base_url": "https://openrouter.ai/api/v1",
    "models": {
        "research": "gpt-4o",
        "outline": "gpt-4o",
        "writing": "gpt-4o"
    },
    "temperature": {...},
    "timeout": 120,
    "max_tokens": {...}
}
```

**Environment Variables:**
- `OPENROUTER_API_KEY` - Required for authentication
- `OPENROUTER_BASE_URL` - Optional override

### 2. Ollama (Local LLM)
**Integration Points:**
- `tools/llama-lore-creator.sh`
- `tools/llama-lore-integrator.sh`
- `generate-agent-lore.py`

**Usage:**
```bash
LLM_PROVIDER=ollama ./tools/llama-lore-creator.sh
```

**Default Model:** llama3.2:3b (or configurable)

### 3. Claude CLI
**Integration:** `tools/llama-lore-creator.sh`, `tools/llama-lore-integrator.sh`

**Usage:**
```bash
LLM_PROVIDER=claude ./tools/llama-lore-creator.sh
```

**Requires:** Claude CLI installed (`npm install -g @anthropic-ai/claude-code`)

### 4. OpenAI API (via OpenRouter)
**Integration:** cURL-based in shell scripts

**Usage:**
```bash
LLM_PROVIDER=openai ./tools/llama-lore-creator.sh
```

**Environment Variables:**
- `OPENAI_API_KEY` or `OPENROUTER_API_KEY`
- `OPENAI_BASE_URL` (defaults to OpenRouter)

## Data Storage

### JSON File System
- **Storage Format:** JSON files
- **Schema Validation:** JSON Schema (Draft 07)
- **Operations:** jq-based CRUD
- **Atomicity:** Temp file + move pattern

**Storage Locations:**
```
knowledge/expanded/lore/
├── entries/           # 1,202 entry JSON files
│   └── entry_{timestamp}[_{hash}].json
├── books/             # 107 book JSON files
│   └── book_{timestamp}.json
└── personas/          # 92 persona JSON files
    └── persona_{timestamp}.json
```

## CLI Framework

### argc (Argument Parsing)
**File:** `Argcfile.sh`

**Features:**
- `@describe` - Help text
- `@meta` - Metadata (version, author, dotenv)
- `@env` - Environment variable documentation
- `@cmd` - Command definitions
- `@arg` - Argument validation with dynamic choices
- `@alias` - Command aliases

**Dynamic Choices:**
```bash
_choice_entries() {
  ls "$ENTRIES_DIR" | sed 's/\.json//'
}
```

## HTTP Client

### Requests Library (Python)
```python
response = requests.post(
    url=f"{base_url}/chat/completions",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    json=data_payload,
    timeout=120
)
```

### cURL (Shell)
```bash
curl -s "$base_url/chat/completions" \
  -H "Authorization: Bearer $api_key" \
  -H "Content-Type: "application/json" \
  -d "{\"model\":\"$MODEL_NAME\",\"messages\":[...]}" | \
  jq -r '.choices[0].message.content'
```

## Schema Validation

### JSON Schemas (Authoritative Contracts)

**Entry Schema:** `knowledge/core/lore/schema.json`
- Required: id, title, content, category
- Category enum: character|place|event|object|concept|custom
- Relationships array with target_id, relationship_type, description

**Book Schema:** `knowledge/core/book-schema.json`
- Required: id, title, description
- Readers/owners arrays (persona-based access control)
- Status enum: draft|active|archived|deprecated
- Hierarchical structure with sections

**Persona Schema:** `knowledge/core/persona/schema.json`
- Required: id, name, core_traits, voice
- Core traits: temperament, values, motivations
- Voice: tone, patterns, vocabulary
- Interaction style enums for formality, humor, directness

### Validation Tools
- **jq:** `scripts/jq/schema-validation/transform.jq`
- **Python:** Schemas loaded but NOT used for runtime validation (gap)
- **Shell:** Validates after jq transformations via argc

## Context Management

### Session Context System
**Location:** `context/`

**Templates:**
- `templates/base-context.json` - Session template
- `templates/persona-context.json` - Persona-specific fields

**Storage:**
- `current/` - Active sessions
- `archive/` - Completed sessions

**Manager:** `tools/context-manager.sh`
- create <template> - Generate session
- update <session_id> <key> <value> - Track state
- archive <session_id> - Store completed

## Git Integration

### Commit Processing
**Pattern:** Extract git diff + commit metadata
```bash
git-diff)
    RAW_CONTENT=$(git diff "$INPUT_CONTENT" || git show "$INPUT_CONTENT")
    GIT_AUTHOR=$(git log -1 --format='%an' "$INPUT_CONTENT")
    ;;
```

### Author Mapping
**File:** `integration/persona-mapping.conf`
```bash
skogix=persona_1744992765        # Amy Ravenwolf
claude=persona_1743770116        # Claude
DEFAULT=persona_1763820091       # Village Elder
```

## System Statistics

**Current Data Volume (2026-01-05):**
- 1,202 lore entries
- 107 books
- 92 personas
- 13 active sessions
- 5 archived sessions

## Key Integration Points

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Content Generation | Python + requests | LLM API calls (OpenRouter) |
| Local Inference | Ollama subprocess | Fast, free local models |
| CLI Parsing | Claude CLI | Direct API access |
| Data Persistence | JSON files | Simple, versioning-friendly |
| Data Transformation | jq | Standardized CRUD operations |
| Session Management | Bash + jq | Context lifecycle tracking |
| Persona Loading | Python JSON | Voice/trait extraction |
| Git Integration | Bash subprocess | Commit metadata extraction |
| Schema Validation | JSON Schema | Contract enforcement |
| HTTP Communication | requests library | OpenRouter API |

## Provider Status

- ✅ **Claude** - Tested via OpenRouter API
- ✅ **OpenAI** - Tested via OpenRouter API
- ✅ **Ollama** - Tested with local models (llama3.2:3b)

All providers confirmed working end-to-end with lore generation pipeline.
