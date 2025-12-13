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

#### NFR1: Integration Format
**Description:** Functions must be argc commands in Argcfile.sh format

**Acceptance Criteria:**
- Functions are defined as argc commands in Argcfile.sh
- Functions use jq transformations from @scripts/jq/ as building blocks
- No external dependencies beyond jq itself

#### NFR2: Schema Validation
**Description:** Standard JSON schema validation against official schemas

**Acceptance Criteria:**
- Validates required fields exist
- Validates field types match schema definitions
- Validates enum values against allowed options
- Returns clear validation results

---

## Success Criteria

### Key Outcomes

1. Argcfile.sh has argc commands that validate entries, books, and personas against schemas
2. argc commands use atomic jq-functions from @scripts/jq/ as building blocks
3. Developers can validate JSON before writing to files
4. Invalid data cannot be written through argc commands

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

1. **No External Dependencies:** Functions use only standard jq
2. **Backward Compatibility:** Must not break existing argc commands
3. **Schema Adherence:** Must follow exact schema contracts in knowledge/core/
4. **argc Format:** Functions defined as argc commands in Argcfile.sh

### Assumptions

1. JSON schemas in knowledge/core/ are stable and complete
2. Existing jq transformations in @scripts/jq/ are reliable
3. argc handles structured I/O for the functions
4. All lore files follow timestamp-based ID format

### Dependencies

1. Existing jq CRUD transformations (crud-get, crud-set, crud-has, etc.)
2. JSON schemas: schema.json, book-schema.json, persona/schema.json
3. Argcfile.sh argc command framework

---

## Out of Scope

The following are explicitly NOT part of this specification:

1. **LLM Integration:** No changes to llama-lore-creator.sh or agent_api.py
2. **Migration Tools:** No automated migration of existing lore files
3. **Web UI:** No web interface for lore management
4. **Search/Indexing:** No full-text search or indexing capabilities
5. **Schema Updates:** No changes to existing schema.json files
6. **Schema Versioning:** No version compatibility validation
7. **Performance Benchmarks:** No specific performance requirements or metrics

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
