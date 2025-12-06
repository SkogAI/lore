# Book API

A book is a collection of lore entries organized by theme, persona, or topic.

## Schema

**Location:** `knowledge/core/book-schema.json`

The book schema is the definitive contract for all lore books. Key requirements:

- **Required fields**: `id`, `title`, `description`
- **Entries array**: List of entry IDs contained in this book
- **Readers/Owners**: Persona-based access control (readers can view, owners can modify)
- **Status enum**: `draft`, `active`, `archived`, `deprecated`
- **Relationships**: Links to other books with types like `sequel`, `prequel`, `expansion`, `contradiction`
- **Structure**: Hierarchical organization with sections and subsections

See the [full JSON Schema](../../knowledge/core/book-schema.json) for complete field definitions, types, and constraints.

## Structure Example

**Storage location:** `knowledge/expanded/lore/books/book_<timestamp>_<hash>.json`

```json
{
  "id": "book_1764992601",
  "title": "Test Chronicles",
  "description": "A collection of test entries to verify system functionality",
  "entries": ["entry_1764992601"],
  "categories": {},
  "tags": [],
  "owners": [],
  "readers": ["persona_1764992753"],
  "metadata": {
    "created_by": "skogix",
    "created_at": "2025-12-06T03:43:21Z",
    "updated_at": "2025-12-06T03:43:21Z",
    "version": "1.0",
    "status": "draft"
  },
  "structure": [
    {
      "name": "Introduction",
      "description": "Overview of this lore book",
      "entries": [],
      "subsections": []
    }
  ],
  "visibility": {
    "public": false,
    "system": false
  }
}
```

## Create a Book

### Using lore_api (Python)

```python
from agents.api.lore_api import LoreAPI

lore = LoreAPI()

book = lore.create_lore_book(
    title="Chronicles of Discovery",
    description="Tales of exploration and learning"
)

print(f"Created: {book['id']}")
# Output: Created: book_1764992601
# File: knowledge/expanded/lore/books/book_1764992601.json
```

### Using argc (CLI)

```bash
argc create-book --title "Chronicles of Discovery" \
                 --description "Tales of exploration and learning"
# Output: Created: book_1764992601
```

### Manual Creation (jq)

```bash
book_id="book_$(date +%s)_$(openssl rand -hex 4)"
timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo '{}' | \
  jq -f scripts/jq/crud-set/transform.jq --arg path "id" --arg value "$book_id" | \
  jq -f scripts/jq/crud-set/transform.jq --arg path "title" --arg value "Chronicles of Discovery" | \
  jq -f scripts/jq/crud-set/transform.jq --arg path "metadata.created_at" --arg value "$timestamp" \
  > "knowledge/expanded/lore/books/${book_id}.json"
```

## Read a Book

### Using lore_api

```python
book = lore.get_lore_book("book_1764992601")
print(book['title'])
# Output: Test Chronicles
```

### Using jq

```bash
# Get full book
cat knowledge/expanded/lore/books/book_1764992601.json

# Get specific field
jq -f scripts/jq/crud-get/transform.jq \
  --arg path "title" \
  knowledge/expanded/lore/books/book_1764992601.json
# Output: "Test Chronicles"

# Get entries list
jq '.entries' knowledge/expanded/lore/books/book_1764992601.json
# Output: ["entry_1764992601"]
```

## Update a Book

### Using lore_api

```python
book = lore.get_lore_book("book_1764992601")
book['title'] = "Updated Chronicles"
# Save manually or use lore_api's update method if implemented
```

### Using jq

```bash
# Update title
jq -f scripts/jq/crud-set/transform.jq \
  --arg path "title" \
  --arg value "Updated Chronicles" \
  knowledge/expanded/lore/books/book_1764992601.json > tmp.json
mv tmp.json knowledge/expanded/lore/books/book_1764992601.json

# Add a tag
jq '.tags += ["updated"]' \
  knowledge/expanded/lore/books/book_1764992601.json > tmp.json
mv tmp.json knowledge/expanded/lore/books/book_1764992601.json
```

## Link Entry to Book

### Using lore_api

```python
lore.add_entry_to_book("entry_1764992601", "book_1764992601")
# Updates both files:
# - Adds entry_id to book['entries']
# - Sets entry['book_id'] = book_id
```

### Using jq

```bash
# Add entry to book's entries array
jq '.entries += ["entry_1764992601"]' \
  knowledge/expanded/lore/books/book_1764992601.json > tmp.json
mv tmp.json knowledge/expanded/lore/books/book_1764992601.json

# Set book_id on entry
jq -f scripts/jq/crud-set/transform.jq \
  --arg path "book_id" \
  --arg value "book_1764992601" \
  knowledge/expanded/lore/entries/entry_1764992601.json > tmp.json
mv tmp.json knowledge/expanded/lore/entries/entry_1764992601.json
```

## Link Persona to Book

### Using lore_api

```python
lore.link_book_to_persona("book_1764992601", "persona_1764992753")
# Adds persona_id to book['readers']
```

### Using jq

```bash
jq '.readers += ["persona_1764992753"]' \
  knowledge/expanded/lore/books/book_1764992601.json > tmp.json
mv tmp.json knowledge/expanded/lore/books/book_1764992601.json
```

## List All Books

### Using lore_api

```python
books = lore.list_lore_books()
for book in books:
    print(f"{book['id']}: {book['title']}")
```

### Using argc

```bash
argc list-books
```

### Using shell

```bash
for book in knowledge/expanded/lore/books/*.json; do
    jq -r '"\(.id): \(.title)"' "$book"
done
```

## Common Patterns

### Get all entries in a book

```python
book = lore.get_lore_book("book_1764992601")
for entry_id in book['entries']:
    entry = lore.get_lore_entry(entry_id)
    print(entry['title'])
```

### Find books by tag

```bash
for book in knowledge/expanded/lore/books/*.json; do
    if jq -e '.tags | contains(["chronicle"])' "$book" > /dev/null; then
        jq -r '.title' "$book"
    fi
done
```

### Books read by a persona

```bash
for book in knowledge/expanded/lore/books/*.json; do
    if jq -e '.readers | contains(["persona_1764992753"])' "$book" > /dev/null; then
        jq -r '.title' "$book"
    fi
done
```
