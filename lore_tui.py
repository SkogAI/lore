#!/usr/bin/env python3
"""
Interactive Terminal UI for browsing lore entries.
Provides keyboard navigation and rich visual feedback.
"""

import os
import sys
from typing import List, Dict, Any, Optional
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.widgets import (
    Header,
    Footer,
    Static,
    ListView,
    ListItem,
    Label,
    Markdown,
    Input,
)
from textual.binding import Binding
from textual.screen import Screen

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.api.lore_api import LoreAPI


class EntryDetailScreen(Screen):
    """Screen for viewing a full entry with markdown rendering."""

    BINDINGS = [
        Binding("b", "back", "Back", priority=True),
        Binding("q", "quit", "Quit", priority=True),
    ]

    def __init__(self, entry: Dict[str, Any], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entry = entry

    def compose(self) -> ComposeResult:
        yield Header()

        # Create markdown content
        content = f"# {self.entry.get('title', 'Untitled')}\n\n"

        # Add metadata
        category = self.entry.get("category", "unknown")
        tags = ", ".join(self.entry.get("tags", []))
        content += f"**Category:** {category}\n\n"
        if tags:
            content += f"**Tags:** {tags}\n\n"

        # Add summary if present
        summary = self.entry.get("summary", "")
        if summary:
            content += f"## Summary\n\n{summary}\n\n"

        # Add main content
        content += f"## Content\n\n{self.entry.get('content', '')}\n\n"

        # Add relationships if present
        relationships = self.entry.get("relationships", [])
        if relationships:
            content += "## Relationships\n\n"
            for rel in relationships:
                content += f"- {rel}\n"

        yield VerticalScroll(Markdown(content))
        yield Footer()

    def action_back(self) -> None:
        """Go back to the previous screen."""
        self.app.pop_screen()

    def action_quit(self) -> None:
        """Quit the application."""
        self.app.exit()


class BookDetailScreen(Screen):
    """Screen for viewing book structure and entries."""

    BINDINGS = [
        Binding("b", "back", "Back", priority=True),
        Binding("q", "quit", "Quit", priority=True),
        Binding("?", "help", "Help", priority=True),
    ]

    def __init__(self, book: Dict[str, Any], api: LoreAPI, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.book = book
        self.api = api
        self.entries: List[Dict[str, Any]] = []
        self.selected_entry_index = 0

    def compose(self) -> ComposeResult:
        yield Header()

        # Title and info
        title_text = f"📚 {self.book.get('title', 'Untitled Book')}"
        entry_count = len(self.book.get("entries", []))
        yield Static(f"{title_text}    [{entry_count} entries]", id="book-title")

        # Main content area
        with Container(id="main-container"):
            # Left panel - Sections
            with Vertical(id="sections-panel"):
                yield Label("Sections:", classes="panel-header")
                yield ListView(id="sections-list")

            # Right panel - Entries
            with Vertical(id="entries-panel"):
                yield Label("Entries:", classes="panel-header")
                yield ListView(id="entries-list")

        yield Footer()

    def on_mount(self) -> None:
        """Populate the lists when the screen is mounted."""
        sections_list = self.query_one("#sections-list", ListView)
        entries_list = self.query_one("#entries-list", ListView)

        # Add sections from book structure
        for section in self.book.get("structure", []):
            section_count = len(section.get("entries", []))
            item = ListItem(
                Label(f"> {section['name']} ({section_count})"),
                id=f"section-{section['name']}",
            )
            sections_list.append(item)

        # Load and display entries
        for entry_id in self.book.get("entries", []):
            entry = self.api.get_lore_entry(entry_id)
            if entry:
                self.entries.append(entry)
                title = entry.get("title", "Untitled")
                summary = entry.get("summary", "")
                truncated_summary = (
                    summary[:50] + "..." if len(summary) > 50 else summary
                )

                item = ListItem(
                    Label(f"• {title}\n  {truncated_summary}"),
                    id=f"entry-{entry_id}",
                )
                entries_list.append(item)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle entry selection."""
        # Check if it's from the entries list
        if event.list_view.id == "entries-list":
            # Extract entry ID from the ListItem ID
            item_id = event.item.id
            if item_id and item_id.startswith("entry-"):
                entry_id = item_id[6:]  # Remove "entry-" prefix

                # Find the entry in our list
                for entry in self.entries:
                    if entry["id"] == entry_id:
                        # Show entry detail screen
                        self.app.push_screen(EntryDetailScreen(entry))
                        break

    def action_back(self) -> None:
        """Go back to the book browser."""
        self.app.pop_screen()

    def action_quit(self) -> None:
        """Quit the application."""
        self.app.exit()

    def action_help(self) -> None:
        """Show help screen."""
        self.app.action_help()


class BookBrowserScreen(Screen):
    """Main screen for browsing all books."""

    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("/", "search", "Search", priority=True),
        Binding("?", "help", "Help", priority=True),
    ]

    def __init__(self, api: LoreAPI, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = api
        self.books: List[Dict[str, Any]] = []

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("📚 Lore Books", id="title")
        yield ListView(id="books-list")
        yield Footer()

    def on_mount(self) -> None:
        """Populate the list when the screen is mounted."""
        # Load all books
        self.books = self.api.list_lore_books()
        books_list = self.query_one("#books-list", ListView)

        if not self.books:
            books_list.append(
                ListItem(Label("No lore books found. Create one to get started!"))
            )
        else:
            for book in self.books:
                title = book.get("title", "Untitled")
                description = book.get("description", "")
                truncated_desc = (
                    description[:80] + "..." if len(description) > 80 else description
                )
                entry_count = len(book.get("entries", []))

                item = ListItem(
                    Label(
                        f"📖 {title}\n   {truncated_desc}\n   [{entry_count} entries]"
                    ),
                    id=f"book-{book['id']}",
                )
                books_list.append(item)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle book selection."""
        # Extract book ID from the ListItem ID
        item_id = event.item.id
        if item_id and item_id.startswith("book-"):
            book_id = item_id[5:]  # Remove "book-" prefix

            # Find the book in our list
            for book in self.books:
                if book["id"] == book_id:
                    # Show book detail screen
                    self.app.push_screen(BookDetailScreen(book, self.api))
                    break

    def action_quit(self) -> None:
        """Quit the application."""
        self.app.exit()

    def action_search(self) -> None:
        """Open search interface."""
        self.app.push_screen(SearchScreen(self.api))

    def action_help(self) -> None:
        """Show help screen."""
        self.app.action_help()


class SearchScreen(Screen):
    """Screen for searching lore entries."""

    BINDINGS = [
        Binding("escape", "cancel", "Cancel", priority=True),
        Binding("b", "cancel", "Cancel", priority=True),
        Binding("q", "quit", "Quit", priority=True),
    ]

    def __init__(self, api: LoreAPI, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = api
        self.results: List[Dict[str, Any]] = []

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("🔍 Search Lore Entries", id="search-title")
        yield Input(placeholder="Enter search query...", id="search-input")
        yield Static("Results:", id="results-label")
        yield ListView(id="search-results")
        yield Footer()

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle search input changes."""
        query = event.value.strip()

        # Get the results list
        results_list = self.query_one("#search-results", ListView)
        results_list.clear()

        if len(query) < 2:
            return

        # Search for entries
        self.results = self.api.search_lore(query)

        # Display results
        if not self.results:
            results_list.append(ListItem(Label("No results found")))
        else:
            for entry in self.results:
                title = entry.get("title", "Untitled")
                summary = entry.get("summary", "")
                truncated_summary = (
                    summary[:60] + "..." if len(summary) > 60 else summary
                )
                category = entry.get("category", "unknown")

                item = ListItem(
                    Label(f"📝 {title} [{category}]\n   {truncated_summary}"),
                    id=f"result-{entry['id']}",
                )
                results_list.append(item)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle result selection."""
        item_id = event.item.id
        if item_id and item_id.startswith("result-"):
            entry_id = item_id[7:]  # Remove "result-" prefix

            # Find the entry in our results
            for entry in self.results:
                if entry["id"] == entry_id:
                    # Show entry detail screen
                    self.app.push_screen(EntryDetailScreen(entry))
                    break

    def action_cancel(self) -> None:
        """Cancel search and go back."""
        self.app.pop_screen()

    def action_quit(self) -> None:
        """Quit the application."""
        self.app.exit()


class LoreTUI(App):
    """Main application for the Lore TUI."""

    CSS = """
    #title {
        dock: top;
        height: 3;
        content-align: center middle;
        background: $primary;
        color: $text;
        text-style: bold;
    }

    #book-title {
        dock: top;
        height: 3;
        content-align: center middle;
        background: $primary;
        color: $text;
        text-style: bold;
    }

    #main-container {
        layout: horizontal;
        height: 100%;
    }

    #sections-panel {
        width: 40%;
        border: solid $primary;
        padding: 1;
    }

    #entries-panel {
        width: 60%;
        border: solid $primary;
        padding: 1;
    }

    .panel-header {
        background: $boost;
        text-style: bold;
        padding: 1;
        margin-bottom: 1;
    }

    ListView {
        height: 100%;
    }

    ListItem {
        padding: 1;
    }

    ListItem:hover {
        background: $boost;
    }

    ListItem > Label {
        width: 100%;
    }

    #search-title {
        dock: top;
        height: 3;
        content-align: center middle;
        background: $primary;
        color: $text;
        text-style: bold;
    }

    #search-input {
        dock: top;
        margin: 1;
    }

    #results-label {
        dock: top;
        background: $boost;
        text-style: bold;
        padding: 1;
        margin-top: 1;
    }

    #search-results {
        height: 100%;
    }
    """

    BINDINGS = [
        Binding("?", "help", "Help", priority=True),
    ]

    def __init__(self, base_dir: str = None):
        super().__init__()

        # Determine base directory
        if base_dir is None:
            # Try to use ~/lore if it exists
            home_skogai = Path.home() / "lore"
            if home_skogai.exists():
                base_dir = str(home_skogai)
            else:
                # Fall back to current directory
                base_dir = str(Path.cwd())

        self.api = LoreAPI(base_dir=base_dir)
        self.title = "Lore Browser"
        self.sub_title = "Interactive Terminal UI for Lore Entries"

    def on_mount(self) -> None:
        """Initialize the application."""
        self.push_screen(BookBrowserScreen(self.api))

    def action_help(self) -> None:
        """Show help information."""
        help_text = """
# Lore Browser Help

## Keyboard Controls

### Navigation
- **Arrow Keys**: Navigate entries
- **Enter**: View full entry
- **Tab**: Switch between panels (in book view)
- **b**: Back to previous view
- **q**: Quit

### Actions
- **/**: Start search
- **?**: Show this help

## Views

### Book Browser
Browse all available lore books. Select a book to view its contents.

### Book Detail
View the structure and entries of a selected book.
- Left panel: Book sections
- Right panel: Entries with summaries

### Entry Detail
View the full content of an entry with markdown formatting.

### Search
Real-time search across all lore entries.
- Type to filter results
- Search by title, content, tags, and summary
- Press Enter to view an entry from results

## Tips
- Use arrow keys to navigate lists
- Press Enter to open/view items
- Press 'b' to go back
- Press 'q' at any time to quit
"""

        class HelpScreen(Screen):
            BINDINGS = [
                Binding("escape", "close", "Close", priority=True),
                Binding("b", "close", "Close", priority=True),
                Binding("q", "quit", "Quit", priority=True),
            ]

            def compose(self) -> ComposeResult:
                yield Header()
                yield VerticalScroll(Markdown(help_text))
                yield Footer()

            def action_close(self) -> None:
                self.app.pop_screen()

            def action_quit(self) -> None:
                self.app.exit()

        self.push_screen(HelpScreen())


def main():
    """Entry point for the Lore TUI."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Interactive Terminal UI for browsing lore entries"
    )
    parser.add_argument(
        "--base-dir",
        type=str,
        default=None,
        help="Base directory for lore data (default: ~/lore or current directory)",
    )

    args = parser.parse_args()

    app = LoreTUI(base_dir=args.base_dir)
    app.run()


if __name__ == "__main__":
    main()
