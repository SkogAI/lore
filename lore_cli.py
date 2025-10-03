#!/usr/bin/env python3
"""
Unified Lore CLI - A book-like navigation interface for SkogAI lore management.

This tool provides an intuitive, human-readable interface to browse, read, and manage
lore entries, books, and personas without exposing internal IDs to users.
"""

import os
import sys
import json
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from rich import print as rprint

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent))

from agents.api.lore_api import LoreAPI

app = typer.Typer(
    name="lore",
    help="Unified SkogAI Lore Management CLI - Navigate and manage lore like a book",
    add_completion=False,
)
console = Console()

# Session state directory
SESSION_DIR = Path.home() / ".skogai-lore"
SESSION_FILE = SESSION_DIR / "session.json"


def get_lore_api() -> LoreAPI:
    """Get a LoreAPI instance with the repository base directory."""
    base_dir = Path(__file__).parent
    return LoreAPI(str(base_dir))


def load_session() -> Dict[str, Any]:
    """Load session state from disk."""
    if not SESSION_FILE.exists():
        return {
            "last_viewed": None,
            "last_type": None,  # 'entry', 'book', or 'persona'
            "bookmarks": [],
            "recent": [],
        }
    
    try:
        with open(SESSION_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {
            "last_viewed": None,
            "last_type": None,
            "bookmarks": [],
            "recent": [],
        }


def save_session(session: Dict[str, Any]):
    """Save session state to disk."""
    SESSION_DIR.mkdir(exist_ok=True)
    with open(SESSION_FILE, 'w') as f:
        json.dump(session, f, indent=2)


def add_to_recent(title: str, id: str, type: str):
    """Add an item to recently viewed list."""
    session = load_session()
    
    # Remove if already in list
    session["recent"] = [r for r in session["recent"] if r.get("id") != id]
    
    # Add to front
    session["recent"].insert(0, {
        "title": title,
        "id": id,
        "type": type,
        "viewed_at": datetime.now().isoformat()
    })
    
    # Keep only last 20
    session["recent"] = session["recent"][:20]
    
    # Update last viewed
    session["last_viewed"] = id
    session["last_type"] = type
    
    save_session(session)


def find_entry_by_title(api: LoreAPI, title: str) -> Optional[Dict[str, Any]]:
    """Find an entry by exact or partial title match."""
    entries = api.list_lore_entries()
    
    # Try exact match first (case-insensitive)
    for entry in entries:
        if entry.get("title", "").lower() == title.lower():
            return entry
    
    # Try partial match
    matches = [e for e in entries if title.lower() in e.get("title", "").lower()]
    
    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        console.print(f"[yellow]Multiple matches found for '{title}':[/yellow]")
        for i, match in enumerate(matches[:10], 1):
            console.print(f"  {i}. {match['title']}")
        if len(matches) > 10:
            console.print(f"  ... and {len(matches) - 10} more")
        console.print("\n[yellow]Please be more specific.[/yellow]")
        return None
    
    return None


def find_book_by_title(api: LoreAPI, title: str) -> Optional[Dict[str, Any]]:
    """Find a book by exact or partial title match."""
    books = api.list_lore_books()
    
    # Try exact match first (case-insensitive)
    for book in books:
        if book.get("title", "").lower() == title.lower():
            return book
    
    # Try partial match
    matches = [b for b in books if title.lower() in b.get("title", "").lower()]
    
    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        console.print(f"[yellow]Multiple matches found for '{title}':[/yellow]")
        for i, match in enumerate(matches[:10], 1):
            console.print(f"  {i}. {match['title']}")
        if len(matches) > 10:
            console.print(f"  ... and {len(matches) - 10} more")
        console.print("\n[yellow]Please be more specific.[/yellow]")
        return None
    
    return None


@app.command()
def browse(
    book: Optional[str] = typer.Argument(None, help="Book title to browse"),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Filter by category"),
    limit: int = typer.Option(20, "--limit", "-l", help="Number of items to show"),
):
    """
    Browse books and entries with book-like navigation.
    
    Examples:
        lore browse                    # List all books
        lore browse "Forest Lore"      # List entries in a book
        lore browse -c character       # List all character entries
    """
    api = get_lore_api()
    
    if book:
        # Browse entries in a specific book
        book_data = find_book_by_title(api, book)
        if not book_data:
            console.print(f"[red]Book not found: {book}[/red]")
            raise typer.Exit(1)
        
        add_to_recent(book_data["title"], book_data["id"], "book")
        
        # Display book information
        console.print(Panel(
            f"[bold cyan]{book_data['title']}[/bold cyan]\n\n"
            f"{book_data.get('description', 'No description')}\n\n"
            f"[dim]Status: {book_data.get('metadata', {}).get('status', 'unknown')}[/dim]",
            title="📚 Lore Book",
            border_style="cyan"
        ))
        
        # List entries in the book
        entry_ids = book_data.get("entries", [])
        if not entry_ids:
            console.print("\n[yellow]This book has no entries yet.[/yellow]")
            return
        
        console.print(f"\n[bold]Entries in this book ({len(entry_ids)}):[/bold]\n")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=4)
        table.add_column("Title", style="cyan")
        table.add_column("Category", style="yellow")
        table.add_column("Tags", style="dim")
        
        for i, entry_id in enumerate(entry_ids[:limit], 1):
            entry = api.get_lore_entry(entry_id)
            if entry:
                tags = ", ".join(entry.get("tags", [])[:3])
                if len(entry.get("tags", [])) > 3:
                    tags += f" +{len(entry.get('tags', [])) - 3}"
                
                table.add_row(
                    str(i),
                    entry.get("title", "Untitled"),
                    entry.get("category", "unknown"),
                    tags or "-"
                )
        
        console.print(table)
        
        if len(entry_ids) > limit:
            console.print(f"\n[dim]... and {len(entry_ids) - limit} more entries[/dim]")
        
        console.print(f"\n[dim]Use 'lore read \"<entry title>\"' to view an entry[/dim]")
    
    else:
        # Browse all books or entries by category
        if category:
            # List entries by category
            entries = api.list_lore_entries(category=category)
            
            if not entries:
                console.print(f"[yellow]No entries found in category: {category}[/yellow]")
                return
            
            console.print(Panel(
                f"[bold cyan]Category: {category}[/bold cyan]\n\n"
                f"Found {len(entries)} entries",
                title="📖 Lore Entries",
                border_style="cyan"
            ))
            
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("#", style="dim", width=4)
            table.add_column("Title", style="cyan")
            table.add_column("Summary", style="white")
            
            for i, entry in enumerate(entries[:limit], 1):
                summary = entry.get("summary", "")[:60]
                if len(entry.get("summary", "")) > 60:
                    summary += "..."
                
                table.add_row(
                    str(i),
                    entry.get("title", "Untitled"),
                    summary or "[dim]No summary[/dim]"
                )
            
            console.print(table)
            
            if len(entries) > limit:
                console.print(f"\n[dim]... and {len(entries) - limit} more entries[/dim]")
        
        else:
            # List all books
            books = api.list_lore_books()
            
            if not books:
                console.print("[yellow]No lore books found.[/yellow]")
                console.print("\n[dim]Use 'lore create book \"Title\"' to create one[/dim]")
                return
            
            console.print(Panel(
                f"[bold cyan]All Lore Books[/bold cyan]\n\n"
                f"Found {len(books)} books",
                title="📚 Library",
                border_style="cyan"
            ))
            
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("#", style="dim", width=4)
            table.add_column("Title", style="cyan")
            table.add_column("Description", style="white")
            table.add_column("Entries", style="yellow", justify="right")
            table.add_column("Status", style="green")
            
            for i, book in enumerate(books[:limit], 1):
                desc = book.get("description", "")[:50]
                if len(book.get("description", "")) > 50:
                    desc += "..."
                
                table.add_row(
                    str(i),
                    book.get("title", "Untitled"),
                    desc or "[dim]No description[/dim]",
                    str(len(book.get("entries", []))),
                    book.get("metadata", {}).get("status", "unknown")
                )
            
            console.print(table)
            
            if len(books) > limit:
                console.print(f"\n[dim]... and {len(books) - limit} more books[/dim]")
            
            console.print(f"\n[dim]Use 'lore browse \"<book title>\"' to view a book's entries[/dim]")


@app.command()
def read(
    title: str = typer.Argument(..., help="Title of the entry to read"),
    show_id: bool = typer.Option(False, "--show-id", help="Show the internal ID"),
):
    """
    Read a specific lore entry by title.
    
    Examples:
        lore read "Skogix"
        lore read "Forest Guardian" --show-id
    """
    api = get_lore_api()
    
    entry = find_entry_by_title(api, title)
    
    if not entry:
        console.print(f"[red]Entry not found: {title}[/red]")
        console.print("\n[dim]Try 'lore search \"<keyword>\"' to find it[/dim]")
        raise typer.Exit(1)
    
    add_to_recent(entry["title"], entry["id"], "entry")
    
    # Build the display
    content = f"# {entry.get('title', 'Untitled')}\n\n"
    
    if entry.get("summary"):
        content += f"*{entry['summary']}*\n\n---\n\n"
    
    content += entry.get("content", "*No content yet*")
    
    # Metadata section
    metadata_lines = [
        f"**Category:** {entry.get('category', 'unknown')}",
    ]
    
    if entry.get("tags"):
        metadata_lines.append(f"**Tags:** {', '.join(entry['tags'])}")
    
    created_by = entry.get("metadata", {}).get("created_by", "unknown")
    created_at = entry.get("metadata", {}).get("created_at", "unknown")
    metadata_lines.append(f"**Created:** {created_at} by {created_by}")
    
    if show_id:
        metadata_lines.append(f"**ID:** `{entry['id']}`")
    
    content += "\n\n---\n\n" + "\n".join(metadata_lines)
    
    # Display with rich markdown
    console.print(Panel(
        Markdown(content),
        title=f"📖 {entry.get('title', 'Entry')}",
        border_style="cyan",
        expand=False
    ))
    
    # Show book information if entry belongs to a book
    if entry.get("book_id"):
        book = api.get_lore_book(entry["book_id"])
        if book:
            console.print(f"\n[dim]Part of book: [cyan]{book['title']}[/cyan][/dim]")


@app.command()
def search(
    query: str = typer.Argument(..., help="Search query"),
    limit: int = typer.Option(10, "--limit", "-l", help="Number of results to show"),
):
    """
    Search lore entries across all books.
    
    Examples:
        lore search "forest"
        lore search "magic" -l 20
    """
    api = get_lore_api()
    
    results = api.search_lore(query)
    
    if not results:
        console.print(f"[yellow]No results found for: {query}[/yellow]")
        return
    
    console.print(Panel(
        f"[bold cyan]Search Results[/bold cyan]\n\n"
        f"Found {len(results)} matches for '{query}'",
        title="🔍 Search",
        border_style="cyan"
    ))
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=4)
    table.add_column("Title", style="cyan")
    table.add_column("Category", style="yellow")
    table.add_column("Summary", style="white")
    
    for i, entry in enumerate(results[:limit], 1):
        summary = entry.get("summary", "")[:60]
        if len(entry.get("summary", "")) > 60:
            summary += "..."
        
        table.add_row(
            str(i),
            entry.get("title", "Untitled"),
            entry.get("category", "unknown"),
            summary or "[dim]No summary[/dim]"
        )
    
    console.print(table)
    
    if len(results) > limit:
        console.print(f"\n[dim]... and {len(results) - limit} more results[/dim]")
    
    console.print(f"\n[dim]Use 'lore read \"<entry title>\"' to view an entry[/dim]")


@app.command()
def recent(
    limit: int = typer.Option(10, "--limit", "-l", help="Number of recent items to show"),
):
    """
    Show recently viewed entries and books.
    """
    session = load_session()
    recent_items = session.get("recent", [])
    
    if not recent_items:
        console.print("[yellow]No recently viewed items.[/yellow]")
        return
    
    console.print(Panel(
        f"[bold cyan]Recently Viewed[/bold cyan]\n\n"
        f"Last {min(len(recent_items), limit)} items",
        title="📜 History",
        border_style="cyan"
    ))
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=4)
    table.add_column("Title", style="cyan")
    table.add_column("Type", style="yellow")
    table.add_column("Viewed", style="dim")
    
    for i, item in enumerate(recent_items[:limit], 1):
        viewed_at = datetime.fromisoformat(item["viewed_at"]).strftime("%Y-%m-%d %H:%M")
        
        table.add_row(
            str(i),
            item.get("title", "Unknown"),
            item.get("type", "unknown"),
            viewed_at
        )
    
    console.print(table)


@app.command()
def stats():
    """
    Show statistics about the lore collection.
    """
    api = get_lore_api()
    
    entries = api.list_lore_entries()
    books = api.list_lore_books()
    personas = api.list_personas()
    
    # Category breakdown
    categories = {}
    for entry in entries:
        cat = entry.get("category", "unknown")
        categories[cat] = categories.get(cat, 0) + 1
    
    # Build stats display
    stats_text = f"""[bold cyan]Lore Collection Statistics[/bold cyan]

📖 **Entries:** {len(entries)}
📚 **Books:** {len(books)}
👤 **Personas:** {len(personas)}

**Entries by Category:**
"""
    
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        stats_text += f"\n  • {cat}: {count}"
    
    console.print(Panel(
        stats_text,
        title="📊 Statistics",
        border_style="cyan"
    ))


@app.command()
def create(
    type: str = typer.Argument(..., help="Type to create: 'entry' or 'book'"),
    title: str = typer.Argument(..., help="Title of the new item"),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Category (for entries)"),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="Description (for books)"),
):
    """
    Create a new lore entry or book.
    
    Examples:
        lore create entry "New Character" -c character
        lore create book "Adventure Log" -d "Our party's adventures"
    """
    api = get_lore_api()
    
    if type.lower() == "entry":
        if not category:
            console.print("[yellow]Please specify a category with --category[/yellow]")
            console.print("Categories: character, place, event, object, concept, custom")
            raise typer.Exit(1)
        
        entry = api.create_lore_entry(
            title=title,
            content="",
            category=category,
            summary="",
        )
        
        console.print(f"[green]✓[/green] Created entry: [cyan]{title}[/cyan]")
        console.print(f"[dim]ID: {entry['id']}[/dim]")
        console.print(f"\nEdit the file at: [yellow]{api.lore_entries_dir}/{entry['id']}.json[/yellow]")
        
    elif type.lower() == "book":
        book = api.create_lore_book(
            title=title,
            description=description or "",
        )
        
        console.print(f"[green]✓[/green] Created book: [cyan]{title}[/cyan]")
        console.print(f"[dim]ID: {book['id']}[/dim]")
        console.print(f"\nEdit the file at: [yellow]{api.lore_books_dir}/{book['id']}.json[/yellow]")
        
    else:
        console.print(f"[red]Unknown type: {type}[/red]")
        console.print("Valid types: entry, book")
        raise typer.Exit(1)


@app.command()
def info():
    """
    Show information about the lore CLI and available tools.
    """
    info_text = """[bold cyan]SkogAI Unified Lore CLI[/bold cyan]

This tool provides a book-like interface for browsing and managing lore.

**Key Features:**
• Navigate by title/name instead of IDs
• Browse books like pages
• Search across all lore
• Session history and bookmarks
• Rich terminal formatting

**Quick Start:**
• `lore browse` - List all books
• `lore browse "Book Name"` - View entries in a book
• `lore read "Entry Title"` - Read an entry
• `lore search "keyword"` - Search for entries
• `lore recent` - Show recently viewed items

**Legacy Tools:**
• `tools/manage-lore.sh` - Original bash interface
• `lore_tui.py` - Terminal UI browser
• `agents/api/lore_api.py` - Python API layer

For detailed help on any command, use: `lore <command> --help`
"""
    
    console.print(Panel(
        info_text,
        title="ℹ️  Lore CLI Info",
        border_style="cyan"
    ))


if __name__ == "__main__":
    app()
