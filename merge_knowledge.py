#!/usr/bin/env python3
"""
Merge all 92 knowledge directories into a single master knowledge base.
Handles duplicates, preserves history, and maintains agent-specific content.
"""

import os
import shutil
import hashlib
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Master knowledge directory
MASTER_DIR = Path("/mnt/extra/backup/skogai-old-all/MASTER_KNOWLEDGE")

# All knowledge directories from the inventory
KNOWLEDGE_DIRS = [
    "/home/skogix/amy/knowledge",
    "/home/skogix/.cache/claude-cli-nodejs/-mnt-warez-2025-06-24-skogai-git-BACKUP-skogai-knowledge-expanded",
    "/home/skogix/.claude/projects/-mnt-warez-2025-06-24-skogai-git-BACKUP-skogai-knowledge-expanded",
    "/home/skogix/dev/dot-claude/knowledge",
    "/home/skogix/dot3/knowledge",
    "/home/skogix/dot/knowledge",
    "/home/skogix/goose/knowledge",
    "/home/skogix/.harbor/agentzero/data/knowledge",
    "/home/skogix/skogai/knowledge",
    "/mnt/extra/20250726/agents/.amy/knowledge",
    "/mnt/extra/20250726/agents/.claude/knowledge",
    "/mnt/extra/20250726/agents/.dot/knowledge",
    "/mnt/extra/20250726/agents/.goose/knowledge",
    "/mnt/extra/20250726/claude-starting/knowledge",
    "/mnt/extra/20250726/claude-starting/knowledge/historic-knowledge",
    "/mnt/extra/20250726/goose-backup/knowledge",
    "/mnt/extra/20250726/knowledge",
    "/mnt/extra/20250730-skogai-main/.amy/knowledge",
    "/mnt/extra/20250730-skogai-main/.claude/.claude-backup/knowledge",
    "/mnt/extra/20250730-skogai-main/.claude/knowledge",
    "/mnt/extra/20250730-skogai-main/.claude/knowledge/historic-knowledge",
    "/mnt/extra/20250730-skogai-main/.claude/knowledge/knowledge",
    "/mnt/extra/20250730-skogai-main/data/skogai-memory/knowledge",
    "/mnt/extra/20250730-skogai-main/.dot/dot/knowledge",
    "/mnt/extra/20250730-skogai-main/.dot/knowledge",
    "/mnt/extra/20250730-skogai-main/.dot/knowledge/knowledge",
    "/mnt/extra/20250730-skogai-main/.goose/knowledge",
    "/mnt/extra/20250730-skogai-main/tmp/dot-goose/knowledge",
    "/mnt/extra/20250730-skogai-main/tmp/goose/knowledge",
    "/mnt/extra/a/skogai-memory/knowledge",
    "/mnt/extra/backup/20250212/dev/knowledge-base-supabase",
    "/mnt/extra/backup/20250219/.skogai/knowledge",
    "/mnt/extra/backup/20250219/.skogix/knowledge",
    "/mnt/extra/backup/20250304/dotskogai/knowledge",
    "/mnt/extra/backup/20250305/dev2/knowledge-base-supabase",
    "/mnt/extra/backup/20250305/dev/knowledge-base-supabase",
    "/mnt/extra/BACKUP-SKOGAI/agents/claude/knowledge",
    "/mnt/extra/BACKUP-SKOGAI/knowledge",
    "/mnt/extra/backup/skogai-old-all/knowledge",
    "/mnt/extra/llama_index/data/agent-claude/knowledge",
    "/mnt/extra/llama_index/data/agent-claude-old2/knowledge",
    "/mnt/extra/llama_index/data/agent-claude-old/knowledge",
    "/mnt/extra/llama_index/data/agent-dot/knowledge",
    "/mnt/extra/llama_index/data/agent-dot-old2/knowledge",
    "/mnt/extra/llama_index/data/agent-dot-old3/knowledge",
    "/mnt/extra/llama_index/data/agent-dot-old/knowledge",
    "/mnt/extra/llama_index/data/agent-goose-old2/knowledge",
    "/mnt/extra/llama_index/data/agent-skogai-old/knowledge",
    "/mnt/extra/llama_index/data/BACKUP-skogai/knowledge",
    "/mnt/extra/llama_index/data/src-gptme-agent/knowledge",
    "/mnt/extra/skogai/BACKUP/knowledge",
    "/mnt/extra/skogai-data-git/skogai-memory/basic-memory/knowledge",
    "/mnt/extra/skogai-data-git/skogai-memory/knowledge",
    "/mnt/extra/src2/gptme-agent-template/knowledge",
    "/mnt/extra/src2/gptme-rag/examples/knowledge-base",
    "/mnt/extra/src/src-gptme-agent/knowledge",
    "/mnt/warez/2025-06-24/dot-amy-old/knowledge",
    "/mnt/warez/2025-06-24/dot-config/skogcli/knowledge",
    "/mnt/warez/2025-06-24/dot-dot-dot-old/knowledge",
    "/mnt/warez/2025-06-24/dot-dot-dot-old/knowledge/knowledge",
    "/mnt/warez/2025-06-24/dot-dot-old/dot/knowledge",
    "/mnt/warez/2025-06-24/dot-dot-old/knowledge",
    "/mnt/warez/2025-06-24/dot-dot-old/knowledge/knowledge",
    "/mnt/warez/2025-06-24/dot-goose-old/knowledge",
    "/mnt/warez/2025-06-24/dot-skogai-backup/agent-zero/knowledge",
    "/mnt/warez/2025-06-24-git/skogai-memory/knowledge",
    "/mnt/warez/2025-06-24/knowledge1",
    "/mnt/warez/2025-06-24/local/claude-backup/knowledge",
    "/mnt/warez/2025-06-24/local/knowledge",
    "/mnt/warez/2025-06-24/old-skogai/knowledge",
    "/mnt/warez/2025-06-24/skogai-git/agent-claude/knowledge",
    "/mnt/warez/2025-06-24/skogai-git/agent-claude-old2/knowledge",
    "/mnt/warez/2025-06-24/skogai-git/agent-claude-old/knowledge",
    "/mnt/warez/2025-06-24/skogai-git/agent-dot/knowledge",
    "/mnt/warez/2025-06-24/skogai-git/agent-dot-old2/knowledge",
    "/mnt/warez/2025-06-24/skogai-git/agent-dot-old3/knowledge",
    "/mnt/warez/2025-06-24/skogai-git/agent-dot-old/knowledge",
    "/mnt/warez/2025-06-24/skogai-git/agent-goose-old2/knowledge",
    "/mnt/warez/2025-06-24/skogai-git/agent-skogai-old/knowledge",
    "/mnt/warez/2025-06-24/skogai-git/BACKUP-skogai/knowledge",
    "/mnt/warez/2025-06-24/skogai-git/src-gptme-agent/knowledge",
    "/mnt/warez/2025-06-24/skogai-memory/knowledge",
    "/mnt/warez/2025-06-24/tmp/patching-bootstrap/knowledge",
    "/mnt/warez/2025-06-24/todo1/claude-home-folder/knowledge",
    "/mnt/warez/agent-zero/agent-zero/knowledge",
    "/mnt/warez/skogai/agents/claude/knowledge",
    "/mnt/warez/skogai/knowledge",
    "/mnt/warez/src/gptme-agent-template/knowledge",
    "/mnt/warez/src/gptme-rag/examples/knowledge-base",
    "/mnt/warez/workspace2/dotskogai/knowledge",
    "/mnt/warez/workspace2/git/dotskogai/knowledge",
    "/mnt/warez/workspace2/goose2/knowledge",
    "/mnt/warez/workspace2/goose/knowledge",
    "/mnt/warez/workspace3/dotskogai/knowledge",
    "/mnt/warez/workspace3/git/dotskogai/knowledge"
]

def get_file_hash(filepath):
    """Calculate SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"Error hashing {filepath}: {e}")
        return None

def determine_agent_from_path(path):
    """Determine which agent a knowledge path belongs to."""
    path_str = str(path).lower()
    if 'amy' in path_str:
        return 'amy'
    elif 'claude' in path_str:
        return 'claude'
    elif 'dot' in path_str:
        return 'dot'
    elif 'goose' in path_str:
        return 'goose'
    elif 'skogai' in path_str:
        return 'skogai'
    else:
        return 'general'

def extract_date_from_path(path):
    """Extract date from backup path if present."""
    import re
    date_patterns = [
        r'(\d{8})',  # YYYYMMDD
        r'(\d{4}-\d{2}-\d{2})',  # YYYY-MM-DD
    ]

    path_str = str(path)
    for pattern in date_patterns:
        match = re.search(pattern, path_str)
        if match:
            return match.group(1)
    return None

def merge_knowledge_directories():
    """Main function to merge all knowledge directories."""

    # Track statistics
    stats = {
        'total_files': 0,
        'duplicates': 0,
        'unique_files': 0,
        'errors': 0,
        'directories_processed': 0,
        'empty_directories': 0
    }

    # Track file hashes to detect duplicates
    file_registry = defaultdict(list)  # hash -> list of (source_path, dest_path)

    # Create manifest
    manifest = {
        'merge_date': datetime.now().isoformat(),
        'source_directories': [],
        'files': []
    }

    print("Starting knowledge merge operation...")
    print(f"Master directory: {MASTER_DIR}")
    print(f"Processing {len(KNOWLEDGE_DIRS)} knowledge directories...")

    for source_dir in KNOWLEDGE_DIRS:
        source_path = Path(source_dir)

        if not source_path.exists():
            print(f"⚠️  Directory does not exist: {source_dir}")
            stats['empty_directories'] += 1
            continue

        if not source_path.is_dir():
            print(f"⚠️  Not a directory: {source_dir}")
            continue

        print(f"\n📂 Processing: {source_dir}")
        stats['directories_processed'] += 1

        # Determine category
        agent = determine_agent_from_path(source_path)
        date = extract_date_from_path(source_path)

        # Determine destination subdirectory
        if agent != 'general':
            if date:
                dest_subdir = MASTER_DIR / 'agents' / agent / f'archive_{date}'
            else:
                dest_subdir = MASTER_DIR / 'agents' / agent / 'current'
        elif 'template' in str(source_path).lower():
            dest_subdir = MASTER_DIR / 'templates'
        elif 'workspace' in str(source_path).lower():
            dest_subdir = MASTER_DIR / 'workspace'
        elif date:
            dest_subdir = MASTER_DIR / 'archives' / date
        else:
            dest_subdir = MASTER_DIR / 'core'

        # Process all files in the source directory
        try:
            for root, dirs, files in os.walk(source_path):
                for filename in files:
                    source_file = Path(root) / filename

                    # Calculate relative path from source_dir
                    try:
                        rel_path = source_file.relative_to(source_path)
                    except ValueError:
                        rel_path = Path(filename)

                    # Destination file path
                    dest_file = dest_subdir / rel_path

                    # Calculate file hash
                    file_hash = get_file_hash(source_file)
                    if not file_hash:
                        stats['errors'] += 1
                        continue

                    stats['total_files'] += 1

                    # Check for duplicates
                    if file_hash in file_registry:
                        stats['duplicates'] += 1
                        # Record duplicate but don't copy
                        file_registry[file_hash].append((str(source_file), str(dest_file)))
                        print(f"  ⚡ Duplicate found: {filename}")
                        continue

                    # Create destination directory
                    dest_file.parent.mkdir(parents=True, exist_ok=True)

                    # Copy file
                    try:
                        shutil.copy2(source_file, dest_file)
                        stats['unique_files'] += 1
                        file_registry[file_hash].append((str(source_file), str(dest_file)))

                        # Add to manifest
                        manifest['files'].append({
                            'source': str(source_file),
                            'destination': str(dest_file),
                            'hash': file_hash,
                            'agent': agent,
                            'date': date
                        })

                        print(f"  ✓ Copied: {rel_path}")

                    except Exception as e:
                        print(f"  ✗ Error copying {source_file}: {e}")
                        stats['errors'] += 1

        except Exception as e:
            print(f"  ✗ Error processing directory {source_dir}: {e}")
            stats['errors'] += 1

        manifest['source_directories'].append({
            'path': str(source_dir),
            'agent': agent,
            'date': date,
            'exists': True
        })

    # Write duplicate report
    duplicate_report = []
    for file_hash, locations in file_registry.items():
        if len(locations) > 1:
            duplicate_report.append({
                'hash': file_hash,
                'count': len(locations),
                'locations': locations
            })

    # Save manifest
    manifest_path = MASTER_DIR / 'MERGE_MANIFEST.json'
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)

    # Save duplicate report
    if duplicate_report:
        duplicate_report_path = MASTER_DIR / 'DUPLICATE_REPORT.json'
        with open(duplicate_report_path, 'w') as f:
            json.dump(duplicate_report, f, indent=2)

    # Create summary report
    summary_path = MASTER_DIR / 'MERGE_SUMMARY.md'
    with open(summary_path, 'w') as f:
        f.write(f"""# Knowledge Merge Summary

**Date:** {datetime.now().isoformat()}

## Statistics

- **Directories Processed:** {stats['directories_processed']}
- **Empty/Missing Directories:** {stats['empty_directories']}
- **Total Files Found:** {stats['total_files']}
- **Unique Files Copied:** {stats['unique_files']}
- **Duplicates Skipped:** {stats['duplicates']}
- **Errors:** {stats['errors']}

## Directory Structure

The merged knowledge base is organized as follows:

```
MASTER_KNOWLEDGE/
├── agents/          # Agent-specific knowledge
│   ├── amy/
│   ├── claude/
│   ├── dot/
│   └── goose/
├── archives/        # Date-based archives
├── core/           # Core knowledge files
├── expanded/       # Expanded knowledge
├── implementation/ # Implementation details
├── historic/       # Historical knowledge
├── workspace/      # Workspace knowledge
└── templates/      # Template knowledge
```

## Reports

- `MERGE_MANIFEST.json` - Complete list of all files and their sources
- `DUPLICATE_REPORT.json` - Details of duplicate files found
- `MERGE_SUMMARY.md` - This summary report
""")

    print("\n" + "="*60)
    print("MERGE COMPLETE!")
    print("="*60)
    print(f"✓ Directories processed: {stats['directories_processed']}")
    print(f"✓ Unique files merged: {stats['unique_files']}")
    print(f"⚡ Duplicates skipped: {stats['duplicates']}")
    print(f"✗ Errors encountered: {stats['errors']}")
    print(f"\n📁 Master knowledge base created at: {MASTER_DIR}")
    print(f"📊 Reports saved in: {MASTER_DIR}")

    return stats

if __name__ == "__main__":
    merge_knowledge_directories()