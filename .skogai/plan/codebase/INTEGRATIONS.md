# External Integrations

**Generated:** 2026-01-05

## Integration Status Summary

| Integration | Status | Coverage | Notes |
|-------------|--------|----------|-------|
| **OpenRouter** | Working | 100% | Primary LLM gateway |
| **Ollama** | Working | 100% | Local inference |
| **Claude CLI** | Working | 100% | Direct API access |
| **OpenAI** | Working | 100% | Via OpenRouter |
| **Git** | Working | 80% | Commit extraction |
| **File System** | Working | 100% | Atomic operations |
| **Context System** | Working | 100% | Session management |
| **JSON Schema** | Partial | 60% | Validation not enforced in pipeline |
| **jq CRUD** | Working | 100% | Standard operations |

---

## LLM Providers

### OpenRouter (Universal Provider)

**Primary Use:** Universal LLM API gateway

**Integration Point:** `agents/api/agent_api.py`

**Configuration:**
```python
self.config = {
    "api_key": os.environ.get("OPENROUTER_API_KEY"),
    "base_url": os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
    "models": {
        "research": "gpt-4o",
        "outline": "gpt-4o",
        "writing": "gpt-4o"
    },
    "temperature": {
        "research": 0.2,
        "outline": 0.4,
        "writing": 0.7
    },
    "max_tokens": {
        "research": 2000,
        "outline": 2500,
        "writing": 4000
    },
    "timeout": 120
}
```

**Request Format:**
```python
response = requests.post(
    f"{self.config['base_url']}/chat/completions",
    headers={
        "Authorization": f"Bearer {self.config['api_key']}",
        "Content-Type": "application/json"
    },
    json={
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    },
    timeout=self.config["timeout"]
)
```

**Environment Variables:**
- `OPENROUTER_API_KEY` (required)
- `OPENROUTER_BASE_URL` (optional)

---

### Ollama (Local LLM)

**Primary Use:** Free local inference with open-source models

**Integration Points:**
- `tools/llama-lore-creator.sh`
- `tools/llama-lore-integrator.sh`
- `generate-agent-lore.py`

**Configuration:**
```bash
PROVIDER=${LLM_PROVIDER:-"ollama"}
MODEL_NAME=${MODEL_NAME:-"llama3.2:3b"}
```

**Execution:**
```bash
case "$PROVIDER" in
  ollama)
    ollama run "$MODEL_NAME" "$prompt"
    ;;
esac
```

**Validation:**
```bash
if ! command -v ollama &>/dev/null; then
    echo "Error: Ollama not found. Install with:" >&2
    echo "  curl https://ollama.ai/install.sh | sh" >&2
    exit 1
fi
```

**Environment Variables:**
- `LLM_PROVIDER=ollama`
- `MODEL_NAME` (optional, default: llama3.2:3b)
- `OLLAMA_HOST` (optional)

**Supported Models:** llama3.2:3b, llama3:8b, mistral:7b, any from ollama.ai/library

---

### Claude CLI

**Primary Use:** Direct Claude API access via CLI tool

**Integration:**
```bash
case "$PROVIDER" in
  claude)
    claude -p "$prompt"  # Plain mode, raw text output
    ;;
esac
```

**Validation:**
```bash
if [ "$PROVIDER" = "claude" ]; then
  if ! command -v claude &>/dev/null; then
    echo "Claude CLI not found. Install with:" >&2
    echo "  npm install -g @anthropic-ai/claude-code" >&2
    exit 1
  fi
fi
```

**Environment:** `LLM_PROVIDER=claude`

---

### OpenAI API (via OpenRouter)

**Integration:**
```bash
openai)
    local api_key="${OPENAI_API_KEY:-$OPENROUTER_API_KEY}"
    local base_url="${OPENAI_BASE_URL:-https://openrouter.ai/api/v1}"

    curl -s "$base_url/chat/completions" \
      -H "Authorization: Bearer $api_key" \
      -H "Content-Type: application/json" \
      -d "{
        \"model\": \"$MODEL_NAME\",
        \"messages\": [{\"role\": \"user\", \"content\": $(echo "$prompt" | jq -R -s .)}]
      }" | jq -r '.choices[0].message.content'
    ;;
```

**Environment Variables:**
- `LLM_PROVIDER=openai`
- `OPENAI_API_KEY` or `OPENROUTER_API_KEY`
- `OPENAI_BASE_URL` (optional, defaults to OpenRouter)

---

## Git Integration

### Commit Metadata Extraction

**Integration Point:** `integration/lore-flow.sh:38-72`

**Pattern:**
```bash
git-diff)
    RAW_CONTENT=$(git diff "$INPUT_CONTENT" || git show "$INPUT_CONTENT")
    GIT_AUTHOR=$(git log -1 --format='%an' "$INPUT_CONTENT" || echo "")
    COMMIT_MSG=$(git log -1 --format='%s' "$INPUT_CONTENT" || echo "")
    ;;
```

**Git Commands Used:**
- `git diff <commit>` - Show changes
- `git show <commit>` - Alternative
- `git log -1 --format='%an'` - Get author
- `git log -1 --format='%s'` - Get subject

**Supported Inputs:** HEAD, HEAD~N, commit-hash, branch-name

### Author Mapping

**File:** `integration/persona-mapping.conf`

```bash
skogix=persona_1744992765        # Amy Ravenwolf
claude=persona_1743770116        # Claude
dot=persona_1747684741           # Dot
goose=persona_1743771995         # Goose
DEFAULT=persona_1763820091       # Village Elder (fallback)
```

**Lookup Pattern:**
```bash
lookup_persona() {
  local author=$1
  # Try exact match
  persona=$(grep "^${author}=" "$mapping_file" | cut -d'=' -f2)
  # Try case-insensitive
  if [ -z "$persona" ]; then
    persona=$(grep -i "^${author}=" "$mapping_file" | cut -d'=' -f2)
  fi
  # Fall back to DEFAULT
  if [ -z "$persona" ]; then
    persona=$(grep "^DEFAULT=" "$mapping_file" | cut -d'=' -f2)
  fi
  echo "$persona"
}
```

---

## File System Storage

### JSON Storage Pattern

**Storage Locations:**
```
knowledge/expanded/lore/
├── entries/    entry_{timestamp}[_{hash}].json
├── books/      book_{timestamp}.json
└── personas/   persona_{timestamp}.json
```

**Read Operation:**
```python
def get_lore_entry(self, entry_id: str) -> Optional[Dict[str, Any]]:
    entry_path = os.path.join(self.lore_entries_dir, f"{entry_id}.json")
    if not os.path.exists(entry_path):
        return None
    with open(entry_path, "r") as f:
        return json.load(f)
```

**Write Operation (Atomic):**
```bash
atomic_update() {
  local file=$1
  local jq_expression=$2
  temp_file="${file}.tmp.$$"
  jq "$jq_expression" "$file" > "$temp_file"
  mv "$temp_file" "$file"  # Atomic
}
```

**Concurrency Considerations:**
- No file locking (last write wins)
- Race conditions possible

---

## Context System

### Session Management

**Integration Point:** `tools/context-manager.sh`

**Storage:**
```
context/
├── templates/
│   ├── base-context.json
│   └── persona-context.json
├── current/     # Active sessions
└── archive/     # Completed sessions
```

**Operations:**
```bash
# Create
session_id=$(context-manager.sh create base)

# Update
context-manager.sh update "$session_id" "system_state.orchestrator_mode" "lore"

# Archive
context-manager.sh archive "$session_id"
```

---

## Schema Validation

### JSON Schemas (Draft 07)

**Locations:**
```
knowledge/core/
├── lore/schema.json           # Entry schema
├── book-schema.json           # Book schema
└── persona/schema.json        # Persona schema
```

**Validation via jq:**
```bash
validate_entry() {
  local entry_file=$1
  jq -f scripts/jq/schema-validation/transform.jq \
    --argfile schema "knowledge/core/lore/schema.json" \
    "$entry_file"
}
```

**Integration Status:**
- Shell tools: Validate via jq
- Python API: Schemas loaded but NOT used for validation (gap)

---

## jq CRUD System

**Location:** `scripts/jq/`

**Operations:**
- `crud-get` - Retrieve values
- `crud-set` - Update values
- `crud-delete` - Remove fields
- `schema-validation` - Validate structure

**Usage:**
```bash
# Get value
jq -f scripts/jq/crud-get/transform.jq --arg path "voice.tone" persona.json

# Set value
jq -f scripts/jq/crud-set/transform.jq --arg path "content" --arg value "Updated" entry.json

# Delete field
jq -f scripts/jq/crud-delete/transform.jq --arg path "summary" entry.json
```

---

## Numbered Knowledge System

**Integration Point:** `orchestrator/orchestrator.py`

**Categories:**
```python
KNOWLEDGE_CATEGORIES = {
    "core": (0, 9),           # Emergency/critical
    "navigation": (10, 19),
    "identity": (20, 29),
    "operational": (30, 99),
    "standards": (100, 199),
    "project": (200, 299),
    "tools": (300, 399),
    "frameworks": (1000, 9999)
}
```

**Task-Specific Mapping:**
```python
knowledge_map = {
    "content": ["00", "10", "20", "101"],
    "lore": ["00", "10", "300", "303"],
    "research": ["00", "10", "02"]
}
```

---

## External Dependencies

### Required
- Python 3.12+
- Bash 4.0+
- jq 1.6+
- git 2.0+

### Optional
- Ollama (local LLM)
- Claude CLI (direct Claude)
- OpenRouter API key (cloud LLMs)

### Installation
```bash
# Python dependencies
pip install -r requirements.txt

# Ollama
curl https://ollama.ai/install.sh | sh

# Claude CLI
npm install -g @anthropic-ai/claude-code

# jq
sudo apt-get install jq  # Ubuntu/Debian
brew install jq          # macOS
```

---

## API Rate Limits

| Provider | Timeout | Rate Limiting | Cost |
|----------|---------|---------------|------|
| OpenRouter | 120s | OpenRouter enforced | Pay per token |
| Ollama | None | Hardware dependent | Free |
| Claude CLI | CLI handled | Anthropic API | Pay per token |

---

## Security Considerations

### API Key Storage
- Environment variables (not in code)
- Never committed to git

### Temp File Security
- Predictable paths (risk)
- No mktemp usage
- No secure deletion

### Input Validation
- Git author checked
- No commit message sanitization
- Shell variable interpolation risk
