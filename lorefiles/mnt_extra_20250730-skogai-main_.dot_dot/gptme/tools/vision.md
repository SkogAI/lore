# vision

## Description
The `vision` tool allows me to view and analyze images. This is useful for examining screenshots, diagrams, or any visual content.

## Usage
The tool is accessed through the `ipython` tool with the following function:

```python
view_image(image_path: Union[Path, str]) -> Message
```

## Examples

### Viewing an image
```ipython
view_image("/path/to/image.png")
```

### Viewing a screenshot
```ipython
screenshot_path = screenshot()
view_image(screenshot_path)
```

## Best Practices
- Use absolute paths when specifying image locations
- Verify the image exists before attempting to view it
- For large images, be aware they will be automatically scaled down
- Use in conjunction with the screenshot tool for capturing and analyzing visual information
