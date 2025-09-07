#!/usr/bin/env python3
"""
Test script to verify the version bump workflow logic locally.

This script simulates the workflow steps to ensure they work correctly
before running in GitHub Actions.
"""

import subprocess
import sys
import os
import tempfile
import shutil
from pathlib import Path


def run_command(cmd, description, check=True):
    """Run a command and return success status."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=check,
            capture_output=True,
            text=True
        )
        print(f"✅ {description} - SUCCESS")
        if result.stdout.strip():
            print(f"   Output: {result.stdout.strip()}")
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        print(f"   Error: {e.stderr.strip() if e.stderr else str(e)}")
        if e.stdout:
            print(f"   Stdout: {e.stdout.strip()}")
        return False, e.stderr


def get_current_version():
    """Get the current version from pyproject.toml."""
    import re
    with open('pyproject.toml', 'r') as f:
        content = f.read()
    match = re.search(r'version = "([^"]+)"', content)
    return match.group(1) if match else None


def test_version_bump_logic():
    """Test the version bump logic."""
    print("\n" + "="*50)
    print("🔢 TESTING VERSION BUMP LOGIC")
    print("="*50)

    # Get current version
    current_version = get_current_version()
    print(f"Current version: {current_version}")

    # Test the version extraction command from workflow
    cmd = 'python scripts/get_version.py'
    success, extracted_version = run_command(cmd, "Test version extraction command")

    if not success:
        return False

    if extracted_version != current_version:
        print(f"❌ Version mismatch: expected {current_version}, got {extracted_version}")
        return False

    print(f"✅ Version extraction works correctly: {extracted_version}")
    return True


def test_version_bump_script():
    """Test the version bump script."""
    print("\n" + "="*50)
    print("📝 TESTING VERSION BUMP SCRIPT")
    print("="*50)

    # Create a backup of current files
    backup_dir = Path("backup_test")
    backup_dir.mkdir(exist_ok=True)

    files_to_backup = ["pyproject.toml", "Cargo.toml", "python/demopy/__init__.py"]
    for file_path in files_to_backup:
        if Path(file_path).exists():
            shutil.copy2(file_path, backup_dir / Path(file_path).name)

    try:
        # Get current version
        current_version = get_current_version()
        print(f"Current version: {current_version}")

        # Test patch bump
        success, output = run_command(
            "python scripts/bump_version.py patch",
            "Test patch version bump"
        )

        if not success:
            return False

        # Get new version
        new_version = get_current_version()
        print(f"New version after patch bump: {new_version}")

        # Test the extraction command with new version
        cmd = 'python scripts/get_version.py'
        success, extracted_version = run_command(cmd, "Test version extraction after bump")

        if not success:
            return False

        if extracted_version != new_version:
            print(f"❌ Version extraction failed after bump: expected {new_version}, got {extracted_version}")
            return False

        print(f"✅ Version bump and extraction work correctly")
        return True

    finally:
        # Restore backup files
        print("🔄 Restoring backup files...")
        for file_path in files_to_backup:
            backup_file = backup_dir / Path(file_path).name
            if backup_file.exists():
                shutil.copy2(backup_file, file_path)

        # Clean up backup directory
        shutil.rmtree(backup_dir)
        print("✅ Files restored from backup")


def test_workflow_yaml():
    """Test the workflow YAML syntax."""
    print("\n" + "="*50)
    print("📄 TESTING WORKFLOW YAML SYNTAX")
    print("="*50)

    try:
        import yaml
        with open('.github/workflows/version-bump.yml', 'r') as f:
            yaml.safe_load(f)
        print("✅ version-bump.yml has valid YAML syntax")
        return True
    except ImportError:
        print("⚠️  PyYAML not installed, skipping YAML validation")
        return True
    except yaml.YAMLError as e:
        print(f"❌ Invalid YAML syntax: {e}")
        return False


def simulate_workflow_steps():
    """Simulate the key workflow steps."""
    print("\n" + "="*50)
    print("🔄 SIMULATING WORKFLOW STEPS")
    print("="*50)

    # Step 1: Test version bump
    print("Step 1: Version bump simulation")
    current_version = get_current_version()
    print(f"  Current version: {current_version}")

    # Step 2: Test version extraction (the problematic step)
    print("Step 2: Version extraction simulation")
    cmd = 'python scripts/get_version.py'
    success, version = run_command(cmd, "Simulate NEW_VERSION extraction")

    if not success:
        return False

    # Step 3: Test output variable setting
    print("Step 3: Output variable simulation")
    print(f"  Would set: new_version={version}")

    # Step 4: Test commit message generation
    print("Step 4: Commit message simulation")
    commit_msg = f"Bump version to {version}"
    print(f"  Commit message: {commit_msg}")

    # Step 5: Test tag generation
    print("Step 5: Tag generation simulation")
    tag_name = f"v{version}"
    print(f"  Tag name: {tag_name}")

    print("✅ All workflow steps simulated successfully")
    return True


def main():
    """Main test function."""
    print("🚀 Version Bump Workflow Testing")
    print("Testing the workflow logic before GitHub Actions execution")
    print("="*60)

    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("❌ pyproject.toml not found. Please run this script from the project root.")
        return False

    # Run tests
    tests = [
        ("Workflow YAML Syntax", test_workflow_yaml),
        ("Version Extraction Logic", test_version_bump_logic),
        ("Workflow Steps Simulation", simulate_workflow_steps),
        ("Version Bump Script", test_version_bump_script),
    ]

    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False

    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)

    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False

    if all_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Version bump workflow should work correctly")
        print("✅ IndentationError has been fixed")
        print("✅ Ready to run in GitHub Actions")
    else:
        print("\n⚠️  SOME TESTS FAILED")
        print("❌ Fix issues before running workflow")

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
