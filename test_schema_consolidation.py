#!/usr/bin/env python3

"""
Test script to validate schema consolidation didn't break functionality.
"""

import os
import json
import tempfile
from pathlib import Path
from agents.api.lore_api import LoreAPI

def test_schema_loading():
    """Test that schemas can be loaded properly from canonical locations."""
    print("Testing schema loading...")
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Copy the canonical schemas to the temp directory structure
        canonical_root = Path("/home/runner/work/lore/lore")
        test_knowledge_dir = temp_path / "knowledge" / "core"
        
        # Create directory structure
        (test_knowledge_dir / "persona").mkdir(parents=True, exist_ok=True)
        (test_knowledge_dir / "lore").mkdir(parents=True, exist_ok=True)
        
        # Copy schema files
        import shutil
        shutil.copy2(
            canonical_root / "knowledge/core/persona/schema.json",
            test_knowledge_dir / "persona/schema.json"
        )
        shutil.copy2(
            canonical_root / "knowledge/core/lore/schema.json",
            test_knowledge_dir / "lore/schema.json"
        )
        shutil.copy2(
            canonical_root / "knowledge/core/lore/book-schema.json",
            test_knowledge_dir / "lore/book-schema.json"
        )
        
        # Test LoreAPI initialization
        try:
            api = LoreAPI(base_dir=str(temp_path))
            
            # Verify all schemas were loaded
            expected_schemas = ["persona", "lore_entry", "lore_book"]
            for schema_type in expected_schemas:
                if schema_type not in api.schemas or not api.schemas[schema_type]:
                    print(f"❌ Failed to load {schema_type} schema")
                    return False
                else:
                    print(f"✅ Successfully loaded {schema_type} schema")
            
            return True
            
        except Exception as e:
            print(f"❌ LoreAPI initialization failed: {e}")
            return False

def test_entity_creation():
    """Test that entities can be created using the loaded schemas."""
    print("\nTesting entity creation...")
    
    try:
        api = LoreAPI(base_dir="/home/runner/work/lore/lore")
        
        # Test persona creation
        persona = api.create_persona(
            name="Test Consolidation Persona",
            core_description="A test persona for schema consolidation",
            personality_traits=["analytical", "systematic", "thorough"],
            voice_tone="professional"
        )
        print(f"✅ Created persona: {persona['id']}")
        
        # Test lore entry creation
        entry = api.create_lore_entry(
            title="Schema Consolidation Test Entry",
            content="This entry validates that schema consolidation works correctly.",
            category="concept",
            tags=["testing", "schema", "consolidation"]
        )
        print(f"✅ Created lore entry: {entry['id']}")
        
        # Test lore book creation
        book = api.create_lore_book(
            title="Schema Consolidation Test Book",
            description="A book to test schema consolidation functionality",
            entries=[entry['id']]
        )
        print(f"✅ Created lore book: {book['id']}")
        
        # Clean up test files
        cleanup_test_files(api, [persona['id'], entry['id'], book['id']])
        
        return True
        
    except Exception as e:
        print(f"❌ Entity creation failed: {e}")
        return False

def cleanup_test_files(api, entity_ids):
    """Clean up test files created during validation."""
    print("\nCleaning up test files...")
    
    for entity_id in entity_ids:
        # Try to remove persona files
        persona_file = Path(api.personas_dir) / f"{entity_id}.json"
        if persona_file.exists():
            persona_file.unlink()
            print(f"  Removed {persona_file}")
            
        # Try to remove entry files
        entry_file = Path(api.lore_entries_dir) / f"{entity_id}.json"
        if entry_file.exists():
            entry_file.unlink()
            print(f"  Removed {entry_file}")
            
        # Try to remove book files
        book_file = Path(api.lore_books_dir) / f"{entity_id}.json"
        if book_file.exists():
            book_file.unlink()
            print(f"  Removed {book_file}")

def test_schema_validation():
    """Test that schemas are valid JSON Schema documents."""
    print("\nTesting schema validation...")
    
    canonical_schemas = [
        "/home/runner/work/lore/lore/knowledge/core/persona/schema.json",
        "/home/runner/work/lore/lore/knowledge/core/lore/schema.json",
        "/home/runner/work/lore/lore/knowledge/core/lore/book-schema.json"
    ]
    
    for schema_path in canonical_schemas:
        try:
            with open(schema_path, 'r') as f:
                schema_data = json.load(f)
                
            # Basic validation checks
            required_fields = ["$schema", "title", "type", "properties"]
            for field in required_fields:
                if field not in schema_data:
                    print(f"❌ Schema {schema_path} missing required field: {field}")
                    return False
                    
            # Check that it's JSON Schema Draft-07
            if not schema_data["$schema"].endswith("draft-07/schema#"):
                print(f"⚠️  Schema {schema_path} not using JSON Schema Draft-07")
                
            print(f"✅ Schema validation passed: {Path(schema_path).name}")
            
        except Exception as e:
            print(f"❌ Schema validation failed for {schema_path}: {e}")
            return False
    
    return True

def main():
    """Run all consolidation tests."""
    print("=== Schema Consolidation Validation Tests ===\n")
    
    tests = [
        ("Schema Loading", test_schema_loading),
        ("Schema Validation", test_schema_validation),
        ("Entity Creation", test_entity_creation)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"Running {test_name} test...")
        try:
            if test_func():
                print(f"✅ {test_name} test PASSED\n")
                passed += 1
            else:
                print(f"❌ {test_name} test FAILED\n")
                failed += 1
        except Exception as e:
            print(f"❌ {test_name} test FAILED with exception: {e}\n")
            failed += 1
    
    print(f"=== Test Results ===")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total: {passed + failed}")
    
    if failed == 0:
        print("\n🎉 All tests passed! Schema consolidation is safe to proceed.")
        return True
    else:
        print(f"\n⚠️  {failed} test(s) failed. Review before proceeding with consolidation.")
        return False

if __name__ == "__main__":
    main()