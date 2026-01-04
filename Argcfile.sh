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
# @env PERSONA_DIR=/home/skogix/lore/knowledge/expanded/personas path to yo persona!
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
  for book_file in "${BOOKS_DIR}"/*.json; do
    [[ ! -f "$book_file" ]] && continue
    local book_id=$(basename "$book_file" .json)

    local title=$(jq -r '.title // "Untitled"' "$book_file")
    local description=$(jq -r '.description // ""' "$book_file" | head -c 80)
    local entry_count=$(jq -r '.entries | length' "$book_file")
    local status=$(jq -r '.metadata.status // "unknown"' "$book_file")

    # Apply filter if provided (check both id and title)
    if [[ -n "$argc_filter" ]]; then
      if [[ ! "$book_id" =~ $argc_filter ]] && [[ ! "$title" =~ $argc_filter ]]; then
        continue
      fi
    fi

    printf "%-30s %-40s [%2d entries] [%s]\n" "$book_id" "$title" "$entry_count" "$status"
  done >>"$LLM_OUTPUT"
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
# @option --filter="" <FILTER> Filter entries by title/id pattern
# @option --category[`_choice_categories`] Filter by category
# @alias list_entries
list-entries() {
  for entry_file in "${ENTRIES_DIR}"/*.json; do
    [[ ! -f "$entry_file" ]] && continue
    local entry_id=$(basename "$entry_file" .json)

    # Apply filter if provided
    if [[ -n "$argc_filter" ]] && [[ ! "$entry_id" =~ $argc_filter ]]; then
      local title=$(jq -r '.title // ""' "$entry_file")
      [[ ! "$title" =~ $argc_filter ]] && continue
    fi

    # Apply category filter if provided
    if [[ -n "$argc_category" ]]; then
      local cat=$(jq -r '.category // ""' "$entry_file")
      [[ "$cat" != "$argc_category" ]] && continue
    fi

    local title=$(jq -r '.title // "Untitled"' "$entry_file")
    local category=$(jq -r '.category // "unknown"' "$entry_file")
    local tags=$(jq -r '.tags | if . then join(", ") else "" end' "$entry_file" | head -c 30)
    local book_id=$(jq -r '.book_id // "unlinked"' "$entry_file")

    printf "%-35s %-35s [%-10s] [%-20s] %s\n" "$entry_id" "$title" "$category" "$book_id" "$tags"
  done >>"$LLM_OUTPUT"
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

# ============================================================================
# 🔮 STRUCTURED IO - Choice Functions for Input Validation
# ============================================================================

# Document file discovery - finds markdown files for lore generation
_choice_doc_files() {
  find "${MYSTICAL_SANCTUM}/docs" "${MYSTICAL_SANCTUM}/knowledge" \
    -type f -name "*.md" 2>/dev/null | \
    sed "s|^${MYSTICAL_SANCTUM}/||" | sort
}

# Document directory discovery
_choice_doc_dirs() {
  find "${MYSTICAL_SANCTUM}" -maxdepth 3 -type d \
    -exec sh -c 'ls "$1"/*.md >/dev/null 2>&1' _ {} \; \
    -print 2>/dev/null | \
    sed "s|^${MYSTICAL_SANCTUM}/||" | sort
}

# Git commit discovery - recent commits
_choice_git_commits() {
  git log --oneline -50 --format="%h" 2>/dev/null
}

# Git reference discovery - branches, tags, HEAD refs
_choice_git_refs() {
  {
    git branch --list --format='%(refname:short)' 2>/dev/null
    git tag --list 2>/dev/null
    echo "HEAD"
    echo "HEAD~1"
    echo "HEAD~5"
    echo "HEAD~10"
  } | sort -u
}

# Queue item discovery
_choice_queue_items() {
  local queue_dir="${MYSTICAL_SANCTUM}/.lore-queue"
  [[ -d "$queue_dir" ]] && basename -s .json "$queue_dir"/*.json 2>/dev/null
}

# Queue input types
_choice_queue_types() {
  echo -e "doc\ngit\nmanual"
}

# Queue statuses
_choice_queue_statuses() {
  echo -e "pending\nprocessing\ndone\nfailed\nall"
}

# Priority levels
_choice_priorities() {
  echo -e "normal\nhigh\nlow"
}

# ============================================================================
# 🛡️ VALIDATION FUNCTIONS - Structured IO Pre-flight Checks
# ============================================================================

# Validate path exists and return resolved path
# Usage: _validate_path "/path/to/file" "file|dir|any"
_validate_path() {
  local path="$1"
  local type="${2:-file}"

  # Resolve relative paths
  [[ "$path" != /* ]] && path="${MYSTICAL_SANCTUM}/$path"

  case "$type" in
    file)
      [[ -f "$path" ]] || { echo "ERROR: File not found: $path" >&2; return 1; }
      ;;
    dir)
      [[ -d "$path" ]] || { echo "ERROR: Directory not found: $path" >&2; return 1; }
      ;;
    any)
      [[ -e "$path" ]] || { echo "ERROR: Path not found: $path" >&2; return 1; }
      ;;
  esac

  echo "$path"
}

# Validate content meets requirements
# Usage: _validate_content "$content" min_words max_words
_validate_content() {
  local content="$1"
  local min_words="${2:-10}"
  local max_words="${3:-10000}"

  local word_count
  word_count=$(echo "$content" | wc -w | tr -d ' ')

  if [[ "$word_count" -lt "$min_words" ]]; then
    echo "ERROR: Content too short ($word_count words, minimum $min_words)" >&2
    return 1
  fi

  if [[ "$word_count" -gt "$max_words" ]]; then
    echo "ERROR: Content too long ($word_count words, maximum $max_words)" >&2
    return 1
  fi

  return 0
}

# Validate LLM-generated lore output
# Usage: _validate_lore_output "$content"
_validate_lore_output() {
  local content="$1"
  local errors=()

  # Check for meta-commentary (LLM preambles)
  if echo "$content" | head -n 1 | \
     grep -qiE '^[[:space:]]*(I will|Let me|Here is|This entry|I need|should I|First,? I|Certainly|Of course)'; then
    errors+=("Contains meta-commentary in first line")
  fi

  # Check word count
  local word_count
  word_count=$(echo "$content" | wc -w | tr -d ' ')
  if [[ "$word_count" -lt 50 ]]; then
    errors+=("Too short ($word_count words, recommended 50+)")
  fi

  if [[ ${#errors[@]} -gt 0 ]]; then
    printf 'WARN: %s\n' "${errors[@]}" >&2
    return 1
  fi

  return 0
}

# Strip meta-commentary from LLM output
_strip_meta_commentary() {
  local content="$1"

  if echo "$content" | head -n 1 | \
     grep -qiE '^[[:space:]]*(I will|Let me|Here is|This entry|I need|should I|First,? I|Certainly|Of course)'; then
    echo "$content" | tail -n +2
  else
    echo "$content"
  fi
}

# ============================================================================
# 🌀 GENERATE NAMESPACE - LLM-powered lore generation
# ============================================================================

readonly QUEUE_DIR="${MYSTICAL_SANCTUM}/.lore-queue"

# @cmd 📜 Generate lore from markdown documents
# @option --path![`_choice_doc_files`] <PATH>   Markdown file to process
# @option --category[`_choice_categories`]      Category for entry (default: concept)
# @option --book[`_choice_books`]               Add entry to this book
# @flag --dry-run                               Preview without creating entry
# @env LLM_PROVIDER=ollama                      LLM provider (ollama|claude|openai)
# @env LLM_MODEL=llama3.2                       Model name
# @alias gen-docs
generate-from-docs() {
  local resolved_path
  resolved_path=$(_validate_path "$argc_path" "file") || return 1

  local content
  content=$(cat "$resolved_path")

  _validate_content "$content" 20 5000 || return 1

  local title
  title=$(basename "$resolved_path" .md | tr '_-' ' ')

  local category="${argc_category:-concept}"
  if head -10 "$resolved_path" | grep -q '^category:'; then
    category=$(head -10 "$resolved_path" | grep '^category:' | cut -d: -f2 | tr -d ' ')
  fi

  _generate_lore_entry "$content" "$title" "$category"
}

# @cmd 📜 Generate lore from git commit
# @arg commit[`_choice_git_refs`]               Commit reference (default: HEAD)
# @option --category=event                      Category for entry
# @option --persona[`_choice_personas`]         Narrator persona
# @option --book[`_choice_books`]               Add entry to this book
# @flag --dry-run                               Preview without creating entry
# @env LLM_PROVIDER=ollama                      LLM provider
# @alias gen-git
generate-from-git() {
  local commit="${argc_commit:-HEAD}"

  if ! git rev-parse --verify "$commit" >/dev/null 2>&1; then
    echo "ERROR: Invalid commit reference: $commit" >&2
    return 1
  fi

  local diff_content
  diff_content=$(git show "$commit" --format="Commit: %H%nAuthor: %an%nDate: %ai%nMessage: %s%n%n%b" --stat)

  _validate_content "$diff_content" 5 || return 1

  local commit_msg
  commit_msg=$(git log -1 --format='%s' "$commit")

  _generate_lore_entry "$diff_content" "$commit_msg" "${argc_category:-event}"
}

# @cmd 📜 Generate lore from stdin (pipe content)
# @option --title! <TITLE>                      Entry title
# @option --category![`_choice_categories`]     Category for entry
# @option --book[`_choice_books`]               Add entry to this book
# @flag --dry-run                               Preview without creating entry
# @env LLM_PROVIDER=ollama                      LLM provider
# @alias gen-stdin
generate-from-stdin() {
  local content
  content=$(cat -)

  _validate_content "$content" 10 10000 || return 1

  _generate_lore_entry "$content" "$argc_title" "$argc_category"
}

_generate_lore_entry() {
  local content="$1"
  local title="$2"
  local category="$3"

  if [[ -n "$argc_dry_run" ]]; then
    echo "DRY RUN: Would create entry '$title' ($category)" >&2
    echo "Content length: $(echo "$content" | wc -w | tr -d ' ') words" >&2
    echo "---" >&2
    echo "$content" | head -c 500
    echo "..." >&2
    return 0
  fi

  local lore_content
  if [[ -x "${LORE_SCRIPTS}/llama-lore-integrator.sh" ]]; then
    local temp_file
    temp_file=$(mktemp)
    echo "$content" > "$temp_file"
    lore_content=$("${LORE_SCRIPTS}/llama-lore-integrator.sh" \
      "${LLM_MODEL:-llama3.2}" extract-lore "$temp_file" lore 2>/dev/null) || lore_content=""
    rm -f "$temp_file"
  fi

  if [[ -z "$lore_content" ]]; then
    echo "WARN: LLM extraction failed, using raw content" >&2
    lore_content="$content"
  fi

  if ! _validate_lore_output "$lore_content"; then
    lore_content=$(_strip_meta_commentary "$lore_content")
  fi

  local entry_id="entry_$(date +%s)_$(openssl rand -hex 4)"
  jq -n \
    --arg id "$entry_id" \
    --arg title "$title" \
    --arg content "$lore_content" \
    --arg category "$category" \
    --arg summary "Generated from ${argc_path:-input}" \
    --arg timestamp "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
    --arg creator "$(whoami)" \
    '{
      id: $id,
      title: $title,
      content: $content,
      summary: $summary,
      category: $category,
      tags: ["generated", "automated"],
      relationships: [],
      attributes: {},
      metadata: {
        created_by: $creator,
        created_at: $timestamp,
        updated_at: $timestamp,
        version: "1.0",
        canonical: true
      },
      visibility: { public: true, restricted_to: [] }
    }' > "${ENTRIES_DIR}/${entry_id}.json"

  echo "Created: $entry_id"

  if [[ -n "$argc_book" ]]; then
    argc_entry="$entry_id" add-to-book
  fi
}

# ============================================================================
# 📋 QUEUE NAMESPACE - Async lore generation queue
# ============================================================================

# @cmd 📋 Add item to generation queue
# @option --type![`_choice_queue_types`] <TYPE>       Input type (doc|git|manual)
# @option --input! <INPUT>                            Input path or content
# @option --category[`_choice_categories`]            Category for entry
# @option --priority[`_choice_priorities`]            Processing priority (default: normal)
# @alias q-add
queue-add() {
  mkdir -p "$QUEUE_DIR"

  local queue_id="queue_$(date +%s)_$(openssl rand -hex 4)"
  local timestamp
  timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  if [[ "$argc_type" == "doc" ]]; then
    _validate_path "$argc_input" "file" >/dev/null || return 1
  elif [[ "$argc_type" == "git" ]]; then
    git rev-parse --verify "$argc_input" >/dev/null 2>&1 || {
      echo "ERROR: Invalid git reference: $argc_input" >&2
      return 1
    }
  fi

  jq -n \
    --arg id "$queue_id" \
    --arg type "$argc_type" \
    --arg input "$argc_input" \
    --arg category "${argc_category:-}" \
    --arg priority "${argc_priority:-normal}" \
    --arg created "$timestamp" \
    '{
      id: $id,
      type: $type,
      input: $input,
      category: (if $category == "" then null else $category end),
      priority: $priority,
      created_at: $created,
      status: "pending"
    }' > "${QUEUE_DIR}/${queue_id}.json"

  echo "Queued: $queue_id (${argc_type}: ${argc_input})"
}

# @cmd 📋 List queued items
# @option --status[`_choice_queue_statuses`]          Filter by status
# @option --format[=table|json]                       Output format
# @alias q-list
queue-list() {
  [[ ! -d "$QUEUE_DIR" ]] && { echo "Queue empty" >&2; return 0; }

  local found=0
  for item in "${QUEUE_DIR}"/*.json; do
    [[ -f "$item" ]] || continue
    found=1

    if [[ -n "$argc_status" ]] && [[ "$argc_status" != "all" ]]; then
      local status
      status=$(jq -r '.status' "$item")
      [[ "$status" != "$argc_status" ]] && continue
    fi

    if [[ "${argc_format:-table}" == "json" ]]; then
      cat "$item"
      echo ""
    else
      local id type input created status priority
      id=$(jq -r '.id' "$item")
      type=$(jq -r '.type' "$item")
      input=$(jq -r '.input' "$item" | head -c 35)
      created=$(jq -r '.created_at' "$item" | cut -dT -f1)
      status=$(jq -r '.status' "$item")
      priority=$(jq -r '.priority' "$item")
      printf "%-28s %-6s %-35s %-12s %-8s [%s]\n" "$id" "$type" "$input" "$created" "$priority" "$status"
    fi
  done

  [[ $found -eq 0 ]] && echo "Queue empty" >&2
}

# @cmd 📋 Process queued items
# @flag --all                                         Process all pending items
# @option --limit=1 <N>                               Number of items to process
# @alias q-process
queue-process() {
  [[ ! -d "$QUEUE_DIR" ]] && { echo "Queue empty" >&2; return 0; }

  local limit="${argc_limit:-1}"
  [[ -n "$argc_all" ]] && limit=9999

  local processed=0
  for item in "${QUEUE_DIR}"/*.json; do
    [[ -f "$item" ]] || continue
    [[ "$processed" -ge "$limit" ]] && break

    local status
    status=$(jq -r '.status' "$item")
    [[ "$status" != "pending" ]] && continue

    _process_queue_item "$item"
    ((processed++))
  done

  echo "Processed $processed item(s)" >&2
}

# @cmd 📋 Clear queue
# @flag --force                                       Skip confirmation
# @option --status[`_choice_queue_statuses`]          Only clear items with this status
# @alias q-clear
queue-clear() {
  [[ ! -d "$QUEUE_DIR" ]] && { echo "Queue empty" >&2; return 0; }

  local count
  count=$(ls -1 "${QUEUE_DIR}"/*.json 2>/dev/null | wc -l | tr -d ' ')

  if [[ "$argc_force" != "1" ]]; then
    echo "This will delete $count queue item(s). Use --force to confirm." >&2
    return 1
  fi

  local cleared=0
  for item in "${QUEUE_DIR}"/*.json; do
    [[ -f "$item" ]] || continue

    if [[ -n "$argc_status" ]] && [[ "$argc_status" != "all" ]]; then
      local status
      status=$(jq -r '.status' "$item")
      [[ "$status" != "$argc_status" ]] && continue
    fi

    rm "$item"
    ((cleared++))
  done

  echo "Cleared $cleared item(s)"
}

_process_queue_item() {
  local item_file="$1"
  local id type input category

  id=$(jq -r '.id' "$item_file")
  type=$(jq -r '.type' "$item_file")
  input=$(jq -r '.input' "$item_file")
  category=$(jq -r '.category // "concept"' "$item_file")

  echo "Processing: $id ($type)" >&2

  jq '.status = "processing"' "$item_file" > "${item_file}.tmp"
  mv "${item_file}.tmp" "$item_file"

  local result=0
  case "$type" in
    doc)
      argc_path="$input" argc_category="$category" argc_dry_run="" generate-from-docs || result=1
      ;;
    git)
      argc_commit="$input" argc_category="$category" argc_dry_run="" generate-from-git || result=1
      ;;
    manual)
      echo "$input" | argc_title="Queued Entry $(date +%s)" argc_category="$category" argc_dry_run="" generate-from-stdin || result=1
      ;;
  esac

  if [[ $result -eq 0 ]]; then
    jq '.status = "done"' "$item_file" > "${item_file}.tmp"
  else
    jq '.status = "failed"' "$item_file" > "${item_file}.tmp"
  fi
  mv "${item_file}.tmp" "$item_file"
}

# 📖 Chronicle inscriptions
# @cmd 🔮 Create new entry yao
# @option --title! <TITLE> Entry title
# @option --category![`_choice_categories`] Entry category
# @alias create_entry
create-entry() {
  local entry_id="entry_$(date +%s)_$(openssl rand -hex 4)"
  jq -f scripts/jq/create-entry/transform.jq \
    --arg id "$entry_id" \
    --arg title "$argc_title" \
    --arg category "$argc_category" \
    --arg timestamp "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
    --arg creator "$(whoami)" \
    --null-input \
    > "${ENTRIES_DIR}/${entry_id}.json" && echo "Created: ${entry_id}" >>"$LLM_OUTPUT"
}

# 📖 Chronicle inscriptions
# @cmd 🔮 Create new book yao
# @option --title! <TITLE> Book title
# @option --description="" <DESC> Book description
# @alias create_book
create-book() {
  local book_id="book_$(date +%s)_$(openssl rand -hex 4)"
  jq -f scripts/jq/create-book/transform.jq \
    --arg id "$book_id" \
    --arg title "$argc_title" \
    --arg description "$argc_description" \
    --arg timestamp "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
    --arg creator "$(whoami)" \
    --null-input \
    > "${BOOKS_DIR}/${book_id}.json" && echo "Created: ${book_id}" >>"$LLM_OUTPUT"
}

# 📖 Chronicle inscriptions
# @cmd 🔮 Create new persona yao
# @option --name! <NAME> Persona name
# @option --voice-tone="neutral" <TONE> Voice tone
# @alias create_persona
create-persona() {
  local persona_id="persona_$(date +%s)"
  jq -f scripts/jq/create-persona/transform.jq \
    --arg id "$persona_id" \
    --arg name "$argc_name" \
    --arg voice_tone "$argc_voice_tone" \
    --arg timestamp "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
    --null-input \
    > "${PERSONA_DIR}/${persona_id}.json" && echo "Created: ${persona_id}" >>"$LLM_OUTPUT"
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
