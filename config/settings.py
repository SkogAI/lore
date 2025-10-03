"""Configuration management for SkogAI

Provides configuration loading and management with environment variable fallbacks.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


class SkogAIConfig:
    """Configuration manager for SkogAI ecosystem."""

    def __init__(self):
        """Initialize configuration manager."""
        self._config: Optional[Dict[str, Any]] = None
        self._config_file: Optional[Path] = None

    def load(self, config_path: Optional[Path] = None) -> Dict[str, Any]:
        """Load configuration from file or environment.

        Args:
            config_path: Optional path to configuration file

        Returns:
            Configuration dictionary
        """
        if config_path is None:
            # Try environment variable first
            if config_env := os.environ.get("SKOGAI_CONFIG_FILE"):
                config_path = Path(config_env)
            else:
                # Import here to avoid circular dependency
                from .paths import paths
                config_path = paths.get_config_file("skogai.json")

        self._config_file = config_path

        # Load config file if it exists
        if config_path.exists():
            try:
                with open(config_path, "r") as f:
                    self._config = json.load(f)
            except json.JSONDecodeError as e:
                # Log error but continue with defaults
                print(f"Warning: Failed to parse config file {config_path}: {e}")
                self._config = {}
        else:
            self._config = {}

        return self._config

    def get(self, key: str, default: Any = None, env_var: Optional[str] = None) -> Any:
        """Get a configuration value.

        Priority order:
        1. Environment variable (if env_var provided)
        2. Loaded configuration file
        3. Default value

        Args:
            key: Configuration key (supports dot notation for nested keys)
            default: Default value if key not found
            env_var: Optional environment variable name to check first

        Returns:
            Configuration value
        """
        # Ensure config is loaded
        if self._config is None:
            self.load()

        # Check environment variable first if provided
        if env_var and (env_value := os.environ.get(env_var)):
            return env_value

        # Navigate nested keys (e.g., "llm.api_key")
        value = self._config
        for part in key.split("."):
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return default

        return value if value != self._config else default

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value.

        Args:
            key: Configuration key (supports dot notation for nested keys)
            value: Value to set
        """
        # Ensure config is loaded
        if self._config is None:
            self.load()

        # Navigate and set nested keys
        parts = key.split(".")
        target = self._config

        for part in parts[:-1]:
            if part not in target:
                target[part] = {}
            target = target[part]

        target[parts[-1]] = value

    def save(self, config_path: Optional[Path] = None) -> None:
        """Save configuration to file.

        Args:
            config_path: Optional path to save to (defaults to loaded path)
        """
        if self._config is None:
            return

        save_path = config_path or self._config_file
        if save_path is None:
            from .paths import paths
            save_path = paths.get_config_file("skogai.json")

        # Ensure directory exists
        save_path.parent.mkdir(parents=True, exist_ok=True)

        with open(save_path, "w") as f:
            json.dump(self._config, f, indent=2)

    @property
    def all(self) -> Dict[str, Any]:
        """Get all configuration values.

        Returns:
            Complete configuration dictionary
        """
        if self._config is None:
            self.load()
        return self._config.copy()


# Global singleton instance
config = SkogAIConfig()
