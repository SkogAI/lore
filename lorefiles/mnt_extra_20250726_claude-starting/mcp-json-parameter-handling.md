# MCP JSON Parameter Handling

## The Problem

When calling MCP tools from command line with JSON parameters, improper quoting breaks the JSON parsing.

## Common Failure Pattern

**WRONG** - Escaped double quotes in double quotes:
```bash
argcfile mcp call librarian read_official_document "{\"document\":\"list\"}"
```

This fails because bash processes the escape sequences before passing to the MCP tool, resulting in malformed JSON.

## Correct Solution

**CORRECT** - Single quotes around JSON:
```bash
argcfile mcp call librarian read_official_document '{"document":"list"}'
```

## Why This Works

1. **Single quotes preserve literal strings** - No bash interpretation of special characters
2. **Double quotes inside single quotes are literal** - No escaping needed
3. **Valid JSON structure maintained** - The MCP tool receives proper JSON

## Real Example from Session

### Failed attempt:
```bash

# This breaks JSON parsing
argcfile mcp call librarian read_official_document "{\"document\":\"list\"}"
```

### Working solution:
```bash

# This works correctly
argcfile mcp call librarian read_official_document '{"document":"list"}'
```

## General Rule

**For any JSON passed through bash command line:**
- Use single quotes around the entire JSON string
- Never escape quotes inside single-quoted JSON
- Test JSON validity before passing to tools

This pattern applies to all MCP tool calls, API requests, and any JSON data passed through shell commands.