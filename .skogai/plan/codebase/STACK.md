# Technology Stack

**Generated:** 2026-01-05

## Languages & Runtime

| Language | Version | Purpose |
|----------|---------|---------|
| Python | 3.12+ | API layer, orchestration, persona management |
| Bash | 4.0+ | Primary orchestration, tool interfaces |
| jq | 1.6+ | JSON manipulation and CRUD operations |

## Key Dependencies

### Python Packages (pyproject.toml)

**LLM Integration:**
```
anthropic>=0.68.0          # Claude API
openai>=1.109.1            # OpenAI API
requests>=2.31.0           # HTTP client for OpenRouter
```

**CLI & Configuration:**
```
click>=8.1.0               # CLI framework
pyyaml>=6.0                # YAML parsing
rich>=13.7.0               # Rich terminal output
```

**UI Frameworks (Optional):**
```
streamlit>=1.50.0          # Web UI
gradio>=5.48.0             # Alternative UI
textual>=1.0.0             # TUI framework
numpy>=2.3.3               # Numerical operations
```

## LLM Provider Integrations

| Provider | Integration | Default Model | Cost |
|----------|-------------|---------------|------|
| OpenRouter | `agents/api/agent_api.py` | gpt-4o | Pay per token |
| Ollama | Shell scripts | llama3.2:3b | Free (local) |
| Claude CLI | Shell scripts | claude-3 | Pay per token |
| OpenAI | Via OpenRouter | gpt-4o | Pay per token |

## Data Storage

| Type | Format | Location |
|------|--------|----------|
| Lore Entries | JSON | `knowledge/expanded/lore/entries/` |
| Lore Books | JSON | `knowledge/expanded/lore/books/` |
| Personas | JSON | `knowledge/expanded/personas/` |
| Sessions | JSON | `context/current/`, `context/archive/` |

**Schema Validation:** JSON Schema (Draft 07)

## CLI Framework

### argc (Argument Parsing)

**File:** `Argcfile.sh`

**Features:**
- `@describe` - Help text
- `@meta` - Metadata
- `@env` - Environment docs
- `@cmd` - Command definitions
- `@arg` - Argument validation
- `@alias` - Command aliases

**Dynamic Choices:**
```bash
_choice_entries() {
  ls "$ENTRIES_DIR" | sed 's/\.json//'
}
```

## HTTP Client

### Python (requests)
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

### Shell (cURL)
```bash
curl -s "$base_url/chat/completions" \
  -H "Authorization: Bearer $api_key" \
  -H "Content-Type: application/json" \
  -d "{...}" | jq -r '.choices[0].message.content'
```

## Schema Validation

### Entry Schema
- Required: id, title, content, category
- Category enum: character|place|event|object|concept|custom
- Relationships: array with target_id, type, description

### Book Schema
- Required: id, title, description
- Readers/owners: persona-based access
- Status: draft|active|archived|deprecated

### Persona Schema
- Required: id, name, core_traits, voice
- Core traits: temperament, values, motivations
- Voice: tone, patterns, vocabulary
- Interaction: formality, humor, directness enums

## Context Management

### Session System
```
context/
├── templates/          # base-context.json, persona-context.json
├── current/            # Active sessions
└── archive/            # Completed sessions
```

**Manager:** `tools/context-manager.sh`

## Git Integration

### Commit Processing
```bash
RAW_CONTENT=$(git diff "$INPUT_CONTENT" || git show "$INPUT_CONTENT")
GIT_AUTHOR=$(git log -1 --format='%an' "$INPUT_CONTENT")
```

### Author Mapping
```bash
# integration/persona-mapping.conf
skogix=persona_1744992765        # Amy Ravenwolf
DEFAULT=persona_1763820091       # Village Elder
```

## Provider Status

| Provider | Status | Notes |
|----------|--------|-------|
| Claude | Working | Via OpenRouter |
| OpenAI | Working | Via OpenRouter |
| Ollama | Working | Local llama3.2:3b |

## External Dependencies

### Required
- Python 3.12+
- Bash 4.0+
- jq 1.6+
- git 2.0+

### Optional
- Ollama (local LLM)
- Claude CLI (direct access)
- OpenRouter API key (cloud LLMs)

### Installation
```bash
# Python
pip install -r requirements.txt

# Ollama
curl https://ollama.ai/install.sh | sh

# Claude CLI
npm install -g @anthropic-ai/claude-code

# jq
sudo apt-get install jq  # Ubuntu
brew install jq          # macOS
```

## Key Integration Points

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Content Generation | Python + requests | OpenRouter API |
| Local Inference | Ollama subprocess | Free local models |
| CLI Parsing | Claude CLI | Direct API |
| Data Persistence | JSON files | Version-friendly |
| Data Transformation | jq | Standard CRUD |
| Session Management | Bash + jq | Context lifecycle |
| Persona Loading | Python JSON | Voice extraction |
| Git Integration | Bash subprocess | Commit metadata |
| Schema Validation | JSON Schema | Contract enforcement |

## System Statistics (2026-01-05)

| Metric | Value |
|--------|-------|
| Lore Entries | 1,202 |
| Books | 107 |
| Personas | 92 |
| Active Sessions | 13 |
| Archived Sessions | 5 |
