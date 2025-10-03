#!/bin/bash

# SkogAI Lore Management Tool
# Provides functionality for creating, listing, and managing lore entries and books

set -e

# Load library functions and paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../config/lib.sh"
source "${SCRIPT_DIR}/../config/paths.sh"

# Load environment variables from skogcli config
load_skogcli_env

# Define directories using centralized paths
LORE_DIR="${SKOGAI_LORE}/knowledge/expanded/lore"
BOOKS_DIR="${LORE_DIR}/books"
ENTRIES_DIR="${LORE_DIR}/entries"
PERSONA_DIR="${SKOGAI_LORE}/knowledge/expanded/personas"

# Ensure directories exist
mkdir -p "${BOOKS_DIR}"
mkdir -p "${ENTRIES_DIR}"
mkdir -p "${PERSONA_DIR}"

# Display help information
show_help() {
  echo "SkogAI Lore Management Tool"
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
  echo "  help             Show this help message"
  echo ""
  echo "For more information, see the documentation in knowledge/core/lore/"
}

# Note: generate_id() function is now provided by config/lib.sh

# Create a new lore entry
create_entry() {
  local title="$1"
  local category="$2"
  local entry_id="entry_$(generate_id)"
  local timestamp=$(get_timestamp)

  if [ -z "$title" ] || [ -z "$category" ]; then
    echo "Usage: $0 create-entry \"Entry Title\" category"
    echo "Categories: character, place, event, object, concept, custom"
    return 1
  fi

  # Create JSON structure
  cat >"${ENTRIES_DIR}/${entry_id}.json" <<EOF
{
  "id": "${entry_id}",
  "title": "${title}",
  "content": "",
  "summary": "",
  "category": "${category}",
  "tags": [],
  "relationships": [],
  "attributes": {},
  "metadata": {
    "created_by": "$(whoami)",
    "created_at": "${timestamp}",
    "updated_at": "${timestamp}",
    "version": "1.0",
    "canonical": true
  },
  "visibility": {
    "public": true,
    "restricted_to": []
  }
}
EOF

  echo "Created lore entry: ${entry_id}"
  echo "Edit the file at: ${ENTRIES_DIR}/${entry_id}.json to add content"
}

# Create a new lore book
create_book() {
  local title="$1"
  local description="$2"
  local book_id="book_$(generate_id)"
  local timestamp=$(get_timestamp)

  if [ -z "$title" ]; then
    echo "Usage: $0 create-book \"Book Title\" \"Optional description\""
    return 1
  fi

  # Create JSON structure
  cat >"${BOOKS_DIR}/${book_id}.json" <<EOF
{
  "id": "${book_id}",
  "title": "${title}",
  "description": "${description}",
  "entries": [],
  "categories": {},
  "tags": [],
  "owners": [],
  "readers": [],
  "metadata": {
    "created_by": "$(whoami)",
    "created_at": "${timestamp}",
    "updated_at": "${timestamp}",
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
EOF

  echo "Created lore book: ${book_id}"
  echo "Edit the file at: ${BOOKS_DIR}/${book_id}.json to add structure and entries"
}

# List all lore entries
list_entries() {
  local category="$1"
  echo "Available Lore Entries:"
  echo "----------------------"

  if [ -z "$(ls -A "${ENTRIES_DIR}" 2>/dev/null)" ]; then
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

  if [ -z "$(ls -A "${BOOKS_DIR}" 2>/dev/null)" ]; then
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

# Add an entry to a book
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
    echo "Error: Entry not found: $entry_id"
    return 1
  fi

  if [ ! -f "$book_file" ]; then
    echo "Error: Book not found: $book_id"
    return 1
  fi

  # Add entry to book's entry list if not already there
  if ! jq -e ".entries | contains([\"$entry_id\"])" "$book_file" >/dev/null; then
    jq ".entries += [\"$entry_id\"]" "$book_file" >"${book_file}.tmp" && mv "${book_file}.tmp" "$book_file"
    echo "Added entry to book's entry list"
  fi

  # If section is specified, add to that section
  if [ -n "$section" ]; then
    if jq -e ".structure[] | select(.name == \"$section\")" "$book_file" >/dev/null; then
      # Section exists, add entry to it
      jq "(.structure[] | select(.name == \"$section\").entries) += [\"$entry_id\"]" "$book_file" >"${book_file}.tmp" && mv "${book_file}.tmp" "$book_file"
      echo "Added entry to section: $section"
    else
      echo "Section not found: $section"
      echo "Available sections:"
      jq -r '.structure[].name' "$book_file"
    fi
  fi

  # Update book's updated_at timestamp
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  jq ".metadata.updated_at = \"$timestamp\"" "$book_file" >"${book_file}.tmp" && mv "${book_file}.tmp" "$book_file"

  # Update entry's book_id
  jq ".book_id = \"$book_id\"" "$entry_file" >"${entry_file}.tmp" && mv "${entry_file}.tmp" "$entry_file"

  echo "Successfully added $entry_id to $book_id"
}

# Link a lore book to a persona
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
    echo "Error: Book not found: $book_id"
    return 1
  fi

  if [ ! -f "$persona_file" ]; then
    echo "Error: Persona not found: $persona_id"
    return 1
  fi

  # Add persona to book's readers list if not already there
  if ! jq -e ".readers | contains([\"$persona_id\"])" "$book_file" >/dev/null; then
    jq ".readers += [\"$persona_id\"]" "$book_file" >"${book_file}.tmp" && mv "${book_file}.tmp" "$book_file"
    echo "Added persona to book's readers list"
  fi

  # Add book to persona's lore_books list if not already there
  if jq -e '.knowledge.lore_books' "$persona_file" >/dev/null; then
    if ! jq -e ".knowledge.lore_books | contains([\"$book_id\"])" "$persona_file" >/dev/null; then
      jq ".knowledge.lore_books += [\"$book_id\"]" "$persona_file" >"${persona_file}.tmp" && mv "${persona_file}.tmp" "$persona_file"
    fi
  else
    # Create lore_books array if it doesn't exist
    jq ".knowledge.lore_books = [\"$book_id\"]" "$persona_file" >"${persona_file}.tmp" && mv "${persona_file}.tmp" "$persona_file"
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

# Main command processing
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
help | --help | -h)
  show_help
  ;;
*)
  echo "Unknown command: $1"
  echo "Run '$0 help' for usage information."
  exit 1
  ;;
esac
