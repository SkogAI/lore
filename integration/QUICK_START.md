# Integration Quick Start

## 30-Second Start

```bash
cd /path/to/lore

# Generate lore from a message
./integration/lore-flow.sh manual "Amy discovered quantum mojitos"

# Generate from latest commit
./integration/lore-flow.sh git-diff HEAD

# Generate from older commit
./integration/lore-flow.sh git-diff HEAD~3
```

## How It Works

```
Your Input → Extract → Select Persona → Generate Story → Save Lore
```

## Add Your Persona

Edit `integration/persona-mapping.conf`:

```bash
your-git-name=persona_XXXXX
```

Find your persona ID:
```bash
python3 integration/persona-bridge/persona-manager.py --list
```

## View Results

```bash
# List all lore entries
./tools/manage-lore.sh list-entries

# View specific entry
./tools/manage-lore.sh show-entry entry_1764315234_a4b3c2d1

# List all books (chronicles)
./tools/manage-lore.sh list-books

# View a chronicle
./tools/manage-lore.sh show-book book_1764315000
```

## Automate It

### Git Hook (every commit becomes lore)

```bash
# Create post-commit hook
cat > .git/hooks/post-commit <<'EOF'
#!/bin/bash
./integration/lore-flow.sh git-diff HEAD &
EOF

chmod +x .git/hooks/post-commit
```

Now every `git commit` generates lore automatically!

### Daily Digest (batch process all activity)

```bash
# Add to crontab
crontab -e

# Add this line (runs midnight)
0 0 * * * cd /path/to/lore && ./integration/workflows/daily-digest.sh
```

## Troubleshooting

**No narrative generated?**
```bash
# Check LLM provider is set
echo $LLM_PROVIDER

# Set it
export LLM_PROVIDER=claude
```

**Persona not found?**
```bash
# List available personas
python3 integration/persona-bridge/persona-manager.py --list

# Update mapping
vim integration/persona-mapping.conf
```

**Entry not created?**
```bash
# Check permissions
ls -la knowledge/expanded/lore/entries/
ls -la knowledge/expanded/lore/books/
```

## Done!

That's it. Your codebase now writes its own mythology. 🎭
