# Persona API

A persona is an AI character profile with unique voice, traits, and characteristics used to generate consistent narrative content.

## Schema

**Location:** `knowledge/core/persona/schema.json`

The persona schema is the definitive contract for all persona definitions. Key requirements:

- **Required fields**: `id`, `name`, `core_traits`, `voice`
- **Core traits**: `temperament` (string), `values` (array), `motivations` (array)
- **Voice**: `tone` (string), `patterns` (array), `vocabulary` (string)
- **Interaction style enums**:
  - `formality`: `very_formal`, `formal`, `neutral`, `casual`, `very_casual`
  - `humor`: `none`, `subtle`, `occasional`, `frequent`, `constant`
  - `directness`: `very_direct`, `direct`, `balanced`, `indirect`, `very_indirect`
- **Knowledge**: Expertise areas, limitations, and lore book references
- **Background**: Origin, significant events, connections to other entities

See the [full JSON Schema](../../knowledge/core/persona/schema.json) for complete field definitions, types, and constraints.

## Structure Example

**Storage location:** `knowledge/expanded/personas/persona_<timestamp>.json`

```json
{
  "id": "persona_1764992753",
  "name": "Aria Nightwhisper",
  "core_traits": {
    "temperament": "balanced",
    "values": ["methodical", "curious"],
    "motivations": ["patient", "detail-oriented"]
  },
  "voice": {
    "tone": "poetic yet precise",
    "patterns": [],
    "vocabulary": "standard"
  },
  "background": {
    "origin": "",
    "significant_events": [],
    "connections": []
  },
  "knowledge": {
    "expertise": [],
    "limitations": [],
    "lore_books": []
  },
  "interaction_style": {
    "formality": "neutral",
    "humor": "occasional",
    "directness": "balanced"
  },
  "meta": {
    "version": "1.0",
    "created": "2025-12-06T03:45:53Z",
    "modified": "2025-12-06T03:45:53Z",
    "tags": []
  }
}
```

## Create a Persona

### Using argc (CLI)

```bash
argc create-persona --name "Aria Nightwhisper" \
                    --voice-tone "poetic yet precise"
# Output: Created: persona_1764992753
```

### Manual Creation (jq)

```bash
persona_id="persona_$(date +%s)"
timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo '{}' | \
  jq -f scripts/jq/crud-set/transform.jq --arg path "id" --arg value "$persona_id" | \
  jq -f scripts/jq/crud-set/transform.jq --arg path "name" --arg value "Aria Nightwhisper" | \
  jq -f scripts/jq/crud-set/transform.jq --arg path "voice.tone" --arg value "poetic yet precise" | \
  jq -f scripts/jq/crud-set/transform.jq --arg path "meta.created" --arg value "$timestamp" \
  > "knowledge/expanded/personas/${persona_id}.json"
```

### Using lore_api (Python)

> **Note:** The Python API (`lore_api.py`) is deprecated.
> Use shell tools for new code. See [CLAUDE.md](../../CLAUDE.md) for canonical interface documentation.

```python
from agents.api.lore_api import LoreAPI

lore = LoreAPI()

persona = lore.create_persona(
    name="Aria Nightwhisper",
    core_description="A keeper of digital records who weaves technical details into narrative tapestries",
    personality_traits=["methodical", "curious", "patient", "detail-oriented"],
    voice_tone="poetic yet precise"
)

print(f"Created: {persona['id']}")
# Output: Created: persona_1764992753
# File: knowledge/expanded/personas/persona_1764992753.json
```

**Note:** The `lore_api.create_persona()` method automatically:
- Splits `personality_traits[0:2]` into `core_traits.values`
- Splits `personality_traits[2:4]` into `core_traits.motivations`
- Sets `voice.tone` from `voice_tone` parameter
- Generates default structure for other fields

## Read a Persona

### Using jq

```bash
# Get full persona
cat knowledge/expanded/personas/persona_1764992753.json

# Get name
jq -f scripts/jq/crud-get/transform.jq \
  --arg path "name" \
  knowledge/expanded/personas/persona_1764992753.json

# Get voice tone
jq -f scripts/jq/crud-get/transform.jq \
  --arg path "voice.tone" \
  knowledge/expanded/personas/persona_1764992753.json

# Get core values
jq '.core_traits.values' knowledge/expanded/personas/persona_1764992753.json
```

### Using lore_api (Python)

> **Note:** The Python API (`lore_api.py`) is deprecated.
> Use shell tools for new code. See [CLAUDE.md](../../CLAUDE.md) for canonical interface documentation.

```python
persona = lore.get_persona("persona_1764992753")
print(persona['name'])
print(persona['voice']['tone'])
```

## Update a Persona

### Using jq

```bash
# Update voice tone
jq -f scripts/jq/crud-set/transform.jq \
  --arg path "voice.tone" \
  --arg value "precise and analytical" \
  knowledge/expanded/personas/persona_1764992753.json > tmp.json
mv tmp.json knowledge/expanded/personas/persona_1764992753.json

# Add expertise
jq '.knowledge.expertise += ["quantum mechanics"]' \
  knowledge/expanded/personas/persona_1764992753.json > tmp.json
mv tmp.json knowledge/expanded/personas/persona_1764992753.json

# Update modified timestamp
jq -f scripts/jq/crud-set/transform.jq \
  --arg path "meta.modified" \
  --arg value "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  knowledge/expanded/personas/persona_1764992753.json > tmp.json
mv tmp.json knowledge/expanded/personas/persona_1764992753.json
```

## Link Persona to Book

See [@docs/api/book.md](./book.md#link-persona-to-book)

## List Personas

### Using shell

```bash
for persona in knowledge/expanded/personas/*.json; do
    jq -r '"\(.id): \(.name)"' "$persona"
done
```

### Using lore_api (Python)

> **Note:** The Python API (`lore_api.py`) is deprecated.
> Use shell tools for new code. See [CLAUDE.md](../../CLAUDE.md) for canonical interface documentation.

```python
personas = lore.list_personas()
for persona in personas:
    print(f"{persona['id']}: {persona['name']}")
```

## Get Persona Context

### Using lore_api (Python)

> **Note:** The Python API (`lore_api.py`) is deprecated.
> Use shell tools for new code. See [CLAUDE.md](../../CLAUDE.md) for canonical interface documentation.

The `lore_api` can build a complete context for a persona including their lore books:

```python
context = lore.get_persona_lore_context("persona_1764992753")

print(f"Persona: {context['persona']['name']}")
print(f"Voice: {context['persona']['voice']['tone']}")
print(f"Books: {len(context['lore_books'])}")
for book in context['lore_books']:
    print(f"  - {book['title']}: {len(book['entries'])} entries")
```

## Common Patterns

### Find books a persona reads

```bash
# Get books linked to persona
for book in knowledge/expanded/lore/books/*.json; do
    if jq -e '.readers | contains(["persona_1764992753"])' "$book" > /dev/null; then
        jq -r '"\(.id): \(.title)"' "$book"
    fi
done
```

### Get all entries written in persona's voice

```bash
# Assuming entries have a "persona_id" field
for entry in knowledge/expanded/lore/entries/*.json; do
    if [ "$(jq -r '.persona_id' "$entry")" = "persona_1764992753" ]; then
        jq -r '.title' "$entry"
    fi
done
```

### Export persona profile

```bash
persona_id="persona_1764992753"
name=$(jq -r '.name' "knowledge/expanded/personas/${persona_id}.json")
tone=$(jq -r '.voice.tone' "knowledge/expanded/personas/${persona_id}.json")
values=$(jq -r '.core_traits.values | join(", ")' "knowledge/expanded/personas/${persona_id}.json")

echo "# $name"
echo ""
echo "**Voice Tone:** $tone"
echo "**Core Values:** $values"
echo ""
```

### Search personas by trait

```bash
# Find personas with "curious" in values
for persona in knowledge/expanded/personas/*.json; do
    if jq -e '.core_traits.values | contains(["curious"])' "$persona" > /dev/null; then
        jq -r '.name' "$persona"
    fi
done
```

## Persona Statistics

```bash
# Count total personas
ls -1 knowledge/expanded/personas/*.json | wc -l

# List all unique voice tones
for persona in knowledge/expanded/personas/*.json; do
    jq -r '.voice.tone' "$persona"
done | sort | uniq

# Count personas by temperament
for persona in knowledge/expanded/personas/*.json; do
    jq -r '.core_traits.temperament' "$persona"
done | sort | uniq -c
```
