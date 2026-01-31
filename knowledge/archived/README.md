# Archived Lore Entities

This directory contains lore entities that have been archived (not deleted) during cleanup operations.

## Structure

The archive structure mirrors `knowledge/expanded/`:

```
knowledge/archived/
├── lore/
│   ├── entries/    # Archived lore entries
│   └── books/      # Archived lore books
└── personas/       # Archived personas
```

## Cleanup History

- **2025-12-31**: Phase 1 cleanup - 871 empty/unlinked test entities
  - 828 entries with empty content (0 chars)
  - 10 books with no entries
  - 33 personas with no lore books
  - See CLEANUP_MANIFEST.json for full details

## Restoration

To restore an archived entity, simply move it back to the corresponding location in `knowledge/expanded/`.

## Why Archive Instead of Delete?

Following the lore project philosophy: "Historical preservation is critical - don't delete lore archives"
