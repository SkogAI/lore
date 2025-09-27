# Lore Knowledge Schema Documentation

## Canonical Schema Locations

The Lore system uses three main schema types with their canonical locations:

### Persona Schema
- **Location**: `knowledge/core/persona/schema.json`
- **Purpose**: Defines the structure for AI persona definitions
- **Key Fields**: id, name, core_traits, voice, background, knowledge, interaction_style

### Lore Entry Schema  
- **Location**: `knowledge/core/lore/schema.json`
- **Purpose**: Defines individual lore entries in the knowledge base
- **Key Fields**: id, title, content, category, tags, relationships, metadata

### Lore Book Schema
- **Location**: `knowledge/core/lore/book-schema.json` 
- **Purpose**: Defines collections of lore entries organized into books
- **Key Fields**: id, title, description, entries, structure, metadata, visibility

## Schema Validation

All schemas follow JSON Schema Draft-07 specification and include:
- Required field validation
- Type checking
- Enum constraints where applicable
- Nested object validation

## API Integration

The `LoreAPI` class automatically loads these schemas for validation:

```python
from agents.api.lore_api import LoreAPI
api = LoreAPI(base_dir="/path/to/repo")
# Schemas are automatically loaded from canonical locations
```

## Schema Consolidation

As of the schema consolidation (Issue: Merge Lore Knowledge Folders), all duplicate
schema files have been removed. The system now uses a single source of truth for
each schema type located in the `knowledge/core/` directory.

### Previous Duplicate Locations (Removed)
- Various backup directories under `mnt_*`
- Archive locations in `MASTER_KNOWLEDGE*`
- Legacy backup folders

## Maintaining Schema Consistency

To maintain schema consistency:
1. Only modify schemas in their canonical locations
2. Do not create duplicate schema files in other directories
3. Use the LoreAPI for schema validation when creating/updating entities
4. Run schema validation tests before committing changes

## Schema Versioning

Schemas include version information in their structure. When making breaking changes:
1. Update the version field in the schema
2. Update corresponding validation logic in LoreAPI
3. Provide migration utilities for existing data if needed
