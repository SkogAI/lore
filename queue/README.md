# Queue System

This directory contains the queue system for offline/batch lore processing.

## Directory Structure

```
queue/
├── README.md          # This file
├── pending/           # Tasks waiting to be processed
├── processing/        # Currently being processed
├── completed/         # Finished tasks with output
└── failed/            # Tasks that errored
```

## Quick Start

```bash
# Add a task
./tools/queue-task.sh entry "The Dark Tower" "place"

# Check status
./tools/queue-task.sh status

# Process queue
./tools/process-queue.sh

# View results
./tools/queue-task.sh list completed
```

## Documentation

See [docs/QUEUE_SYSTEM.md](../docs/QUEUE_SYSTEM.md) for comprehensive documentation.

## Task Files

Task files are JSON documents with the format:

```json
{
  "id": "task_1704567890_12345_6789",
  "type": "entry",
  "prompt_ref": "prompts/lore-entry-generation.yaml",
  "data": {
    "title": "The Dark Tower",
    "category": "place"
  },
  "created_at": "2026-01-04T12:00:00Z",
  "priority": "normal",
  "persona_id": "",
  "status": "pending"
}
```

## Notes

- Task JSON files are gitignored - only the directory structure is tracked
- Failed tasks are preserved for debugging - clear them with `./tools/queue-task.sh clear failed`
- Processing moves tasks through states: pending → processing → completed/failed
