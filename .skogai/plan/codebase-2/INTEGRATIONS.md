# External Integrations

*Generated: 2026-01-05*
*Focus: Lore generation and connections created with context and lore-integrator*

## LLM Providers

### OpenRouter (Universal Provider)

**Primary Use:** Universal LLM API gateway

**Integration Point:** `agents/api/agent_api.py`

**Configuration:**
```python
self.config = {
    "api_key": os.environ.get("OPENROUTER_API_KEY"),
    "base_url": os.environ.get("OPENROUTER_BASE_URL",
                              "https://openrouter.ai/api/v1"),
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

**Response Parsing:**
```python
if response.status_code == 200:
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    return content
else:
    raise Exception(f"API error: {response.status_code} - {response.text}")
```

**Environment Variables:**
- `OPENROUTER_API_KEY` (required) - API authentication key
- `OPENROUTER_BASE_URL` (optional) - Override API endpoint

**Usage Example:**
```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
python agents/api/agent_api.py
```

**Supported Models:**
- gpt-4o (default for all task types)
- Any model available on OpenRouter platform

**Rate Limiting:**
- Timeout: 120 seconds per request
- No retry logic (fail immediately)
- No rate limit handling

**Error Handling:**
- HTTP 200: Success
- HTTP 4xx: Client error (authentication, invalid request)
- HTTP 5xx: Server error (OpenRouter down)
- Timeout: Request exceeded 120s

---

### Ollama (Local LLM)

**Primary Use:** Free local inference with open-source models

**Integration Points:**
- `tools/llama-lore-creator.sh`
- `tools/llama-lore-integrator.sh`
- `generate-agent-lore.py`

**Configuration:**
```bash
# Provider selection
PROVIDER=${LLM_PROVIDER:-"ollama"}

# Model selection
MODEL_NAME=${MODEL_NAME:-"llama3.2:3b"}
```

**Execution Pattern:**
```bash
case "$PROVIDER" in
  ollama)
    # Direct subprocess execution
    ollama run "$MODEL_NAME" "$prompt"
    ;;
esac
```

**Validation:**
```bash
# Check if Ollama is installed
if ! command -v ollama &>/dev/null; then
    echo "Error: Ollama not found. Install with:" >&2
    echo "  curl https://ollama.ai/install.sh | sh" >&2
    exit 1
fi

# Check if model is available
if ! ollama list | grep -q "$MODEL_NAME"; then
    echo "Model $MODEL_NAME not found. Pulling..." >&2
    ollama pull "$MODEL_NAME"
fi
```

**Environment Variables:**
- `LLM_PROVIDER=ollama` - Activate Ollama provider
- `MODEL_NAME` (optional) - Model to use (default: llama3.2:3b)
- `OLLAMA_HOST` (optional) - Ollama server URL

**Usage Example:**
```bash
LLM_PROVIDER=ollama ./tools/llama-lore-creator.sh - entry "The Dark Tower" "place"
```

**Supported Models:**
- llama3.2:3b (default - lightweight)
- llama3:8b (larger, more capable)
- mistral:7b (alternative)
- Any model from ollama.ai/library

**Performance:**
- Local inference - no API costs
- Speed depends on hardware
- No network latency

**Error Handling:**
- Model not found → Auto-pull
- Ollama not installed → User guidance
- Generation fails → Return empty content

---

### Claude CLI

**Primary Use:** Direct Claude API access via CLI tool

**Integration Points:**
- `tools/llama-lore-creator.sh`
- `tools/llama-lore-integrator.sh`

**Configuration:**
```bash
case "$PROVIDER" in
  claude)
    # Execute Claude CLI with plain mode
    claude -p "$prompt"
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

**Environment Variables:**
- `LLM_PROVIDER=claude` - Activate Claude provider
- Claude CLI reads API key from its own configuration

**Usage Example:**
```bash
LLM_PROVIDER=claude ./tools/llama-lore-creator.sh - entry "The Dark Tower" "place"
```

**Authentication:**
- Claude CLI handles authentication internally
- User must run `claude login` once
- API key stored in Claude CLI config

**Features:**
- Plain mode (`-p`) - No formatting, raw text output
- Streaming support (not used in lore system)
- Multi-turn conversations (not used)

**Error Handling:**
- CLI not installed → User guidance
- Not authenticated → User must run `claude login`
- API error → Propagates to caller

---

### OpenAI API (via OpenRouter)

**Primary Use:** Access OpenAI models through OpenRouter

**Integration Point:** cURL in shell scripts

**Configuration:**
```bash
openai)
    local api_key="${OPENAI_API_KEY:-$OPENROUTER_API_KEY}"
    local base_url="${OPENAI_BASE_URL:-https://openrouter.ai/api/v1}"
    local model="${MODEL_NAME:-gpt-4o}"

    curl -s "$base_url/chat/completions" \
      -H "Authorization: Bearer $api_key" \
      -H "Content-Type: application/json" \
      -d "{
        \"model\": \"$model\",
        \"messages\": [{\"role\": \"user\", \"content\": $(echo "$prompt" | jq -R -s .)}]
      }" | \
      jq -r '.choices[0].message.content'
    ;;
```

**Environment Variables:**
- `LLM_PROVIDER=openai` - Activate OpenAI provider
- `OPENAI_API_KEY` or `OPENROUTER_API_KEY` - API key
- `OPENAI_BASE_URL` (optional) - Override endpoint (defaults to OpenRouter)

**Usage Example:**
```bash
export OPENAI_API_KEY="sk-or-v1-..."
LLM_PROVIDER=openai ./tools/llama-lore-creator.sh openai entry "Title" "category"
```

**Supported Models:**
- gpt-4o (default)
- gpt-4-turbo
- gpt-3.5-turbo
- Any OpenAI model available on OpenRouter

**Error Handling:**
- Missing API key → Exit with error
- cURL failure → Empty response
- JSON parsing error → jq error message

---

## Git Integration

### Commit Metadata Extraction

**Integration Point:** `integration/lore-flow.sh:38-72`

**Extraction Pattern:**
```bash
git-diff)
    # Extract diff
    RAW_CONTENT=$(git diff "$INPUT_CONTENT" || git show "$INPUT_CONTENT")

    # Extract author
    GIT_AUTHOR=$(git log -1 --format='%an' "$INPUT_CONTENT" || echo "")

    # Extract commit message (if needed)
    COMMIT_MSG=$(git log -1 --format='%s' "$INPUT_CONTENT" || echo "")
    ;;
```

**Git Commands Used:**
- `git diff <commit>` - Show changes in commit
- `git show <commit>` - Alternative to git diff
- `git log -1 --format='%an'` - Get author name
- `git log -1 --format='%s'` - Get commit subject

**Supported Input Formats:**
- `HEAD` - Most recent commit
- `HEAD~N` - N commits ago
- `<commit-hash>` - Specific commit
- `<branch>` - Latest commit on branch

**Usage Examples:**
```bash
# Process latest commit
./integration/lore-flow.sh git-diff HEAD

# Process previous commit
./integration/lore-flow.sh git-diff HEAD~1

# Process specific commit
./integration/lore-flow.sh git-diff a1b2c3d
```

**Author Mapping:**
```bash
# Map git author to persona ID
lookup_persona() {
  local author=$1
  local mapping_file="integration/persona-mapping.conf"

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

**Persona Mapping File:**
```bash
# integration/persona-mapping.conf
skogix=persona_1744992765        # Amy Ravenwolf
claude=persona_1743770116        # Claude
dot=persona_1747684741           # Dot
goose=persona_1743771995         # Goose

DEFAULT=persona_1763820091       # Village Elder (fallback)
```

---

## File System

### JSON Storage

**Pattern:** Direct file I/O with atomic operations

**Storage Locations:**
```
knowledge/expanded/lore/
├── entries/
│   └── entry_{timestamp}[_{hash}].json
├── books/
│   └── book_{timestamp}.json
└── personas/
    └── persona_{timestamp}.json
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

  # Write to temp file
  temp_file="${file}.tmp.$$"
  jq "$jq_expression" "$file" > "$temp_file"

  # Move (atomic)
  mv "$temp_file" "$file"
}
```

**Concurrency Considerations:**
- ❌ No file locking
- ❌ Last write wins (no merge)
- ⚠️  Race conditions possible with concurrent writes

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
├── current/
│   └── context-{session_id}.json
└── archive/
    └── context-{session_id}.json
```

**Operations:**

**Create:**
```bash
session_id=$(context-manager.sh create base)
# Creates: context/current/context-{timestamp}.json
# Returns: session_id (timestamp)
```

**Update:**
```bash
context-manager.sh update "$session_id" "system_state.orchestrator_mode" "lore"
# Uses jq to modify specific field
# Maintains JSON structure
```

**Archive:**
```bash
context-manager.sh archive "$session_id"
# Moves: current/context-{session_id}.json → archive/
```

**Integration with Pipeline:**
```bash
# lore-flow.sh creates session context at start
SESSION_ID=$(date +%s)

# All operations reference this session
TEMP_CONTENT="/tmp/lore-content-$SESSION_ID.txt"
ENTRY_ID="entry_${SESSION_ID}_..."

# Context tracks session progress
context-manager.sh update "$SESSION_ID" "current_task" "generate_narrative"
```

---

## Schema Validation

### JSON Schema (Draft 07)

**Schema Locations:**
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
  local schema_file="knowledge/core/lore/schema.json"

  jq -f scripts/jq/schema-validation/transform.jq \
    --argfile schema "$schema_file" \
    "$entry_file"
}
```

**Integration Points:**
- **Shell tools:** Validate after jq transformations
- **Python API:** Schemas loaded but NOT used for validation (gap)
- **argc CLI:** Validates before operations

**Validation Results:**
```json
{
  "valid": true,
  "errors": []
}

// Or on failure:
{
  "valid": false,
  "errors": [
    "missing required field: content",
    "invalid category: must be one of [character, place, event, object, concept, custom]"
  ]
}
```

---

## jq CRUD System

### Standard JSON Operations

**Location:** `scripts/jq/`

**Available Operations:**
- **crud-get** - Retrieve values at path
- **crud-set** - Update values at path
- **crud-delete** - Remove fields
- **schema-validation** - Validate structure
- **type-conversion** - to-array, to-object, to-number
- **data-extraction** - extract-urls, group-by-field

**Usage Pattern:**
```bash
# Get value
jq -f scripts/jq/crud-get/transform.jq \
  --arg path "voice.tone" \
  persona.json

# Set value
jq -f scripts/jq/crud-set/transform.jq \
  --arg path "content" \
  --arg value "Updated narrative..." \
  entry.json > tmp.json
mv tmp.json entry.json

# Delete field
jq -f scripts/jq/crud-delete/transform.jq \
  --arg path "summary" \
  entry.json > tmp.json
mv tmp.json entry.json
```

**Integration:**
- All shell tools use jq for JSON manipulation
- Python API doesn't use jq (native json module)
- Consistent interface across all skogai projects

---

## Numbered Knowledge System

### Task-Specific Knowledge Loading

**Integration Point:** `orchestrator/orchestrator.py`

**Knowledge Categories:**
```python
KNOWLEDGE_CATEGORIES = {
    "core": (0, 9),           # Emergency/critical
    "navigation": (10, 19),   # Navigation guides
    "identity": (20, 29),     # Agent identity
    "operational": (30, 99),  # Operational procedures
    "standards": (100, 199),  # Standards and conventions
    "project": (200, 299),    # Project-specific
    "tools": (300, 399),      # Tool documentation
    "frameworks": (1000, 9999)  # Framework references
}
```

**Loading Pattern:**
```python
def load_numbered_knowledge(numbers: List[str]) -> Dict[str, str]:
    """Load knowledge files by number prefix."""
    knowledge_base = "lorefiles/skogai/current/goose-memory-backup"
    knowledge = {}

    for filename in sorted(os.listdir(knowledge_base)):
        for num in numbers:
            if filename.startswith(num):
                with open(filepath, 'r') as f:
                    knowledge[filename] = f.read()

    return knowledge
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

## Integration Status Summary

| Integration | Status | Coverage | Notes |
|-------------|--------|----------|-------|
| **OpenRouter** | ✅ Working | 100% | Primary LLM gateway |
| **Ollama** | ✅ Working | 100% | Local inference |
| **Claude CLI** | ✅ Working | 100% | Direct API access |
| **OpenAI** | ✅ Working | 100% | Via OpenRouter |
| **Git** | ✅ Working | 80% | Commit extraction working |
| **File System** | ✅ Working | 100% | Atomic operations |
| **Context System** | ✅ Working | 100% | Session management |
| **JSON Schema** | ⚠️  Partial | 60% | Validation not enforced |
| **jq CRUD** | ✅ Working | 100% | Standard operations |
| **Knowledge Loading** | ✅ Working | 100% | Task-specific routing |

**Legend:**
- ✅ Working - Fully functional
- ⚠️  Partial - Working but incomplete
- ❌ Broken - Not functional

## External Dependencies

### Required
- Python 3.12+
- Bash 4.0+
- jq 1.6+
- git 2.0+

### Optional
- Ollama (for local LLM)
- Claude CLI (for direct Claude access)
- OpenRouter API key (for cloud LLMs)

### Installation

```bash
# Python dependencies
pip install -r requirements.txt

# Ollama (optional)
curl https://ollama.ai/install.sh | sh

# Claude CLI (optional)
npm install -g @anthropic-ai/claude-code

# jq (required)
# Ubuntu/Debian
sudo apt-get install jq

# macOS
brew install jq
```

## API Rate Limits

### OpenRouter
- **Timeout:** 120 seconds per request
- **Retry:** No automatic retry
- **Rate limiting:** Enforced by OpenRouter
- **Cost:** Pay per token

### Ollama
- **Timeout:** None (local)
- **Rate limiting:** Hardware dependent
- **Cost:** Free

### Claude CLI
- **Timeout:** Handled by CLI
- **Rate limiting:** Enforced by Anthropic API
- **Cost:** Pay per token (via API key)

## Security Considerations

### API Key Storage
- Environment variables (not in code)
- Never committed to git
- User responsible for securing keys

### Temp File Security
- ⚠️  Predictable paths (`/tmp/lore-$SESSION_ID.txt`)
- ❌ No mktemp usage (race condition risk)
- ⚠️  No secure deletion

### Input Validation
- ✅ Git author checked before use
- ❌ No sanitization of git commit messages
- ⚠️  Shell variable interpolation in Python (injection risk)

## Future Integration Opportunities

1. **Database Backend**
   - SQLite for structured queries
   - PostgreSQL for multi-user scenarios
   - Graph database for relationships

2. **Message Queue**
   - Redis for async processing
   - RabbitMQ for distributed workers

3. **Search Engine**
   - Elasticsearch for full-text search
   - Vector database for semantic search

4. **Monitoring**
   - Prometheus for metrics
   - Grafana for visualization
   - Sentry for error tracking

5. **Authentication**
   - OAuth for multi-user access
   - API keys for programmatic access
   - RBAC for permission management
