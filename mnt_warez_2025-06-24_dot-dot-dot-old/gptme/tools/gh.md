# gh

## Description
The `gh` tool provides access to GitHub functionality through the GitHub CLI. This allows me to interact with GitHub repositories, issues, pull requests, and more directly from the terminal.

## Usage
The tool is accessed through the `shell` tool using the `gh` command:

```shell
gh <command> <subcommand> [flags]
```

## Common Commands

### Repository Management
- `gh repo create`: Create a new repository
- `gh repo clone`: Clone a repository
- `gh repo view`: View repository details
- `gh repo fork`: Fork a repository

### Issues and Pull Requests
- `gh issue list`: List issues
- `gh issue create`: Create a new issue
- `gh issue view`: View issue details
- `gh pr list`: List pull requests
- `gh pr create`: Create a new pull request
- `gh pr checkout`: Check out a pull request

### Workflows
- `gh run list`: List workflow runs
- `gh run view`: View workflow run details
- `gh run watch`: Watch a workflow run in real-time

## Examples

### Creating a repository
```shell
REPO=$(basename $(pwd))
gh repo create $REPO --public --source . --push
```

### Listing issues
```shell
gh issue list --repo $REPO
```

### Viewing workflow runs
```shell
gh run list --repo $REPO --limit 5
```

## Best Practices
- Store repository names in variables for reuse
- Use `--help` with any command to see available options
- Prefer using absolute paths and explicit repository names
- Use `gh auth status` to verify authentication before performing operations
