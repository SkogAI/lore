# ipython

## Description
The `ipython` tool provides an interactive Python execution environment. This allows me to run Python code, access specialized functions, and perform complex operations that would be difficult in a shell environment.

## Usage
To execute Python code, I use a code block with the language tag `ipython`:

```ipython
python_code_here
```

## Available Libraries
The ipython environment includes several pre-installed libraries:
- PIL (Python Imaging Library)

## Available Functions
The environment also provides special functions:
- `list_chats(max_results: int, include_summary: bool)`: List recent chat conversations
- `search_chats(query: str, max_results: int, sort: Literal["date", "count"])`: Search past conversations
- `read_chat(conversation: str, max_results: int)`: Read a specific conversation
- `rag_index(paths: str, glob: Union[str, NoneType]) -> str`: Index documents for RAG
- `rag_search(query: str, return_full: bool) -> str`: Search indexed documents
- `rag_status() -> str`: Show RAG index status
- `screenshot(path: Union[Path, NoneType]) -> Path`: Take a screenshot
- `view_image(image_path: Union[Path, str]) -> Message`: View an image

## Examples

### Basic Python operations
```ipython
x = 10
y = 20
print(f"The sum is: {x + y}")
x + y  # The result of the last expression is returned
```

### Using special functions
```ipython

# Take a screenshot and view it
screenshot_path = screenshot()
view_image(screenshot_path)
```

### Data manipulation
```ipython

# Create and manipulate a list
numbers = [1, 2, 3, 4, 5]
squared = [x**2 for x in numbers]
squared
```

## Best Practices
- Use variables to store intermediate results
- The result of the last expression is automatically returned
- Break complex operations into smaller, verifiable steps
- Use Python's rich library ecosystem for data manipulation
- Combine with other tools for comprehensive workflows
