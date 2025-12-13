#!/bin/bash

# Script to generate a searchable index of all knowledge files

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INDEX_FILE="$REPO_ROOT/knowledge/INDEX.md"

echo "# SkogAI Knowledge Index" >"$INDEX_FILE"
echo "" >>"$INDEX_FILE"
echo "Generated: $(date)" >>"$INDEX_FILE"
echo "" >>"$INDEX_FILE"

echo "## Core Knowledge (00-09)" >>"$INDEX_FILE"
find "$REPO_ROOT/knowledge/core" -type f -name "*.md" | sort | while read file; do
  id=$(grep -m 1 "ID:" "$file" | sed 's/ID: //' | tr -d '[]')
  title=$(head -n 1 "$file" | sed 's/# //')
  tags=$(grep -m 1 "Tags:" "$file" | sed 's/Tags: //' | tr -d '[]')
  echo "- [$id] $title ($tags)" >>"$INDEX_FILE"
done

echo "" >>"$INDEX_FILE"
echo "## Expanded Knowledge (10-89)" >>"$INDEX_FILE"
find "$REPO_ROOT/knowledge/expanded" -type f -name "*.md" | sort | while read file; do
  id=$(grep -m 1 "ID:" "$file" | sed 's/ID: //' | tr -d '[]')
  title=$(head -n 1 "$file" | sed 's/# //')
  tags=$(grep -m 1 "Tags:" "$file" | sed 's/Tags: //' | tr -d '[]')
  echo "- [$id] $title ($tags)" >>"$INDEX_FILE"
done

echo "" >>"$INDEX_FILE"
echo "## Implementation Knowledge (90-99)" >>"$INDEX_FILE"
find "$REPO_ROOT/knowledge/implementation" -type f -name "*.md" | sort | while read file; do
  id=$(grep -m 1 "ID:" "$file" | sed 's/ID: //' | tr -d '[]')
  title=$(head -n 1 "$file" | sed 's/# //')
  tags=$(grep -m 1 "Tags:" "$file" | sed 's/Tags: //' | tr -d '[]')
  echo "- [$id] $title ($tags)" >>"$INDEX_FILE"
done

