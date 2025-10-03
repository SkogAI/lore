"""SkogAI Configuration System

This module provides centralized path and configuration management for the SkogAI ecosystem.
All hardcoded paths should be replaced with calls to this configuration system.

Usage:
    from config import paths

    # Get configured paths
    agent_path = paths.get_agent_path("implementations/small_model_agents.py")
    context_dir = paths.get_context_dir()
    config_file = paths.get_config_file("llm_config.json")
"""

from .paths import SkogAIPathResolver, paths
from .settings import SkogAIConfig, config

__all__ = ["SkogAIPathResolver", "paths", "SkogAIConfig", "config"]
