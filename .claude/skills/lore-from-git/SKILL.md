---
name: lore-from-git
description: Generate lore entries from git commits. Transforms code changes into mythological narrative through a persona's voice, creates the entry, links it to the persona's chronicle book, and refreshes the explorer data.
allowed-tools: Bash, Read, Write, Edit
---

# Generate Lore from Git

Transform recent git commits into narrative lore entries using the 5-step lore-flow pipeline.

## Arguments

- **No args**: Generate from `HEAD` (latest commit)
- **Commit ref**: e.g., `HEAD~3`, `abc1234`, a branch name — generates from that commit/range
- **`--all-new`**: Generate from all commits since last lore generation

## Workflow

### 1. Determine scope

```bash
# Default: latest commit
REF="${ARGS:-HEAD}"

# Show what we're working with
git log --oneline "$REF" -1
git diff "$REF"~ "$REF" --stat
```

If `--all-new`, find the last lore-tagged commit:
```bash
git log --oneline --grep="Lore growth detected" -1 --format="%H"
```

### 2. Run the lore-flow pipeline

The pipeline lives at `integration/lore-flow.sh` and does 5 steps:
1. Extract content (git diff)
2. Select persona (via `integration/persona-mapping.conf`)
3. Load persona context (voice, traits, lore books)
4. Generate narrative (LLM transforms technical → mythological)
5. Create & store entry → link to book → link to persona

```bash
./integration/lore-flow.sh git-diff "$REF"
```

**Persona mapping** (`integration/persona-mapping.conf`):
- `skogix` → Amy Ravenwolf (`persona_1744992765`)
- `DEFAULT` → Village Elder (`persona_1763820091`)

### 3. Verify the output

After `lore-flow.sh` completes, it prints the entry ID. Verify:

```bash
argc show-entry "$ENTRY_ID"
```

Check:
- [ ] `content` is non-empty narrative (not raw diff)
- [ ] `category` is appropriate (`event` for changes, `concept` for new patterns)
- [ ] `book_id` links to a chronicle book
- [ ] `tags` include meaningful keywords

### 4. Refresh explorer data

```bash
./tools/build-explorer-data.sh
```

### 5. Report

Output what was created:
- Entry ID and title
- Which persona narrated it
- Which chronicle book it was added to
- Entry count in that book

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_PROVIDER` | (from lore-flow) | `claude`, `openai`, or `ollama` |
| `LLM_MODEL` | `llama3.2` | Model to use for generation |

To use Claude as the generator:
```bash
LLM_PROVIDER=claude ./integration/lore-flow.sh git-diff HEAD
```

## When the pipeline fails

If `lore-flow.sh` fails (missing persona-manager deps, LLM unavailable), fall back to manual generation:

1. Read the git diff yourself: `git show HEAD`
2. Load the persona voice: `argc show-entry` on recent entries in their chronicle
3. Write the narrative yourself following the persona's voice
4. Create entry: `argc create-entry "Title" "event"`
5. Edit the entry JSON to add your narrative content
6. Link to book: `argc add-to-book $ENTRY_ID $BOOK_ID`

Use the `lore-creation-starting-skill` for narrative patterns and anti-patterns.

## Example

```
/lore-from-git HEAD~2

→ Reading commit abc1234: "Add lore explorer playground"
→ Persona: Amy Ravenwolf (skogix → persona_1744992765)
→ Running lore-flow pipeline...
→ Entry created: entry_1739912345_a1b2c3d4
→ Added to: Amy Ravenwolf's Chronicles (book_1764315000)
→ Explorer data refreshed (66 books, 378 entries)
```
