#!/usr/bin/env python3

import os
import sys
import json
import logging
from typing import Dict, Any, List, Optional
import time
import re
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("lore_api")


class LoreAPI:
    """API layer for lore book and persona management."""

    def __init__(self, base_dir: str = None):
        """Initialize the LoreAPI with paths to lore and persona storage."""
        if base_dir is None:
            base_dir = Path(__file__).parent.parent.parent
        self.base_dir = str(base_dir)
        self.lore_entries_dir = os.path.join(
            base_dir, "knowledge/expanded/lore/entries"
        )
        self.lore_books_dir = os.path.join(base_dir, "knowledge/expanded/lore/books")
        self.personas_dir = os.path.join(base_dir, "knowledge/expanded/personas")

        # Ensure directories exist
        os.makedirs(self.lore_entries_dir, exist_ok=True)
        os.makedirs(self.lore_books_dir, exist_ok=True)
        os.makedirs(self.personas_dir, exist_ok=True)

        # Load schema definitions
        self.load_schemas()

    def load_schemas(self):
        """Load schema definitions for validation."""
        schema_paths = {
            "persona": os.path.join(
                self.base_dir, "knowledge/core/persona/schema.json"
            ),
            "lore_entry": os.path.join(
                self.base_dir, "knowledge/core/lore/schema.json"
            ),
            "lore_book": os.path.join(
                self.base_dir, "knowledge/core/lore/book-schema.json"
            ),
        }

        self.schemas = {}
        for schema_type, path in schema_paths.items():
            try:
                with open(path, "r") as f:
                    self.schemas[schema_type] = json.load(f)
                logger.info(f"Loaded {schema_type} schema from {path}")
            except Exception as e:
                logger.error(f"Failed to load {schema_type} schema: {e}")
                self.schemas[schema_type] = {}

    def generate_id(self, prefix: str = "") -> str:
        """Generate a unique identifier for a new entity."""
        timestamp = int(time.time())
        return f"{prefix}{timestamp}"

    def create_lore_entry(
        self,
        title: str,
        content: str,
        category: str,
        tags: List[str] = None,
        summary: str = "",
    ) -> Dict[str, Any]:
        """Create a new lore entry."""
        entry_id = self.generate_id("entry_")
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        entry = {
            "id": entry_id,
            "title": title,
            "content": content,
            "summary": summary,
            "category": category,
            "tags": tags or [],
            "relationships": [],
            "attributes": {},
            "metadata": {
                "created_by": os.environ.get("USER", "system"),
                "created_at": timestamp,
                "updated_at": timestamp,
                "version": "1.0",
                "canonical": True,
            },
            "visibility": {"public": True, "restricted_to": []},
        }

        # Save to file
        entry_path = os.path.join(self.lore_entries_dir, f"{entry_id}.json")
        with open(entry_path, "w") as f:
            json.dump(entry, f, indent=2)

        logger.info(f"Created lore entry: {entry_id}")
        return entry

    def create_lore_book(
        self, title: str, description: str, entries: List[str] = None
    ) -> Dict[str, Any]:
        """Create a new lore book."""
        book_id = self.generate_id("book_")
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        book = {
            "id": book_id,
            "title": title,
            "description": description,
            "entries": entries or [],
            "categories": {},
            "tags": [],
            "owners": [],
            "readers": [],
            "metadata": {
                "created_by": os.environ.get("USER", "system"),
                "created_at": timestamp,
                "updated_at": timestamp,
                "version": "1.0",
                "status": "draft",
            },
            "structure": [
                {
                    "name": "Introduction",
                    "description": "Overview of this lore book",
                    "entries": [],
                    "subsections": [],
                }
            ],
            "visibility": {"public": False, "system": False},
        }

        # Save to file
        book_path = os.path.join(self.lore_books_dir, f"{book_id}.json")
        with open(book_path, "w") as f:
            json.dump(book, f, indent=2)

        logger.info(f"Created lore book: {book_id}")
        return book

    def create_persona(
        self,
        name: str,
        core_description: str,
        personality_traits: List[str],
        voice_tone: str,
    ) -> Dict[str, Any]:
        """Create a new persona."""
        persona_id = self.generate_id("persona_")
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        persona = {
            "id": persona_id,
            "name": name,
            "core_traits": {
                "temperament": "balanced",
                "values": (
                    personality_traits[:2]
                    if len(personality_traits) > 2
                    else personality_traits
                ),
                "motivations": (
                    personality_traits[2:4]
                    if len(personality_traits) > 4
                    else personality_traits[2:] if len(personality_traits) > 2 else []
                ),
            },
            "voice": {"tone": voice_tone, "patterns": [], "vocabulary": "standard"},
            "background": {"origin": "", "significant_events": [], "connections": []},
            "knowledge": {"expertise": [], "limitations": [], "lore_books": []},
            "interaction_style": {
                "formality": "neutral",
                "humor": "occasional",
                "directness": "balanced",
            },
            "meta": {
                "version": "1.0",
                "created": timestamp,
                "modified": timestamp,
                "tags": [],
            },
        }

        # Save to file
        persona_path = os.path.join(self.personas_dir, f"{persona_id}.json")
        with open(persona_path, "w") as f:
            json.dump(persona, f, indent=2)

        logger.info(f"Created persona: {persona_id}")
        return persona

    def get_lore_entry(self, entry_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a lore entry by ID."""
        entry_path = os.path.join(self.lore_entries_dir, f"{entry_id}.json")

        if not os.path.exists(entry_path):
            logger.warning(f"Lore entry not found: {entry_id}")
            return None

        try:
            with open(entry_path, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load lore entry {entry_id}: {e}")
            return None

    def get_lore_book(self, book_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a lore book by ID."""
        book_path = os.path.join(self.lore_books_dir, f"{book_id}.json")

        if not os.path.exists(book_path):
            logger.warning(f"Lore book not found: {book_id}")
            return None

        try:
            with open(book_path, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load lore book {book_id}: {e}")
            return None

    def get_persona(self, persona_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a persona by ID."""
        persona_path = os.path.join(self.personas_dir, f"{persona_id}.json")

        if not os.path.exists(persona_path):
            logger.warning(f"Persona not found: {persona_id}")
            return None

        try:
            with open(persona_path, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load persona {persona_id}: {e}")
            return None

    def list_lore_entries(self, category: str = None) -> List[Dict[str, Any]]:
        """List all lore entries, optionally filtered by category."""
        entries = []

        for filename in os.listdir(self.lore_entries_dir):
            if not filename.endswith(".json"):
                continue

            try:
                with open(os.path.join(self.lore_entries_dir, filename), "r") as f:
                    entry = json.load(f)

                    if category is None or entry.get("category") == category:
                        entries.append(entry)
            except Exception as e:
                logger.error(f"Failed to load lore entry {filename}: {e}")

        return entries

    def list_lore_books(self) -> List[Dict[str, Any]]:
        """List all lore books."""
        books = []

        for filename in os.listdir(self.lore_books_dir):
            if not filename.endswith(".json"):
                continue

            try:
                with open(os.path.join(self.lore_books_dir, filename), "r") as f:
                    book = json.load(f)
                    books.append(book)
            except Exception as e:
                logger.error(f"Failed to load lore book {filename}: {e}")

        return books

    def list_personas(self) -> List[Dict[str, Any]]:
        """List all personas."""
        personas = []

        for filename in os.listdir(self.personas_dir):
            if not filename.endswith(".json"):
                continue

            try:
                with open(os.path.join(self.personas_dir, filename), "r") as f:
                    persona = json.load(f)
                    personas.append(persona)
            except Exception as e:
                logger.error(f"Failed to load persona {filename}: {e}")

        return personas

    def add_entry_to_book(
        self, entry_id: str, book_id: str, section: str = None
    ) -> bool:
        """Add a lore entry to a book."""
        entry = self.get_lore_entry(entry_id)
        book = self.get_lore_book(book_id)

        if not entry or not book:
            return False

        # Add entry to book's entries list if not already there
        if entry_id not in book["entries"]:
            book["entries"].append(entry_id)

        # Add to section if specified
        if section:
            for struct in book["structure"]:
                if struct["name"] == section:
                    if entry_id not in struct["entries"]:
                        struct["entries"].append(entry_id)
                    break
            else:
                logger.warning(f"Section {section} not found in book {book_id}")

        # Update timestamps
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        book["metadata"]["updated_at"] = timestamp

        # Save book
        book_path = os.path.join(self.lore_books_dir, f"{book_id}.json")
        with open(book_path, "w") as f:
            json.dump(book, f, indent=2)

        # Update entry's book_id
        entry["book_id"] = book_id
        entry_path = os.path.join(self.lore_entries_dir, f"{entry_id}.json")
        with open(entry_path, "w") as f:
            json.dump(entry, f, indent=2)

        logger.info(f"Added entry {entry_id} to book {book_id}")
        return True

    def link_book_to_persona(self, book_id: str, persona_id: str) -> bool:
        """Link a lore book to a persona."""
        book = self.get_lore_book(book_id)
        persona = self.get_persona(persona_id)

        if not book or not persona:
            return False

        # Add persona to book's readers (ensure readers field exists)
        if "readers" not in book:
            book["readers"] = []

        if persona_id not in book["readers"]:
            book["readers"].append(persona_id)

        # Add book to persona's lore_books
        if "lore_books" not in persona.get("knowledge", {}):
            if "knowledge" not in persona:
                persona["knowledge"] = {}
            persona["knowledge"]["lore_books"] = []

        if book_id not in persona["knowledge"]["lore_books"]:
            persona["knowledge"]["lore_books"].append(book_id)

        # Update timestamps
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        book["metadata"]["updated_at"] = timestamp

        if "meta" in persona:
            persona["meta"]["modified"] = timestamp

        # Save both entities
        book_path = os.path.join(self.lore_books_dir, f"{book_id}.json")
        with open(book_path, "w") as f:
            json.dump(book, f, indent=2)

        persona_path = os.path.join(self.personas_dir, f"{persona_id}.json")
        with open(persona_path, "w") as f:
            json.dump(persona, f, indent=2)

        logger.info(f"Linked book {book_id} to persona {persona_id}")
        return True

    def search_lore(self, query: str) -> List[Dict[str, Any]]:
        """Search lore entries by keyword."""
        results = []
        seen_ids = set()  # Track seen entry IDs to prevent duplicates

        for entry in self.list_lore_entries():
            entry_id = entry.get("id")
            # Skip entries without an ID
            if entry_id is None:
                logger.warning("Skipping entry without ID")
                continue
            # Skip duplicates
            if entry_id in seen_ids:
                logger.debug(f"Skipping duplicate entry: {entry_id}")
                continue

            searchable_text = " ".join(
                [
                    entry.get("title", ""),
                    entry.get("content", ""),
                    entry.get("summary", ""),
                    " ".join(entry.get("tags", [])),
                ]
            ).lower()

            if query.lower() in searchable_text:
                results.append(entry)
                seen_ids.add(entry_id)

        return results

    def import_lorebook_format(self, lorebook_json: Dict[str, Any]) -> Dict[str, Any]:
        """Import a lorebook from external format (like example-lorebook.json)."""
        if "entries" not in lorebook_json:
            logger.error("Invalid lorebook format: missing 'entries' key")
            return {"success": False, "error": "Invalid lorebook format"}

        book_id = self.generate_id("book_")
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        # Create the book
        book = {
            "id": book_id,
            "title": "Imported Lorebook",
            "description": "Lorebook imported from external format",
            "entries": [],
            "categories": {},
            "tags": [],
            "metadata": {
                "created_by": os.environ.get("USER", "system"),
                "created_at": timestamp,
                "updated_at": timestamp,
                "version": "1.0",
                "status": "active",
            },
            "structure": [
                {
                    "name": "Imported Entries",
                    "description": "Entries imported from external format",
                    "entries": [],
                    "subsections": [],
                }
            ],
            "visibility": {"public": True, "system": False},
        }

        # Save book
        book_path = os.path.join(self.lore_books_dir, f"{book_id}.json")
        with open(book_path, "w") as f:
            json.dump(book, f, indent=2)

        # Process entries
        for uid, entry_data in lorebook_json["entries"].items():
            # Extract content (remove any conversation formatting if present)
            content = entry_data.get("content", "")
            content = re.sub(r"{{user}}.*?{{char}}:", "", content)
            content = re.sub(r"{{user}}:.*?\n", "", content)
            content = re.sub(r"{{char}}:", "", content)
            content = content.strip()

            # Create entry
            entry = self.create_lore_entry(
                title=entry_data.get("comment", f"Entry {uid}"),
                content=content,
                category="custom",
                tags=entry_data.get("key", []),
                summary=entry_data.get("comment", ""),
            )

            # Add to book
            book["entries"].append(entry["id"])
            book["structure"][0]["entries"].append(entry["id"])

            # Add category if needed
            category = "custom"
            if category not in book["categories"]:
                book["categories"][category] = []
            book["categories"][category].append(entry["id"])

        # Update book with entries
        with open(book_path, "w") as f:
            json.dump(book, f, indent=2)

        logger.info(
            f"Imported lorebook with {len(lorebook_json['entries'])} entries to book {book_id}"
        )
        return {
            "success": True,
            "book_id": book_id,
            "entry_count": len(lorebook_json["entries"]),
        }

    def get_persona_lore_context(self, persona_id: str) -> Dict[str, Any]:
        """Get all lore content accessible to a persona."""
        persona = self.get_persona(persona_id)
        if not persona:
            return {"error": f"Persona not found: {persona_id}"}

        result = {"persona": persona, "lore_books": [], "lore_entries": []}

        # Get all lore books accessible to this persona
        lore_book_ids = persona.get("knowledge", {}).get("lore_books", [])
        for book_id in lore_book_ids:
            book = self.get_lore_book(book_id)
            if book:
                result["lore_books"].append(book)

                # Get all entries in this book
                for entry_id in book.get("entries", []):
                    entry = self.get_lore_entry(entry_id)
                    if entry:
                        result["lore_entries"].append(entry)

        return result


# Example usage
if __name__ == "__main__":
    api = LoreAPI()

    # Import example lorebook if it exists
    repo_root = Path(__file__).parent.parent.parent
    example_path = repo_root / "example-lorebook.json"
    if example_path.exists():
        try:
            with open(example_path, "r") as f:
                example_data = json.load(f)
                result = api.import_lorebook_format(example_data)
                print(f"Import result: {json.dumps(result, indent=2)}")
        except Exception as e:
            print(f"Failed to import example lorebook: {e}")

    # Create a test persona
    persona = api.create_persona(
        name="Test Forest Guardian",
        core_description="A magical protector of the forest glade",
        personality_traits=["compassionate", "protective", "wise", "gentle"],
        voice_tone="serene and comforting",
    )

    print(f"Created test persona: {persona['id']}")

    # If we imported a lorebook, link it to the persona
    if "result" in locals() and result.get("success"):
        api.link_book_to_persona(result["book_id"], persona["id"])
        print(f"Linked lorebook {result['book_id']} to persona {persona['id']}")

        # Get full context for the persona
        context = api.get_persona_lore_context(persona["id"])
        print(f"Persona has access to {len(context['lore_entries'])} lore entries")
