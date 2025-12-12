#!/bin/bash

# Script to generate a searchable index of all knowledge files

echo "# SkogAI Knowledge Index" >/home/skogix/lore/knowledge/INDEX.md
echo "" >>/home/skogix/lore/knowledge/INDEX.md
echo "Generated: $(date)" >>/home/skogix/lore/knowledge/INDEX.md
echo "" >>/home/skogix/lore/knowledge/INDEX.md

echo "## Core Knowledge (00-09)" >>/home/skogix/lore/knowledge/INDEX.md
find /home/skogix/lore/knowledge/core -type f -name "*.md" | sort | while read file; do
  id=$(grep -m 1 "ID:" "$file" | sed 's/ID: //' | tr -d '[]')
  title=$(head -n 1 "$file" | sed 's/# //')
  tags=$(grep -m 1 "Tags:" "$file" | sed 's/Tags: //' | tr -d '[]')
  echo "- [$id] $title ($tags)" >>/home/skogix/lore/knowledge/INDEX.md
done

echo "" >>/home/skogix/lore/knowledge/INDEX.md
echo "## Expanded Knowledge (10-89)" >>/home/skogix/lore/knowledge/INDEX.md
find /home/skogix/lore/knowledge/expanded -type f -name "*.md" | sort | while read file; do
  id=$(grep -m 1 "ID:" "$file" | sed 's/ID: //' | tr -d '[]')
  title=$(head -n 1 "$file" | sed 's/# //')
  tags=$(grep -m 1 "Tags:" "$file" | sed 's/Tags: //' | tr -d '[]')
  echo "- [$id] $title ($tags)" >>/home/skogix/lore/knowledge/INDEX.md
done

echo "" >>/home/skogix/lore/knowledge/INDEX.md
echo "## Implementation Knowledge (90-99)" >>/home/skogix/lore/knowledge/INDEX.md
find /home/skogix/lore/knowledge/implementation -type f -name "*.md" | sort | while read file; do
  id=$(grep -m 1 "ID:" "$file" | sed 's/ID: //' | tr -d '[]')
  title=$(head -n 1 "$file" | sed 's/# //')
  tags=$(grep -m 1 "Tags:" "$file" | sed 's/Tags: //' | tr -d '[]')
  echo "- [$id] $title ($tags)" >>/home/skogix/lore/knowledge/INDEX.md
done

