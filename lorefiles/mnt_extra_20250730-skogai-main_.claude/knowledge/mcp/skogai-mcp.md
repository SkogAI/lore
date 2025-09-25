# SkogAI-MCP Server

## Overview

The SkogAI-MCP server is a simple but well-architected Model Context Protocol (MCP) server that provides note storage and management capabilities. It demonstrates proper MCP protocol implementation with real-time state synchronization.

## Technical Architecture

### Core Components

**Server Instance:**
```python
server = Server("skogai-mcp")
```

**State Management:**
- Simple in-memory storage: `notes: dict[str, str] = {}`
- No persistence - state lost on server restart
- Real-time client notifications via `server.request_context.session.send_resource_list_changed()`

### Function Signatures

**Entry Points:**
```python
def main() -> None  # __init__.py
async def main() -> None  # server.py - stdio transport
```

**MCP Protocol Handlers:**
```python
@server.list_resources()
async def handle_list_resources() -> list[types.Resource]
    """List available note resources with note:// URI scheme"""

@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str
    """Read note content by URI"""

@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]
    """List available prompts"""

@server.get_prompt()
async def handle_get_prompt(name: str, arguments: dict[str, str] | None) -> types.GetPromptResult
    """Generate prompts with optional arguments"""

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]
    """List available tools with JSON Schema"""

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]
    """Handle tool execution with state modification"""
```

## Dependencies

**Direct Dependencies:**
- `mcp>=1.10.1` - Model Context Protocol framework
- `pydantic` - Data validation (AnyUrl import)

**Build System:**
- `hatchling` - Build backend
- `uv` - Package manager and executor
- Python `>=3.13`

**Key Transitive Dependencies:**
- `asyncio` - Async runtime
- `anyio==4.9.0` - Async I/O abstraction
- `attrs==25.3.0` - Class decorators
- `click==8.2.1` - CLI framework

## Integration Points

### MCP Protocol Integration
- **Transport:** stdio (stdin/stdout streams)
- **Protocol:** Model Context Protocol over JSON-RPC
- **Capabilities:** Resources, Prompts, Tools with notifications

### Claude Desktop Integration
```json
"mcpServers": {
  "skogai-mcp": {
    "command": "uv",
    "args": ["--directory", "/path/to/skogai-mcp", "run", "skogai-mcp"]
  }
}
```

### API Endpoints
- **Resources:** `note://internal/{name}` URI scheme
- **Prompts:** `summarize-notes` with optional style/shakespeare arguments
- **Tools:** `add-note` with required name/content parameters

## Project Structure

```
skogai-mcp/
├── pyproject.toml          # Project config, dependencies, entry points
├── README.md              # Documentation and debugging instructions
├── uv.lock               # Dependency lockfile
└── src/skogai_mcp/
    ├── __init__.py       # Package entry point
    └── server.py         # Core MCP server implementation
```

## Operational Characteristics

### Strengths
- **Simple Implementation:** Focused, single-purpose design
- **Proper Async Patterns:** Clean async/await usage
- **MCP Compliance:** Follows protocol specifications correctly
- **Real-time Sync:** Immediate client notifications on state changes
- **Developer-Friendly:** Clear debugging support with MCP Inspector

### Limitations
- **No Persistence:** In-memory only, state lost on restart
- **Single Purpose:** Only handles note storage
- **No Auth:** No authentication or authorization mechanisms
- **No Error Recovery:** Basic error handling only

## Development and Debugging

**Local Development:**
```bash
uv --directory /path/to/skogai-mcp run skogai-mcp
```

**Debugging with MCP Inspector:**
```bash
npx @modelcontextprotocol/inspector uv --directory /path/to/skogai-mcp run skogai-mcp
```

**Publishing:**
```bash
uv publish
```

## Implementation Patterns

This server demonstrates several important MCP patterns:

1. **State Synchronization:** Proper use of resource list change notifications
2. **URI Schemes:** Custom `note://` scheme for resource identification
3. **Tool Integration:** Clean separation between read operations (resources) and write operations (tools)
4. **Async Architecture:** Proper async/await patterns throughout
5. **Schema Validation:** Using JSON Schema for tool parameter validation

## Integration with SkogAI Ecosystem

The SkogAI-MCP server serves as a reference implementation and testing ground for MCP protocol features within the broader SkogAI ecosystem. It provides a foundation for understanding how MCP servers should be structured and integrated with Claude Desktop and other MCP clients.