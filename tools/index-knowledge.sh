#!/bin/bash

# Script to generate a searchable index of all knowledge files

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INDEX_FILE="$REPO_ROOT/knowledge/INDEX.md"

echo "# SkogAI Knowledge Index" >"$INDEX_FILE"
echo "" >>"$INDEX_FILE"
echo "Generated: $(date)" >>"$INDEX_FILE"
echo "" >>"$INDEX_FILE"

echo "## Core Knowledge (00-09)" >>"$INDEX_FILE"
if [ -d "$REPO_ROOT/knowledge/core" ]; then
  find "$REPO_ROOT/knowledge/core" -type f -name "*.md" | sort | while read file; do
    id=$(grep -m 1 "ID:" "$file" | sed 's/ID: //' | tr -d '[]')
    title=$(head -n 1 "$file" | sed 's/# //')
    tags=$(grep -m 1 "Tags:" "$file" | sed 's/Tags: //' | tr -d '[]')
    echo "- [$id] $title ($tags)" >>"$INDEX_FILE"
  done
fi

echo "" >>"$INDEX_FILE"
echo "## Expanded Knowledge (10-89)" >>"$INDEX_FILE"
if [ -d "$REPO_ROOT/knowledge/expanded" ]; then
  find "$REPO_ROOT/knowledge/expanded" -type f -name "*.md" | sort | while read file; do
    id=$(grep -m 1 "ID:" "$file" | sed 's/ID: //' | tr -d '[]')
    title=$(head -n 1 "$file" | sed 's/# //')
    tags=$(grep -m 1 "Tags:" "$file" | sed 's/Tags: //' | tr -d '[]')
    echo "- [$id] $title ($tags)" >>"$INDEX_FILE"
  done
fi

echo "" >>"$INDEX_FILE"
echo "## Implementation Knowledge (90-99)" >>"$INDEX_FILE"
if [ -d "$REPO_ROOT/knowledge/implementation" ]; then
  find "$REPO_ROOT/knowledge/implementation" -type f -name "*.md" | sort | while read file; do
    id=$(grep -m 1 "ID:" "$file" | sed 's/ID: //' | tr -d '[]')
    title=$(head -n 1 "$file" | sed 's/# //')
    tags=$(grep -m 1 "Tags:" "$file" | sed 's/Tags: //' | tr -d '[]')
    echo "- [$id] $title ($tags)" >>"$INDEX_FILE"
  done
fi

echo "" >>"$INDEX_FILE"
echo "## Archived Knowledge" >>"$INDEX_FILE"
if [ -d "$REPO_ROOT/knowledge/archived" ]; then
  # Count archived entities
  archived_entries=$(find "$REPO_ROOT/knowledge/archived/lore/entries" -type f -name "*.json" 2>/dev/null | wc -l)
  archived_books=$(find "$REPO_ROOT/knowledge/archived/lore/books" -type f -name "*.json" 2>/dev/null | wc -l)
  archived_personas=$(find "$REPO_ROOT/knowledge/archived/personas" -type f -name "*.json" 2>/dev/null | wc -l)

  echo "- **Entries**: $archived_entries archived test entries" >>"$INDEX_FILE"
  echo "- **Books**: $archived_books archived test books" >>"$INDEX_FILE"
  echo "- **Personas**: $archived_personas archived test personas" >>"$INDEX_FILE"
  echo "- See \`knowledge/archived/CLEANUP_MANIFEST.json\` for details" >>"$INDEX_FILE"
fi
