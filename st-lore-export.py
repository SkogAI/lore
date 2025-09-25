#!/usr/bin/env python3
"""
Tool to export lore books from SkogAI to SillyTavern format.
"""

import os
import json
import argparse
import logging
from typing import Dict, Any, List, Optional
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import LoreAPI from agents/api
from agents.api.lore_api import LoreAPI

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("st_lore_export")

def export_to_sillytavern(api: LoreAPI, book_id: str, output_path: str, 
                         char_name: str = "{{char}}", user_name: str = "{{user}}",
                         add_instruction: bool = True) -> Dict[str, Any]:
    """
    Export a lore book to SillyTavern format.
    
    Args:
        api: LoreAPI instance
        book_id: ID of the book to export
        output_path: Where to save the exported lorebook
        char_name: Name to use for character template (defaults to {{char}})
        user_name: Name to use for user template (defaults to {{user}})
        add_instruction: Whether to add instruction prefix
        
    Returns:
        Dictionary with status and results
    """
    # Get the book
    book = api.get_lore_book(book_id)
    if not book:
        return {"success": False, "error": f"Book not found: {book_id}"}
    
    # Get all entries
    entries = {}
    for entry_id in book.get('entries', []):
        entry = api.get_lore_entry(entry_id)
        if entry:
            # Create SillyTavern format entry
            entry_data = {
                "id": entry_id,
                "keys": entry.get("tags", []),
                "comment": entry.get("title", ""),
                "content": format_entry_content(entry.get("content", ""), 
                                               char_name, user_name, add_instruction),
                # Add ST-specific fields
                "selective": False,
                "constant": True,
                "priority": calculate_priority(entry),
                "position": "before_char",
                "extensions": {
                    "category": entry.get("category", "custom"),
                    "summary": entry.get("summary", ""),
                    "source": "SkogAI"
                }
            }
            entries[entry_id] = entry_data
    
    # Create SillyTavern lorebook structure
    lorebook = {
        "name": book.get("title", "SkogAI Lorebook"),
        "description": book.get("description", ""),
        "entries": entries,
        "extensions": {
            "source": "SkogAI",
            "created_at": book.get("metadata", {}).get("created_at", ""),
            "updated_at": book.get("metadata", {}).get("updated_at", ""),
            "version": "1.0",
            "categories": book.get("categories", {})
        }
    }
    
    # Save to file
    with open(output_path, 'w') as f:
        json.dump(lorebook, f, indent=2)
    
    logger.info(f"Exported lorebook to {output_path} with {len(entries)} entries")
    return {
        "success": True,
        "book_id": book_id,
        "entry_count": len(entries),
        "output_path": output_path
    }

def format_entry_content(content: str, char_name: str, user_name: str, add_instruction: bool) -> str:
    """Format entry content for SillyTavern with character and user placeholders."""
    # Clean up content
    content = content.strip()
    
    # Add instruction prefix if requested
    if add_instruction and not content.lower().startswith(("remember", "know", "information")):
        content = f"Remember this information about the world: {content}"
    
    # Replace any explicit character/user references with templates
    # Only do this if char_name is not already the template
    if char_name != "{{char}}":
        content = content.replace(char_name, "{{char}}")
    
    if user_name != "{{user}}":
        content = content.replace(user_name, "{{user}}")
    
    return content

def calculate_priority(entry: Dict[str, Any]) -> int:
    """Calculate priority for SillyTavern based on entry attributes."""
    # Base priority
    priority = 50
    
    # Adjust based on category
    category_weights = {
        "character": 70,
        "place": 60,
        "event": 55,
        "object": 50,
        "concept": 45,
        "custom": 40
    }
    
    category = entry.get("category", "custom")
    priority = category_weights.get(category, priority)
    
    # Adjust based on metadata
    if entry.get("metadata", {}).get("canonical", False):
        priority += 10
    
    # Adjust based on visibility
    if entry.get("visibility", {}).get("public", True):
        priority += 5
    
    return min(100, max(1, priority))

def export_persona_lore(api: LoreAPI, persona_id: str, output_dir: str, 
                       char_name: str = None, user_name: str = "{{user}}") -> Dict[str, Any]:
    """
    Export all lore books linked to a persona.
    
    Args:
        api: LoreAPI instance
        persona_id: ID of the persona
        output_dir: Directory to save exported lorebooks
        char_name: Name to use for character (defaults to persona name)
        user_name: Name to use for user template
        
    Returns:
        Dictionary with status and results
    """
    # Get the persona
    persona = api.get_persona(persona_id)
    if not persona:
        return {"success": False, "error": f"Persona not found: {persona_id}"}
    
    # Use persona name as character name if not specified
    if char_name is None:
        char_name = persona.get("name", "{{char}}")
    
    # Get lore context
    context = api.get_persona_lore_context(persona_id)
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    results = {
        "success": True,
        "persona_id": persona_id,
        "persona_name": persona.get("name", ""),
        "exported_books": []
    }
    
    # Export each book
    for book in context.get("lore_books", []):
        book_id = book.get("id", "")
        if not book_id:
            continue
            
        output_path = os.path.join(output_dir, f"{book_id}_st.json")
        result = export_to_sillytavern(api, book_id, output_path, char_name, user_name)
        
        if result.get("success", False):
            results["exported_books"].append({
                "book_id": book_id,
                "title": book.get("title", ""),
                "output_path": output_path,
                "entry_count": result.get("entry_count", 0)
            })
    
    # Also export a combined lorebook with all entries
    if context.get("lore_entries"):
        # Create a temporary book with all entries
        combined_book = api.create_lore_book(
            title=f"Combined Lorebook for {persona.get('name', 'Character')}",
            description=f"All lore entries accessible to {persona.get('name', 'this character')}"
        )
        
        # Add all entries to the book
        for entry in context.get("lore_entries", []):
            entry_id = entry.get("id", "")
            if entry_id:
                api.add_entry_to_book(entry_id, combined_book["id"])
        
        # Export the combined book
        combined_path = os.path.join(output_dir, f"{persona_id}_combined_st.json")
        result = export_to_sillytavern(api, combined_book["id"], combined_path, char_name, user_name)
        
        if result.get("success", False):
            results["combined_book"] = {
                "book_id": combined_book["id"],
                "title": combined_book["title"],
                "output_path": combined_path,
                "entry_count": result.get("entry_count", 0)
            }
    
    logger.info(f"Exported {len(results.get('exported_books', []))} lorebooks for persona {persona_id}")
    return results

def main():
    parser = argparse.ArgumentParser(description="Export SkogAI lore books to SillyTavern format")
    parser.add_argument("--book", help="ID of the lore book to export")
    parser.add_argument("--persona", help="ID of the persona to export all linked lore books")
    parser.add_argument("--output", required=True, help="Output file or directory")
    parser.add_argument("--char-name", default="{{char}}", help="Character name to use in templates")
    parser.add_argument("--user-name", default="{{user}}", help="User name to use in templates")
    parser.add_argument("--list-books", action="store_true", help="List available lore books")
    parser.add_argument("--list-personas", action="store_true", help="List available personas")
    parser.add_argument("--no-instructions", action="store_true", help="Don't add instruction prefixes")
    
    args = parser.parse_args()
    
    # Initialize API
    api = LoreAPI()
    
    # List available books
    if args.list_books:
        books = api.list_lore_books()
        print("\nAvailable Lore Books:")
        print("--------------------")
        for book in books:
            print(f"{book.get('id')} - {book.get('title')} ({len(book.get('entries', []))} entries)")
        print()
    
    # List available personas
    if args.list_personas:
        personas = api.list_personas()
        print("\nAvailable Personas:")
        print("------------------")
        for persona in personas:
            lore_books = persona.get('knowledge', {}).get('lore_books', [])
            print(f"{persona.get('id')} - {persona.get('name')} ({len(lore_books)} linked lore books)")
        print()
    
    # Export a specific book
    if args.book:
        output_path = args.output
        # If output is a directory, create a file name
        if os.path.isdir(output_path):
            output_path = os.path.join(output_path, f"{args.book}_st.json")
            
        result = export_to_sillytavern(
            api, args.book, output_path, 
            args.char_name, args.user_name, 
            not args.no_instructions
        )
        
        if result.get("success", False):
            print(f"Successfully exported book {args.book} to {output_path}")
            print(f"Exported {result.get('entry_count', 0)} entries")
        else:
            print(f"Failed to export book: {result.get('error', 'Unknown error')}")
    
    # Export all books linked to a persona
    if args.persona:
        output_dir = args.output
        # Ensure output is a directory
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            
        result = export_persona_lore(
            api, args.persona, output_dir,
            args.char_name, args.user_name
        )
        
        if result.get("success", False):
            print(f"Successfully exported persona {args.persona} lore books:")
            for book in result.get("exported_books", []):
                print(f"- {book.get('title')} ({book.get('entry_count')} entries) -> {book.get('output_path')}")
                
            if "combined_book" in result:
                print(f"\nCombined lorebook: {result['combined_book']['title']} " +
                     f"({result['combined_book']['entry_count']} entries) -> " +
                     f"{result['combined_book']['output_path']}")
        else:
            print(f"Failed to export persona lore: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()