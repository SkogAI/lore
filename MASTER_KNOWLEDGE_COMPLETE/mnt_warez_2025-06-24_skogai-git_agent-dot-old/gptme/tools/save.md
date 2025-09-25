# save

## Description
The `save` tool allows me to create new files or overwrite existing files with specified content.

## Usage
To save content to a file, I use a code block with the language tag `save <path>`:

```save <path>
Content to save to the file
```

## Examples

### Creating a new text file
```save /path/to/new_file.txt
This is the content of the new file.
Multiple lines are supported.
```

### Creating a Python script
```save /path/to/script.py
def hello():
    print("Hello, world!")

if __name__ == "__main__":
    hello()
```

### Overwriting an existing file
```save /path/to/existing_file.txt
This content will replace everything in the existing file.
```

## Best Practices
- Use absolute paths when possible to avoid confusion
- Be cautious when overwriting existing files
- Verify the file was created/modified as expected
- For appending to files instead of overwriting, use the `append` tool
