#!/usr/bin/env python3

"""
Schema Consolidation Script for Lore Repository

This script identifies and removes duplicate schema files while maintaining
canonical schema files in the /knowledge/core/ directory structure.
"""

import os
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple

# Canonical schema locations (these will be preserved)
CANONICAL_SCHEMAS = {
    "persona": "/knowledge/core/persona/schema.json",
    "lore_entry": "/knowledge/core/lore/schema.json", 
    "lore_book": "/knowledge/core/lore/book-schema.json"
}

def get_file_hash(file_path: Path) -> str:
    """Get MD5 hash of a file."""
    try:
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

def find_schema_files(repo_root: Path) -> Dict[str, List[Tuple[Path, str]]]:
    """Find all schema files and their hashes."""
    schema_patterns = ["schema.json", "book-schema.json"]
    found_schemas = {
        "persona": [],
        "lore_entry": [],
        "lore_book": []
    }
    
    for pattern in schema_patterns:
        for schema_file in repo_root.rglob(pattern):
            # Skip hidden directories and temp files
            if any(part.startswith('.') for part in schema_file.parts):
                continue
                
            file_hash = get_file_hash(schema_file)
            if not file_hash:
                continue
                
            # Determine schema type based on path and filename
            if "persona" in str(schema_file) and pattern == "schema.json":
                found_schemas["persona"].append((schema_file, file_hash))
            elif "lore" in str(schema_file) and pattern == "book-schema.json":
                found_schemas["lore_book"].append((schema_file, file_hash))
            elif "lore" in str(schema_file) and pattern == "schema.json":
                found_schemas["lore_entry"].append((schema_file, file_hash))
    
    return found_schemas

def validate_canonical_schemas(repo_root: Path) -> bool:
    """Ensure canonical schema files exist and are valid JSON."""
    print("Validating canonical schema files...")
    
    all_valid = True
    for schema_type, relative_path in CANONICAL_SCHEMAS.items():
        canonical_path = repo_root / relative_path.lstrip('/')
        
        if not canonical_path.exists():
            print(f"❌ Canonical schema missing: {canonical_path}")
            all_valid = False
            continue
            
        try:
            with open(canonical_path, 'r') as f:
                schema_data = json.load(f)
                print(f"✅ Valid canonical schema: {schema_type} ({canonical_path})")
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in canonical schema {canonical_path}: {e}")
            all_valid = False
        except Exception as e:
            print(f"❌ Error reading canonical schema {canonical_path}: {e}")
            all_valid = False
    
    return all_valid

def identify_duplicates(repo_root: Path, found_schemas: Dict[str, List[Tuple[Path, str]]]) -> Dict[str, List[Path]]:
    """Identify duplicate schema files that can be safely removed."""
    duplicates_to_remove = {
        "persona": [],
        "lore_entry": [],
        "lore_book": []
    }
    
    print("\nAnalyzing schema duplicates...")
    
    for schema_type, relative_path in CANONICAL_SCHEMAS.items():
        canonical_path = repo_root / relative_path.lstrip('/')
        if not canonical_path.exists():
            continue
            
        canonical_hash = get_file_hash(canonical_path)
        if not canonical_hash:
            continue
            
        print(f"\n{schema_type.upper()} Schema Analysis:")
        print(f"Canonical: {canonical_path}")
        print(f"Canonical hash: {canonical_hash}")
        
        identical_count = 0
        different_count = 0
        
        for schema_path, schema_hash in found_schemas[schema_type]:
            # Skip the canonical file itself
            if schema_path.resolve() == canonical_path.resolve():
                continue
                
            if schema_hash == canonical_hash:
                identical_count += 1
                duplicates_to_remove[schema_type].append(schema_path)
                print(f"  ✓ Duplicate: {schema_path}")
            else:
                different_count += 1
                print(f"  ⚠ Different: {schema_path} (hash: {schema_hash})")
        
        print(f"Summary: {identical_count} identical duplicates, {different_count} different versions")
    
    return duplicates_to_remove

def create_documentation(repo_root: Path) -> None:
    """Create documentation about the consolidated schema structure."""
    doc_content = """# Lore Knowledge Schema Documentation

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
"""
    
    doc_path = repo_root / "docs" / "schema-reference.md"
    doc_path.parent.mkdir(exist_ok=True)
    
    with open(doc_path, 'w') as f:
        f.write(doc_content)
    
    print(f"Created schema documentation: {doc_path}")

def remove_duplicates(duplicates_to_remove: Dict[str, List[Path]], dry_run: bool = True) -> int:
    """Remove duplicate schema files."""
    removed_count = 0
    
    for schema_type, duplicates in duplicates_to_remove.items():
        if not duplicates:
            continue
            
        print(f"\n{schema_type.upper()} duplicates:")
        for dup_path in duplicates:
            if dry_run:
                print(f"  [DRY RUN] Would remove: {dup_path}")
            else:
                try:
                    dup_path.unlink()
                    print(f"  ✅ Removed: {dup_path}")
                    removed_count += 1
                except Exception as e:
                    print(f"  ❌ Failed to remove {dup_path}: {e}")
    
    return removed_count

def main():
    """Main consolidation process."""
    import sys
    
    repo_root = Path("/home/runner/work/lore/lore")
    dry_run = "--execute" not in sys.argv
    
    print("=== Lore Schema Consolidation ===")
    print(f"Repository root: {repo_root}")
    if dry_run:
        print("🔍 DRY RUN MODE - No files will be deleted. Use --execute to perform actual removal.")
    else:
        print("⚠️  EXECUTION MODE - Files will be permanently deleted!")
    
    # Step 1: Validate canonical schemas exist and are valid
    if not validate_canonical_schemas(repo_root):
        print("\n❌ Cannot proceed: Canonical schemas are invalid or missing")
        return False
    
    # Step 2: Find all schema files
    print("\nSearching for schema files...")
    found_schemas = find_schema_files(repo_root)
    
    total_found = sum(len(schemas) for schemas in found_schemas.values())
    print(f"Found {total_found} schema files across all locations")
    
    # Step 3: Identify duplicates
    duplicates_to_remove = identify_duplicates(repo_root, found_schemas)
    
    total_duplicates = sum(len(dups) for dups in duplicates_to_remove.values())
    print(f"\n📊 Summary: {total_duplicates} duplicate files identified for removal")
    
    # Step 4: Create documentation
    print("\nCreating schema documentation...")
    create_documentation(repo_root)
    
    # Step 5: Remove duplicates (dry run or actual)
    print(f"\n🗑 {'Files that would be removed' if dry_run else 'Removing duplicate files'}:")
    removed_count = remove_duplicates(duplicates_to_remove, dry_run)
    
    if dry_run:
        print(f"\n✅ Schema consolidation analysis complete!")
        print(f"   - Canonical schemas: {len(CANONICAL_SCHEMAS)} validated")
        print(f"   - Duplicate files identified: {total_duplicates}")
        print(f"   - Documentation created: docs/schema-reference.md")
        print(f"   - Run with --execute to perform actual file removal")
    else:
        print(f"\n✅ Schema consolidation complete!")
        print(f"   - Canonical schemas: {len(CANONICAL_SCHEMAS)} validated")
        print(f"   - Duplicate files removed: {removed_count}")
        print(f"   - Documentation created: docs/schema-reference.md")
    
    return True

if __name__ == "__main__":
    main()