#!/usr/bin/env python3
"""
Interactive Terminal UI for browsing lore entries.
Provides Vim-style keyboard navigation and rich visual feedback.
"""

import os
import sys
import json
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
from textual import events


class LoreDataAccess:
    """Direct JSON file access for lore data (read-only)."""

    def __init__(self, base_dir: str = None):
        """Initialize with paths to lore storage."""
        if base_dir is None:
            base_dir = Path(__file__).parent.parent
        self.base_dir = Path(base_dir)
        self.lore_entries_dir = self.base_dir / "knowledge" / "expanded" / "lore" / "entries"
        self.lore_books_dir = self.base_dir / "knowledge" / "expanded" / "lore" / "books"

        # Ensure directories exist
        self.lore_entries_dir.mkdir(parents=True, exist_ok=True)
        self.lore_books_dir.mkdir(parents=True, exist_ok=True)

    def list_lore_books(self) -> List[Dict[str, Any]]:
        """List all lore books by reading JSON files directly."""
        books = []
        for book_file in self.lore_books_dir.glob("*.json"):
            try:
                with open(book_file, "r") as f:
                    book = json.load(f)
                    books.append(book)
            except (json.JSONDecodeError, OSError):
                # Skip invalid or unreadable files
                pass
        return books

    def get_lore_book(self, book_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a lore book by ID."""
        book_path = self.lore_books_dir / f"{book_id}.json"
        if not book_path.exists():
            return None
        try:
            with open(book_path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return None

    def list_lore_entries(self, category: str = None) -> List[Dict[str, Any]]:
        """List all lore entries, optionally filtered by category."""
        entries = []
        for entry_file in self.lore_entries_dir.glob("*.json"):
            try:
                with open(entry_file, "r") as f:
                    entry = json.load(f)
                    if category is None or entry.get("category") == category:
                        entries.append(entry)
            except (json.JSONDecodeError, OSError):
                # Skip invalid or unreadable files
                pass
        return entries

    def get_lore_entry(self, entry_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a lore entry by ID."""
        entry_path = self.lore_entries_dir / f"{entry_id}.json"
        if not entry_path.exists():
            return None
        try:
            with open(entry_path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return None

    def search_lore(self, query: str) -> List[Dict[str, Any]]:
        """Search lore entries by keyword."""
        results = []
        seen_ids = set()
        query_lower = query.lower()

        for entry in self.list_lore_entries():
            entry_id = entry.get("id")
            if entry_id is None or entry_id in seen_ids:
                continue

            searchable_text = " ".join([
                entry.get("title", ""),
                entry.get("content", ""),
                entry.get("summary", ""),
                " ".join(entry.get("tags", [])),
            ]).lower()

            if query_lower in searchable_text:
                results.append(entry)
                seen_ids.add(entry_id)

        return results


# Vim keybindings mixin for screens with ListView
class VimNavigationMixin:
    """Mixin providing Vim-style navigation for screens with ListViews."""

    _pending_g: bool = False  # Track 'g' key for 'gg' command

    def get_active_list_view(self) -> Optional[ListView]:
        """Override in subclass to return the currently active ListView."""
        return None

    def vim_select_current(self) -> None:
        """Override in subclass to handle selection of current item."""
        pass

    def on_key(self, event: events.Key) -> None:
        """Handle Vim-style key navigation."""
        list_view = self.get_active_list_view()
        if list_view is None:
            return

        key = event.key

        # Handle 'gg' for go to top
        if self._pending_g:
            self._pending_g = False
            if key == "g":
                # gg - go to first item
                if len(list_view) > 0:
                    list_view.index = 0
                event.prevent_default()
                return

        if key == "j":
            # Move down
            if list_view.index < len(list_view) - 1:
                list_view.index += 1
            event.prevent_default()
        elif key == "k":
            # Move up
            if list_view.index > 0:
                list_view.index -= 1
            event.prevent_default()
        elif key == "g":
            # Start 'gg' sequence
            self._pending_g = True
            event.prevent_default()
        elif key == "G":
            # Go to last item
            if len(list_view) > 0:
                list_view.index = len(list_view) - 1
            event.prevent_default()
        elif key == "ctrl+d":
            # Page down (move 10 items)
            new_index = min(list_view.index + 10, len(list_view) - 1)
            if new_index >= 0:
                list_view.index = new_index
            event.prevent_default()
        elif key == "ctrl+u":
            # Page up (move 10 items)
            new_index = max(list_view.index - 10, 0)
            list_view.index = new_index
            event.prevent_default()
        elif key == "l":
            # Select current item (like Enter)
            self.vim_select_current()
            event.prevent_default()
        elif key == "h":
            # Go back (like 'b')
            if hasattr(self, "action_back"):
                self.action_back()
            elif hasattr(self, "action_cancel"):
                self.action_cancel()
            event.prevent_default()


class EntryDetailScreen(VimNavigationMixin, Screen):
    """Screen for viewing a full entry with markdown rendering."""

    BINDINGS = [
        Binding("h", "back", "←Back", priority=True),
        Binding("b", "back", "Back"),
        Binding("q", "quit", "Quit", priority=True),
        Binding("j", "scroll_down", "↓", show=False),
        Binding("k", "scroll_up", "↑", show=False),
        Binding("ctrl+d", "page_down", "PgDn", show=False),
        Binding("ctrl+u", "page_up", "PgUp", show=False),
        Binding("g", "go_top", "Top", show=False),
        Binding("G", "go_bottom", "Bottom", show=False),
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

    def action_scroll_down(self) -> None:
        """Scroll content down (j key)."""
        scroll = self.query_one(VerticalScroll)
        scroll.scroll_down()

    def action_scroll_up(self) -> None:
        """Scroll content up (k key)."""
        scroll = self.query_one(VerticalScroll)
        scroll.scroll_up()

    def action_page_down(self) -> None:
        """Page down (Ctrl+d)."""
        scroll = self.query_one(VerticalScroll)
        scroll.scroll_page_down()

    def action_page_up(self) -> None:
        """Page up (Ctrl+u)."""
        scroll = self.query_one(VerticalScroll)
        scroll.scroll_page_up()

    def action_go_top(self) -> None:
        """Go to top (g key, part of gg)."""
        scroll = self.query_one(VerticalScroll)
        scroll.scroll_home()

    def action_go_bottom(self) -> None:
        """Go to bottom (G key)."""
        scroll = self.query_one(VerticalScroll)
        scroll.scroll_end()


class BookDetailScreen(VimNavigationMixin, Screen):
    """Screen for viewing book structure and entries."""

    BINDINGS = [
        Binding("h", "back", "←Back", priority=True),
        Binding("b", "back", "Back"),
        Binding("q", "quit", "Quit", priority=True),
        Binding("?", "help", "Help", priority=True),
        Binding("l", "select", "Select", show=False),
        Binding("tab", "switch_panel", "Tab", priority=True),
    ]

    def __init__(self, book: Dict[str, Any], data_access: LoreDataAccess, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.book = book
        self.data_access = data_access
        self.entries: List[Dict[str, Any]] = []
        self.selected_entry_index = 0
        self._active_panel = "entries"  # Track which panel is active
        self._pending_g = False

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
            entry = self.data_access.get_lore_entry(entry_id)
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

    def get_active_list_view(self) -> Optional[ListView]:
        """Return the currently active ListView."""
        if self._active_panel == "sections":
            return self.query_one("#sections-list", ListView)
        return self.query_one("#entries-list", ListView)

    def vim_select_current(self) -> None:
        """Handle selection via 'l' key."""
        self.action_select()

    def action_switch_panel(self) -> None:
        """Switch between sections and entries panels."""
        if self._active_panel == "entries":
            self._active_panel = "sections"
            self.query_one("#sections-list", ListView).focus()
        else:
            self._active_panel = "entries"
            self.query_one("#entries-list", ListView).focus()

    def action_select(self) -> None:
        """Select the current item in the active list."""
        list_view = self.get_active_list_view()
        if list_view and list_view.index is not None and list_view.index >= 0:
            if list_view.index < len(list_view):
                item = list_view.children[list_view.index]
                if hasattr(item, "id") and item.id:
                    if item.id.startswith("entry-"):
                        entry_id = item.id[6:]
                        for entry in self.entries:
                            if entry["id"] == entry_id:
                                self.app.push_screen(EntryDetailScreen(entry))
                                break

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


class BookBrowserScreen(VimNavigationMixin, Screen):
    """Main screen for browsing all books."""

    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("/", "search", "Search", priority=True),
        Binding("?", "help", "Help", priority=True),
        Binding("l", "select", "Select", show=False),
    ]

    def __init__(self, data_access: LoreDataAccess, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_access = data_access
        self.books: List[Dict[str, Any]] = []
        self._pending_g = False

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("📚 Lore Books", id="title")
        yield ListView(id="books-list")
        yield Footer()

    def on_mount(self) -> None:
        """Populate the list when the screen is mounted."""
        # Load all books
        self.books = self.data_access.list_lore_books()
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

    def get_active_list_view(self) -> Optional[ListView]:
        """Return the books list."""
        return self.query_one("#books-list", ListView)

    def vim_select_current(self) -> None:
        """Handle selection via 'l' key."""
        self.action_select()

    def action_select(self) -> None:
        """Select the current book."""
        list_view = self.get_active_list_view()
        if list_view and list_view.index is not None and list_view.index >= 0:
            if list_view.index < len(self.books):
                book = self.books[list_view.index]
                self.app.push_screen(BookDetailScreen(book, self.data_access))

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
                    self.app.push_screen(BookDetailScreen(book, self.data_access))
                    break

    def action_quit(self) -> None:
        """Quit the application."""
        self.app.exit()

    def action_search(self) -> None:
        """Open search interface."""
        self.app.push_screen(SearchScreen(self.data_access))

    def action_help(self) -> None:
        """Show help screen."""
        self.app.action_help()


class SearchScreen(VimNavigationMixin, Screen):
    """Screen for searching lore entries."""

    BINDINGS = [
        Binding("escape", "cancel", "Cancel", priority=True),
        Binding("h", "cancel", "←Back", priority=True),
        Binding("b", "cancel", "Back"),
        Binding("q", "quit", "Quit", priority=True),
        Binding("l", "select", "Select", show=False),
    ]

    def __init__(self, data_access: LoreDataAccess, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_access = data_access
        self.results: List[Dict[str, Any]] = []
        self._pending_g = False
        self._in_search_input = True  # Track if we're in search input

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("🔍 Search Lore Entries", id="search-title")
        yield Input(placeholder="Enter search query (Esc to navigate results)...", id="search-input")
        yield Static("Results:", id="results-label")
        yield ListView(id="search-results")
        yield Footer()

    def on_mount(self) -> None:
        """Focus the search input on mount."""
        self.query_one("#search-input", Input).focus()

    def get_active_list_view(self) -> Optional[ListView]:
        """Return the results list if not in search input."""
        if self._in_search_input:
            return None
        return self.query_one("#search-results", ListView)

    def vim_select_current(self) -> None:
        """Handle selection via 'l' key."""
        if not self._in_search_input:
            self.action_select()

    def action_select(self) -> None:
        """Select the current result."""
        list_view = self.query_one("#search-results", ListView)
        if list_view.index is not None and 0 <= list_view.index < len(self.results):
            entry = self.results[list_view.index]
            self.app.push_screen(EntryDetailScreen(entry))

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle Enter in search input - switch to results."""
        self._in_search_input = False
        self.query_one("#search-results", ListView).focus()

    def on_key(self, event: events.Key) -> None:
        """Handle key events for mode switching."""
        if event.key == "escape":
            if self._in_search_input:
                # Switch to results navigation
                self._in_search_input = False
                self.query_one("#search-results", ListView).focus()
                event.prevent_default()
            else:
                # Go back
                self.action_cancel()
                event.prevent_default()
        elif event.key == "i" and not self._in_search_input:
            # Switch back to search input (like Vim insert mode)
            self._in_search_input = True
            self.query_one("#search-input", Input).focus()
            event.prevent_default()
        elif not self._in_search_input:
            # Use vim navigation when not in search input
            super().on_key(event)

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle search input changes."""
        query = event.value.strip()

        # Get the results list
        results_list = self.query_one("#search-results", ListView)
        results_list.clear()

        if len(query) < 2:
            return

        # Search for entries
        self.results = self.data_access.search_lore(query)

        # Display results
        if not self.results:
            results_list.append(ListItem(Label("No results found")))
        else:
            for idx, entry in enumerate(self.results):
                title = entry.get("title", "Untitled")
                summary = entry.get("summary", "")
                truncated_summary = (
                    summary[:60] + "..." if len(summary) > 60 else summary
                )
                category = entry.get("category", "unknown")

                item = ListItem(
                    Label(f"📝 {title} [{category}]\n   {truncated_summary}"),
                    id=f"result-{entry['id']}-{idx}",
                )
                results_list.append(item)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle result selection."""
        item_id = event.item.id
        if item_id and item_id.startswith("result-"):
            # Extract index suffix from the ID (format: result-{entry_id}-{idx})
            # Use the index to look up the entry directly from self.results
            try:
                idx = int(item_id.rsplit("-", 1)[1])
                if 0 <= idx < len(self.results):
                    entry = self.results[idx]
                    # Show entry detail screen
                    self.app.push_screen(EntryDetailScreen(entry))
            except (ValueError, IndexError):
                # Fall back to searching by entry ID if index parsing fails
                entry_id = item_id[7:].rsplit("-", 1)[0]
                for entry in self.results:
                    if entry.get("id") == entry_id:
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

        self.data_access = LoreDataAccess(base_dir=base_dir)
        self.title = "Lore Browser"
        self.sub_title = "Interactive Terminal UI for Lore Entries"

    def on_mount(self) -> None:
        """Initialize the application."""
        self.push_screen(BookBrowserScreen(self.data_access))

    def action_help(self) -> None:
        """Show help information."""
        help_text = """
# Lore Browser Help

## Vim-Style Navigation

### Movement
- **j/↓**: Move down
- **k/↑**: Move up
- **gg**: Go to first item
- **G**: Go to last item
- **Ctrl+d**: Page down
- **Ctrl+u**: Page up

### Actions
- **l/Enter**: Select/Open item
- **h/b**: Go back
- **q**: Quit
- **/**: Start search
- **?**: Show this help
- **Tab**: Switch panels (in book view)

## Views

### Book Browser
Browse all available lore books.
- Use **j/k** to navigate
- Press **l** or **Enter** to open a book

### Book Detail
View the structure and entries of a selected book.
- Left panel: Book sections
- Right panel: Entries with summaries
- **Tab**: Switch between panels

### Entry Detail
View the full content of an entry with markdown formatting.
- **j/k**: Scroll content
- **Ctrl+d/u**: Page down/up
- **gg/G**: Top/Bottom

### Search
Real-time search across all lore entries.
- Type to filter results
- **Esc**: Switch to results navigation
- **i**: Switch back to search input
- **j/k**: Navigate results
- **l/Enter**: View selected entry

## Tips
- Think of it like Vim: **h**=left/back, **j**=down, **k**=up, **l**=right/select
- **gg** goes to top, **G** goes to bottom
- **Ctrl+d/u** for fast scrolling
"""

        class HelpScreen(Screen):
            BINDINGS = [
                Binding("escape", "close", "Close", priority=True),
                Binding("h", "close", "←Back", priority=True),
                Binding("b", "close", "Back"),
                Binding("q", "quit", "Quit", priority=True),
                Binding("j", "scroll_down", "↓", show=False),
                Binding("k", "scroll_up", "↑", show=False),
                Binding("ctrl+d", "page_down", "PgDn", show=False),
                Binding("ctrl+u", "page_up", "PgUp", show=False),
                Binding("G", "go_bottom", "Bottom", show=False),
            ]

            def compose(self) -> ComposeResult:
                yield Header()
                yield VerticalScroll(Markdown(help_text), id="help-scroll")
                yield Footer()

            def action_close(self) -> None:
                self.app.pop_screen()

            def action_quit(self) -> None:
                self.app.exit()

            def action_scroll_down(self) -> None:
                self.query_one("#help-scroll", VerticalScroll).scroll_down()

            def action_scroll_up(self) -> None:
                self.query_one("#help-scroll", VerticalScroll).scroll_up()

            def action_page_down(self) -> None:
                self.query_one("#help-scroll", VerticalScroll).scroll_page_down()

            def action_page_up(self) -> None:
                self.query_one("#help-scroll", VerticalScroll).scroll_page_up()

            def action_go_bottom(self) -> None:
                self.query_one("#help-scroll", VerticalScroll).scroll_end()

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
