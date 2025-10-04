# append

## Description
The `append` tool allows me to append text to an existing file without overwriting its current content.

## Usage
To append content to a file, I use a code block with the language tag `append <path>`:

```append <path>
Content to append
```

## Examples
Adding a new line to a file:

```append example.txt
This line will be appended to the end of example.txt
```

Adding code to a Python file:

```append script.py
def new_function():
    return "This function was appended"
```

## Best Practices
- Verify the file exists before appending to it
- Use absolute paths when possible to avoid confusion
- Check the file content before and after appending to ensure the operation worked as expected
- For large additions, consider using the `save` tool with a complete rewrite instead
