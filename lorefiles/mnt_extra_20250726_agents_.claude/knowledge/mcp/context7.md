# context7 MCP Server

## Purpose
Library documentation lookup and resolution

## Functions
- `mcp__context7__resolve-library-id`
- `mcp__context7__get-library-docs`

## Parameters

### resolve-library-id
- `libraryName` (string): Library name to search for and retrieve Context7-compatible ID

### get-library-docs
- `context7CompatibleLibraryID` (string): Exact Context7-compatible library ID (e.g., '/mongodb/docs')
- `tokens` (number, optional): Max tokens of documentation to retrieve (default: 10000)
- `topic` (string, optional): Topic to focus documentation on (e.g., 'hooks', 'routing')

## Use Cases
- Getting up-to-date documentation for libraries
- Resolving package names to library IDs
- Focused documentation lookup by topic

## Workflow
1. Use `resolve-library-id` to get the correct library ID
2. Use `get-library-docs` with the resolved ID to fetch documentation

## Test Results
✅ **Tested**: Successfully resolved "react" to `/context7/react_dev` and retrieved React hooks documentation

## Status
Available and functional