#!/bin/bash

# SkogAI Lore Management Tool
# Provides functionality for creating, listing, and managing lore entries and books
#
# ⚠️  DEPRECATION NOTICE:
# This bash-based tool is deprecated in favor of the Python API.
# Please use agents/api/lore_api.py for new integrations.
# See docs/guides/migration/MIGRATION_GUIDE.md for migration instructions.
# Features:
# - Schema validation using jq
# - Input validation and sanitization
# - Atomic file operations (write to temp, then move)
# - Proper error handling with cleanup
# - Duplicate detection

set -e

SKOGAI_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LORE_DIR="${SKOGAI_DIR}/knowledge/expanded/lore"
BOOKS_DIR="${LORE_DIR}/books"
ENTRIES_DIR="${LORE_DIR}/entries"
PERSONA_DIR="${SKOGAI_DIR}/knowledge/expanded/personas"
SCHEMA_DIR="${SKOGAI_DIR}/knowledge/core/lore"
ENTRY_SCHEMA="${SCHEMA_DIR}/schema.json"
BOOK_SCHEMA="${SCHEMA_DIR}/book-schema.json"

# Valid categories for lore entries
VALID_CATEGORIES=("character" "place" "event" "object" "concept" "custom")

# Ensure directories exist
mkdir -p "${BOOKS_DIR}"
mkdir -p "${ENTRIES_DIR}"
mkdir -p "${PERSONA_DIR}"

# Show deprecation warning (can be suppressed with LORE_NO_DEPRECATION_WARNING=1)
# show_deprecation_warning() {
#   if [ "${LORE_NO_DEPRECATION_WARNING}" != "1" ]; then
#     echo "⚠️  DEPRECATION WARNING" >&2
#     echo "   This bash tool is deprecated in favor of the Python API." >&2
#     echo "   Use: from agents.api.lore_api import LoreAPI" >&2
#     echo "   See: docs/guides/migration/MIGRATION_GUIDE.md" >&2
#     echo "   Set LORE_NO_DEPRECATION_WARNING=1 to suppress this warning." >&2
#     echo "" >&2
#   fi
# }

# Display help information
show_help() {
  echo "SkogAI Lore Management Tool"
  echo ""
  echo "⚠️  NOTE: This tool is deprecated. Use the Python API instead."
  echo "   See: docs/guides/migration/MIGRATION_GUIDE.md"
  echo ""
  echo "Usage: $0 [command] [options]"
  echo ""
  echo "Commands:"
  echo "  create-entry     Create a new lore entry"
  echo "  create-book      Create a new lore book"
  echo "  list-entries     List all lore entries"
  echo "  list-books       List all lore books"
  echo "  show-entry ID    Display a specific lore entry"
  echo "  show-book ID     Display a specific lore book"
  echo "  add-to-book      Add an entry to a book"
  echo "  link-to-persona  Associate a lore book with a persona"
  echo "  search           Search lore entries by keyword"
  echo "  validate-entry   Validate an entry JSON file"
  echo "  validate-book    Validate a book JSON file"
  echo "  help             Show this help message"
  echo ""
  echo "Features:"
  echo "  - Schema validation using jq"
  echo "  - Input sanitization and validation"
  echo "  - Atomic file operations"
  echo "  - Duplicate detection with warnings"
  echo ""
  echo "Categories: ${VALID_CATEGORIES[*]}"
  echo ""
  echo "For more information, see the documentation in knowledge/core/lore/"
}

# ============================================================================
# Core Functions
# ============================================================================

# Atomic update function - updates JSON file atomically
atomic_update() {
  local file="$1"
  local jq_expression="$2"
  local validate_type="$3"  # "entry", "book", or empty for no validation

  if [ ! -f "$file" ]; then
    echo "ERROR: File not found: $file" >&2
    return 1
  fi

  local temp_file="${file}.tmp.$$"

  # Apply jq transformation
  if ! jq "$jq_expression" "$file" > "$temp_file" 2>/dev/null; then
    echo "ERROR: jq transformation failed" >&2
    rm -f "$temp_file"
    return 1
  fi

  # Move temp file to target
  if ! mv "$temp_file" "$file"; then
    echo "ERROR: Failed to update file" >&2
    rm -f "$temp_file"
    return 1
  fi

  return 0
}

# Generate a unique identifier
generate_id() {
  echo "$(date +%s)_$(openssl rand -hex 4)"
}

# Create a new lore entry with validation and atomic write
create_entry() {
  local title="$1"
  local category="$2"

  # Generate ID and check for duplicates
  local entry_id="entry_$(generate_id)"
  local timestamp
  timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  local creator
  creator=$(whoami)

  # Build JSON using jq for proper escaping
  local json_content
  json_content=$(jq -n \
    --arg id "$entry_id" \
    --arg title "$title" \
    --arg category "$category" \
    --arg creator "$creator" \
    --arg timestamp "$timestamp" \
    '{
      id: $id,
      title: $title,
      content: "",
      summary: "",
      category: $category,
      tags: [],
      relationships: [],
      attributes: {},
      metadata: {
        created_by: $creator,
        created_at: $timestamp,
        updated_at: $timestamp,
        version: "1.0",
        canonical: true
      },
      visibility: {
        public: true,
        restricted_to: []
      }
    }')

  local target_file="${ENTRIES_DIR}/${entry_id}.json"
  echo $json_content >$target_file
  echo "Created lore entry: ${entry_id}"
  echo "Edit the file at: ${target_file} to add content"
}

# Create a new lore book with validation and atomic write
create_book() {
  local title="$1"
  local description="$2"

  # Generate ID and check for duplicates
  local book_id="book_$(generate_id)"
  local timestamp
  timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  local creator
  creator=$(whoami)

  # Build JSON using jq for proper escaping
  local json_content
  json_content=$(jq -n \
    --arg id "$book_id" \
    --arg title "$title" \
    --arg description "$description" \
    --arg creator "$creator" \
    --arg timestamp "$timestamp" \
    '{
      id: $id,
      title: $title,
      description: $description,
      entries: [],
      categories: {},
      tags: [],
      owners: [],
      readers: [],
      metadata: {
        created_by: $creator,
        created_at: $timestamp,
        updated_at: $timestamp,
        version: "1.0",
        status: "draft"
      },
      structure: [
        {
          name: "Introduction",
          description: "Overview of this lore book",
          entries: [],
          subsections: []
        }
      ],
      visibility: {
        public: false,
        system: false
      }
    }')

  local target_file="${BOOKS_DIR}/${book_id}.json"

  echo $json_content >$target_file
  echo "Created lore book: ${book_id}"
  echo "Edit the file at: ${target_file} to add structure and entries"
}

# List all lore entries
list_entries() {
  local category="$1"
  echo "Available Lore Entries:"
  echo "----------------------"

  if [ -z "$(ls -A "${ENTRIES_DIR}")" ]; then
    echo "No lore entries found."
    return 0
  fi

  for entry_file in "${ENTRIES_DIR}"/*.json; do
    if [ -f "$entry_file" ]; then
      local id=$(jq -r '.id' "$entry_file")
      local title=$(jq -r '.title' "$entry_file")
      local entry_category=$(jq -r '.category' "$entry_file")

      if [ -z "$category" ] || [ "$category" = "$entry_category" ]; then
        echo "$id - $title ($entry_category)"
      fi
    fi
  done
}

# List all lore books
list_books() {
  echo "Available Lore Books:"
  echo "-------------------"

  if [ -z "$(ls -A "${BOOKS_DIR}")" ]; then
    echo "No lore books found."
    return 0
  fi

  for book_file in "${BOOKS_DIR}"/*.json; do
    if [ -f "$book_file" ]; then
      local id=$(jq -r '.id' "$book_file")
      local title=$(jq -r '.title' "$book_file")
      local entry_count=$(jq '.entries | length' "$book_file")
      local status=$(jq -r '.metadata.status' "$book_file")

      echo "$id - $title ($entry_count entries) [$status]"
    fi
  done
}

# Show a specific lore entry
show_entry() {
  local entry_id="$1"

  if [ -z "$entry_id" ]; then
    echo "Usage: $0 show-entry entry_id"
    return 1
  fi

  local entry_file="${ENTRIES_DIR}/${entry_id}.json"

  if [ ! -f "$entry_file" ]; then
    echo "Error: Entry not found: $entry_id"
    return 1
  fi

  echo "Lore Entry: $(jq -r '.title' "$entry_file")"
  echo "ID: $(jq -r '.id' "$entry_file")"
  echo "Category: $(jq -r '.category' "$entry_file")"
  echo "---"
  echo "Summary: $(jq -r '.summary' "$entry_file")"
  echo "---"
  echo "Content:"
  jq -r '.content' "$entry_file"
  echo "---"
  echo "Tags: $(jq -r '.tags | join(", ")' "$entry_file")"
  echo "Created: $(jq -r '.metadata.created_at' "$entry_file") by $(jq -r '.metadata.created_by' "$entry_file")"
}

# Show a specific lore book
show_book() {
  local book_id="$1"

  if [ -z "$book_id" ]; then
    echo "Usage: $0 show-book book_id"
    return 1
  fi

  local book_file="${BOOKS_DIR}/${book_id}.json"

  if [ ! -f "$book_file" ]; then
    echo "Error: Book not found: $book_id"
    return 1
  fi

  echo "Lore Book: $(jq -r '.title' "$book_file")"
  echo "ID: $(jq -r '.id' "$book_file")"
  echo "Description: $(jq -r '.description' "$book_file")"
  echo "Status: $(jq -r '.metadata.status' "$book_file")"
  echo "---"
  echo "Structure:"
  jq -r '.structure[] | "• " + .name + ": " + .description' "$book_file"
  echo "---"
  echo "Entries ($(jq '.entries | length' "$book_file")):"

  local entries=$(jq -r '.entries[]' "$book_file")
  if [ -n "$entries" ]; then
    for entry_id in $entries; do
      local entry_file="${ENTRIES_DIR}/${entry_id}.json"
      if [ -f "$entry_file" ]; then
        echo "• $(jq -r '.title' "$entry_file") ($entry_id)"
      else
        echo "• $entry_id (missing file)"
      fi
    done
  else
    echo "No entries in this book yet."
  fi
}

# Add an entry to a book with atomic operations
add_to_book() {
  local entry_id="$1"
  local book_id="$2"
  local section="$3"

  if [ -z "$entry_id" ] || [ -z "$book_id" ]; then
    echo "Usage: $0 add-to-book entry_id book_id [section_name]"
    return 1
  fi

  local entry_file="${ENTRIES_DIR}/${entry_id}.json"
  local book_file="${BOOKS_DIR}/${book_id}.json"

  if [ ! -f "$entry_file" ]; then
    echo "ERROR: Entry not found: $entry_id" >&2
    return 1
  fi

  if [ ! -f "$book_file" ]; then
    echo "ERROR: Book not found: $book_id" >&2
    return 1
  fi

  # Add entry to book's entry list if not already there
  if ! jq -e ".entries | contains([\"$entry_id\"])" "$book_file" >/dev/null; then
    if ! atomic_update "$book_file" ".entries += [\"$entry_id\"]" "book"; then
      echo "ERROR: Failed to add entry to book's entry list" >&2
      return 1
    fi
    echo "Added entry to book's entry list"
  fi

  # If section is specified, add to that section
  if [ -n "$section" ]; then
    if jq -e ".structure[] | select(.name == \"$section\")" "$book_file" >/dev/null; then
      # Section exists, add entry to it
      if ! atomic_update "$book_file" "(.structure[] | select(.name == \"$section\").entries) += [\"$entry_id\"]" "book"; then
        echo "ERROR: Failed to add entry to section" >&2
        return 1
      fi
      echo "Added entry to section: $section"
    else
      echo "Section not found: $section"
      echo "Available sections:"
      jq -r '.structure[].name' "$book_file"
      return 1
    fi
  fi

  # Update book's updated_at timestamp
  local timestamp
  timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  if ! atomic_update "$book_file" ".metadata.updated_at = \"$timestamp\"" "book"; then
    echo "WARNING: Failed to update timestamp" >&2
  fi

  # Update entry's book_id
  if ! atomic_update "$entry_file" ".book_id = \"$book_id\"" "entry"; then
    echo "WARNING: Failed to update entry's book_id" >&2
  fi

  echo "Successfully added $entry_id to $book_id"
}

# Link a lore book to a persona with atomic operations
link_to_persona() {
  local book_id="$1"
  local persona_id="$2"

  if [ -z "$book_id" ] || [ -z "$persona_id" ]; then
    echo "Usage: $0 link-to-persona book_id persona_id"
    return 1
  fi

  local book_file="${BOOKS_DIR}/${book_id}.json"
  local persona_file="${PERSONA_DIR}/${persona_id}.json"

  if [ ! -f "$book_file" ]; then
    echo "ERROR: Book not found: $book_id" >&2
    return 1
  fi

  if [ ! -f "$persona_file" ]; then
    echo "ERROR: Persona not found: $persona_id" >&2
    return 1
  fi

  # Add persona to book's readers list if not already there
  if ! jq -e ".readers | contains([\"$persona_id\"])" "$book_file" >/dev/null; then
    if ! atomic_update "$book_file" ".readers += [\"$persona_id\"]" "book"; then
      echo "ERROR: Failed to add persona to book's readers list" >&2
      return 1
    fi
    echo "Added persona to book's readers list"
  fi

  # Add book to persona's lore_books list if not already there
  if jq -e '.knowledge.lore_books' "$persona_file" >/dev/null 2>&1; then
    if ! jq -e ".knowledge.lore_books | contains([\"$book_id\"])" "$persona_file" >/dev/null; then
      if ! atomic_update "$persona_file" ".knowledge.lore_books += [\"$book_id\"]" ""; then
        echo "ERROR: Failed to add book to persona's lore_books" >&2
        return 1
      fi
    fi
  else
    # Create lore_books array if it doesn't exist
    if ! atomic_update "$persona_file" ".knowledge.lore_books = [\"$book_id\"]" ""; then
      echo "ERROR: Failed to create lore_books in persona" >&2
      return 1
    fi
  fi

  echo "Successfully linked book $book_id to persona $persona_id"
}

# Search lore entries
search_lore() {
  local query="$1"

  if [ -z "$query" ]; then
    echo "Usage: $0 search \"search term\""
    return 1
  fi

  echo "Searching for: $query"
  echo "-------------------"

  local found=0

  for entry_file in "${ENTRIES_DIR}"/*.json; do
    if [ -f "$entry_file" ]; then
      if jq -r '.title + " " + .content + " " + .summary + " " + (.tags | join(" "))' "$entry_file" | grep -qi "$query"; then
        local id=$(jq -r '.id' "$entry_file")
        local title=$(jq -r '.title' "$entry_file")
        local category=$(jq -r '.category' "$entry_file")
        echo "$id - $title ($category)"
        found=1
      fi
    fi
  done

  if [ $found -eq 0 ]; then
    echo "No matches found."
  fi
}

# ============================================================================
# Validation Commands
# ============================================================================

# Validate an entry file
validate_entry_file() {
  local file="$1"

  if [ -z "$file" ]; then
    echo "Usage: $0 validate-entry <file.json>"
    return 1
  fi

  if [ ! -f "$file" ]; then
    echo "ERROR: File not found: $file" >&2
    return 1
  fi

  if validate_entry_schema "$file"; then
    echo "✓ Entry validation passed: $file"
    return 0
  else
    echo "✗ Entry validation failed: $file"
    return 1
  fi
}

# Validate a book file
validate_book_file() {
  local file="$1"

  if [ -z "$file" ]; then
    echo "Usage: $0 validate-book <file.json>"
    return 1
  fi

  if [ ! -f "$file" ]; then
    echo "ERROR: File not found: $file" >&2
    return 1
  fi

  if validate_book_schema "$file"; then
    echo "✓ Book validation passed: $file"
    return 0
  else
    echo "✗ Book validation failed: $file"
    return 1
  fi
}

# ============================================================================
# Main Command Processing
# ============================================================================

case "$1" in
create-entry)
  create_entry "$2" "$3"
  ;;
create-book)
  create_book "$2" "$3"
  ;;
list-entries)
  list_entries "$2"
  ;;
list-books)
  list_books
  ;;
show-entry)
  show_entry "$2"
  ;;
show-book)
  show_book "$2"
  ;;
add-to-book)
  add_to_book "$2" "$3" "$4"
  ;;
link-to-persona)
  link_to_persona "$2" "$3"
  ;;
search)
  search_lore "$2"
  ;;
validate-entry)
  validate_entry_file "$2"
  ;;
validate-book)
  validate_book_file "$2"
  ;;
help | --help | -h)
  show_help
  ;;
*)
  echo "Unknown command: $1"
  echo "Run '$0 help' for usage information."
  exit 1
  ;;
esac
