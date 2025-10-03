"""
Configuration module for LORE project paths and settings.
"""
from .paths import (
    get_base_dir,
    get_agents_dir,
    get_config_dir,
    get_demo_dir,
    get_context_dir,
    get_docs_dir,
    get_knowledge_dir,
    get_lorefiles_dir,
    get_path,
    ensure_dir,
)

__all__ = [
    "get_base_dir",
    "get_agents_dir",
    "get_config_dir",
    "get_demo_dir",
    "get_context_dir",
    "get_docs_dir",
    "get_knowledge_dir",
    "get_lorefiles_dir",
    "get_path",
    "ensure_dir",
]
