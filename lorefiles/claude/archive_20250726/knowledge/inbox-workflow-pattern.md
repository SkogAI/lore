# Inbox Workflow Pattern

## Core Concept

An inbox.md file serves as a message queue for autonomous work. Messages are consumed by:

1. Reading the message to understand the problem
2. Performing the necessary work to address it
3. Removing the message from inbox.md before committing
4. Committing with intent that connects the inbox message to the changes made

## Example Workflow

**Message**: "There has been a problem with x, can you look it up <3 skogix"
**Process**:

1. Read inbox.md to see the message
2. Investigate and fix problem x
3. Remove message from inbox.md
4. Commit with intent: "Responding to inbox.md: Fixed problem x - [description of changes made]"

## Why This Works

- **Autonomous operation**: Claude can work independently on queued tasks
- **Intent preservation**: Each commit connects the trigger (inbox message) to the response (changes made)
- **Clean state**: Inbox is cleared after processing, preventing duplicate work
- **Audit trail**: Git history shows both the intent and the resolution

## Connection to Our System

- Aligns with "connection intent with change" principle
- Provides mechanism for asynchronous collaboration
- Maintains transparency in autonomous actions
- Creates clear cause-and-effect relationships in git history

## Implementation Pattern

```
Intent: Responding to inbox.md: [original message summary]
Change: [specific changes made to address the message]
```

This creates a complete narrative from problem identification to resolution.

---

skogix:

In the SkogAI ecosystem, git diffs are elevated from mere change tracking to first-class knowledge artifacts. They serve as structured representations of thought evolution, decision-making processes, and system transformations. This document explains how git diffs are used as a foundational knowledge representation mechanism.

Git diffs in SkogAI are designed to tell complete stories with a beginning, middle, and end:

- **Input State**: The original condition of files/knowledge
- **Transformation**: The specific changes made
- **Output State**: The resulting condition after changes

This narrative structure allows diffs to document not just what changed, but why and how it evolved.

The diff history allows reconstruction of idea development:

- New tasks appearing after discussions imply conceptual connections
- File reorganizations reflect evolving understanding
- Changes to terminology indicate refinement of concepts

Commit sequences reveal decision-making patterns:

- Initial attempts followed by refinements show iterative problem-solving
- Sequence of related changes illustrates methodology
- Timing between changes highlights priority and difficulty

Diffs provide a common language for agent communication:

- Changes proposed by one agent can be reviewed by another
- Intent is preserved even across different implementations
- Complex actions can be composed from simple, well-defined changes

