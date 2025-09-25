---
allowed-tools: Task, Read, Bash(git:*), Bash(gh:*), WebSearch, Grep, Glob
description: Create a well-researched GitHub issue from description
argument-hint: <issue-description>
model: claude-3-5-sonnet-20241022
---

# Create GitHub Issue

## Task Overview
Research and create a GitHub issue based on: $ARGUMENTS

## Current Repository Context
!git remote get-url origin
!git branch --show-current
!gh repo view --json name,owner,description

## Issue Creation Process

1. First, use the researcher agent to analyze existing documentation and codebase:
   - Search for related documentation in README.md, CLAUDE.md, and docs/
   - Look for similar existing issues or patterns
   - Understand the project context and conventions

2. Use the orchestrator agent to:
   - Synthesize findings from research
   - Structure the issue according to GitHub best practices
   - Ensure alignment with project goals

3. Create the issue with:
   - Clear, descriptive title
   - Problem statement or feature description
   - Context from documentation research
   - Acceptance criteria or expected behavior
   - Technical details if applicable
   - Related issues or PRs if found

## Instructions for Claude

1. Launch researcher agent to investigate:
   - Existing documentation about the topic
   - Similar issues in the repository
   - Code patterns or implementations related to the request

2. Based on research, draft a comprehensive issue that includes:
   - **Title**: Concise and descriptive
   - **Description**: Clear problem/feature statement
   - **Context**: Reference to relevant documentation or code
   - **Acceptance Criteria**: What defines "done"
   - **Technical Notes**: Implementation considerations if applicable

3. Use `gh issue create` to submit the issue with proper formatting

The issue should be well-researched and reference existing project documentation to maintain consistency with the codebase.