#!/usr/bin/env bash
set -e

# @describe 📚 Chronicles of the Digital Realm - A mystical toolkit for weaving digital legends
# @meta version 3.0.0
# @meta author The Grand Chronicler <chronicler@realms.mystic>
# @meta dotenv .env.arcane
# @meta require-tools jq
# @meta man-section 1

# 🌟 Ancient Mystical Variables
# @env SKOGAI_DIR=/home/skogix/ path to yo skogai-folder!
# @env LORE_SCRIPTS=/home/skogix/lore/tools path to yo skogai-folder!
# @env LORE_DIR=/home/skogix/lore/knowledge/expanded/lore path to yo lore!
# @env BOOKS_DIR=/home/skogix/lore/knowledge/expanded/lore/books path to yo books!
# @env ENTRIES_DIR=/home/skogix/lore/knowledge/expanded/lore/entries path to yo entries!
# @env PERSONA_DIR=/home/skogix/lore/knowledge/expanded/persona path to yo persona!
# @env LLM_OUTPUT=/dev/stdout The output path

# 📜 Sacred configuration scrolls
readonly MYSTICAL_SANCTUM="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly CHRONICLES_TOME="lore.chronicle"

# ✨ Enchantment helpers for manifestations
_essence_forms() {
  echo "parchment runes crystals scrolls codex"
}

_time_epoch() {
  date +"%Y%m%d_%H%M%S"
}

_legendary_branches() {
  git branch -r 2>/dev/null | sed 's/origin\///' | tr -d ' ' || echo "genesis epoch legend"
}

_wisdom_depths() {
  echo "whisper insight warning catastrophe"
}

_portal_gateways() {
  echo "3000 8000 8080 9000"
}

# 🔍 Schema field helpers
_get_category() {
  jq -r '.category' "$1"
}

_get_status() {
  jq -r '.metadata.status // empty' "$1"
}

_get_book_id() {
  jq -r '.book_id // empty' "$1"
}

# 📖 Chronicle inscriptions
# @cmd 🔮 Validate entry schema yao
# @arg entry![`_choice_entries`] Entry to validate
# @alias validate_entry
validate-entry() {
  jq -f scripts/jq/schema-validation/transform.jq --arg schema '{"required":["id","title","content","category"],"types":{"id":"string","title":"string","content":"string","category":"string"}}' "${ENTRIES_DIR}/${argc_entry}.json"
}

# 📖 Chronicle inscriptions
# @cmd 🔮 Validate book schema yao
# @arg book![`_choice_books`] Book to validate
# @alias validate_book
validate-book() {
  jq -f scripts/jq/schema-validation/transform.jq --arg schema '{"required":["id","title","description"],"types":{"id":"string","title":"string","description":"string","entries":"array"}}' "${BOOKS_DIR}/${argc_book}.json"
}

# 📖 Chronicle inscriptions
# @cmd 🔮 Validate persona schema yao
# @arg persona![`_choice_personas`] Persona to validate
# @alias validate_persona
validate-persona() {
  jq -f scripts/jq/schema-validation/transform.jq --arg schema '{"required":["id","name","core_traits","voice"],"types":{"id":"string","name":"string","core_traits":"object","voice":"object"}}' "${PERSONA_DIR}/${argc_persona}.json"
}

# 📖 Chronicle inscriptions
# @cmd 🔮 List them books yao
# @option --filter="" <FILTER> Filter books by name pattern
# @alias list_books
list-books() {
  _choice_books >>"$LLM_OUTPUT"
}

# 📖 Chronicle inscriptions
# @cmd 🔮 Show them books yao
# @option --format[=json|yaml] Output format
# @arg book[`_choice_books`] Book to show (omit to list all)
# @alias show_book
show-book() {
  [[ -z "$argc_book" ]] && _choice_books && return
  [[ "${argc_format:-json}" == "yaml" ]] && json2yaml <"${BOOKS_DIR}/${argc_book}.json" || cat "${BOOKS_DIR}/${argc_book}.json"
}

# 📖 Chronicle inscriptions
# @cmd 🔮 List them entries yao
# @alias list_entries
list-entries() {
  _choice_entries >>"$LLM_OUTPUT"
}

# 📖 Chronicle inscriptions
# @cmd 🔮 Show them entries yao
# @option --format[=json|yaml] Output format
# @arg entry[`_choice_entries`] Entry to show (omit to list all)
# @alias show_entry
show-entry() {
  [[ -z "$argc_entry" ]] && _choice_entries && return
  [[ "${argc_format:-json}" == "yaml" ]] && json2yaml <"${ENTRIES_DIR}/${argc_entry}.json" || cat "${ENTRIES_DIR}/${argc_entry}.json"
}

# 📖 Chronicle inscriptions
# @cmd 🔮 Read all entries in a book yao
# @option --format[=json|yaml] Output format
# @arg book![`_choice_books`] Book to read entries from
# @alias read_book_entries
read-book-entries() {
  jq -r '.entries[]' "${BOOKS_DIR}/${argc_book}.json" | while read entry_id; do
    [[ -f "${ENTRIES_DIR}/${entry_id}.json" ]] || continue
    [[ "${argc_format:-json}" == "yaml" ]] && json2yaml <"${ENTRIES_DIR}/${entry_id}.json" || cat "${ENTRIES_DIR}/${entry_id}.json"
    echo "---"
  done
}

_choice_books() { basename -s .json "${BOOKS_DIR}"/*.json; }
_choice_entries() { basename -s .json "${ENTRIES_DIR}"/*.json; }
_choice_personas() { basename -s .json "${PERSONA_DIR}"/*.json; }

_choice_categories() { echo -e "character\nplace\nevent\nobject\nconcept\ncustom"; }

# 📖 Chronicle inscriptions
# @cmd 🔮 Create new entry yao
# @option --title! <TITLE> Entry title
# @option --category![`_choice_categories`] Entry category
# @alias create_entry
create-entry() {
  local entry_id="entry_$(date +%s)_$(openssl rand -hex 4)"
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  cat >"${ENTRIES_DIR}/${entry_id}.json" <<EOF
{
  "id": "${entry_id}",
  "title": "${argc_title}",
  "content": "",
  "summary": "",
  "category": "${argc_category}",
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

  echo "Created: ${entry_id}" >>"$LLM_OUTPUT"
}

# 📖 Chronicle inscriptions
# @cmd 🔮 Create new book yao
# @option --title! <TITLE> Book title
# @option --description="" <DESC> Book description
# @alias create_book
create-book() {
  local book_id="book_$(date +%s)_$(openssl rand -hex 4)"
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  cat >"${BOOKS_DIR}/${book_id}.json" <<EOF
{
  "id": "${book_id}",
  "title": "${argc_title}",
  "description": "${argc_description}",
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

  echo "Created: ${book_id}" >>"$LLM_OUTPUT"
}

# 📖 Chronicle inscriptions
# @cmd 🔮 Add entry to book yao
# @option --entry![`_choice_entries`] Entry to add
# @option --book![`_choice_books`] Book to add to
# @alias add_to_book
add-to-book() {
  local book_file="${BOOKS_DIR}/${argc_book}.json"

  jq ".entries += [\"${argc_entry}\"]" "$book_file" >"${book_file}.tmp" && mv "${book_file}.tmp" "$book_file"
  echo "Added ${argc_entry} to ${argc_book}" >>"$LLM_OUTPUT"
}

# 📖 Chronicle inscriptions
# @cmd 🔮 Link book to persona yao
# @option --book![`_choice_books`] Book to link
# @option --persona![`_choice_personas`] Persona to link to
# @alias link_to_persona
link-to-persona() {
  local book_file="${BOOKS_DIR}/${argc_book}.json"
  local persona_file="${PERSONA_DIR}/${argc_persona}.json"

  jq ".readers += [\"${argc_persona}\"]" "$book_file" >"${book_file}.tmp" && mv "${book_file}.tmp" "$book_file"
  jq ".knowledge.lore_books += [\"${argc_book}\"]" "$persona_file" >"${persona_file}.tmp" && mv "${persona_file}.tmp" "$persona_file"

  echo "Linked ${argc_book} to ${argc_persona}" >>"$LLM_OUTPUT"
}

# The sacred argc incantation line - must remain at the end!
eval "$(argc --argc-eval "$0" "$@")"
