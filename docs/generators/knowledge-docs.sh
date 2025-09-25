#!/bin/bash

# Generate documentation from knowledge files

OUTPUT_DIR="/home/skogix/skogai/docs/generated"
mkdir -p $OUTPUT_DIR

# Generate main index
echo "# SkogAI Knowledge Documentation" > "$OUTPUT_DIR/index.md"
echo "" >> "$OUTPUT_DIR/index.md"
echo "Generated: $(date)" >> "$OUTPUT_DIR/index.md"
echo "" >> "$OUTPUT_DIR/index.md"

# Generate sections for each knowledge category
for category in "core" "expanded" "implementation"; do
  upper_category=$(echo $category | tr '[:lower:]' '[:upper:]')
  echo "## $upper_category Knowledge" >> "$OUTPUT_DIR/index.md"
  echo "" >> "$OUTPUT_DIR/index.md"
  
  # Create category file
  cat_file="$OUTPUT_DIR/$category-knowledge.md"
  echo "# $upper_category Knowledge" > "$cat_file"
  echo "" >> "$cat_file"
  
  # Find and process all markdown files in this category
  find "/home/skogix/skogai/knowledge/$category" -type f -name "*.md" | sort | while read file; do
    filename=$(basename "$file")
    id=$(grep -m 1 "ID:" "$file" | sed 's/ID: //' | tr -d '[]')
    title=$(head -n 1 "$file" | sed 's/# //')
    
    # Add to index
    echo "- [$title]($category-knowledge.md#$id)" >> "$OUTPUT_DIR/index.md"
    
    # Add to category file
    echo "### $title" >> "$cat_file"
    echo "" >> "$cat_file"
    echo "ID: $id" >> "$cat_file"
    echo "" >> "$cat_file"
    
    # Extract and add summary
    summary=$(grep -A 2 "## Summary" "$file" | tail -n 1)
    echo "$summary" >> "$cat_file"
    echo "" >> "$cat_file"
    
    # Add link to full document
    rel_path=${file#/home/skogix/skogai/}
    echo "[View full document](../../$rel_path)" >> "$cat_file"
    echo "" >> "$cat_file"
  done
  
  echo "" >> "$OUTPUT_DIR/index.md"
done

echo "Documentation generated successfully in $OUTPUT_DIR"