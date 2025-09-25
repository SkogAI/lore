# chats

## Description
The `chats` tool provides functionality to list, search, and summarize past conversation logs. This allows me to reference previous interactions and extract relevant information.

## Usage
The tool is accessed through the `ipython` tool with the following functions:

1. `list_chats(max_results: int, include_summary: bool)`: Lists recent chat conversations with optional summaries
2. `search_chats(query: str, max_results: int, sort: Literal["date", "count"])`: Searches past conversations for specific terms
3. `read_chat(conversation: str, max_results: int)`: Reads a specific conversation log

## Examples

### Listing recent conversations
```ipython
list_chats(5, True)  # List 5 most recent chats with summaries
```

### Searching for specific topics
```ipython
search_chats("python", 10, "date")  # Find 10 most recent conversations mentioning "python"
```

### Reading a specific conversation
```ipython
read_chat("conversation_20250326_123456", 20)  # Read up to 20 messages from the specified conversation
```

## Best Practices
- Use specific search terms to narrow down results
- Include summaries when listing chats to quickly identify relevant conversations
- Limit the number of results to avoid information overload
- Use the sort parameter to organize search results by relevance or recency
