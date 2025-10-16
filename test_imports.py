#!/usr/bin/env python3
"""
Test script to verify all dependencies can be imported.
"""

import sys

def test_imports():
    """Test importing all dependencies."""
    failures = []
    successes = []
    
    # Core dependencies
    imports = [
        ("streamlit", "streamlit"),
        ("anthropic", "anthropic"),
        ("openai", "openai"),
        ("requests", "requests"),
        ("textual", "textual"),
        ("rich", "rich"),
        ("gradio", "gradio"),
        ("numpy", "numpy"),
    ]
    
    print("Testing dependency imports...")
    print("-" * 50)
    
    for display_name, import_name in imports:
        try:
            __import__(import_name)
            print(f"✓ {display_name}")
            successes.append(display_name)
        except ImportError as e:
            print(f"✗ {display_name}: {e}")
            failures.append((display_name, str(e)))
    
    print("-" * 50)
    print(f"\nResults: {len(successes)} succeeded, {len(failures)} failed")
    
    if failures:
        print("\nFailed imports:")
        for name, error in failures:
            print(f"  - {name}: {error}")
        return 1
    else:
        print("\n✅ All dependencies imported successfully!")
        return 0

if __name__ == "__main__":
    sys.exit(test_imports())
