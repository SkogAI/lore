# Unified Lore CLI

A book-like navigation interface for SkogAI lore management that hides internal IDs and provides intuitive, human-readable access to the lore system.

## Quick Start

```bash
# View all lore books
./lore browse

# View entries in a specific book
./lore browse "Claudes Home"

# Read a specific entry by title
./lore read "The Goose"

# Search for entries
./lore search "forest"

# Show recently viewed items
./lore recent

# Show collection statistics
./lore stats

# Get help
./lore --help
```

## Features

### 🔍 **No More IDs!**
Navigate by title and name instead of remembering cryptic IDs like `entry_1743758088`:
```bash
# Instead of: tools/manage-lore.sh show-entry entry_1743758088
./lore read "Character Name"
```

### 📚 **Book-like Navigation**
Browse lore like reading a book with intuitive commands:
```bash
./lore browse                    # List all books
./lore browse "Book Title"       # View entries in a book
./lore browse -c character       # Filter by category
```

### 🔎 **Powerful Search**
Search across all lore entries with a simple command:
```bash
./lore search "keyword"
```

### 📜 **Session History**
The CLI remembers what you've viewed:
```bash
./lore recent                    # See recently viewed entries and books
```

### 📊 **Statistics & Discovery**
Get insights into your lore collection:
```bash
./lore stats                     # View collection statistics
./lore info                      # Learn about available features
```

### 🎨 **Rich Terminal Display**
Beautiful, readable output with:
- Color-coded information
- Tables and panels
- Markdown rendering for entry content
- Smart text truncation

## Installation

The CLI is already available in the repository. Just make sure you have the dependencies:

```bash
# If using the repository's virtual environment
source .venv/bin/activate

# Or install dependencies manually
pip install typer rich textual
```

## Commands Reference

### `browse [BOOK]`
Browse books and entries with book-like navigation.

**Options:**
- `--category, -c`: Filter entries by category
- `--limit, -l`: Number of items to show (default: 20)

**Examples:**
```bash
./lore browse                          # List all books
./lore browse "Forest Lore"            # View entries in a book
./lore browse -c character             # List all character entries
./lore browse -c place -l 50           # Show 50 place entries
```

### `read TITLE`
Read a specific lore entry by title.

**Options:**
- `--show-id`: Display the internal ID (for debugging)

**Examples:**
```bash
./lore read "Skogix"                   # Read entry by exact title
./lore read "forest" --show-id         # Show ID for reference
```

**Note:** If multiple entries match, you'll see a list to choose from.

### `search QUERY`
Search lore entries across all books.

**Options:**
- `--limit, -l`: Number of results to show (default: 10)

**Examples:**
```bash
./lore search "magic"                  # Search for "magic"
./lore search "forest guardian" -l 20  # Show 20 results
```

### `recent`
Show recently viewed entries and books.

**Options:**
- `--limit, -l`: Number of recent items to show (default: 10)

**Examples:**
```bash
./lore recent                          # Show last 10 items
./lore recent -l 20                    # Show last 20 items
```

### `stats`
Show statistics about the lore collection including:
- Total entries, books, and personas
- Breakdown by category
- Collection health metrics

**Examples:**
```bash
./lore stats
```

### `create TYPE TITLE`
Create a new lore entry or book.

**Options:**
- `--category, -c`: Category for entries (required)
- `--description, -d`: Description for books (optional)

**Examples:**
```bash
./lore create entry "New Character" -c character
./lore create book "Adventure Log" -d "Our party's adventures"
```

**Categories:**
- character
- place
- event
- object
- concept
- custom

### `info`
Show information about the lore CLI and available tools.

**Examples:**
```bash
./lore info
```

## Session Management

The CLI automatically tracks your navigation:
- **Last Viewed**: Remembers the last entry/book you viewed
- **Recent History**: Keeps track of the last 20 items you've accessed
- **Session State**: Stored in `~/.skogai-lore/session.json`

Future enhancements will include bookmarks and more navigation features.

## Comparison with Legacy Tools

### Before (manage-lore.sh)
```bash
# List entries with IDs exposed
./tools/manage-lore.sh list-entries

# Output:
# entry_1743758088 - Character Name (character)
# entry_1743758119 - Place Name (place)

# View specific entry (need to know ID)
./tools/manage-lore.sh show-entry entry_1743758088

# Search requires exact matches
./tools/manage-lore.sh search "exact phrase"
```

### After (lore CLI)
```bash
# List books (more intuitive grouping)
./lore browse

# View entries in a book
./lore browse "Book Name"

# Read by title (no IDs needed)
./lore read "Character Name"

# Fuzzy search with smart matching
./lore search "char"
```

## Integration with Existing Tools

The Unified Lore CLI **wraps** existing tools without replacing them:

- **lore_api.py**: Core API layer (used internally)
- **manage-lore.sh**: Original bash interface (still works)
- **lore_tui.py**: Terminal UI browser (complementary)
- **generate-agent-lore.py**: Agent-specific generation (still available)
- **st-lore-export.py**: SillyTavern export (still available)

All existing functionality is preserved. The CLI provides a unified, user-friendly interface on top.

## Architecture

```
┌─────────────────┐
│   lore (bash)   │  ← Simple wrapper script
└────────┬────────┘
         │
┌────────▼────────┐
│  lore_cli.py    │  ← Main CLI application (typer + rich)
└────────┬────────┘
         │
┌────────▼────────┐
│  lore_api.py    │  ← Core API layer
└────────┬────────┘
         │
┌────────▼────────┐
│ JSON Data Files │  ← Lore entries, books, personas
└─────────────────┘
```

## Technical Details

- **Language**: Python 3.12+
- **CLI Framework**: Typer (provides beautiful CLI with minimal code)
- **Terminal UI**: Rich (provides colors, tables, markdown rendering)
- **Session Storage**: JSON files in `~/.skogai-lore/`
- **Data Location**: `knowledge/expanded/lore/`

## Future Enhancements

Planned features (see issue for full roadmap):
- [ ] Bookmarks system
- [ ] Interactive linking wizard
- [ ] Export/import wizards
- [ ] Inline editing mode
- [ ] Table of contents view
- [ ] Relationship graph visualization
- [ ] Full-text search with relevance ranking
- [ ] Undo/redo for modifications

## Troubleshooting

### "Entry not found"
Try using `./lore search "partial title"` to find the exact title.

### "Multiple matches found"
Be more specific with the title, or browse the book to see all options.

### Virtual environment issues
```bash
# Recreate virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install typer rich textual
```

### Permission denied
```bash
chmod +x lore
chmod +x lore_cli.py
```

## Contributing

This CLI is part of the SkogAI lore system. To contribute:

1. Keep the interface intuitive and ID-free
2. Maintain backward compatibility with lore_api.py
3. Add tests for new features
4. Update this README with new commands
5. Follow the existing code style

## Philosophy

The Unified Lore CLI embodies these principles:

1. **Human-First Design**: Users shouldn't need to remember IDs
2. **Book-like Navigation**: Browse lore as you would read a book
3. **Discovery**: Make relationships and connections obvious
4. **Preservation**: Wrap, don't replace, existing tools
5. **Simplicity**: Common tasks should be simple

---

*Part of the SkogAI Master Knowledge Repository*  
*"Every bash command became a spell, every config file became an artifact"*
