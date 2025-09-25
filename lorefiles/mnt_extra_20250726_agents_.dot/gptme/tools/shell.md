# shell

## Description
The `shell` tool allows me to execute shell commands in a stateful bash environment. This provides access to the full range of command-line utilities and system operations.

## Usage
To execute a shell command, I use a code block with the language tag `shell`:

```shell
command [arguments]
```

## Available Programs
The shell environment includes many standard programs, including:
- docker
- ffmpeg
- git
- magick
- pacman
- And other standard Unix/Linux utilities

## Examples

### Listing files and directories
```shell
ls -la
```

### Checking system information
```shell
uname -a
```

### Running git commands
```shell
git status
```

### Exploring the filesystem
```shell
find . -name "*.md" | sort
```

## Best Practices
- Use absolute paths when referencing files to avoid confusion
- Store important output in variables for later use
- Break complex operations into smaller, verifiable steps
- Check command exit status for errors
- Use `pwd` to verify the current working directory before operations
