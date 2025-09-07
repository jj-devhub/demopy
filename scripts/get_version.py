#!/usr/bin/env python3
"""
Simple script to extract the current version from pyproject.toml.

This script is used by the GitHub Actions workflow to get the version
after the bump_version.py script has updated it.
"""

import re
import sys
from pathlib import Path


def get_version():
    """Extract version from pyproject.toml."""
    pyproject_path = Path("pyproject.toml")

    if not pyproject_path.exists():
        print("ERROR: pyproject.toml not found", file=sys.stderr)
        sys.exit(1)

    try:
        with open(pyproject_path, "r") as f:
            content = f.read()

        # Search for version line
        match = re.search(r'version = "([^"]+)"', content)

        if match:
            version = match.group(1)
            print(version)
            return version
        else:
            print("ERROR: Version not found in pyproject.toml", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"ERROR: Failed to read pyproject.toml: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    get_version()
