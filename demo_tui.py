usr/bin/env python3
"""
Demo script to create sample lore data and launch the TUI.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.api.lore_api import LoreAPI


def create_demo_data():
    """Create sample lore data for testing the TUI."""
    # Create a temporary demo directory
    demo_dir = Path.cwd() / "/home/skogix/lore"
    demo_dir.mkdir(exist_ok=True)

    print(f"Creating demo data in: {demo_dir}")

    # Initialize API with demo directory
    api = LoreAPI(base_dir=str(demo_dir))

    # Create a demo lore book
    book = api.create_lore_book(
        title="Eldoria: Land of Magic",
        description="A magical realm where light and darkness battle for dominance"
    )
    print(f"Created book: {book['title']}")

    # Add a section to the book
    book['structure'].append({
        "name": "World Information",
        "description": "Core world information",
        "entries": [],
        "subsections": []
    })
    book['structure'].append({
        "name": "Characters",
        "description": "Important characters in Eldoria",
        "entries": [],
        "subsections": []
    })

    # Save updated book
    import json
    book_path = Path(api.lore_books_dir) / f"{book['id']}.json"
    with open(book_path, 'w') as f:
        json.dump(book, f, indent=2)

    # Create demo lore entries
    entries_data = [
        {
            "title": "The Forest Glade",
            "content": "The Forest Glade is a haven of safety warded with ancient magic. No foul beast may enter, nor any with ill intent. While Eldoria was once a place of wonder, since the Shadowfangs came darkness reigns. Their evil cannot penetrate the glade though — its magic protects all within. Those who find the glade need not fear the night, for guardians keep watch till dawn.",
            "category": "place",
            "tags": ["glade", "safe haven", "refuge", "forest"],
            "summary": "A protected sanctuary within the corrupted forest",
            "section": "World Information"
        },
        {
            "title": "Shadowfangs",
            "content": "The Shadowfangs are beasts of darkness, corrupted creatures that feast on suffering. When they came, the forest turned perilous — filled with monsters that stalk the night. They spread their curse, twisting innocent creatures into sinister beasts without heart or mercy, turning them into one of their own. Though they prey on travelers, there are sanctuaries where their influence cannot reach, protected by guardians of light.",
            "category": "creature",
            "tags": ["shadowfang", "beast", "monster", "darkness"],
            "summary": "Corrupted beasts that spread darkness throughout Eldoria",
            "section": "World Information"
        },
        {
            "title": "Eldoria",
            "content": "Eldoria is a magical forest realm that was once a place of wonder. Rolling meadows, a vast lake, and mountains that touched the sky characterized this beautiful land. However, the Shadowfangs came and darkness now reigns where once was light. The lake turned bitter, mountains fell to ruin, and beasts stalk where travelers once walked in peace. Some places the light still lingers, pockets of hope midst despair - havens warded from the shadows, oases in a desert of danger.",
            "category": "place",
            "tags": ["eldoria", "forest", "magical realm", "corrupted"],
            "summary": "A once-beautiful forest realm now corrupted by darkness",
            "section": "World Information"
        },
        {
            "title": "Seraphina the Guardian",
            "content": "Seraphina is a powerful guardian who protects the Forest Glade from the corruption of the Shadowfangs. With silver hair that gleams like moonlight and eyes that shine with ancient wisdom, she stands as a beacon of hope in the darkness. Her magic is drawn from the forest itself, allowing her to ward off even the most powerful dark creatures. She is compassionate to those who seek refuge, but fierce against any who threaten her sanctuary.",
            "category": "character",
            "tags": ["seraphina", "guardian", "protector", "magic"],
            "summary": "A powerful guardian who protects the Forest Glade",
            "section": "Characters"
        },
        {
            "title": "The Dark Lord Malakar",
            "content": "Malakar is the ancient evil who summoned the Shadowfangs to Eldoria. Once a powerful mage who sought immortality, he made a pact with dark forces and was transformed into an undead being of terrible power. From his fortress in the Blighted Mountains, he commands the Shadowfangs and seeks to corrupt all of Eldoria. Only the protected sanctuaries like the Forest Glade remain beyond his reach.",
            "category": "character",
            "tags": ["malakar", "villain", "dark lord", "undead"],
            "summary": "The ancient evil who commands the Shadowfangs",
            "section": "Characters"
        },
    ]

    for entry_data in entries_data:
        section = entry_data.pop("section")
        entry = api.create_lore_entry(**entry_data)
        print(f"Created entry: {entry['title']}")

        # Add entry to book and section
        api.add_entry_to_book(entry['id'], book['id'], section)

    print(f"\nDemo data created successfully!")
    print(f"Location: {demo_dir}")
    print(f"\nTo view the data in the TUI, run:")
    print(f"  python3 lore_tui.py --base-dir {demo_dir}")

    return str(demo_dir)


if __name__ == "__main__":
    demo_dir = create_demo_data()

    # Ask if user wants to launch the TUI
    response = input("\nLaunch the TUI now? (y/n): ").strip().lower()

    if response == 'y':
        from lore_tui import LoreTUI
        app = LoreTUI(base_dir=demo_dir)
        app.run()
