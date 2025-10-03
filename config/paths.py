"""
Centralized path configuration for LORE project.

This module provides a single source of truth for all file system paths used
throughout the LORE project. It supports:

- Environment variable overrides (SKOGAI_BASE_DIR)
- Git-aware path resolution (auto-detects repository root)
- Backward compatibility (defaults to /home/skogix/skogai)
- Multiple deployment scenarios

Usage:
    from config.paths import get_agents_dir, get_logs_dir

    agents_dir = get_agents_dir()
    log_file = get_path("logs", "agent.log")
"""

import os
import subprocess
from pathlib import Path
from typing import Optional


def get_repo_root() -> Path:
    """
    Get the repository root directory using git.

    Returns:
        Path: Absolute path to the repository root

    Raises:
        RuntimeError: If not in a git repository
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True
        )
        return Path(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Failed to determine git repository root: {e.stderr}"
        )
    except FileNotFoundError:
        raise RuntimeError("git command not found - is git installed?")


def get_base_dir() -> Path:
    """
    Get the base directory for the LORE project.

    Resolution order:
    1. SKOGAI_BASE_DIR environment variable
    2. Git repository root (if available)
    3. Default: /home/skogix/skogai (for backward compatibility)

    Returns:
        Path: Absolute path to the base directory
    """
    # Check environment variable first
    env_base = os.getenv("SKOGAI_BASE_DIR")
    if env_base:
        return Path(env_base).resolve()

    # Try to use git repository root
    try:
        return get_repo_root()
    except RuntimeError:
        pass

    # Fall back to default for backward compatibility
    return Path("/home/skogix/skogai")


def get_agents_dir() -> Path:
    """Get the agents directory path."""
    return get_base_dir() / "agents"


def get_config_dir() -> Path:
    """Get the config directory path."""
    return get_base_dir() / "config"


def get_demo_dir() -> Path:
    """Get the demo directory path."""
    return get_base_dir() / "demo"


def get_docs_dir() -> Path:
    """Get the docs directory path."""
    return get_base_dir() / "docs"


def get_logs_dir() -> Path:
    """
    Get the logs directory path.

    Can be overridden with SKOGAI_LOGS_DIR environment variable.
    """
    env_logs = os.getenv("SKOGAI_LOGS_DIR")
    if env_logs:
        return Path(env_logs).resolve()
    return get_base_dir() / "logs"


def get_lorefiles_dir() -> Path:
    """Get the lorefiles directory path."""
    return get_base_dir() / "lorefiles"


def get_tools_dir() -> Path:
    """Get the tools directory path."""
    return get_base_dir() / "tools"


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
        >>> log_file = ensure_dir(get_logs_dir()) / "agent.log"
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


# Convenience function for logging configuration
def get_log_file(filename: str) -> Path:
    """
    Get a log file path, ensuring the logs directory exists.

    Args:
        filename: Name of the log file

    Returns:
        Path: Full path to the log file

    Example:
        >>> log_file = get_log_file("agent.log")
    """
    logs_dir = ensure_dir(get_logs_dir())
    return logs_dir / filename
