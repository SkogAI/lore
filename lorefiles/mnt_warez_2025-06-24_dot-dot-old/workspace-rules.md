# Workspace Rules

## Overview
This document outlines the critical rules and protocols that must be followed when working within dot's workspace. These rules ensure consistency, traceability, and effective communication between agents and humans.

## Git Management Rules

1. **Workspace State Rule**
   - A git workspace can only be in three states:
     - Files are committed (clean state)
     - Files are explicitly ignored (via .gitignore)
     - The workspace is "on fire" (uncommitted changes that need immediate attention)
   - After any change, files should be committed promptly
   - If the workspace is not committed, it is considered "on lockdown" until cleaned

2. **End-of-Interaction Commit Rule** (CRITICAL)
   - Every interaction MUST end with a clean workspace
   - Before ending any interaction, always run: `git add . && git commit -m "message"`
   - Even a minimal commit message (e.g., `git commit -m "."`) is acceptable
   - This rule is non-negotiable and prevents asynchronous conflicts
   - Example workflow:
     ```bash
     # Make changes to files
     # Before ending interaction:
     git add .
     git commit -m "Updated workspace rules documentation"
     ```

3. **Commit Frequency**
   - Commit after each logical change or set of related changes
   - Don't leave uncommitted changes when completing a task
   - Use atomic commits where possible (one logical change per commit)

4. **Workspace Lockdown**
   - If a workspace has uncommitted changes, it is "on lockdown"
   - No agent should work on a workspace that is "on fire" (has uncommitted changes)
   - This prevents conflicts and ensures clean state transitions
   - Only the agent who left the workspace "on fire" or Skogix should clean it up

## Communication Protocols

1. **INBOX.md Protocol**
   - Messages are appended as single lines to INBOX.md
   - Format: `echo "<message>" >> $SKOGAI_HOME/INBOX.md`
   - Messages are one-way communications from other agents or systems
   - When a message is processed, it should be removed from INBOX.md and the file committed
   - If a message requires human input, note it and leave it pending

2. **SKOGIX.md Protocol**
   - Used for direct communication with Skogix
   - Contains questions that need human answers
   - Skogix will fetch this file when needed
   - Format should be clear and structured for easy response

3. **Message Processing Workflow**
   - Read message from INBOX.md
   - Take appropriate action
   - Remove the processed message
   - Commit changes with descriptive message
   - If human input is needed, add question to SKOGIX.md

## Documentation Rules

1. **Knowledge Base Management**
   - All rules and protocols should be documented in the knowledge base
   - Documentation should be updated whenever rules change
   - Cross-reference related documents
   - Use consistent formatting and structure

2. **Home Folder Management**
   - Be proactive in organizing and maintaining the home folder
   - Document changes to folder structure or organization
   - Keep the workspace clean and well-organized

## Agent Interaction Rules

1. **Task Delegation**
   - Clear specifications when delegating tasks to other agents
   - Follow established communication protocols
   - Provide necessary context for task completion

2. **Knowledge Sharing**
   - Document insights and learnings in the knowledge base
   - Share relevant information with other agents as appropriate
   - Maintain consistent documentation standards

## Success Criteria

Following these rules should result in:
- A clean, well-organized workspace
- Clear communication between agents and humans
- Traceable history of changes and decisions
- Efficient task processing and delegation

## Tags
tags: [rules, protocols, workflow, git, communication]
created: 2025-03-26
updated: 2025-03-26
