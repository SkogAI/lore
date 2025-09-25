# screenshot

## Description
The `screenshot` tool allows me to capture a screenshot of the current screen and save it to a file.

## Usage
The tool is accessed through the `ipython` tool with the following function:

```python
screenshot(path: Union[Path, NoneType]) -> Path
```

## Examples

### Taking a screenshot with default path
```ipython
screenshot()
```

### Taking a screenshot with a specific path
```ipython
screenshot("/path/to/save/screenshot.png")
```

## Best Practices
- Provide a descriptive filename when saving screenshots
- Use absolute paths when specifying the save location
- Verify the screenshot was captured successfully
- Use the returned path to reference the screenshot in documentation
