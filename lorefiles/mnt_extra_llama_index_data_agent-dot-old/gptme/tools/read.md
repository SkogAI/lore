# read

## Description
The `read` tool allows me to view the content of a file. It's a simple wrapper around the `cat` command.

## Usage
To read a file, I use the `shell` tool with the `cat` command:

```shell
cat <path>
```

## Examples

### Reading a text file
```shell
cat /path/to/file.txt
```

### Reading a code file
```shell
cat /path/to/script.py
```

## Best Practices
- Use absolute paths when possible to avoid confusion
- For large files, consider using `head` or `tail` to view only portions of the file
- For binary files, use appropriate tools instead of `cat`
