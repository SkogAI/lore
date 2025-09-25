# Interrupt_User MCP Server

## Purpose
Ask user for missing context during research and development

## Function
- `mcp__Interrupt_User__asking_user_missing_context`

## Parameters
- `question` (string): Specific question about missing context (max 1000 chars)
- `context` (string, optional): Background info explaining why context is needed (max 2000 chars)

## Use Cases
- Multiple valid implementation approaches exist
- Need clarification on preferred tech stack/framework
- Missing domain-specific requirements or constraints
- Uncertain about user's goals or priorities
- Need to understand existing codebase patterns

## Test Results
✅ **Tested**: Successfully prompted user for testing preferences (timed out after 1 minute, which is expected behavior)

## Status
Available and functional