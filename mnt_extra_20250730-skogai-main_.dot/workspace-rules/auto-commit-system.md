# Auto-Commit System

## Overview

The auto-commit system is a critical component of dot's workspace management, ensuring that the workspace remains in a clean state by automatically committing changes. This system implements the core rule that "a git workspace can be in three states: committed, ignored, or on fire."

## Purpose

The auto-commit system addresses several key needs:

1. **Preventing Workspace Lockdown**: Ensures the workspace doesn't get "locked" due to uncommitted changes
2. **Maintaining Clean State**: Keeps the workspace in a committed state for other agents to work with
3. **Enabling Asynchronous Work**: Allows multiple agents to work on the workspace without conflicts
4. **Providing Change History**: Creates a detailed commit history of all changes
5. **Implementing the "Zombie Rule"**: Ensures the system continues to function even in failure scenarios

## System Architecture

### Components

The system consists of:

1. **File Change Detection**:
   - Uses inotifywait to monitor file system events
   - Detects create, modify, delete, move, and close_write events
   - Excludes .git and tmp directories

2. **Auto-Commit Logic**:
   - Checks for uncommitted changes
   - Creates descriptive commit messages
   - Performs the actual git operations

3. **Systemd Integration**:
   - Ensures the monitoring runs continuously
   - Restarts the service if it fails
   - Provides logging and status information

### Service Details

The system runs as systemd user services:

#### skogai-inotifywait.service
