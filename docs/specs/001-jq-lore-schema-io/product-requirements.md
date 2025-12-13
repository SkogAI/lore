# Product Requirements Document: jq-based Lore Schema I/O

**Specification ID:** 001
**Feature Name:** jq-lore-schema-io
**Status:** Draft
**Created:** 2025-12-13
**Last Updated:** 2025-12-13

---

## Executive Summary

Build small, reusable, atomic jq-functions that integrate with Argcfile.sh to handle JSON I/O operations for lore entries, books, and personas while ensuring schema validation and compliance.

### Problem Statement

Currently, Argcfile.sh uses manual jq commands for JSON manipulation, which:
- Lacks schema validation against official schemas (schema.json, book-schema.json, persona/schema.json)
- Duplicates jq logic across multiple argc functions
- Provides no type safety or field validation
- Makes it difficult to ensure data integrity
- Doesn't leverage the existing jq transformation library in @scripts/jq/

### Target Users

**Primary:**
- Developers using argc CLI commands (list-books, show-book, create-entry, etc.)
- Shell scripts that manipulate lore JSON files

**Secondary:**
- Future automation workflows
- Integration pipelines (lore-flow.sh)

### Value Proposition

Provide a reusable library of jq-functions that:
1. Validate JSON against official lore schemas
2. Provide safe CRUD operations with type checking
3. Follow the atomic, composable pattern from @scripts/jq/
4. Integrate seamlessly with Argcfile.sh argc commands
5. Prevent invalid data from being written to lore files

---

## Requirements

### Functional Requirements

#### FR1: Schema Validation Functions
**Priority:** Must Have
**Description:** Create jq-functions that validate JSON objects against schema.json, book-schema.json, and persona/schema.json

**Acceptance Criteria:**
- Function validates required fields exist
- Function validates field types match schema
- Function validates enum values (e.g., category, status)
- Function returns boolean true/false or detailed error object
- Function works with all three schema types

**User Story:**
As a developer using argc commands, I want validation to prevent creating invalid entries so that all lore data maintains schema compliance.

#### FR2: Safe Field Access Functions
**Priority:** Must Have
**Description:** Wrapper functions around crud-get that handle missing fields gracefully

**Acceptance Criteria:**
- Function safely retrieves nested fields (e.g., "metadata.created_at")
- Function returns null or default value for missing fields instead of erroring
- Function handles all JSON types (string, number, boolean, array, object, null)
- Function integrates with existing crud-get transformation

**User Story:**
As a script reading lore data, I want safe field access so that missing optional fields don't cause script failures.

#### FR3: Safe Field Update Functions
**Priority:** Must Have
**Description:** Wrapper functions around crud-set that validate before writing

**Acceptance Criteria:**
- Function validates new value matches expected type
- Function validates enum fields against allowed values
- Function updates timestamp fields (metadata.updated_at) automatically
- Function prevents writing invalid data
- Function integrates with existing crud-set transformation

**User Story:**
As a developer updating lore entries, I want automatic validation so that I can't accidentally write malformed data.

#### FR4: Array Manipulation Functions
**Priority:** Should Have
**Description:** Safe functions for adding/removing items from arrays (tags, entries, readers, etc.)

**Acceptance Criteria:**
- Function adds item to array without duplicates
- Function removes item from array
- Function validates array item types
- Function handles missing arrays gracefully (creates if needed)

**User Story:**
As a script managing book entries, I want safe array operations so that I don't create duplicate entries or invalid references.

#### FR5: Relationship Management Functions
**Priority:** Should Have
**Description:** Functions to create and validate relationships between entries

**Acceptance Criteria:**
- Function creates relationship object with target_id and relationship_type
- Function validates relationship_type against allowed values
- Function ensures bidirectional links are consistent
- Function prevents circular dependencies

**User Story:**
As a lore curator, I want validated relationships so that the lore graph remains coherent and navigable.

### Non-Functional Requirements

#### NFR1: Compatibility
**Description:** Functions must work with existing jq CRUD transformations in @scripts/jq/

**Acceptance Criteria:**
- Functions use crud-get/crud-set/crud-has as building blocks
- Functions follow same invocation pattern (jq -f transform.jq --arg ...)
- Functions maintain same directory structure (function-name/transform.jq, schema.json, test.sh)

#### NFR2: Performance
**Description:** Functions must execute quickly for CLI usage

**Acceptance Criteria:**
- Validation completes in <100ms for typical entry/book/persona files
- No external dependencies beyond jq itself
- Functions don't read multiple files unless necessary

#### NFR3: Testability
**Description:** All functions must have comprehensive test suites

**Acceptance Criteria:**
- Minimum 8-10 test cases per function
- Tests cover happy path, edge cases, error cases
- Tests validate against all three schema types
- Tests check falsy value handling (null, false, 0, "", [], {})

#### NFR4: Documentation
**Description:** Functions must be self-documenting and provide clear usage examples

**Acceptance Criteria:**
- Each function has jq header comment with usage
- schema.json provides examples
- Integration with Argcfile.sh is documented
- Error messages are clear and actionable

---

## Success Criteria

### Metrics

1. **Schema Compliance:** 100% of lore files validate against their schemas
2. **Code Reuse:** Argcfile.sh reduces jq code duplication by 60%+
3. **Error Prevention:** Zero invalid JSON files written after deployment
4. **Test Coverage:** 90%+ test coverage for all functions

### Key Outcomes

1. Argcfile.sh uses atomic jq-functions instead of inline jq commands
2. All three schemas (entry, book, persona) have validation functions
3. Developers can validate JSON before writing to files
4. Integration tests demonstrate end-to-end schema compliance

---

## User Journeys

### Journey 1: Creating a New Entry via argc

**Actor:** Developer using CLI

**Steps:**
1. Developer runs `argc create-entry --title "Test" --category character`
2. Argcfile.sh calls `validate-entry` jq-function with generated JSON
3. Validation checks required fields, category enum, field types
4. If valid, Argcfile.sh writes file; if invalid, shows clear error
5. Developer sees confirmation or actionable error message

**Success:** Valid entry created and saved to disk

### Journey 2: Linking Entry to Book

**Actor:** Shell script in lore-flow.sh

**Steps:**
1. Script calls `add-entry-to-book` jq-function
2. Function validates entry_id exists and book_id exists
3. Function adds entry to book.entries array (no duplicates)
4. Function updates book.metadata.updated_at timestamp
5. Function returns updated book JSON

**Success:** Entry linked to book with validated references

### Journey 3: Updating Persona Voice

**Actor:** Developer editing persona

**Steps:**
1. Developer runs `argc edit-persona persona_123 voice.tone "mysterious"`
2. Argcfile.sh calls `safe-set-field` jq-function
3. Function validates voice.tone is a string
4. Function updates persona.meta.modified timestamp
5. Function returns updated persona JSON
6. Argcfile.sh writes validated JSON to file

**Success:** Persona updated with automatic timestamp and validation

---

## Constraints and Assumptions

### Constraints

1. **No External Dependencies:** Functions must use only standard jq (no external tools)
2. **Backward Compatibility:** Must not break existing argc commands
3. **Schema Adherence:** Must follow exact schema contracts in knowledge/core/
4. **Performance:** Must execute in <100ms for CLI responsiveness

### Assumptions

1. JSON schemas in knowledge/core/ are stable and complete
2. Existing jq transformations in @scripts/jq/ are reliable
3. Argcfile.sh can be modified to use new functions
4. All lore files follow timestamp-based ID format

### Dependencies

1. Existing jq CRUD transformations (crud-get, crud-set, crud-has, etc.)
2. JSON schemas: schema.json, book-schema.json, persona/schema.json
3. Argcfile.sh argc command framework
4. Test infrastructure matching @scripts/jq/test-all.sh pattern

---

## Out of Scope

The following are explicitly NOT part of this specification:

1. **LLM Integration:** No changes to llama-lore-creator.sh or agent_api.py
2. **File System Operations:** Functions only handle JSON transformation, not file I/O
3. **Migration Tools:** No automated migration of existing lore files
4. **Web UI:** No web interface for lore management
5. **Search/Indexing:** No full-text search or indexing capabilities
6. **Schema Updates:** No changes to existing schema.json files

---

## Open Questions

1. **Validation Strictness:** Should validation be strict (fail on unknown fields) or permissive (allow additional fields)?
2. **Error Format:** Should errors return boolean false or detailed error objects with messages?
3. **Batch Operations:** Do we need functions that validate/update multiple files at once?
4. **Version Handling:** Should functions validate schema version compatibility?
5. **Integration Point:** Should functions be in @scripts/jq/ or separate @scripts/jq-lore/ directory?

---

## Appendix

### Referenced Documents

- @scripts/jq/CLAUDE.md - jq transformation library patterns
- @scripts/jq/IMPLEMENTATION_SPEC.md - Implementation requirements
- @knowledge/core/lore/schema.json - Entry schema
- @knowledge/core/book-schema.json - Book schema
- @knowledge/core/persona/schema.json - Persona schema
- @Argcfile.sh - Current argc command implementation

### Related Work

- Existing jq transformations: crud-get, crud-set, crud-delete, crud-has, array-filter, etc.
- manage-lore.sh - Current lore management script
- lore_api.py - Python-based lore API (reference for operations)
