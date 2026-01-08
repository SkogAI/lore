# Queue System for Offline/Batch Lore Processing

## Overview

The SkogAI queue system enables you to queue lore generation tasks during work sessions and process them later during downtime or in batch mode. This is particularly useful for:

- **Offline Processing**: Queue tasks during work, process them when you have LLM access
- **Batch Processing**: Generate multiple entries efficiently in one session
- **Cost Optimization**: Process queues during cheaper rate periods
- **Review Workflow**: Generate content first, review before committing

## Architecture

The queue system uses a simple file-based approach with the following directory structure:

```
queue/
├── pending/           # Tasks waiting to be processed
│   └── task_1704567890.json
├── processing/        # Currently being processed
├── completed/         # Finished tasks with output
│   └── task_1704567890.json
└── failed/            # Tasks that errored
```

## Task Format

Each task is stored as a JSON file with the following structure:

```json
{
  "id": "task_1704567890",
  "type": "entry",
  "prompt_ref": "prompts/lore-entry-generation.yaml",
  "data": {
    "title": "The Dark Tower",
    "category": "place"
  },
  "created_at": "2026-01-04T12:00:00Z",
  "priority": "normal",
  "persona_id": "persona_1744992765",
  "status": "pending"
}
```

### Task States

- **pending**: Task is queued and waiting to be processed
- **processing**: Task is currently being processed
- **completed**: Task completed successfully, includes result
- **failed**: Task failed with error message

## CLI Usage

### Adding Tasks to the Queue

Use `queue-task.sh` to add tasks to the queue:

```bash
# Basic entry task
./tools/queue-task.sh entry "The Dark Tower" "place"

# With persona association
./tools/queue-task.sh entry "Elara the Wise" "character" --persona amy

# With priority
./tools/queue-task.sh entry "The Great War" "event" --priority high

# Multiple parameters
./tools/queue-task.sh entry "Ancient Artifact" "object" --persona persona_1234567890 --priority high
```

#### Entry Categories

Valid categories for lore entries:
- `place` - Locations, realms, dimensions
- `character` - People, beings, entities
- `object` - Items, artifacts, tools
- `event` - Historical events, moments
- `concept` - Abstract ideas, principles
- `custom` - Custom categories

#### Priority Levels

- `low` - Process last
- `normal` - Default priority
- `high` - Process first

### Checking Queue Status

```bash
# Show queue statistics
./tools/queue-task.sh status

# Output:
# 📊 Queue Status
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#   Pending:    3 tasks
#   Processing: 0 tasks
#   Completed:  5 tasks
#   Failed:     1 tasks
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Listing Tasks

```bash
# List pending tasks (default)
./tools/queue-task.sh list

# List specific state
./tools/queue-task.sh list pending
./tools/queue-task.sh list completed
./tools/queue-task.sh list failed

# List all tasks
./tools/queue-task.sh list all
```

### Viewing Task Details

```bash
# Show full task JSON
./tools/queue-task.sh show task_1704567890
```

### Clearing Completed/Failed Tasks

```bash
# Clear completed tasks (with confirmation)
./tools/queue-task.sh clear completed

# Clear failed tasks
./tools/queue-task.sh clear failed

# Clear both
./tools/queue-task.sh clear all
```

## Processing the Queue

Use `process-queue.sh` to process pending tasks:

```bash
# Process all pending tasks with default provider (ollama)
./tools/process-queue.sh

# Use a specific provider
LLM_PROVIDER=ollama ./tools/process-queue.sh

# Use Claude
LLM_PROVIDER=claude ./tools/process-queue.sh

# Use OpenAI/OpenRouter
LLM_PROVIDER=openai LLM_MODEL=gpt-4 ./tools/process-queue.sh

# Process with command-line options
./tools/process-queue.sh --provider claude --model claude-3-sonnet

# Process only a limited number of tasks
./tools/process-queue.sh --limit 5
```

### LLM Provider Configuration

The queue processor supports the same providers as `llama-lore-creator.sh`:

#### Ollama (Default)
```bash
LLM_PROVIDER=ollama LLM_MODEL=llama3.2:3b ./tools/process-queue.sh
```

#### Claude CLI
```bash
LLM_PROVIDER=claude ./tools/process-queue.sh
```

#### OpenAI/OpenRouter
```bash
export OPENAI_API_KEY="your-api-key"
export OPENAI_BASE_URL="https://openrouter.ai/api/v1"  # Optional
LLM_PROVIDER=openai LLM_MODEL=gpt-4 ./tools/process-queue.sh
```

## Workflow Examples

### Example 1: Daily Batch Processing

```bash
# During work: Queue tasks as ideas come
./tools/queue-task.sh entry "The Crimson Citadel" "place"
./tools/queue-task.sh entry "Lord Vexxar" "character" --priority high
./tools/queue-task.sh entry "The Shattering" "event"

# Check what's queued
./tools/queue-task.sh status

# Later: Process entire queue
LLM_PROVIDER=ollama ./tools/process-queue.sh

# Review completed entries
./tools/queue-task.sh list completed

# View specific entry
./tools/manage-lore.sh show-entry entry_1704567890

# Clear completed tasks
./tools/queue-task.sh clear completed
```

### Example 2: Persona-Specific Generation

```bash
# Queue entries for a specific persona
./tools/queue-task.sh entry "Amy's Workshop" "place" --persona amy
./tools/queue-task.sh entry "The Fire Crystal" "object" --persona amy
./tools/queue-task.sh entry "Amy's Awakening" "event" --persona amy

# Process with persona context
./tools/process-queue.sh
```

### Example 3: Priority-Based Processing

```bash
# Queue with different priorities
./tools/queue-task.sh entry "Important Place" "place" --priority high
./tools/queue-task.sh entry "Regular Entry" "character" --priority normal
./tools/queue-task.sh entry "Nice to Have" "concept" --priority low

# Process limited batch (high priority first)
./tools/process-queue.sh --limit 1

# High priority task will be processed first
```

## Integration with Existing Tools

The queue system integrates seamlessly with existing SkogAI tools:

### With llama-lore-creator.sh

`process-queue.sh` internally calls `llama-lore-creator.sh` to generate content:

```bash
# Queue system uses this under the hood:
./tools/llama-lore-creator.sh <model> entry "<title>" "<category>"
```

### With manage-lore.sh

Once processing completes, view and manage entries normally:

```bash
# View the generated entry
./tools/manage-lore.sh show-entry entry_1704567890

# List all entries
./tools/manage-lore.sh list-entries

# Add to a lorebook
./tools/manage-lore.sh add-to-book entry_1704567890 book_1704567890
```

### With create-persona.sh

Use personas with queued tasks:

```bash
# Create a persona
./tools/create-persona.sh create "Storyteller" "Master of tales" "wise,eloquent,patient" "narrative"

# Queue entries for this persona
./tools/queue-task.sh entry "The First Tale" "event" --persona persona_1704567890
```

## Prompt Templates

The queue system uses YAML prompt templates stored in `prompts/`:

```yaml
---
name: "lore-entry-generation"
version: "1.0"
description: "Generate rich narrative lore entries"

template: |
  You are a master lore writer...
  Create a {{category}} entry titled "{{title}}"
  ...

config:
  max_tokens: 2048
  temperature: 0.7
```

Tasks reference these templates via the `prompt_ref` field. This allows:
- **Consistency**: Same prompts across manual and queued generation
- **Version Control**: Track prompt changes over time
- **Customization**: Create custom prompts for different task types

## Error Handling

When tasks fail, they are moved to the `failed/` directory with error details:

```json
{
  "id": "task_1704567890",
  "status": "failed",
  "failed_at": "2026-01-04T14:30:00Z",
  "error": "Failed to generate lore entry: Connection timeout",
  ...
}
```

View failed tasks:

```bash
./tools/queue-task.sh list failed
./tools/queue-task.sh show task_1704567890
```

Retry failed tasks:

```bash
# Move failed task back to pending (manual)
mv queue/failed/task_1704567890.json queue/pending/

# Update status in JSON
jq '.status = "pending" | del(.failed_at, .error)' \
  queue/pending/task_1704567890.json > temp.json
mv temp.json queue/pending/task_1704567890.json

# Process again
./tools/process-queue.sh
```

## Best Practices

### 1. Queue During Ideation

Don't interrupt your flow - queue tasks as ideas emerge:

```bash
# Quick task additions
./tools/queue-task.sh entry "The Void Nexus" "place"
./tools/queue-task.sh entry "Quantum Blade" "object"
```

### 2. Process in Batches

Run processing during dedicated time slots:

```bash
# Morning batch
./tools/process-queue.sh --limit 10

# Full daily process
./tools/process-queue.sh
```

### 3. Use Priorities Strategically

Mark urgent or time-sensitive entries as high priority:

```bash
./tools/queue-task.sh entry "Critical Plot Point" "event" --priority high
```

### 4. Associate with Personas

Link entries to personas for consistent voice:

```bash
./tools/queue-task.sh entry "Amy's Memory" "event" --persona amy
```

### 5. Review Before Committing

Check completed entries before committing to the repository:

```bash
# View completed
./tools/queue-task.sh list completed

# Review specific entries
./tools/manage-lore.sh show-entry entry_1704567890

# If satisfied, commit
git add knowledge/expanded/lore/entries/
git commit -m "Add queued lore entries"

# Clear completed
./tools/queue-task.sh clear completed
```

## Troubleshooting

### No pending tasks processed

**Problem**: `process-queue.sh` reports "No pending tasks"

**Solutions**:
```bash
# Check queue status
./tools/queue-task.sh status

# List pending
./tools/queue-task.sh list pending

# Verify files exist
ls -la queue/pending/
```

### LLM provider not found

**Problem**: Error about missing LLM provider

**Solutions**:
```bash
# For Ollama: Install and pull model
ollama pull llama3.2:3b

# For Claude: Install CLI
npm install -g @anthropic-ai/claude-code

# For OpenAI: Set API key
export OPENAI_API_KEY="your-key"
```

### Task stuck in processing

**Problem**: Task remains in `processing/` after crash

**Solution**:
```bash
# Move back to pending manually
mv queue/processing/task_*.json queue/pending/

# Or move to failed
mv queue/processing/task_*.json queue/failed/
```

### Permissions issues

**Problem**: Cannot create queue directories

**Solution**:
```bash
# Ensure scripts are executable
chmod +x tools/queue-task.sh
chmod +x tools/process-queue.sh

# Ensure write permissions
chmod -R u+w queue/
```

## Advanced Usage

### Custom Task Processing

You can manually process tasks with custom parameters:

```bash
# Get task details
TASK=$(cat queue/pending/task_1704567890.json)
TITLE=$(echo "$TASK" | jq -r '.data.title')
CATEGORY=$(echo "$TASK" | jq -r '.data.category')

# Process with custom model
LLM_PROVIDER=openai LLM_MODEL=gpt-4-turbo \
  ./tools/llama-lore-creator.sh gpt-4-turbo entry "$TITLE" "$CATEGORY"
```

### Batch Scripts

Create shell scripts for common workflows:

```bash
#!/bin/bash
# process-nightly.sh - Nightly queue processing

echo "Starting nightly lore processing..."

# Use cheaper overnight rates
LLM_PROVIDER=openai LLM_MODEL=gpt-3.5-turbo \
  ./tools/process-queue.sh

# Email results
./tools/queue-task.sh status | mail -s "Queue Results" you@example.com
```

### Monitoring

Monitor queue processing with watch:

```bash
# Live queue status
watch -n 5 './tools/queue-task.sh status'

# Live processing state
watch -n 2 'ls -1 queue/processing/'
```

## Future Enhancements

Potential improvements to the queue system:

- **Scheduled Processing**: Cron-based automatic processing
- **Webhook Notifications**: Alert on completion/failure
- **Parallel Processing**: Process multiple tasks simultaneously
- **Task Dependencies**: Chain tasks together
- **Template Expansion**: Support more task types (persona, lorebook, etc.)
- **Web UI**: Browser-based queue management
- **Retry Logic**: Automatic retry with exponential backoff

## See Also

- [llama-lore-creator.sh](../tools/llama-lore-creator.sh) - Core lore generation
- [manage-lore.sh](../tools/manage-lore.sh) - Lore management
- [create-persona.sh](../tools/create-persona.sh) - Persona creation
- [DOCUMENTATION.md](DOCUMENTATION.md) - Overall system documentation
