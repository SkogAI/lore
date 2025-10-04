# run.sh Functionality

## What run.sh Does

**Arguments**: All non-flag arguments become prompt parts passed to `claude`

**--dry-run** prints what command would be executed instead of running it

**Default behavior**:

- Runs `./scripts/context.sh > tmp/context.md`
- Executes `claude [prompt_parts] tmp/context.md`

## Context Generation (context.sh)

**Main script** runs these components in order:

- Header with timestamp
- `context-journal.sh` - most recent journal entry
- `tasks.py status --compact` - current task status
- `context-workspace.sh` - directory structure via `tree`
- `git status -vv` - git repository status

**context-journal.sh** finds most recent `YYYY-MM-DD.md` file and shows if it's today's, yesterday's, or older

**context-workspace.sh** uses `tree` to show 1-level main directory plus full structure of `tasks/`, `projects/`, `journal/`, `knowledge/`, `people/`

## Versions

- 0.1: skogix: initial version from base gptme
- 0.2: add --diff functionality via context-git.sh
