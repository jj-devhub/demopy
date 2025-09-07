#!/usr/bin/env python3
"""
Test script for automated release logic.

This script simulates the automated release workflow logic to help debug
version bumping and release detection issues.
"""

import re
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description=""):
    """Run a command and return success status and output."""
    try:
        result = subprocess.run(
            cmd, shell=True, check=True, capture_output=True, text=True
        )
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {cmd}")
        if e.stderr:
            print(f"Error: {e.stderr.strip()}")
        return False, e.stderr.strip() if e.stderr else ""


def get_current_version():
    """Get current version from pyproject.toml."""
    try:
        with open("pyproject.toml", "r") as f:
            content = f.read()
        match = re.search(r'version = "([^"]+)"', content)
        if match:
            return match.group(1)
        else:
            print("ERROR: Version not found in pyproject.toml")
            return None
    except Exception as e:
        print(f"ERROR: Failed to read pyproject.toml: {e}")
        return None


def analyze_commits():
    """Analyze commits since last tag to determine version bump type."""
    print("=" * 60)
    print("ANALYZING COMMITS FOR VERSION BUMP")
    print("=" * 60)

    # Get current version
    current_version = get_current_version()
    if not current_version:
        return None, None, None

    print(f"Current version: {current_version}")

    # Get last tag
    success, last_tag = run_command("git describe --tags --abbrev=0")
    if not success or not last_tag.strip():
        print("No previous tags found, analyzing all commits")
        success, commits = run_command("git log --oneline")
        last_tag = "initial"
    else:
        last_tag = last_tag.strip()
        print(f"Last tag: {last_tag}")
        success, commits = run_command(f"git log {last_tag}..HEAD --oneline")

    if not success:
        print("Failed to get commit history")
        return None, None, None

    if not commits.strip():
        print("No commits found since last tag")
        return current_version, "none", []

    commit_lines = commits.strip().split("\n")
    print(f"Analyzing {len(commit_lines)} commits since {last_tag}:")
    for i, commit in enumerate(commit_lines, 1):
        print(f"  {i}. {commit}")

    # Determine version bump type
    version_type = "none"
    matching_commits = []

    # Check for breaking changes (major version)
    for commit in commit_lines:
        if re.search(r"(BREAKING CHANGE|breaking:|major:)", commit, re.IGNORECASE):
            version_type = "major"
            matching_commits.append(f"BREAKING: {commit}")

    # Check for new features (minor version) if no breaking changes
    if version_type == "none":
        for commit in commit_lines:
            if re.search(r"(feat:|feature:|minor:)", commit, re.IGNORECASE):
                version_type = "minor"
                matching_commits.append(f"FEATURE: {commit}")

    # Check for bug fixes and other changes (patch version) if no features
    if version_type == "none":
        for commit in commit_lines:
            if re.search(
                r"(fix:|patch:|chore:|docs:|style:|refactor:|perf:|test:)",
                commit,
                re.IGNORECASE,
            ):
                version_type = "patch"
                matching_commits.append(f"FIX/MAINTENANCE: {commit}")

    print("\nVersion bump analysis:")
    print(f"  Determined type: {version_type}")
    if matching_commits:
        print("  Matching commits:")
        for match in matching_commits:
            print(f"    - {match}")
    else:
        print("  No version-relevant commits found")

    return current_version, version_type, commit_lines


def simulate_version_bump(current_version, version_type):
    """Simulate version bump calculation."""
    if version_type == "none":
        return current_version

    # Parse current version
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)$", current_version)
    if not match:
        print(f"ERROR: Invalid version format: {current_version}")
        return None

    major, minor, patch = map(int, match.groups())

    if version_type == "major":
        new_version = f"{major + 1}.0.0"
    elif version_type == "minor":
        new_version = f"{major}.{minor + 1}.0"
    elif version_type == "patch":
        new_version = f"{major}.{minor}.{patch + 1}"
    else:
        new_version = current_version

    print("\nVersion bump simulation:")
    print(f"  Current: {current_version}")
    print(f"  Type: {version_type}")
    print(f"  New: {new_version}")

    return new_version


def check_version_consistency():
    """Check if version is consistent across all files."""
    print("\n" + "=" * 60)
    print("CHECKING VERSION CONSISTENCY")
    print("=" * 60)

    files_to_check = [
        ("pyproject.toml", r'version = "([^"]+)"'),
        ("Cargo.toml", r'version = "([^"]+)"'),
        ("python/demopy/__init__.py", r'__version__ = "([^"]+)"'),
    ]

    versions = {}
    all_consistent = True

    for file_path, pattern in files_to_check:
        if Path(file_path).exists():
            try:
                with open(file_path, "r") as f:
                    content = f.read()
                match = re.search(pattern, content)
                if match:
                    version = match.group(1)
                    versions[file_path] = version
                    print(f"  {file_path}: {version}")
                else:
                    print(f"  {file_path}: VERSION NOT FOUND")
                    all_consistent = False
            except Exception as e:
                print(f"  {file_path}: ERROR - {e}")
                all_consistent = False
        else:
            print(f"  {file_path}: FILE NOT FOUND")
            all_consistent = False

    # Check if all versions are the same
    unique_versions = set(versions.values())
    if len(unique_versions) == 1:
        print(f"\n✅ All versions are consistent: {list(unique_versions)[0]}")
    else:
        print("\n❌ Version inconsistency detected!")
        print(f"   Found versions: {unique_versions}")
        all_consistent = False

    return all_consistent, versions


def main():
    """Main test function."""
    print("🧪 Automated Release Logic Test")
    print("Testing version bump detection and consistency")
    print("=" * 60)

    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print(
            "❌ pyproject.toml not found. Please run this script from the project root."
        )
        return False

    # Check version consistency
    consistent, versions = check_version_consistency()

    # Analyze commits for version bump
    current_version, version_type, commits = analyze_commits()

    if current_version is None:
        print("❌ Failed to analyze commits")
        return False

    # Simulate version bump
    if version_type != "none":
        new_version = simulate_version_bump(current_version, version_type)
        if new_version:
            print("\n🎯 Release Decision:")
            print("   Should release: YES")
            print(f"   Version bump: {current_version} → {new_version}")
            print(f"   Bump type: {version_type}")
        else:
            print("\n❌ Failed to calculate new version")
            return False
    else:
        print("\n🎯 Release Decision:")
        print("   Should release: NO")
        print("   Reason: No version-relevant commits found")

    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)

    if consistent:
        print("✅ Version files are consistent")
    else:
        print("❌ Version files are inconsistent - this will cause release issues")

    if version_type != "none":
        print(f"✅ Found {version_type} commits - release should be triggered")
    else:
        print("ℹ️  No release-triggering commits found")

    print("\n💡 Next Steps:")
    if not consistent:
        print("   1. Fix version inconsistencies in files")
    if version_type != "none":
        print("   2. Push changes to trigger automated release")
        print("   3. Monitor GitHub Actions for release workflow")
    else:
        print("   1. Make commits with semantic prefixes (feat:, fix:, etc.)")
        print("   2. Push to main branch to trigger release")

    return consistent and (version_type != "none")


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
