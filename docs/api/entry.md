# Entry API

> ⚠️ **DEPRECATION NOTICE**: The Python API (`lore_api.py`) is deprecated. Please use shell tools instead.  
> See [DEPRECATION.md](./DEPRECATION.md) for migration guide.

An entry is a single piece of narrative content - the atomic unit of lore.

## Recommended Tools

**Shell scripts** (PRIMARY):
- `tools/manage-lore.sh create-entry` - Create entries
- `tools/manage-lore.sh list-entries` - List all entries
- `tools/manage-lore.sh show-entry <id>` - Show entry details
- `tools/manage-lore.sh search <keyword>` - Search entries
- `tools/llama-lore-creator.sh - entry` - Generate with LLM

**CLI** (argc-based):
- `argc create-entry` - Create entry with flags
- `argc list-entries` - List all entries

## Schema

**Location:** `knowledge/core/lore/schema.json`

The entry schema is the definitive contract for all lore entries. Key requirements:

- **Required fields**: `id`, `title`, `content`, `category`
- **Category enum**: `character`, `place`, `event`, `object`, `concept`, `custom`
- **Content field**: Main narrative text in markdown format
- **Relationships**: Structured links to other entries with `target_id` and `relationship_type`
- **Visibility controls**: Public flag and persona-based access restrictions

See the [full JSON Schema](../../knowledge/core/lore/schema.json) for complete field definitions, types, and constraints.

## Structure Example

**Storage location:** `knowledge/expanded/lore/entries/entry_<timestamp>.json`

```json
{
  "id": "entry_1764992601",
  "title": "The Test Chronicle",
  "content": "In the depths of the digital realm, a test was conducted to verify the ancient systems still functioned as designed.",
  "summary": "",
  "category": "lore",
  "tags": ["test", "chronicle", "verification"],
  "relationships": [],
  "attributes": {},
  "book_id": "book_1764992601",
  "metadata": {
    "created_by": "skogix",
    "created_at": "2025-12-06T03:43:21Z",
    "updated_at": "2025-12-06T03:43:21Z",
    "version": "1.0",
    "canonical": true
  },
  "visibility": {
    "public": true,
    "restricted_to": []
  }
}
```

## Create an Entry

### Using manage-lore.sh (Recommended)

```bash
# Create entry
entry_id=$(./tools/manage-lore.sh create-entry "The Discovery" "lore")

# Update with content using jq
jq -f scripts/jq/crud-set/transform.jq \
  --arg path "content" \
  --arg value "In the twilight hours, the researcher uncovered patterns..." \
  "knowledge/expanded/lore/entries/${entry_id}.json" > tmp.json
mv tmp.json "knowledge/expanded/lore/entries/${entry_id}.json"

# Or generate content with LLM
LLM_PROVIDER=claude ./tools/llama-lore-creator.sh - entry "The Discovery" "lore"
```

### Using lore_api (Python) - DEPRECATED

> ⚠️ **Deprecated**: Use shell tools or CLI instead.

<details>
<summary>Legacy Python API example (not recommended)</summary>

```python
from agents.api.lore_api import LoreAPI

lore = LoreAPI()

entry = lore.create_lore_entry(
    title="The Discovery",
    content="In the twilight hours, the researcher uncovered patterns in the data that defied conventional understanding...",
    category="lore",
    tags=["discovery", "research", "mystery"]
)

print(f"Created: {entry['id']}")
# Output: Created: entry_1764992601
# File: knowledge/expanded/lore/entries/entry_1764992601.json
```

</details>

### Using argc (CLI)

```bash
argc create-entry --title "The Discovery" \
                  --content "In the twilight hours..." \
                  --category lore \
                  --tags discovery research mystery
# Output: Created: entry_1764992601
```

### Manual Creation (jq)

```bash
entry_id="entry_$(date +%s)"
timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo '{}' | \
  jq -f scripts/jq/crud-set/transform.jq --arg path "id" --arg value "$entry_id" | \
  jq -f scripts/jq/crud-set/transform.jq --arg path "title" --arg value "The Discovery" | \
  jq -f scripts/jq/crud-set/transform.jq --arg path "content" --arg value "In the twilight hours..." | \
  jq -f scripts/jq/crud-set/transform.jq --arg path "metadata.created_at" --arg value "$timestamp" \
  > "knowledge/expanded/lore/entries/${entry_id}.json"
```

## Read an Entry

### Using manage-lore.sh (Recommended)

```bash
# Show full entry
./tools/manage-lore.sh show-entry entry_1764992601

# Get specific field with jq
jq -r '.content' knowledge/expanded/lore/entries/entry_1764992601.json
```

### Using lore_api - DEPRECATED

> ⚠️ **Deprecated**: Use shell tools instead.

<details>
<summary>Legacy Python API example (not recommended)</summary>

```python
entry = lore.get_lore_entry("entry_1764992601")
print(entry['title'])
print(entry['content'])
```

</details>

### Using jq (Direct JSON manipulation)

```bash
# Get full entry
cat knowledge/expanded/lore/entries/entry_1764992601.json

# Get specific field
jq -f scripts/jq/crud-get/transform.jq \
  --arg path "content" \
  knowledge/expanded/lore/entries/entry_1764992601.json

# Get title and content only
jq '{title, content}' knowledge/expanded/lore/entries/entry_1764992601.json
```

## Update an Entry

### Using jq

```bash
# Update content
jq -f scripts/jq/crud-set/transform.jq \
  --arg path "content" \
  --arg value "Updated narrative text..." \
  knowledge/expanded/lore/entries/entry_1764992601.json > tmp.json
mv tmp.json knowledge/expanded/lore/entries/entry_1764992601.json

# Add a tag
jq '.tags += ["updated"]' \
  knowledge/expanded/lore/entries/entry_1764992601.json > tmp.json
mv tmp.json knowledge/expanded/lore/entries/entry_1764992601.json

# Update timestamp
jq -f scripts/jq/crud-set/transform.jq \
  --arg path "metadata.updated_at" \
  --arg value "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  knowledge/expanded/lore/entries/entry_1764992601.json > tmp.json
mv tmp.json knowledge/expanded/lore/entries/entry_1764992601.json
```

## Link Entry to Book

See [@docs/api/book.md](./book.md#link-entry-to-book)

## List Entries

### Using manage-lore.sh (Recommended)

```bash
# All entries
./tools/manage-lore.sh list-entries

# By category
./tools/manage-lore.sh list-entries lore

# Using argc
argc list-entries

# Using shell - all entries
for entry in knowledge/expanded/lore/entries/*.json; do
    jq -r '"\(.id): \(.title)"' "$entry"
done
```

### Using lore_api - DEPRECATED

> ⚠️ **Deprecated**: Use shell tools instead.

<details>
<summary>Legacy Python API example (not recommended)</summary>

```python
# All entries
entries = lore.list_lore_entries()

# By category
lore_entries = lore.list_lore_entries(category="lore")

for entry in lore_entries:
    print(f"{entry['id']}: {entry['title']}")
```

</details>

### Using shell (Advanced filters)

```bash
# All entries
for entry in knowledge/expanded/lore/entries/*.json; do
    jq -r '"\(.id): \(.title)"' "$entry"
done

# By category
for entry in knowledge/expanded/lore/entries/*.json; do
    if [ "$(jq -r '.category' "$entry")" = "lore" ]; then
        jq -r '.title' "$entry"
    fi
done

# By tag
for entry in knowledge/expanded/lore/entries/*.json; do
    if jq -e '.tags | contains(["discovery"])' "$entry" > /dev/null; then
        jq -r '.title' "$entry"
    fi
done
```

## Search Entries

### Using manage-lore.sh (Recommended)

```bash
./tools/manage-lore.sh search "quantum"
./tools/manage-lore.sh search "forest"
```

### By content (shell)

```bash
# Search for keyword in content
for entry in knowledge/expanded/lore/entries/*.json; do
    content=$(jq -r '.content' "$entry")
    if echo "$content" | grep -qi "quantum"; then
        jq -r '"\(.id): \(.title)"' "$entry"
    fi
done
```

### By date

```bash
# Entries created after a date
for entry in knowledge/expanded/lore/entries/*.json; do
    created=$(jq -r '.metadata.created_at' "$entry")
    if [[ "$created" > "2025-12-01" ]]; then
        jq -r '"\(.created_at): \(.title)"' "$entry"
    fi
done
```

## Common Patterns

### Read all entries in a book

```bash
argc read-book-entries book_1764992601
```

Or manually:

```bash
book_entries=$(jq -r '.entries[]' knowledge/expanded/lore/books/book_1764992601.json)
for entry_id in $book_entries; do
    cat "knowledge/expanded/lore/entries/${entry_id}.json"
done
```

### Get entry statistics

```bash
# Count entries by category
for entry in knowledge/expanded/lore/entries/*.json; do
    jq -r '.category' "$entry"
done | sort | uniq -c

# Count entries by tag
for entry in knowledge/expanded/lore/entries/*.json; do
    jq -r '.tags[]' "$entry"
done | sort | uniq -c
```

### Export entries to markdown

```bash
for entry in knowledge/expanded/lore/entries/*.json; do
    title=$(jq -r '.title' "$entry")
    content=$(jq -r '.content' "$entry")
    echo "# $title"
    echo ""
    echo "$content"
    echo ""
done > all_lore.md
```
