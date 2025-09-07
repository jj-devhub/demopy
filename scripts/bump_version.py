#!/usr/bin/env python3
"""
Version bumping script for demopy_gb_jj

This script updates version numbers across all relevant files:
- Cargo.toml
- pyproject.toml
- python/demopy/__init__.py

Usage:
    python scripts/bump_version.py patch    # 0.2.5 -> 0.2.6
    python scripts/bump_version.py minor    # 0.2.5 -> 0.3.0
    python scripts/bump_version.py major    # 0.2.5 -> 1.0.0
    python scripts/bump_version.py 1.2.3    # Set specific version
"""

import argparse
import re
import sys
from pathlib import Path


def parse_version(version_str):
    """Parse a semantic version string into major, minor, patch components."""
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)$", version_str)
    if not match:
        raise ValueError(f"Invalid version format: {version_str}")
    return tuple(map(int, match.groups()))


def bump_version(current_version, bump_type):
    """Bump version according to the specified type."""
    major, minor, patch = parse_version(current_version)

    if bump_type == "major":
        return f"{major + 1}.0.0"
    elif bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    elif bump_type == "patch":
        return f"{major}.{minor}.{patch + 1}"
    else:
        # Assume it's a specific version
        parse_version(bump_type)  # Validate format
        return bump_type


def get_current_version():
    """Get current version from pyproject.toml."""
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        raise FileNotFoundError("pyproject.toml not found")

    content = pyproject_path.read_text()
    match = re.search(r'^version = "([^"]+)"', content, re.MULTILINE)
    if not match:
        raise ValueError("Version not found in pyproject.toml")

    return match.group(1)


def update_file(file_path, pattern, replacement):
    """Update version in a file using regex pattern."""
    path = Path(file_path)
    if not path.exists():
        print(f"Warning: {file_path} not found, skipping...")
        return False

    content = path.read_text()
    new_content = re.sub(pattern, replacement, content)

    if content != new_content:
        path.write_text(new_content)
        print(f"Updated {file_path}")
        return True
    else:
        print(f"No changes needed in {file_path}")
        return False


def update_all_versions(new_version):
    """Update version in all relevant files."""
    files_updated = []

    # Update pyproject.toml
    if update_file(
        "pyproject.toml", r'version = "[^"]+"', f'version = "{new_version}"'
    ):
        files_updated.append("pyproject.toml")

    # Update Cargo.toml (only the package version, not dependencies)
    if update_file(
        "Cargo.toml",
        r'(\[package\][\s\S]*?)version = "[^"]+"',
        rf'\1version = "{new_version}"',
    ):
        files_updated.append("Cargo.toml")

    # Update python/demopy/__init__.py
    if update_file(
        "python/demopy/__init__.py",
        r'__version__ = "[^"]+"',
        f'__version__ = "{new_version}"',
    ):
        files_updated.append("python/demopy/__init__.py")

    return files_updated


def main():
    parser = argparse.ArgumentParser(
        description="Bump version across all project files"
    )
    parser.add_argument(
        "bump_type",
        help="Version bump type (major, minor, patch) or specific version (e.g., 1.2.3)",
    )

    args = parser.parse_args()

    # Handle argument parsing
    bump_type = args.bump_type

    try:
        current_version = get_current_version()
        print(f"Current version: {current_version}")

        new_version = bump_version(current_version, bump_type)
        print(f"New version: {new_version}")

        files_updated = update_all_versions(new_version)

        if files_updated:
            print(f"\nSuccessfully updated version to {new_version} in:")
            for file in files_updated:
                print(f"  - {file}")
        else:
            print("No files were updated.")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
