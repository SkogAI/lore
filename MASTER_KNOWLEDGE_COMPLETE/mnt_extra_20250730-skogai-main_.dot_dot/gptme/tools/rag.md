# rag

## Description
The `rag` (Retrieval-Augmented Generation) tool provides functionality to index and search project documentation. This allows me to quickly find relevant information within the project's files.

## Usage
The tool is accessed through the `ipython` tool with the following functions:

1. `rag_index(paths: str, glob: Union[str, NoneType]) -> str`: Indexes documents in specified paths
2. `rag_search(query: str, return_full: bool) -> str`: Searches indexed documents
3. `rag_status() -> str`: Shows the current status of the index

## Examples

### Indexing documents
```ipython
rag_index()  # Index the current directory
```

```ipython
rag_index("/path/to/docs", "*.md")  # Index markdown files in a specific directory
```

### Searching for information
```ipython
rag_search("function documentation", False)  # Search for information about function documentation
```

### Checking index status
```ipython
rag_status()  # Show how many documents are indexed
```

## Best Practices
- Index relevant directories before searching
- Use specific search queries to get more relevant results
- Check the index status to ensure documents are properly indexed
- Consider re-indexing after significant changes to documentation
- Use the `return_full` parameter to control the amount of context returned
