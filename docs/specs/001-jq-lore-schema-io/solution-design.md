# Solution Design Document: jq-based Lore Schema I/O

**Specification ID:** 001
**Feature Name:** jq-lore-schema-io
**Status:** Draft
**Created:** 2025-12-13
**Last Updated:** 2025-12-13

---

## Executive Summary

This document describes the technical architecture for implementing argc commands in Argcfile.sh that validate and manipulate lore JSON files using atomic jq transformations. The solution leverages existing jq CRUD operations from @scripts/jq/ and adds schema validation capabilities.

### Design Goals

1. **Reusability:** Build on existing jq transformations (crud-get, crud-set, crud-has)
2. **Simplicity:** Keep argc commands simple and composable
3. **Validation:** Ensure schema compliance before writing data
4. **Maintainability:** Follow existing patterns in Argcfile.sh and @scripts/jq/

---

## Architecture Overview

### Component Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Argcfile.sh                           │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  argc Commands (new validation commands)       │    │
│  │  - validate-entry                              │    │
│  │  - validate-book                               │    │
│  │  - validate-persona                            │    │
│  │  - safe-set-field                              │    │
│  │  - add-to-array                                │    │
│  └─────────────────┬──────────────────────────────┘    │
│                    │                                     │
│  ┌─────────────────▼──────────────────────────────┐    │
│  │  Helper Functions (validation logic)           │    │
│  │  - _validate_required_fields                   │    │
│  │  - _validate_field_type                        │    │
│  │  - _validate_enum                              │    │
│  └─────────────────┬──────────────────────────────┘    │
└────────────────────┼──────────────────────────────────┘
                     │
         ┌───────────┴──────────────┐
         │                          │
         ▼                          ▼
┌─────────────────┐        ┌──────────────────┐
│  scripts/jq/    │        │  knowledge/core/ │
│  - crud-get     │        │  - schema.json   │
│  - crud-set     │        │  - book-schema   │
│  - crud-has     │        │  - persona/      │
│  - array-*      │        │    schema.json   │
└─────────────────┘        └──────────────────┘
```

### Data Flow

```
User Command
    │
    ▼
argc Command (Argcfile.sh)
    │
    ├─► Read JSON file
    │
    ├─► Validate using helper functions + jq
    │   │
    │   ├─► Check required fields (crud-has)
    │   ├─► Check field types (jq type checks)
    │   └─► Check enum values (jq contains checks)
    │
    ├─► If valid: Apply transformation (crud-set, array-filter, etc.)
    │
    └─► Write JSON file OR Return error
```

---

## Design Decisions

### Decision 1: Validation in Bash vs Pure jq

**Options Considered:**
1. Pure jq validation transformations (separate .jq files)
2. Bash helper functions that call jq commands
3. Hybrid: bash orchestration + jq for actual checks

**Decision:** Hybrid approach (bash helpers + jq)

**Rationale:**
- argc commands are already bash functions in Argcfile.sh
- Schema files are JSON, easier to read with bash + jq than pure jq
- Allows readable error messages from bash
- Can compose existing jq transformations
- Simpler to test and maintain

### Decision 2: Schema Storage Location

**Options Considered:**
1. Hardcode schema paths in Argcfile.sh
2. Use environment variables
3. Derive from existing directory structure

**Decision:** Hardcode relative paths from MYSTICAL_SANCTUM

**Rationale:**
- Schemas are in fixed locations (knowledge/core/)
- MYSTICAL_SANCTUM already provides repo root
- No need for additional env vars
- Clear and explicit

### Decision 3: Error Handling Strategy

**Options Considered:**
1. Silent failures (return empty/null)
2. Exit on error (set -e)
3. Return error codes with messages to stderr

**Decision:** Return error codes with messages to stderr

**Rationale:**
- Allows calling code to decide how to handle errors
- Preserves existing argc error handling patterns
- Users get clear feedback about validation failures
- Doesn't break existing commands

### Decision 4: Validation Scope

**Options Considered:**
1. Full JSON Schema validation (recursive, all constraints)
2. Minimal validation (required fields + types)
3. Progressive validation (required now, expand later)

**Decision:** Minimal validation (required fields, types, enums)

**Rationale:**
- Sufficient to prevent most invalid data
- Simpler to implement and maintain
- Faster execution
- Can expand later if needed
- Matches stated requirements

---

## Component Design

### 1. Schema Validation Helper Functions

Located in Argcfile.sh, these bash functions provide validation logic:

#### `_validate_required_fields()`

**Purpose:** Check that all required fields exist in JSON object

**Signature:**
```bash
_validate_required_fields <json_file> <field1> <field2> ...
# Returns: 0 if all fields exist, 1 otherwise
```

**Implementation Approach:**
```bash
_validate_required_fields() {
  local json_file="$1"
  shift
  local required_fields=("$@")

  for field in "${required_fields[@]}"; do
    if ! jq -e "has(\"$field\")" "$json_file" >/dev/null 2>&1; then
      echo "Error: Missing required field: $field" >&2
      return 1
    fi
  done
  return 0
}
```

Uses: `jq -e has()` to check field existence

#### `_validate_field_type()`

**Purpose:** Check that field has expected type

**Signature:**
```bash
_validate_field_type <json_file> <field_path> <expected_type>
# Returns: 0 if type matches, 1 otherwise
# expected_type: string, number, boolean, array, object, null
```

**Implementation Approach:**
```bash
_validate_field_type() {
  local json_file="$1"
  local field_path="$2"
  local expected_type="$3"

  local actual_type=$(jq -r ".$field_path | type" "$json_file" 2>/dev/null)

  if [[ "$actual_type" != "$expected_type" ]]; then
    echo "Error: Field '$field_path' must be $expected_type, got $actual_type" >&2
    return 1
  fi
  return 0
}
```

Uses: `jq type` builtin

#### `_validate_enum()`

**Purpose:** Check that field value is in allowed enum list

**Signature:**
```bash
_validate_enum <json_file> <field_path> <allowed_value1> <allowed_value2> ...
# Returns: 0 if value is allowed, 1 otherwise
```

**Implementation Approach:**
```bash
_validate_enum() {
  local json_file="$1"
  local field_path="$2"
  shift 2
  local allowed_values=("$@")

  local actual_value=$(jq -r ".$field_path" "$json_file" 2>/dev/null)

  for allowed in "${allowed_values[@]}"; do
    if [[ "$actual_value" == "$allowed" ]]; then
      return 0
    fi
  done

  echo "Error: Field '$field_path' must be one of: ${allowed_values[*]}, got '$actual_value'" >&2
  return 1
}
```

Uses: bash array iteration and comparison

---

### 2. argc Validation Commands

#### `validate-entry`

**Purpose:** Validate lore entry against schema.json

**argc Signature:**
```bash
# @cmd 🔮 Validate a lore entry against schema
# @arg entry_file! Path to entry JSON file
validate-entry() {
  local entry_file="$argc_entry_file"

  # Check required fields
  _validate_required_fields "$entry_file" "id" "title" "content" "category" || return 1

  # Check types
  _validate_field_type "$entry_file" "id" "string" || return 1
  _validate_field_type "$entry_file" "title" "string" || return 1
  _validate_field_type "$entry_file" "content" "string" || return 1
  _validate_field_type "$entry_file" "category" "string" || return 1

  # Check category enum
  _validate_enum "$entry_file" "category" "character" "place" "event" "object" "concept" "custom" || return 1

  # Optional: check tags is array if present
  if jq -e 'has("tags")' "$entry_file" >/dev/null 2>&1; then
    _validate_field_type "$entry_file" "tags" "array" || return 1
  fi

  echo "✓ Entry is valid" >&2
  return 0
}
```

**Data Flow:**
1. Read entry file path from argc parameter
2. Check required fields exist
3. Check field types match schema
4. Check enum values are valid
5. Check optional fields if present
6. Return success/failure

#### `validate-book`

**Purpose:** Validate lore book against book-schema.json

**argc Signature:**
```bash
# @cmd 🔮 Validate a lore book against schema
# @arg book_file! Path to book JSON file
validate-book() {
  local book_file="$argc_book_file"

  # Check required fields
  _validate_required_fields "$book_file" "id" "title" "description" || return 1

  # Check types
  _validate_field_type "$book_file" "id" "string" || return 1
  _validate_field_type "$book_file" "title" "string" || return 1
  _validate_field_type "$book_file" "description" "string" || return 1

  # Check optional arrays
  if jq -e 'has("entries")' "$book_file" >/dev/null 2>&1; then
    _validate_field_type "$book_file" "entries" "array" || return 1
  fi

  # Check status enum if present
  if jq -e 'has("metadata") and .metadata | has("status")' "$book_file" >/dev/null 2>&1; then
    _validate_enum "$book_file" "metadata.status" "draft" "active" "archived" "deprecated" || return 1
  fi

  echo "✓ Book is valid" >&2
  return 0
}
```

#### `validate-persona`

**Purpose:** Validate persona against persona/schema.json

**argc Signature:**
```bash
# @cmd 🔮 Validate a persona against schema
# @arg persona_file! Path to persona JSON file
validate-persona() {
  local persona_file="$argc_persona_file"

  # Check required fields
  _validate_required_fields "$persona_file" "id" "name" "core_traits" "voice" || return 1

  # Check types
  _validate_field_type "$persona_file" "id" "string" || return 1
  _validate_field_type "$persona_file" "name" "string" || return 1
  _validate_field_type "$persona_file" "core_traits" "object" || return 1
  _validate_field_type "$persona_file" "voice" "object" || return 1

  # Check nested required fields in core_traits
  if ! jq -e '.core_traits | has("temperament") and has("values") and has("motivations")' "$persona_file" >/dev/null 2>&1; then
    echo "Error: core_traits must have temperament, values, and motivations" >&2
    return 1
  fi

  # Check nested required fields in voice
  if ! jq -e '.voice | has("tone") and has("patterns") and has("vocabulary")' "$persona_file" >/dev/null 2>&1; then
    echo "Error: voice must have tone, patterns, and vocabulary" >&2
    return 1
  fi

  echo "✓ Persona is valid" >&2
  return 0
}
```

---

### 3. Safe Update Commands

#### `safe-set-field`

**Purpose:** Set field value with automatic validation and timestamp update

**argc Signature:**
```bash
# @cmd 🔮 Safely set a field value with validation
# @arg file! Path to JSON file
# @arg path! Dot-separated path to field (e.g., "title" or "metadata.version")
# @arg value! New value to set
# @option --type[=string|number|boolean] Expected type (default: string)
safe-set-field() {
  local file="$argc_file"
  local path="$argc_path"
  local value="$argc_value"
  local expected_type="${argc_type:-string}"

  # Determine file type (entry, book, persona) from file path
  local file_type=""
  if [[ "$file" == *"/entries/"* ]]; then
    file_type="entry"
  elif [[ "$file" == *"/books/"* ]]; then
    file_type="book"
  elif [[ "$file" == *"/personas/"* ]]; then
    file_type="persona"
  else
    echo "Error: Cannot determine file type from path" >&2
    return 1
  fi

  # Create temporary file with updated value
  local tmp_file="${file}.tmp"
  jq -f "$MYSTICAL_SANCTUM/scripts/jq/crud-set/transform.jq" \
    --arg path "$path" \
    --arg value "$value" \
    "$file" > "$tmp_file"

  # Update timestamp based on file type
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  if [[ "$file_type" == "entry" ]] || [[ "$file_type" == "book" ]]; then
    jq --arg ts "$timestamp" '.metadata.updated_at = $ts' "$tmp_file" > "${tmp_file}.2"
    mv "${tmp_file}.2" "$tmp_file"
  elif [[ "$file_type" == "persona" ]]; then
    jq --arg ts "$timestamp" '.meta.modified = $ts' "$tmp_file" > "${tmp_file}.2"
    mv "${tmp_file}.2" "$tmp_file"
  fi

  # Validate the result
  case "$file_type" in
    entry)
      validate-entry "$tmp_file" || { rm "$tmp_file"; return 1; }
      ;;
    book)
      validate-book "$tmp_file" || { rm "$tmp_file"; return 1; }
      ;;
    persona)
      validate-persona "$tmp_file" || { rm "$tmp_file"; return 1; }
      ;;
  esac

  # If valid, replace original file
  mv "$tmp_file" "$file"
  echo "✓ Field updated successfully" >&2
  return 0
}
```

**Data Flow:**
1. Determine file type from path
2. Apply crud-set transformation to update field
3. Update appropriate timestamp field
4. Validate result against schema
5. If valid, replace original file
6. If invalid, remove temp file and return error

#### `add-to-array`

**Purpose:** Add item to array field with duplicate prevention

**argc Signature:**
```bash
# @cmd 🔮 Add item to array field (no duplicates)
# @arg file! Path to JSON file
# @arg path! Dot-separated path to array field (e.g., "tags" or "entries")
# @arg value! Value to add
add-to-array() {
  local file="$argc_file"
  local path="$argc_path"
  local value="$argc_value"

  # Check if value already exists in array
  if jq -e --arg path "$path" --arg val "$value" \
    '(getpath($path | split(".")) // []) | contains([$val])' \
    "$file" >/dev/null 2>&1; then
    echo "✓ Value already in array, skipping" >&2
    return 0
  fi

  # Add to array using jq
  local tmp_file="${file}.tmp"
  jq --arg path "$path" --arg val "$value" \
    '(($path | split(".")) as $keys |
      if getpath($keys) | type == "array" then
        setpath($keys; getpath($keys) + [$val])
      else
        setpath($keys; [$val])
      end)' \
    "$file" > "$tmp_file"

  # Update timestamp
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  if jq -e 'has("metadata")' "$tmp_file" >/dev/null 2>&1; then
    jq --arg ts "$timestamp" '.metadata.updated_at = $ts' "$tmp_file" > "${tmp_file}.2"
    mv "${tmp_file}.2" "$tmp_file"
  fi

  mv "$tmp_file" "$file"
  echo "✓ Added to array" >&2
  return 0
}
```

**Data Flow:**
1. Check if value already in array (prevent duplicates)
2. If not present, add to array using jq
3. Update timestamp if metadata exists
4. Replace original file

---

## Integration Points

### Integration with Existing Commands

Current Argcfile.sh commands will be updated to use validation:

**Before:**
```bash
create-entry() {
  local entry_id="entry_$(date +%s)_$(openssl rand -hex 4)"
  # ... create JSON ...
  echo "$json" > "${ENTRIES_DIR}/${entry_id}.json"
}
```

**After:**
```bash
create-entry() {
  local entry_id="entry_$(date +%s)_$(openssl rand -hex 4)"
  local tmp_file="/tmp/${entry_id}.json"
  # ... create JSON ...
  echo "$json" > "$tmp_file"

  # Validate before writing
  if validate-entry "$tmp_file"; then
    mv "$tmp_file" "${ENTRIES_DIR}/${entry_id}.json"
    echo "Created: ${entry_id}" >>"$LLM_OUTPUT"
  else
    rm "$tmp_file"
    echo "Error: Entry validation failed" >&2
    return 1
  fi
}
```

### Integration with jq Transformations

New commands use existing transformations as building blocks:

- **crud-get**: Used in validation helpers to check field existence and values
- **crud-set**: Used in safe-set-field to update values
- **crud-has**: Used in _validate_required_fields to check field existence
- **array-filter**: Could be used for relationship validation (future)

No modifications to existing jq transformations needed.

---

## Error Handling

### Error Categories

1. **Validation Errors:** Missing fields, wrong types, invalid enums
2. **File Errors:** File not found, permission denied
3. **Parse Errors:** Invalid JSON syntax

### Error Reporting

All errors written to stderr with clear messages:

```bash
# Missing field
Error: Missing required field: title

# Wrong type
Error: Field 'category' must be string, got number

# Invalid enum
Error: Field 'category' must be one of: character place event object concept custom, got 'invalid'

# File not found
Error: Cannot read file: /path/to/missing.json
```

### Error Codes

- `0`: Success
- `1`: Validation error
- `2`: File error (future)
- `3`: Parse error (future)

---

## Testing Strategy

### Unit Tests

Each helper function needs test coverage:

1. **_validate_required_fields:**
   - All fields present → success
   - Missing one field → failure with error message
   - Missing multiple fields → failure with first missing field

2. **_validate_field_type:**
   - Correct type → success
   - Wrong type → failure with clear message
   - Field doesn't exist → failure

3. **_validate_enum:**
   - Valid enum value → success
   - Invalid enum value → failure with allowed values listed
   - Missing field → failure

### Integration Tests

Test complete validation commands:

1. **validate-entry:**
   - Valid entry file → success
   - Missing required field → failure
   - Invalid category enum → failure
   - Wrong field type → failure

2. **safe-set-field:**
   - Update existing field → success + timestamp updated
   - Create new field → success + timestamp updated
   - Invalid update → no changes to file

3. **add-to-array:**
   - Add new item → success
   - Add duplicate → skipped with message
   - Add to non-existent array → creates array

### Test Data

Use existing lore files from knowledge/expanded/ for testing:
- Valid entries, books, personas as positive test cases
- Create invalid test files for negative cases

---

## Performance Considerations

### jq Execution

Each validation involves multiple jq invocations:
- `has()` check: ~5-10ms per field
- `type` check: ~5-10ms per field
- File read: ~10-20ms

Total validation time: ~50-100ms for typical entry

This is acceptable for CLI usage.

### Optimization Opportunities (Future)

1. **Batch validation:** Single jq invocation for all checks
2. **Caching:** Skip validation if file hasn't changed
3. **Parallel execution:** Validate multiple files concurrently

Not needed for MVP.

---

## Security Considerations

### Input Validation

- File paths should be validated (no directory traversal)
- User input sanitized before passing to jq
- Use `jq --arg` to safely pass variables (prevents injection)

### File Permissions

- Validation commands are read-only
- Update commands use temp files and atomic mv
- Original file only replaced if validation passes

---

## Deployment Plan

### Phase 1: Core Validation

1. Add helper functions to Argcfile.sh
2. Implement validate-entry, validate-book, validate-persona
3. Test with existing lore files

### Phase 2: Safe Updates

1. Implement safe-set-field
2. Implement add-to-array
3. Update create-entry, create-book commands to use validation

### Phase 3: Integration

1. Update remaining argc commands to use validation
2. Add validation to manage-lore.sh integration points
3. Document new commands

---

## Open Technical Questions

1. **Nested Object Validation:** Should we validate nested required fields recursively?
   - Current design: Only check top-level and one level deep (e.g., metadata.status)
   - Alternative: Full recursive validation

2. **Array Item Validation:** Should we validate items within arrays (e.g., each relationship object)?
   - Current design: Only check array type
   - Alternative: Validate each item's structure

3. **Relationship Integrity:** Should validate-entry check if relationship target_ids exist?
   - Current design: No referential integrity checks
   - Alternative: Check if referenced entries exist

4. **Schema Evolution:** How to handle schema updates without breaking existing files?
   - Current design: Validate against current schema only
   - Alternative: Schema versioning support (out of scope for now)

---

## Appendix

### Reference Implementation Examples

#### Example: Validate Entry Command Usage

```bash
# Validate an entry file
argc validate-entry knowledge/expanded/lore/entries/entry_1764992601.json

# Output on success:
✓ Entry is valid

# Output on failure:
Error: Missing required field: category
```

#### Example: Safe Set Field Usage

```bash
# Update entry content with validation
argc safe-set-field \
  knowledge/expanded/lore/entries/entry_1764992601.json \
  content \
  "Updated narrative text..."

# Output:
✓ Entry is valid
✓ Field updated successfully
```

#### Example: Add to Array Usage

```bash
# Add tag to entry
argc add-to-array \
  knowledge/expanded/lore/entries/entry_1764992601.json \
  tags \
  "quantum"

# Output:
✓ Added to array
```

### Directory Structure

```
lore/
├── Argcfile.sh                           # argc commands (updated)
├── scripts/jq/                           # Existing jq transformations
│   ├── crud-get/transform.jq
│   ├── crud-set/transform.jq
│   ├── crud-has/transform.jq
│   └── ...
└── knowledge/core/                       # Schemas
    ├── lore/schema.json                  # Entry schema
    ├── book-schema.json                  # Book schema
    └── persona/schema.json               # Persona schema
```

No new directories needed - all changes in Argcfile.sh.
