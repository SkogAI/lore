# Implementation Plan: jq-based Lore Schema I/O

**Specification ID:** 001
**Feature Name:** jq-lore-schema-io
**Status:** Draft
**Created:** 2025-12-13
**Last Updated:** 2025-12-13

---

## Overview

This plan defines the exact function signatures and I/O contracts for implementing schema validation and safe JSON manipulation in Argcfile.sh. Focus is on **what** each function accepts and returns, not **how** it's implemented.

---

## Schema Field Type Contracts

These are the exact field types and constraints that validation functions must check.

### Entry Schema Field Types

**Source:** `knowledge/core/lore/schema.json`

| Field Path | Type | Required | Constraints |
|------------|------|----------|-------------|
| `id` | string | YES | - |
| `title` | string | YES | - |
| `content` | string | YES | - |
| `summary` | string | NO | - |
| `category` | string | YES | ENUM: "character", "place", "event", "object", "concept", "custom" |
| `tags` | array | NO | Items must be strings |
| `relationships` | array | NO | Items must be objects with required fields |
| `relationships[].target_id` | string | YES (if relationship exists) | - |
| `relationships[].relationship_type` | string | YES (if relationship exists) | - |
| `relationships[].description` | string | NO | - |
| `attributes` | object | NO | additionalProperties allowed |
| `metadata` | object | NO | - |
| `metadata.created_by` | string | NO | - |
| `metadata.created_at` | string | NO | format: date-time (ISO 8601) |
| `metadata.updated_at` | string | NO | format: date-time (ISO 8601) |
| `metadata.version` | string | NO | - |
| `metadata.canonical` | boolean | NO | default: true |
| `visibility` | object | NO | - |
| `visibility.public` | boolean | NO | default: true |
| `visibility.restricted_to` | array | NO | Items must be strings (persona IDs) |
| `book_id` | string | NO | Must reference existing book file if present |
| `references` | array | NO | Items must be objects |

**Referential Integrity Checks:**
- `relationships[].target_id`: Must reference existing entry file (entries/*.json)
- `book_id`: Must reference existing book file (books/*.json)

### Book Schema Field Types

**Source:** `knowledge/core/book-schema.json`

| Field Path | Type | Required | Constraints |
|------------|------|----------|-------------|
| `id` | string | YES | - |
| `title` | string | YES | - |
| `description` | string | YES | - |
| `entries` | array | NO | Items must be strings (entry IDs) |
| `categories` | object | NO | Values must be arrays of strings |
| `tags` | array | NO | Items must be strings |
| `owners` | array | NO | Items must be strings (persona IDs) |
| `readers` | array | NO | Items must be strings (persona IDs) |
| `metadata` | object | NO | - |
| `metadata.created_by` | string | NO | - |
| `metadata.created_at` | string | NO | format: date-time (ISO 8601) |
| `metadata.updated_at` | string | NO | format: date-time (ISO 8601) |
| `metadata.version` | string | NO | - |
| `metadata.status` | string | NO | ENUM: "draft", "active", "archived", "deprecated" |
| `structure` | array | NO | Items must be objects (sections) |
| `structure[].name` | string | NO | - |
| `structure[].description` | string | NO | - |
| `structure[].entries` | array | NO | Items must be strings (entry IDs) |
| `structure[].subsections` | array | NO | Recursive structure |
| `relationships` | array | NO | Items must be objects |
| `relationships[].target_id` | string | YES (if relationship exists) | - |
| `relationships[].relationship_type` | string | YES (if relationship exists) | ENUM: "sequel", "prequel", "expansion", "contradiction", "reference", "custom" |
| `relationships[].description` | string | NO | - |
| `visibility` | object | NO | - |
| `visibility.public` | boolean | NO | default: false |
| `visibility.system` | boolean | NO | default: false |

**Referential Integrity Checks:**
- `entries[]`: Each entry ID must reference existing entry file (entries/*.json)
- `owners[]`: Each persona ID must reference existing persona file (personas/*.json)
- `readers[]`: Each persona ID must reference existing persona file (personas/*.json)
- `relationships[].target_id`: Must reference existing book file (books/*.json)

### Persona Schema Field Types

**Source:** `knowledge/core/persona/schema.json`

| Field Path | Type | Required | Constraints |
|------------|------|----------|-------------|
| `id` | string | YES | - |
| `name` | string | YES | - |
| `core_traits` | object | YES | Must have required nested fields |
| `core_traits.temperament` | string | YES | - |
| `core_traits.values` | array | YES | Items must be strings |
| `core_traits.motivations` | array | YES | Items must be strings |
| `voice` | object | YES | Must have required nested fields |
| `voice.tone` | string | YES | - |
| `voice.patterns` | array | YES | Items must be strings |
| `voice.vocabulary` | string | YES | - |
| `background` | object | NO | - |
| `background.origin` | string | NO | - |
| `background.significant_events` | array | NO | Items must be strings |
| `background.connections` | array | NO | Items must be objects |
| `background.connections[].entity` | string | NO | - |
| `background.connections[].relationship` | string | NO | - |
| `knowledge` | object | NO | - |
| `knowledge.expertise` | array | NO | Items must be strings |
| `knowledge.limitations` | array | NO | Items must be strings |
| `knowledge.lore_books` | array | NO | Items must be strings (book IDs) |
| `interaction_style` | object | NO | - |
| `interaction_style.formality` | string | NO | ENUM: "very_formal", "formal", "neutral", "casual", "very_casual" |
| `interaction_style.humor` | string | NO | ENUM: "none", "subtle", "occasional", "frequent", "constant" |
| `interaction_style.directness` | string | NO | ENUM: "very_direct", "direct", "balanced", "indirect", "very_indirect" |
| `meta` | object | NO | - |
| `meta.version` | string | NO | - |
| `meta.created` | string | NO | format: date-time (ISO 8601) |
| `meta.modified` | string | NO | format: date-time (ISO 8601) |
| `meta.tags` | array | NO | Items must be strings |

**Referential Integrity Checks:**
- `knowledge.lore_books[]`: Each book ID must reference existing book file (books/*.json)

---

## Function Signatures

### Helper Functions (Internal)

These bash functions are called by argc commands but not exposed directly to users.

#### `_validate_required_fields`

**Signature:**
```bash
_validate_required_fields <json_file> <field1> [field2] [field3] ...
```

**Input:**
- `json_file` (string): Absolute or relative path to JSON file
- `field1..fieldN` (strings): Required field names (top-level only)

**Output:**
- Exit code `0`: All required fields exist
- Exit code `1`: One or more fields missing
- stderr: Error message for first missing field

**Examples:**
```bash
# Success case
_validate_required_fields "entry.json" "id" "title" "content" "category"
# Returns: 0
# stderr: (nothing)

# Failure case
_validate_required_fields "entry.json" "id" "title" "missing_field"
# Returns: 1
# stderr: Error: Missing required field: missing_field
```

---

#### `_validate_field_type`

**Signature:**
```bash
_validate_field_type <json_file> <field_path> <expected_type>
```

**Input:**
- `json_file` (string): Path to JSON file
- `field_path` (string): Dot-separated path (e.g., "category" or "metadata.status")
- `expected_type` (string): One of: `string`, `number`, `boolean`, `array`, `object`, `null`

**Output:**
- Exit code `0`: Field has expected type
- Exit code `1`: Field has wrong type or doesn't exist
- stderr: Error message with field path, expected type, and actual type

**Examples:**
```bash
# Success case
_validate_field_type "entry.json" "category" "string"
# Returns: 0
# stderr: (nothing)

# Failure case
_validate_field_type "entry.json" "category" "array"
# Returns: 1
# stderr: Error: Field 'category' must be array, got string
```

---

#### `_validate_enum`

**Signature:**
```bash
_validate_enum <json_file> <field_path> <value1> [value2] [value3] ...
```

**Input:**
- `json_file` (string): Path to JSON file
- `field_path` (string): Dot-separated path to field
- `value1..valueN` (strings): Allowed enum values

**Output:**
- Exit code `0`: Field value matches one of the allowed values
- Exit code `1`: Field value not in allowed list
- stderr: Error message with field path, allowed values, and actual value

**Examples:**
```bash
# Success case
_validate_enum "entry.json" "category" "character" "place" "event" "object" "concept" "custom"
# Returns: 0
# stderr: (nothing)

# Failure case
_validate_enum "entry.json" "category" "character" "place"
# Returns: 1
# stderr: Error: Field 'category' must be one of: character place, got event
```

---

#### `_validate_file_exists`

**Signature:**
```bash
_validate_file_exists <file_id> <file_type>
```

**Input:**
- `file_id` (string): ID to check (e.g., "entry_123", "book_456", "persona_789")
- `file_type` (string): Type of file - "entry" | "book" | "persona"

**Output:**
- Exit code `0`: File exists
- Exit code `1`: File does not exist
- stderr: Error message if file missing

**File Path Resolution:**
- `entry` → `$ENTRIES_DIR/${file_id}.json`
- `book` → `$BOOKS_DIR/${file_id}.json`
- `persona` → `$PERSONA_DIR/${file_id}.json`

**Examples:**
```bash
# Success case
_validate_file_exists "entry_1234567890" "entry"
# Returns: 0
# stderr: (nothing)

# Failure case
_validate_file_exists "entry_missing" "entry"
# Returns: 1
# stderr: Error: Referenced entry does not exist: entry_missing
```

---

### argc Commands (User-Facing)

These are the public API exposed via argc CLI.

#### `validate-entry`

**Signature:**
```bash
argc validate-entry <entry_file>
```

**Input:**
- `entry_file` (arg): Path to lore entry JSON file

**Output:**
- Exit code `0`: Entry is valid against schema.json
- Exit code `1`: Entry fails validation
- stderr: "✓ Entry is valid" (success) or validation error messages (failure)

**Validation Rules:**

See "Entry Schema Field Types" table for complete field type contract.

**Minimum validation (required fields only):**
- `id` exists and is string
- `title` exists and is string
- `content` exists and is string
- `category` exists and is string with enum value: "character", "place", "event", "object", "concept", or "custom"

**Optional field validation (if present):**
- `tags` is array
- `metadata.updated_at` is string (date-time format)
- `visibility.public` is boolean

**Referential integrity checks:**
- If `book_id` present: Book file must exist at `$BOOKS_DIR/${book_id}.json`
- If `relationships[]` present: Each `target_id` must reference existing entry file

**Examples:**
```bash
# Valid entry
argc validate-entry knowledge/expanded/lore/entries/entry_123.json
# Returns: 0
# stderr: ✓ Entry is valid

# Invalid entry (missing required field)
argc validate-entry invalid_entry.json
# Returns: 1
# stderr: Error: Missing required field: category
```

---

#### `validate-book`

**Signature:**
```bash
argc validate-book <book_file>
```

**Input:**
- `book_file` (arg): Path to lore book JSON file

**Output:**
- Exit code `0`: Book is valid against book-schema.json
- Exit code `1`: Book fails validation
- stderr: "✓ Book is valid" (success) or validation error messages (failure)

**Validation Rules:**

See "Book Schema Field Types" table for complete field type contract.

**Minimum validation (required fields only):**
- `id` exists and is string
- `title` exists and is string
- `description` exists and is string

**Optional field validation (if present):**
- `entries` is array of strings
- `metadata.status` is string with enum value: "draft", "active", "archived", or "deprecated"
- `readers` is array of strings
- `owners` is array of strings

**Referential integrity checks:**
- If `entries[]` present: Each entry ID must reference existing entry file at `$ENTRIES_DIR/${entry_id}.json`
- If `readers[]` present: Each persona ID must reference existing persona file at `$PERSONA_DIR/${persona_id}.json`
- If `owners[]` present: Each persona ID must reference existing persona file at `$PERSONA_DIR/${persona_id}.json`
- If `relationships[]` present: Each `target_id` must reference existing book file

**Examples:**
```bash
# Valid book
argc validate-book knowledge/expanded/lore/books/book_456.json
# Returns: 0
# stderr: ✓ Book is valid

# Invalid book (wrong type)
argc validate-book invalid_book.json
# Returns: 1
# stderr: Error: Field 'entries' must be array, got string
```

---

#### `validate-persona`

**Signature:**
```bash
argc validate-persona <persona_file>
```

**Input:**
- `persona_file` (arg): Path to persona JSON file

**Output:**
- Exit code `0`: Persona is valid against persona/schema.json
- Exit code `1`: Persona fails validation
- stderr: "✓ Persona is valid" (success) or validation error messages (failure)

**Validation Rules:**

See "Persona Schema Field Types" table for complete field type contract.

**Minimum validation (required fields):**
- `id` exists and is string
- `name` exists and is string
- `core_traits` exists and is object
- `core_traits.temperament` exists and is string
- `core_traits.values` exists and is array
- `core_traits.motivations` exists and is array
- `voice` exists and is object
- `voice.tone` exists and is string
- `voice.patterns` exists and is array
- `voice.vocabulary` exists and is string

**Optional field validation (if present):**
- `interaction_style.formality` is string with enum value: "very_formal", "formal", "neutral", "casual", or "very_casual"
- `interaction_style.humor` is string with enum value: "none", "subtle", "occasional", "frequent", or "constant"
- `interaction_style.directness` is string with enum value: "very_direct", "direct", "balanced", "indirect", or "very_indirect"
- `knowledge.lore_books` is array of strings
- `meta.modified` is string (date-time format)

**Referential integrity checks:**
- If `knowledge.lore_books[]` present: Each book ID must reference existing book file at `$BOOKS_DIR/${book_id}.json`

**Examples:**
```bash
# Valid persona
argc validate-persona knowledge/expanded/personas/persona_789.json
# Returns: 0
# stderr: ✓ Persona is valid

# Invalid persona (missing nested field)
argc validate-persona invalid_persona.json
# Returns: 1
# stderr: Error: core_traits must have temperament, values, and motivations
```

---

#### `safe-set-field`

**Signature:**
```bash
argc safe-set-field <file> <path> <value> [--type=<type>]
```

**Input:**
- `file` (arg): Path to JSON file (entry, book, or persona)
- `path` (arg): Dot-separated field path (e.g., "title" or "metadata.version")
- `value` (arg): New value to set
- `--type` (option): Expected type (default: "string")
  - Values: `string`, `number`, `boolean`

**Output:**
- Exit code `0`: Field updated successfully
- Exit code `1`: Validation failed after update
- Modified file in place (atomic replace via temp file)
- Auto-updated timestamp field based on file type:
  - Entry/Book: `metadata.updated_at`
  - Persona: `meta.modified`
- stderr: "✓ Field updated successfully" (success) or validation error (failure)

**Examples:**
```bash
# Update entry title
argc safe-set-field entry_123.json title "New Title"
# Returns: 0
# stderr: ✓ Entry is valid
#         ✓ Field updated successfully
# Side effect: entry_123.json modified, metadata.updated_at set to current UTC time

# Invalid update (validation fails)
argc safe-set-field entry_123.json category "invalid_category"
# Returns: 1
# stderr: Error: Field 'category' must be one of: character place event object concept custom, got invalid_category
# Side effect: Original file unchanged (temp file removed)
```

---

#### `add-to-array`

**Signature:**
```bash
argc add-to-array <file> <path> <value>
```

**Input:**
- `file` (arg): Path to JSON file
- `path` (arg): Dot-separated path to array field (e.g., "tags" or "entries")
- `value` (arg): Value to add to array

**Output:**
- Exit code `0`: Value added or already exists (idempotent)
- Modified file in place (atomic replace via temp file)
- Auto-updated timestamp field (if metadata/meta exists)
- stderr: "✓ Added to array" (new item) or "✓ Value already in array, skipping" (duplicate)

**Behavior:**
- If array doesn't exist: Create array with single item
- If array exists and value not present: Append value
- If array exists and value already present: No-op (idempotent)
- If field exists but is not array: Error (exit 1)

**Examples:**
```bash
# Add new tag
argc add-to-array entry_123.json tags "quantum"
# Returns: 0
# stderr: ✓ Added to array
# Side effect: tags array now contains "quantum"

# Add duplicate tag
argc add-to-array entry_123.json tags "quantum"
# Returns: 0
# stderr: ✓ Value already in array, skipping
# Side effect: File unchanged (idempotent)

# Add to non-array field
argc add-to-array entry_123.json title "value"
# Returns: 1
# stderr: Error: Field 'title' is not an array
# Side effect: File unchanged
```

---

## Implementation Phases

### Phase 1: Validation Foundation

**Deliverables:**
1. Helper function: `_validate_required_fields`
2. Helper function: `_validate_field_type`
3. Helper function: `_validate_enum`
4. Helper function: `_validate_file_exists`

**Validation Checkpoint:**
- Test each helper with valid and invalid inputs
- Verify exit codes and error messages

---

### Phase 2: Schema Validation Commands

**Deliverables:**
1. argc command: `validate-entry`
2. argc command: `validate-book`
3. argc command: `validate-persona`

**Dependencies:**
- Phase 1 complete
- Access to schema files (knowledge/core/)

**Validation Checkpoint:**
- Test each command with existing lore files
- Test with invalid files (missing fields, wrong types, bad enums)
- Verify all error messages are clear and actionable

---

### Phase 3: Safe Update Commands

**Deliverables:**
1. argc command: `safe-set-field`
2. argc command: `add-to-array`

**Dependencies:**
- Phase 2 complete
- Existing jq transformations (crud-set)

**Validation Checkpoint:**
- Test field updates with validation
- Test timestamp auto-update
- Test atomic file replacement (no corruption on failure)
- Test idempotency of add-to-array

---

### Phase 4: Integration with Existing Commands

**Deliverables:**
1. Update `create-entry` to call `validate-entry` before writing
2. Update `create-book` to call `validate-book` before writing
3. Update `create-persona` to call `validate-persona` before writing

**Dependencies:**
- Phase 2 complete

**Validation Checkpoint:**
- Test that invalid entries cannot be created
- Verify backward compatibility (existing commands still work)
- Test error handling (temp files cleaned up on failure)

---

## Data Contracts

### File Type Detection

Commands detect file type from path:
- Contains `/entries/` → Entry
- Contains `/books/` → Book
- Contains `/personas/` → Persona

**Contract:**
```
Input: file path string
Output: "entry" | "book" | "persona" | error
```

### Timestamp Field Mapping

Different file types use different timestamp fields:

| File Type | Updated Field |
|-----------|---------------|
| Entry | `metadata.updated_at` |
| Book | `metadata.updated_at` |
| Persona | `meta.modified` |

**Contract:**
```
Input: file type ("entry" | "book" | "persona")
Output: field path string ("metadata.updated_at" | "meta.modified")
```

### Schema Path Mapping

Schema files located relative to repo root:

| File Type | Schema Path |
|-----------|-------------|
| Entry | `knowledge/core/lore/schema.json` |
| Book | `knowledge/core/book-schema.json` |
| Persona | `knowledge/core/persona/schema.json` |

**Contract:**
```
Input: file type ("entry" | "book" | "persona")
Output: absolute path to schema file
```

---

## Error Handling Contracts

### Exit Codes

All commands use consistent exit codes:

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Validation error or invalid input |

### Error Output

All errors written to stderr with format:
```
Error: <clear description of what's wrong>
```

Success messages written to stderr with format:
```
✓ <success message>
```

**Contract:**
- stdout: Empty (reserved for future structured output)
- stderr: Human-readable messages
- Exit code: 0 (success) or 1 (error)

---

## Integration Contracts

### With Existing jq Transformations

Commands call existing jq transformations via pipe or file:

**crud-get usage:**
```bash
jq -f scripts/jq/crud-get/transform.jq --arg path "field.path" file.json
```

**crud-set usage:**
```bash
jq -f scripts/jq/crud-set/transform.jq --arg path "field.path" --arg value "new value" file.json > output.json
```

**crud-has usage:**
```bash
jq -f scripts/jq/crud-has/transform.jq --arg path "field.path" file.json
# Returns: true or false
```

**Contract:**
- Input: JSON file + arguments
- Output: Transformed JSON or boolean
- No side effects (jq transformations are pure)

### With Existing argc Commands

New validation commands integrate with existing commands:

**create-entry integration:**
```bash
# Current flow:
create-entry() {
  # ... generate JSON ...
  echo "$json" > file.json
}

# New flow:
create-entry() {
  # ... generate JSON ...
  echo "$json" > temp.json
  if validate-entry temp.json; then
    mv temp.json file.json
  else
    rm temp.json
    return 1
  fi
}
```

**Contract:**
- Validation happens before file write
- Original flow preserved if validation passes
- Temp file cleaned up if validation fails

---

## Testing Contracts

### Test Data Requirements

Each validation command needs test files:

**Valid test files:**
- `test-valid-entry.json` - Minimal valid entry
- `test-valid-book.json` - Minimal valid book
- `test-valid-persona.json` - Minimal valid persona

**Invalid test files:**
- `test-missing-field-entry.json` - Entry missing required field
- `test-wrong-type-entry.json` - Entry with wrong field type
- `test-invalid-enum-entry.json` - Entry with invalid category value

**Contract:**
```
Input: Test file path
Expected: Specific exit code and error message
Verify: Exit code matches, error message contains expected text
```

### Test Execution

Each command must pass:
1. Valid input → exit 0, no errors
2. Invalid input → exit 1, clear error message
3. Missing file → exit 1, file not found error
4. Malformed JSON → exit 1, parse error

**Contract:**
```bash
# Test template
test_command() {
  result=$(argc command test-file.json 2>&1)
  exit_code=$?

  assert_equals "$exit_code" "0"
  assert_contains "$result" "✓ Valid"
}
```

---

## Acceptance Criteria

### Phase 1 (Validation Foundation)
- [ ] `_validate_required_fields` implemented with correct signature
- [ ] `_validate_field_type` implemented with correct signature
- [ ] `_validate_enum` implemented with correct signature
- [ ] `_validate_file_exists` implemented with correct signature
- [ ] All helpers return correct exit codes
- [ ] All helpers write clear error messages to stderr

### Phase 2 (Schema Validation)
- [ ] `validate-entry` validates against schema.json contract
- [ ] `validate-entry` checks referential integrity (book_id, relationships[].target_id)
- [ ] `validate-book` validates against book-schema.json contract
- [ ] `validate-book` checks referential integrity (entries[], readers[], owners[], relationships[].target_id)
- [ ] `validate-persona` validates against persona/schema.json contract
- [ ] `validate-persona` checks referential integrity (knowledge.lore_books[])
- [ ] All validation commands tested with existing lore files (pass)
- [ ] All validation commands tested with invalid files (fail with clear errors)
- [ ] All validation commands tested with invalid references (fail with clear errors)

### Phase 3 (Safe Updates)
- [ ] `safe-set-field` updates field and validates result
- [ ] `safe-set-field` auto-updates timestamp based on file type
- [ ] `safe-set-field` uses atomic file replacement
- [ ] `add-to-array` adds items without duplicates (idempotent)
- [ ] `add-to-array` auto-updates timestamp
- [ ] Both commands preserve original file if validation fails

### Phase 4 (Integration)
- [ ] `create-entry` validates before writing
- [ ] `create-book` validates before writing
- [ ] `create-persona` validates before writing
- [ ] Invalid data cannot be written through argc commands
- [ ] Existing commands backward compatible

---

## Success Metrics

1. **API Completeness:** All 5 argc commands implemented with exact signatures
2. **Contract Compliance:** All functions respect input/output contracts
3. **Error Handling:** All error cases return correct exit codes and messages
4. **Integration:** Existing argc commands use validation without breaking changes

---

## Appendix: Quick Reference

### Command Summary Table

| Command | Input | Output | Side Effects |
|---------|-------|--------|--------------|
| `validate-entry <file>` | JSON file path | Exit code 0/1, stderr message | None |
| `validate-book <file>` | JSON file path | Exit code 0/1, stderr message | None |
| `validate-persona <file>` | JSON file path | Exit code 0/1, stderr message | None |
| `safe-set-field <file> <path> <value>` | File path, field path, new value | Exit code 0/1, stderr message | Modifies file, updates timestamp |
| `add-to-array <file> <path> <value>` | File path, array path, item | Exit code 0/1, stderr message | Modifies file, updates timestamp |

### Helper Function Summary Table

| Helper | Input | Output | Purpose |
|--------|-------|--------|---------|
| `_validate_required_fields <file> <fields...>` | File path, field names | Exit code 0/1 | Check required fields exist |
| `_validate_field_type <file> <path> <type>` | File path, field path, type name | Exit code 0/1 | Check field has correct type |
| `_validate_enum <file> <path> <values...>` | File path, field path, allowed values | Exit code 0/1 | Check field value is allowed |
| `_validate_file_exists <file_id> <file_type>` | File ID, file type | Exit code 0/1 | Check referenced file exists |
