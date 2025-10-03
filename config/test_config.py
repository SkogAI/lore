#!/usr/bin/env python3
"""
Simple test script to verify the configuration system works correctly.
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import config
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.paths import (
    get_base_dir,
    get_agents_dir,
    get_config_dir,
    get_demo_dir,
    get_docs_dir,
    get_logs_dir,
    get_lorefiles_dir,
    get_tools_dir,
    get_path,
    get_log_file,
    ensure_dir,
)


def test_basic_paths():
    """Test basic path resolution."""
    print("Testing basic path resolution...")

    base = get_base_dir()
    assert base.is_absolute(), "Base directory should be absolute"
    print(f"  ✅ Base directory: {base}")

    agents = get_agents_dir()
    assert agents == base / "agents"
    print(f"  ✅ Agents directory: {agents}")

    config = get_config_dir()
    assert config == base / "config"
    print(f"  ✅ Config directory: {config}")

    demo = get_demo_dir()
    assert demo == base / "demo"
    print(f"  ✅ Demo directory: {demo}")

    docs = get_docs_dir()
    assert docs == base / "docs"
    print(f"  ✅ Docs directory: {docs}")

    logs = get_logs_dir()
    assert logs == base / "logs"
    print(f"  ✅ Logs directory: {logs}")

    lorefiles = get_lorefiles_dir()
    assert lorefiles == base / "lorefiles"
    print(f"  ✅ Lorefiles directory: {lorefiles}")

    tools = get_tools_dir()
    assert tools == base / "tools"
    print(f"  ✅ Tools directory: {tools}")


def test_custom_paths():
    """Test custom path construction."""
    print("\nTesting custom path construction...")

    path1 = get_path("demo", "workflow.py")
    assert path1 == get_base_dir() / "demo" / "workflow.py"
    print(f"  ✅ Custom path 1: {path1}")

    path2 = get_path("agents", "api", "agent_api.py")
    assert path2 == get_base_dir() / "agents" / "api" / "agent_api.py"
    print(f"  ✅ Custom path 2: {path2}")


def test_log_file():
    """Test log file path generation."""
    print("\nTesting log file generation...")

    log = get_log_file("test.log")
    assert log == get_logs_dir() / "test.log"
    print(f"  ✅ Log file: {log}")


def test_ensure_dir():
    """Test directory creation."""
    print("\nTesting directory creation...")

    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir) / "test" / "nested" / "dir"
        result = ensure_dir(test_dir)
        assert test_dir.exists()
        assert test_dir.is_dir()
        assert result == test_dir
        print(f"  ✅ Directory creation works")


def main():
    print("=" * 70)
    print("Configuration System Test")
    print("=" * 70)
    print()

    try:
        test_basic_paths()
        test_custom_paths()
        test_log_file()
        test_ensure_dir()

        print()
        print("=" * 70)
        print("✅ All tests passed!")
        print("=" * 70)
        return 0

    except AssertionError as e:
        print()
        print("=" * 70)
        print(f"❌ Test failed: {e}")
        print("=" * 70)
        return 1

    except Exception as e:
        print()
        print("=" * 70)
        print(f"❌ Unexpected error: {e}")
        print("=" * 70)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
