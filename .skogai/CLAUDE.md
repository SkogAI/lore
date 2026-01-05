# .skogai Directory

Project-level skogai configuration and state.

## Contents

| Directory | Purpose |
|-----------|---------|
| `garden/` | Plugin trial system - tracks experimental components |
| `plan/` | Project planning documents |
| `todos/` | Task tracking |

## Garden

Trial-based plugin evaluation system. Test plugins before committing permanently.

Quick commands:
- `/garden:status` - View state
- `/garden:trial <plugin>` - Start trial
- `/garden:keep <plugin>` - Promote to permanent

See `@.skogai/garden/README.md` for full documentation.
