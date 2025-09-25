# Code Style Rules (Observed)

## Shell Scripts

### Conventions
- Use `#!/usr/bin/env bash` shebang
- Always make scripts executable (`chmod +x`)
- Use `printf` over `echo` for output
- Pattern: `./scripts/context-*.sh` for context generation scripts
- Pattern: `./scripts/git/*.sh` for git flow operations

### Context Scripts Structure
```bash
#!/usr/bin/env bash

printf "# Section Header\n"
command_output
```

### Update Script Pattern
- Scripts append to `tmp/context.md` with `>>`
- First script uses `>` to overwrite, rest use `>>`
- Order matters: start → env → git → custom → status → end

## File Organization

### Directory Structure
- `./scripts/` - Automation scripts
- `./scripts/git/` - Git flow operations  
- `./scripts/context-*.sh` - Context generation components
- `./state/` - Session state files
- `./knowledge/` - Documentation and patterns
- `./.serena/` - MCP tool memories
- `./tmp/` - Generated context files

### Naming Conventions
- Scripts: `kebab-case.sh`
- Context scripts: `context-{purpose}.sh`
- Git scripts: `{operation}-{action}.sh` (e.g., `feature-start.sh`)

## Git Flow

### Branch Management
- Use git flow commands via `./scripts/git/` wrappers
- Feature branches: `feature/{descriptive-name}`
- Always use descriptive commit messages with context

### Commit Message Style
```
Short descriptive title

- Bullet point changes
- Implementation details
- Context about why/what changed
```

## Data Flow

### Context Generation
1. `context-start.sh` → creates initial structure
2. Multiple `context-*.sh` → append sections  
3. `context-end.sh` → closes structure
4. All wrapped in `[@claude:context:generated]` tags

### File Modifications
- Scripts auto-update `tmp/context.md`
- System reminders track file changes
- Never manually edit generated files

## Code Principles

### Simplicity First
- Use standard Unix tools (`tree`, `git`, `find`)
- Avoid complex logic in shell scripts
- Prefer composition over monolithic scripts

### Functional Approach
- Small, single-purpose scripts
- Composable via update script orchestration
- Data transformations over control flow

### Universal Compatibility
- Avoid system-specific syntax
- Use tools available across environments
- Shell commands over language-specific tools