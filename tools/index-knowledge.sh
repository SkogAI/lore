#!/bin/bash

# Script to generate a searchable index of all knowledge files

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
KNOWLEDGE_DIR="${BASE_DIR}/knowledge"
INDEX_FILE="${KNOWLEDGE_DIR}/INDEX.md"

echo "# SkogAI Knowledge Index" >"$INDEX_FILE"
echo "" >>"$INDEX_FILE"
echo "Generated: $(date)" >>"$INDEX_FILE"
echo "" >>"$INDEX_FILE"

echo "## Core Knowledge (00-09)" >>"$INDEX_FILE"
find "$KNOWLEDGE_DIR/core" -type f -name "*.md" | sort | while read file; do
  id=$(grep -m 1 "ID:" "$file" | sed 's/ID: //' | tr -d '[]')
  title=$(head -n 1 "$file" | sed 's/# //')
  tags=$(grep -m 1 "Tags:" "$file" | sed 's/Tags: //' | tr -d '[]')
  echo "- [$id] $title ($tags)" >>"$INDEX_FILE"
done

echo "" >>"$INDEX_FILE"
echo "## Expanded Knowledge (10-89)" >>"$INDEX_FILE"
find "$KNOWLEDGE_DIR/expanded" -type f -name "*.md" | sort | while read file; do
  id=$(grep -m 1 "ID:" "$file" | sed 's/ID: //' | tr -d '[]')
  title=$(head -n 1 "$file" | sed 's/# //')
  tags=$(grep -m 1 "Tags:" "$file" | sed 's/Tags: //' | tr -d '[]')
  echo "- [$id] $title ($tags)" >>"$INDEX_FILE"
done

echo "" >>"$INDEX_FILE"
echo "## Implementation Knowledge (90-99)" >>"$INDEX_FILE"
find "$KNOWLEDGE_DIR/implementation" -type f -name "*.md" | sort | while read file; do
  id=$(grep -m 1 "ID:" "$file" | sed 's/ID: //' | tr -d '[]')
  title=$(head -n 1 "$file" | sed 's/# //')
  tags=$(grep -m 1 "Tags:" "$file" | sed 's/Tags: //' | tr -d '[]')
  echo "- [$id] $title ($tags)" >>"$INDEX_FILE"
done
<<<<<<< HEAD

=======
>>>>>>> 687095b (```json)
