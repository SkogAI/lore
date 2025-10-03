"""Path resolution utilities for SkogAI

Provides centralized path management with environment variable fallbacks.
"""

import os
from pathlib import Path
from typing import Optional


class SkogAIPathResolver:
    """Centralized path resolution for SkogAI ecosystem."""

    def __init__(self):
        """Initialize path resolver with environment-based configuration."""
        # Base directory - defaults to project root or /home/skogix/skogai
        self._base_dir = self._resolve_base_dir()

        # Create commonly used path properties
        self._agents_dir = None
        self._context_dir = None
        self._knowledge_dir = None
        self._config_dir = None
        self._demo_dir = None
        self._tools_dir = None
        self._metrics_dir = None
        self._venv_dir = None

    def _resolve_base_dir(self) -> Path:
        """Resolve the base directory from environment or defaults."""
        # Priority order:
        # 1. SKOGAI_BASE_DIR environment variable
        # 2. Current git repository root
        # 3. Legacy /home/skogix/skogai (for backward compatibility)

        if base_dir := os.environ.get("SKOGAI_BASE_DIR"):
            return Path(base_dir)

        # Try to find git repository root
        current = Path.cwd()
        while current != current.parent:
            if (current / ".git").exists():
                return current
            current = current.parent

        # Fallback to legacy path
        return Path("/home/skogix/skogai")

    @property
    def base_dir(self) -> Path:
        """Get the base directory for SkogAI."""
        return self._base_dir

    @property
    def agents_dir(self) -> Path:
        """Get the agents directory."""
        if self._agents_dir is None:
            self._agents_dir = Path(
                os.environ.get("SKOGAI_AGENTS_DIR", self._base_dir / "agents")
            )
        return self._agents_dir

    @property
    def context_dir(self) -> Path:
        """Get the context directory."""
        if self._context_dir is None:
            self._context_dir = Path(
                os.environ.get("SKOGAI_CONTEXT_DIR", self._base_dir / "context")
            )
        return self._context_dir

    @property
    def knowledge_dir(self) -> Path:
        """Get the knowledge directory."""
        if self._knowledge_dir is None:
            self._knowledge_dir = Path(
                os.environ.get("SKOGAI_KNOWLEDGE_DIR", self._base_dir / "knowledge")
            )
        return self._knowledge_dir

    @property
    def config_dir(self) -> Path:
        """Get the config directory."""
        if self._config_dir is None:
            self._config_dir = Path(
                os.environ.get("SKOGAI_CONFIG_DIR", self._base_dir / "config")
            )
        return self._config_dir

    @property
    def demo_dir(self) -> Path:
        """Get the demo directory."""
        if self._demo_dir is None:
            self._demo_dir = Path(
                os.environ.get("SKOGAI_DEMO_DIR", self._base_dir / "demo")
            )
        return self._demo_dir

    @property
    def tools_dir(self) -> Path:
        """Get the tools directory."""
        if self._tools_dir is None:
            self._tools_dir = Path(
                os.environ.get("SKOGAI_TOOLS_DIR", self._base_dir / "tools")
            )
        return self._tools_dir

    @property
    def metrics_dir(self) -> Path:
        """Get the metrics directory."""
        if self._metrics_dir is None:
            self._metrics_dir = Path(
                os.environ.get("SKOGAI_METRICS_DIR", self._base_dir / "metrics")
            )
        return self._metrics_dir

    @property
    def venv_dir(self) -> Path:
        """Get the virtual environment directory."""
        if self._venv_dir is None:
            self._venv_dir = Path(
                os.environ.get("SKOGAI_VENV_DIR", self._base_dir / ".venv")
            )
        return self._venv_dir

    def get_agent_path(self, relative_path: str) -> Path:
        """Get a path within the agents directory.

        Args:
            relative_path: Path relative to agents directory

        Returns:
            Full path to the agent resource
        """
        return self.agents_dir / relative_path

    def get_context_path(self, relative_path: str) -> Path:
        """Get a path within the context directory.

        Args:
            relative_path: Path relative to context directory

        Returns:
            Full path to the context resource
        """
        return self.context_dir / relative_path

    def get_knowledge_path(self, relative_path: str) -> Path:
        """Get a path within the knowledge directory.

        Args:
            relative_path: Path relative to knowledge directory

        Returns:
            Full path to the knowledge resource
        """
        return self.knowledge_dir / relative_path

    def get_config_file(self, filename: str) -> Path:
        """Get a path to a configuration file.

        Args:
            filename: Configuration filename

        Returns:
            Full path to the configuration file
        """
        return self.config_dir / filename

    def get_demo_output_dir(self, session_id: Optional[str] = None, prefix: str = "output") -> Path:
        """Get a demo output directory, optionally with a session ID.

        Args:
            session_id: Optional session identifier
            prefix: Prefix for the output directory name

        Returns:
            Full path to the demo output directory
        """
        if session_id:
            return self.demo_dir / f"{prefix}_{session_id}"
        return self.demo_dir / prefix

    def ensure_dir(self, path: Path) -> Path:
        """Ensure a directory exists, creating it if necessary.

        Args:
            path: Path to ensure exists

        Returns:
            The path that now exists
        """
        path.mkdir(parents=True, exist_ok=True)
        return path


# Global singleton instance
paths = SkogAIPathResolver()
