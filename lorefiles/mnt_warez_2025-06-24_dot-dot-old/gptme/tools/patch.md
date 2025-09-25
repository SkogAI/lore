# patch

## Description
The `patch` tool allows me to make targeted modifications to specific parts of a file without rewriting the entire file. It uses an adapted version of git conflict markers to identify which sections to replace.

## Usage
To patch a file, I use a code block with the language tag `patch <path>` and include the original content between `<<<<<<< ORIGINAL` and `=======`, followed by the updated content between `=======` and `>>>>>>> UPDATED`:

```patch <path>
<<<<<<< ORIGINAL
Original content to be replaced
=======
New content to replace the original
>>>>>>> UPDATED
```

## Examples

### Modifying a function in a Python file
```patch script.py
<<<<<<< ORIGINAL
def hello():
    print("Hello world")
=======
def hello():
    name = input("What is your name? ")
    print(f"Hello {name}")
>>>>>>> UPDATED
```

### Updating configuration in a JSON file
```patch config.json
<<<<<<< ORIGINAL
  "debug": false,
  "timeout": 30,
=======
  "debug": true,
  "timeout": 60,
>>>>>>> UPDATED
```

## Best Practices
- Keep patches as small and focused as possible
- Ensure the original content matches exactly what's in the file
- Include enough context to uniquely identify the section to be patched
- For large changes, consider using the `save` tool instead
- Avoid using placeholders in patches as they may cause the patch to fail
- Scope patches to logical units like functions, classes, or imports
