#!/usr/bin/env python3

import os
import sys
import json
import time
import logging
from pathlib import Path

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.api.lore_api import LoreAPI

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("lore_demo")

def create_demo_workspace():
    """Create a demo workspace with timestamp to avoid overwriting existing data."""
    timestamp = int(time.time())
    demo_dir = Path(f"demo/lore_demo_{timestamp}")
    demo_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Created demo workspace at: {demo_dir}")
    return demo_dir

def save_to_workspace(workspace, name, data):
    """Save data to the workspace directory."""
    file_path = workspace / f"{name}.json"
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)
    logger.info(f"Saved {name} to {file_path}")
    return file_path

def check_for_example_lorebook():
    """Check if example-lorebook.json exists."""
    example_path = Path("example-lorebook.json")
    if example_path.exists():
        logger.info(f"Found example lorebook at {example_path}")
        return example_path
    else:
        logger.warning("example-lorebook.json not found")
        return None

def create_demo_persona(api, name, description, persona_traits, voice):
    """Create a demo persona."""
    persona = api.create_persona(
        name=name,
        core_description=description,
        personality_traits=persona_traits,
        voice_tone=voice
    )
    logger.info(f"Created persona: {persona['name']} ({persona['id']})")
    return persona

def create_demo_lore_book(api, title, description):
    """Create a demo lore book."""
    book = api.create_lore_book(
        title=title,
        description=description
    )
    logger.info(f"Created lore book: {book['title']} ({book['id']})")
    return book

def create_demo_lore_entries(api, topics):
    """Create demo lore entries for each topic."""
    entries = []
    
    for topic in topics:
        entry = api.create_lore_entry(
            title=topic['title'],
            content=topic['content'],
            category=topic['category'],
            tags=topic['tags'],
            summary=topic['summary']
        )
        entries.append(entry)
        logger.info(f"Created lore entry: {entry['title']} ({entry['id']})")
    
    return entries

def add_entries_to_book(api, book, entries, section_name="World Information"):
    """Add entries to a book under a specific section."""
    # First, make sure the section exists
    section_exists = False
    for section in book['structure']:
        if section['name'] == section_name:
            section_exists = True
            break
    
    if not section_exists:
        book['structure'].append({
            "name": section_name,
            "description": "Core world information",
            "entries": [],
            "subsections": []
        })
        # Save the updated book
        book_path = os.path.join(api.lore_books_dir, f"{book['id']}.json")
        with open(book_path, 'w') as f:
            json.dump(book, f, indent=2)
    
    # Add each entry to the book
    for entry in entries:
        api.add_entry_to_book(entry['id'], book['id'], section_name)
        logger.info(f"Added entry {entry['title']} to book {book['title']}")
    
    # Reload the book to get the updated version
    return api.get_lore_book(book['id'])

def link_book_to_persona(api, book, persona):
    """Link a lore book to a persona."""
    result = api.link_book_to_persona(book['id'], persona['id'])
    if result:
        logger.info(f"Linked book {book['title']} to persona {persona['name']}")
    else:
        logger.error(f"Failed to link book {book['id']} to persona {persona['id']}")

def run_demo():
    """Run the lore system demo."""
    print("\n===== SkogAI Lore System Demo =====\n")
    
    # Create workspace
    workspace = create_demo_workspace()
    
    # Initialize API
    api = LoreAPI()
    
    # Check for example lorebook
    example_lorebook_path = check_for_example_lorebook()
    imported_book = None
    
    if example_lorebook_path:
        print("\n=== Importing Example Lorebook ===")
        try:
            with open(example_lorebook_path, 'r') as f:
                example_data = json.load(f)
                result = api.import_lorebook_format(example_data)
                if result.get('success'):
                    print(f"Successfully imported lorebook with {result['entry_count']} entries")
                    imported_book = api.get_lore_book(result['book_id'])
                    save_to_workspace(workspace, "imported_lorebook", imported_book)
                else:
                    print(f"Failed to import lorebook: {result.get('error')}")
        except Exception as e:
            print(f"Error importing lorebook: {e}")
    
    # Create demo persona
    print("\n=== Creating Demo Persona ===")
    seraphina = create_demo_persona(
        api,
        "Seraphina",
        "A magical guardian of the forest glade",
        ["compassionate", "protective", "wise", "gentle"],
        "serene and comforting"
    )
    save_to_workspace(workspace, "persona", seraphina)
    
    # Create demo lore book if we didn't import one
    if not imported_book:
        print("\n=== Creating Demo Lore Book ===")
        book = create_demo_lore_book(
            api,
            "Eldoria: Land of Magic and Shadow",
            "A magical realm where light and darkness battle for dominance"
        )
        
        # Create demo lore entries
        print("\n=== Creating Demo Lore Entries ===")
        lore_topics = [
            {
                "title": "Eldoria",
                "content": "Eldoria is a magical forest realm that was once a place of wonder. Rolling meadows, a vast lake, and mountains that touched the sky characterized this beautiful land. However, the Shadowfangs came and darkness now reigns where once was light. The lake turned bitter, mountains fell to ruin, and beasts stalk where travelers once walked in peace. Some places the light still lingers, pockets of hope midst despair - havens warded from the shadows, oases in a desert of danger.",
                "category": "place",
                "tags": ["eldoria", "forest", "magical forest"],
                "summary": "A once-beautiful forest realm now corrupted by darkness"
            },
            {
                "title": "Shadowfangs",
                "content": "The Shadowfangs are beasts of darkness, corrupted creatures that feast on suffering. When they came, the forest turned perilous — filled with monsters that stalk the night. They spread their curse, twisting innocent creatures into sinister beasts without heart or mercy, turning them into one of their own. Though they prey on travelers, there are sanctuaries where their influence cannot reach, protected by guardians of light.",
                "category": "character",
                "tags": ["shadowfang", "beast", "monster"],
                "summary": "Corrupted beasts that spread darkness throughout Eldoria"
            },
            {
                "title": "The Forest Glade",
                "content": "The Forest Glade is a haven of safety warded with ancient magic. No foul beast may enter, nor any with ill intent. While Eldoria was once a place of wonder, since the Shadowfangs came darkness reigns. Their evil cannot penetrate the glade though — its magic protects all within. Those who find the glade need not fear the night, for guardians keep watch till dawn.",
                "category": "place",
                "tags": ["glade", "safe haven", "refuge"],
                "summary": "A protected sanctuary within the corrupted forest"
            }
        ]
        
        entries = create_demo_lore_entries(api, lore_topics)
        save_to_workspace(workspace, "lore_entries", entries)
        
        # Add entries to book
        print("\n=== Adding Entries to Lore Book ===")
        updated_book = add_entries_to_book(api, book, entries)
        save_to_workspace(workspace, "lore_book", updated_book)
    else:
        # Use the imported book
        book = imported_book
    
    # Link book to persona
    print("\n=== Linking Lore Book to Persona ===")
    link_book_to_persona(api, book, seraphina)
    
    # Get full context for the persona
    print("\n=== Generating Persona Context ===")
    context = api.get_persona_lore_context(seraphina['id'])
    save_to_workspace(workspace, "persona_context", context)
    
    # Create a markdown representation of the persona with lore
    print("\n=== Creating Markdown Representation ===")
    
    markdown = f"""# {seraphina['name']}

## Core Identity
{seraphina.get('core_traits', {}).get('temperament', '')} guardian of the forest glade.

## Personality Traits
{', '.join(seraphina.get('core_traits', {}).get('values', []))}

## Voice and Communication Style
{seraphina.get('voice', {}).get('tone', '')}

## Knowledge

### Lore Books
"""
    
    for book in context.get('lore_books', []):
        markdown += f"- {book['title']}\n"
    
    markdown += "\n### Lore Entries\n"
    
    for entry in context.get('lore_entries', []):
        markdown += f"#### {entry['title']}\n"
        markdown += f"{entry['summary']}\n\n"
        markdown += f"{entry['content']}\n\n"
    
    markdown_path = workspace / "persona_with_lore.md"
    with open(markdown_path, 'w') as f:
        f.write(markdown)
    
    print(f"\nDemo completed! Results saved to: {workspace}")
    print(f"Persona markdown file: {markdown_path}")

if __name__ == "__main__":
    run_demo()