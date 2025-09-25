#!/bin/bash

# Copy all knowledge directories to master location
MASTER_DIR="/mnt/extra/backup/skogai-old-all/MASTER_KNOWLEDGE_COMPLETE"

echo "Creating master knowledge directory..."
mkdir -p "$MASTER_DIR"

echo "Starting complete knowledge copy operation..."

# Counter for statistics
total=0
copied=0
failed=0

# Copy each knowledge directory
for dir in \
    "/home/skogix/amy/knowledge" \
    "/home/skogix/dev/dot-claude/knowledge" \
    "/home/skogix/dot3/knowledge" \
    "/home/skogix/dot/knowledge" \
    "/home/skogix/goose/knowledge" \
    "/home/skogix/.harbor/agentzero/data/knowledge" \
    "/home/skogix/skogai/knowledge" \
    "/mnt/extra/20250726/agents/.amy/knowledge" \
    "/mnt/extra/20250726/agents/.claude/knowledge" \
    "/mnt/extra/20250726/agents/.dot/knowledge" \
    "/mnt/extra/20250726/agents/.goose/knowledge" \
    "/mnt/extra/20250726/claude-starting/knowledge" \
    "/mnt/extra/20250726/goose-backup/knowledge" \
    "/mnt/extra/20250726/knowledge" \
    "/mnt/extra/20250730-skogai-main/.amy/knowledge" \
    "/mnt/extra/20250730-skogai-main/.claude/.claude-backup/knowledge" \
    "/mnt/extra/20250730-skogai-main/.claude/knowledge" \
    "/mnt/extra/20250730-skogai-main/data/skogai-memory/knowledge" \
    "/mnt/extra/20250730-skogai-main/.dot/dot/knowledge" \
    "/mnt/extra/20250730-skogai-main/.dot/knowledge" \
    "/mnt/extra/20250730-skogai-main/.goose/knowledge" \
    "/mnt/extra/20250730-skogai-main/tmp/dot-goose/knowledge" \
    "/mnt/extra/20250730-skogai-main/tmp/goose/knowledge" \
    "/mnt/extra/a/skogai-memory/knowledge" \
    "/mnt/extra/backup/20250219/.skogai/knowledge" \
    "/mnt/extra/backup/20250219/.skogix/knowledge" \
    "/mnt/extra/backup/20250304/dotskogai/knowledge" \
    "/mnt/extra/BACKUP-SKOGAI/agents/claude/knowledge" \
    "/mnt/extra/BACKUP-SKOGAI/knowledge" \
    "/mnt/extra/backup/skogai-old-all/knowledge" \
    "/mnt/extra/llama_index/data/agent-claude/knowledge" \
    "/mnt/extra/llama_index/data/agent-claude-old2/knowledge" \
    "/mnt/extra/llama_index/data/agent-claude-old/knowledge" \
    "/mnt/extra/llama_index/data/agent-dot/knowledge" \
    "/mnt/extra/llama_index/data/agent-dot-old2/knowledge" \
    "/mnt/extra/llama_index/data/agent-dot-old3/knowledge" \
    "/mnt/extra/llama_index/data/agent-dot-old/knowledge" \
    "/mnt/extra/llama_index/data/agent-goose-old2/knowledge" \
    "/mnt/extra/llama_index/data/agent-skogai-old/knowledge" \
    "/mnt/extra/llama_index/data/BACKUP-skogai/knowledge" \
    "/mnt/extra/llama_index/data/src-gptme-agent/knowledge" \
    "/mnt/extra/skogai/BACKUP/knowledge" \
    "/mnt/extra/skogai-data-git/skogai-memory/basic-memory/knowledge" \
    "/mnt/extra/skogai-data-git/skogai-memory/knowledge" \
    "/mnt/extra/src2/gptme-agent-template/knowledge" \
    "/mnt/extra/src2/gptme-rag/examples/knowledge-base" \
    "/mnt/extra/src/src-gptme-agent/knowledge" \
    "/mnt/warez/2025-06-24/dot-amy-old/knowledge" \
    "/mnt/warez/2025-06-24/dot-config/skogcli/knowledge" \
    "/mnt/warez/2025-06-24/dot-dot-dot-old/knowledge" \
    "/mnt/warez/2025-06-24/dot-dot-old/dot/knowledge" \
    "/mnt/warez/2025-06-24/dot-dot-old/knowledge" \
    "/mnt/warez/2025-06-24/dot-goose-old/knowledge" \
    "/mnt/warez/2025-06-24/dot-skogai-backup/agent-zero/knowledge" \
    "/mnt/warez/2025-06-24-git/skogai-memory/knowledge" \
    "/mnt/warez/2025-06-24/knowledge1" \
    "/mnt/warez/2025-06-24/local/claude-backup/knowledge" \
    "/mnt/warez/2025-06-24/local/knowledge" \
    "/mnt/warez/2025-06-24/old-skogai/knowledge" \
    "/mnt/warez/2025-06-24/skogai-git/agent-claude/knowledge" \
    "/mnt/warez/2025-06-24/skogai-git/agent-claude-old2/knowledge" \
    "/mnt/warez/2025-06-24/skogai-git/agent-claude-old/knowledge" \
    "/mnt/warez/2025-06-24/skogai-git/agent-dot/knowledge" \
    "/mnt/warez/2025-06-24/skogai-git/agent-dot-old2/knowledge" \
    "/mnt/warez/2025-06-24/skogai-git/agent-dot-old3/knowledge" \
    "/mnt/warez/2025-06-24/skogai-git/agent-dot-old/knowledge" \
    "/mnt/warez/2025-06-24/skogai-git/agent-goose-old2/knowledge" \
    "/mnt/warez/2025-06-24/skogai-git/agent-skogai-old/knowledge" \
    "/mnt/warez/2025-06-24/skogai-git/BACKUP-skogai/knowledge" \
    "/mnt/warez/2025-06-24/skogai-git/src-gptme-agent/knowledge" \
    "/mnt/warez/2025-06-24/skogai-memory/knowledge" \
    "/mnt/warez/2025-06-24/tmp/patching-bootstrap/knowledge" \
    "/mnt/warez/2025-06-24/todo1/claude-home-folder/knowledge" \
    "/mnt/warez/agent-zero/agent-zero/knowledge" \
    "/mnt/warez/skogai/agents/claude/knowledge" \
    "/mnt/warez/skogai/knowledge" \
    "/mnt/warez/src/gptme-agent-template/knowledge" \
    "/mnt/warez/src/gptme-rag/examples/knowledge-base" \
    "/mnt/warez/workspace2/dotskogai/knowledge" \
    "/mnt/warez/workspace2/git/dotskogai/knowledge" \
    "/mnt/warez/workspace2/goose2/knowledge" \
    "/mnt/warez/workspace2/goose/knowledge" \
    "/mnt/warez/workspace3/dotskogai/knowledge" \
    "/mnt/warez/workspace3/git/dotskogai/knowledge"
do
    ((total++))

    if [ ! -d "$dir" ]; then
        echo "⚠️  Directory does not exist: $dir"
        ((failed++))
        continue
    fi

    # Create safe directory name from path
    safe_name=$(echo "$dir" | sed 's|/|_|g' | sed 's|^_||' | sed 's|_knowledge$||')
    dest_dir="$MASTER_DIR/$safe_name"

    echo "📂 Copying: $dir -> $dest_dir"

    # Use cp -r to copy everything, preserving structure
    if cp -r "$dir" "$dest_dir" 2>/dev/null; then
        ((copied++))
        echo "  ✓ Success"
    else
        ((failed++))
        echo "  ✗ Failed"
    fi
done

# Also copy the cache directories that might have knowledge
echo "📂 Copying cache directories..."
cache_dirs=(
    "/home/skogix/.cache/claude-cli-nodejs/-mnt-warez-2025-06-24-skogai-git-BACKUP-skogai-knowledge-expanded"
    "/home/skogix/.claude/projects/-mnt-warez-2025-06-24-skogai-git-BACKUP-skogai-knowledge-expanded"
)

for dir in "${cache_dirs[@]}"; do
    ((total++))

    if [ ! -d "$dir" ]; then
        echo "⚠️  Cache directory does not exist: $dir"
        ((failed++))
        continue
    fi

    safe_name=$(echo "$dir" | sed 's|/|_|g' | sed 's|^_||')
    dest_dir="$MASTER_DIR/cache_$safe_name"

    echo "📂 Copying cache: $dir -> $dest_dir"

    if cp -r "$dir" "$dest_dir" 2>/dev/null; then
        ((copied++))
        echo "  ✓ Success"
    else
        ((failed++))
        echo "  ✗ Failed"
    fi
done

# Create summary
echo ""
echo "========================================="
echo "COMPLETE KNOWLEDGE COPY FINISHED"
echo "========================================="
echo "Total directories processed: $total"
echo "Successfully copied: $copied"
echo "Failed: $failed"
echo ""
echo "Master knowledge location: $MASTER_DIR"
echo ""

# Count total files
total_files=$(find "$MASTER_DIR" -type f 2>/dev/null | wc -l)
echo "Total files in master directory: $total_files"

# Show disk usage
du -sh "$MASTER_DIR" 2>/dev/null