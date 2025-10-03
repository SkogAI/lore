"""
Centralized path configuration for LORE project.

This module provides a single source of truth for all file system paths used
throughout the LORE project.

Requirements:
    SKOGAI_LORE must be set (via skogcli config export-env --namespace skogai)

Usage:
    from config.paths import get_agents_dir, get_context_dir

    agents_dir = get_agents_dir()
    context_file = get_path("context", "session.json")
"""

import os
from pathlib import Path


def get_base_dir() -> Path:
    """
    Get the base directory for the LORE repository.

    Requires:
        SKOGAI_LORE environment variable (set by skogcli config)

    Returns:
        Path: Absolute path to the LORE repository

    Raises:
        RuntimeError: If SKOGAI_LORE is not set
    """
    lore_dir = os.getenv("SKOGAI_LORE")
    if not lore_dir:
        raise RuntimeError(
            "SKOGAI_LORE environment variable not set. Please set this variable to point to the lore repository path."
        )
    return Path(lore_dir).resolve()


def get_agents_dir() -> Path:
    """Get the agents directory path."""
    return get_base_dir() / "agents"


def get_config_dir() -> Path:
    """Get the config directory path."""
    return get_base_dir() / "config"


def get_demo_dir() -> Path:
    """Get the demo directory path."""
    return get_base_dir() / "demo"


def get_context_dir() -> Path:
    """Get the context directory path."""
    return get_base_dir() / "context"


def get_docs_dir() -> Path:
    """Get the docs directory path."""
    return get_base_dir() / "docs"


def get_knowledge_dir() -> Path:
    """Get the knowledge directory path."""
    return get_base_dir() / "knowledge"


def get_lorefiles_dir() -> Path:
    """Get the lorefiles directory path."""
    return get_base_dir() / "lorefiles"


# Note: get_logs_dir() removed - logs managed by skogai config (SKOGAI_LOGS_DIR)
# Note: get_tools_dir() removed - tools managed by skogcli scripts


def get_path(*parts: str) -> Path:
    """
    Get a path relative to the base directory.

    Args:
        *parts: Path components to join (e.g., "logs", "agent.log")

    Returns:
        Path: Absolute path constructed from base_dir + parts

    Example:
        >>> get_path("logs", "agent.log")
        PosixPath('/home/skogix/skogai/logs/agent.log')

        >>> get_path("agents", "api", "agent_api.py")
        PosixPath('/home/skogix/skogai/agents/api/agent_api.py')
    """
    return get_base_dir().joinpath(*parts)


def ensure_dir(path: Path) -> Path:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        path: Directory path to ensure exists

    Returns:
        Path: The same path (for chaining)

    Example:
        >>> context_file = ensure_dir(get_context_dir()) / "session.json"
    """
    path.mkdir(parents=True, exist_ok=True)
    return path
