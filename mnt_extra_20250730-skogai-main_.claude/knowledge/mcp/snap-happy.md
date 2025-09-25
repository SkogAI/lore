# snap-happy MCP Server

## Purpose
Screenshot capture and window management

## Functions
- `mcp__snap-happy__GetLastScreenshot`
- `mcp__snap-happy__TakeScreenshot`
- `mcp__snap-happy__ListWindows`

## Parameters

### TakeScreenshot
- `windowId` (number, optional): Window ID to capture specific window (macOS only)

### GetLastScreenshot
- No parameters

### ListWindows
- No parameters (macOS only)

## Use Cases
- Taking screenshots for debugging/documentation
- Capturing specific application windows
- Getting the most recent screenshot without taking a new one
- Window management and identification

## Test Results
✅ **Tested**: Successfully captured full-screen screenshot showing Claude Code interface

## Status
Available and functional