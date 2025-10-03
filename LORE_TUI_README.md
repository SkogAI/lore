# Lore Browser - Interactive Terminal UI

An interactive terminal UI for browsing lore entries with keyboard navigation and rich visual feedback.

## Features

### 🎯 Core Navigation
- **Arrow Keys**: Navigate through lists
- **Enter**: View full entry or open book
- **Tab**: Switch between panels (in book view)
- **b**: Back to previous view
- **q**: Quit application
- **?**: Show help

### 📚 Book Browser
Browse all available lore books with:
- Book titles and descriptions
- Entry counts for each book
- Quick navigation to book contents

### 📖 Book Detail View
Explore book structure with:
- **Left Panel**: Book sections with entry counts
- **Right Panel**: Entry list with summaries
- Navigate between sections and entries

### 📝 Entry Viewer
View full entries with:
- Markdown rendering
- Syntax highlighting
- Metadata display (category, tags)
- Relationship links

### 🔍 Search
Real-time search across all lore entries:
- Search by title, content, tags, and summary
- Results update as you type
- Navigate directly to entries from search results
- Press `/` from book browser to open search

## Installation

### Dependencies

The TUI requires the `textual` library. Install it with:

```bash
# Using uv (recommended)
uv pip install textual

# Or using pip
pip install textual
```

Or add to `pyproject.toml`:

```toml
dependencies = [
    "textual>=1.0.0",
]
```

### Setup

1. Ensure the lore API is configured:
   ```bash
   # The TUI uses the LoreAPI which expects lore data at:
   # ~/skogai/knowledge/expanded/lore/
   # or you can specify a custom base directory
   ```

2. Make the launch script executable:
   ```bash
   chmod +x lore_browse.sh
   ```

## Usage

### Basic Usage

```bash
# Launch the browser (uses ~/skogai or current directory)
./lore_browse.sh

# Or run directly with Python
python3 lore_tui.py
```

### Advanced Usage

```bash
# Specify a custom base directory
python3 lore_tui.py --base-dir /path/to/lore/data

# View help
python3 lore_tui.py --help
```

## Visual Layout

```
┌─────────────────────────────────────────────┐
│ 📚 Eldoria: Land of Magic    [3 entries]    │
├─────────────────────────────────────────────┤
│ Sections:          │ Entries:               │
│ > Introduction     │ • The Forest Glade     │
│   World Info (3)   │   A protected...       │
│   Characters (5)   │ • Shadowfangs          │
│                    │   Corrupted beasts...  │
└─────────────────────────────────────────────┘
[↑↓] Navigate [Enter] View [Tab] Switch [q] Quit
```

## Keyboard Reference

### Global Controls
- **q**: Quit the application
- **?**: Show help screen

### Navigation
- **↑/↓**: Move up/down in lists
- **Enter**: Select item
- **b**: Go back to previous screen
- **Escape**: Close help screen

### Search
- **/**: Open search interface
- **Type**: Real-time search as you type
- **Enter**: View entry from results
- **Escape/b**: Close search

### Future Features (Coming Soon)
- **n**: New entry in current book
- **e**: Edit current entry
- **l**: Link entries
- **x**: Export selection
- **i**: Import from file

## Architecture

### Components

1. **LoreTUI (Main App)**
   - Manages application state
   - Handles screen navigation
   - Provides help system

2. **BookBrowserScreen**
   - Lists all lore books
   - Shows book metadata
   - Entry point for book navigation

3. **BookDetailScreen**
   - Displays book structure
   - Shows sections and entries
   - Dual-panel layout

4. **EntryDetailScreen**
   - Renders full entry content
   - Markdown formatting
   - Displays metadata and relationships

### Data Flow

```
LoreAPI → BookBrowserScreen → BookDetailScreen → EntryDetailScreen
   ↓            ↓                    ↓                  ↓
 JSON Files   Book List         Entry List        Full Entry
```

## Customization

### Styling

The TUI uses Textual's CSS-like styling. Modify the `CSS` property in `LoreTUI` class to customize:

- Colors: `$primary`, `$boost`, `$text`
- Layouts: Panel widths, borders
- Typography: Font styles, padding

### Base Directory

The TUI automatically looks for lore data in:
1. `~/skogai/` (if it exists)
2. Current working directory
3. Custom path via `--base-dir`

## Troubleshooting

### No books found
- Ensure lore data exists in the base directory
- Check paths: `{base_dir}/knowledge/expanded/lore/books/`
- Run the lore demo first: `python demo/lore_demo.py`

### Import errors
- Verify textual is installed: `pip list | grep textual`
- Check Python version: requires Python 3.13+
- Install missing dependencies: `uv pip install -r pyproject.toml`

### Display issues
- Use a modern terminal with Unicode support
- Ensure terminal size is adequate (min 80x24)
- Try different color schemes if text is hard to read

## Development

### Adding New Features

1. **Search Functionality**
   - Implement in `action_search()` method
   - Use LoreAPI's `search_lore()` method
   - Create SearchResultsScreen

2. **Entry Editing**
   - Add edit bindings
   - Create EntryEditScreen with TextArea
   - Update entries via LoreAPI

3. **Relationship Navigation**
   - Parse relationship data
   - Make relationships clickable
   - Navigate between related entries

### Testing

```bash
# Manual testing workflow
python3 lore_tui.py

# Test with demo data
python3 demo/lore_demo.py  # Create test data
python3 lore_tui.py        # Browse test data
```

## Integration

### CLI Integration

Add to your main CLI:

```python
import subprocess

def browse_lore():
    """Launch interactive lore browser."""
    subprocess.run(["python3", "lore_tui.py"])
```

### API Integration

Use the TUI programmatically:

```python
from lore_tui import LoreTUI

app = LoreTUI(base_dir="/custom/path")
app.run()
```

## Quick Start Demo

Want to try it out? Run the demo script:

```bash
# Create sample lore data and launch TUI
python3 demo_tui.py
```

This will:
1. Create a sample "Eldoria" lore book with 5 entries
2. Set up demo data in `demo_tui_data/` directory
3. Optionally launch the TUI to browse the demo data

## Future Enhancements

- [x] Real-time search with filtering
- [ ] Entry creation and editing
- [ ] Relationship graph visualization (ASCII art)
- [ ] Export selected entries
- [ ] Import from various formats
- [ ] Mouse support for navigation
- [ ] Color themes and customization
- [ ] Bookmark favorite entries
- [ ] Recent entries history
- [ ] Multi-book search

## Credits

Built with [Textual](https://textual.textualize.io/) - a TUI framework for Python.

Part of the SkogAI lore management system.

---

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
