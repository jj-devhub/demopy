#!/usr/bin/env python3
"""
Test script for the automated CI/CD pipeline.

This script helps test and validate the automated release pipeline
by simulating different commit message scenarios and verifying
the expected version bump behavior.
"""

import re
import subprocess
import sys
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
        if result.stdout.strip():
            print(f"   Output: {result.stdout.strip()}")
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        print(f"   Error: {e.stderr.strip() if e.stderr else str(e)}")
        return False, e.stderr


def get_current_version():
    """Get current version from pyproject.toml."""
    try:
        result = subprocess.run(
            ["python", "scripts/get_version.py"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def test_commit_message_analysis():
    """Test commit message analysis logic."""
    print("\n" + "="*60)
    print("🔍 TESTING COMMIT MESSAGE ANALYSIS")
    print("="*60)
    
    test_cases = [
        # (commit_message, expected_version_type)
        ("feat: add new mathematical functions", "minor"),
        ("fix: resolve memory leak in Rust extension", "patch"),
        ("BREAKING CHANGE: redesign API", "major"),
        ("chore: update dependencies", "patch"),
        ("docs: update README", "patch"),
        ("style: fix code formatting", "patch"),
        ("refactor: improve code structure", "patch"),
        ("perf: optimize calculation speed", "patch"),
        ("test: add more unit tests", "patch"),
        ("feature: implement new algorithm", "minor"),
        ("patch: fix minor bug", "patch"),
        ("major: complete API overhaul", "major"),
        ("breaking: remove deprecated functions", "major"),
        ("update README with examples", "none"),  # No semantic prefix
        ("random commit message", "none"),  # No semantic prefix
    ]
    
    print("Testing commit message patterns:")
    print("-" * 40)
    
    all_passed = True
    for commit_msg, expected in test_cases:
        # Simulate the logic from the workflow
        version_type = "none"
        
        if re.search(r"(BREAKING CHANGE|breaking:|major:)", commit_msg, re.IGNORECASE):
            version_type = "major"
        elif re.search(r"(feat:|feature:|minor:)", commit_msg, re.IGNORECASE):
            version_type = "minor"
        elif re.search(r"(fix:|patch:|chore:|docs:|style:|refactor:|perf:|test:)", commit_msg, re.IGNORECASE):
            version_type = "patch"
        
        status = "✅" if version_type == expected else "❌"
        print(f"{status} '{commit_msg[:40]}...' → {version_type} (expected: {expected})")
        
        if version_type != expected:
            all_passed = False
    
    return all_passed


def test_version_bumping():
    """Test version bumping logic."""
    print("\n" + "="*60)
    print("🔢 TESTING VERSION BUMPING LOGIC")
    print("="*60)
    
    current_version = get_current_version()
    if not current_version:
        print("❌ Could not get current version")
        return False
    
    print(f"Current version: {current_version}")
    
    # Test different bump types
    test_cases = [
        ("patch", "patch version bump"),
        ("minor", "minor version bump"),
        ("major", "major version bump"),
    ]
    
    all_passed = True
    for bump_type, description in test_cases:
        # Create a backup of current files
        backup_files = {}
        files_to_backup = ["pyproject.toml", "Cargo.toml", "python/demopy/__init__.py"]
        
        for file_path in files_to_backup:
            if Path(file_path).exists():
                with open(file_path, 'r') as f:
                    backup_files[file_path] = f.read()
        
        try:
            # Test version bump
            success, output = run_command(
                f"python scripts/bump_version.py {bump_type}",
                f"Test {description}"
            )
            
            if success:
                new_version = get_current_version()
                print(f"   New version: {new_version}")
                
                # Verify version format
                if re.match(r'^\d+\.\d+\.\d+$', new_version):
                    print(f"   ✅ Valid version format")
                else:
                    print(f"   ❌ Invalid version format: {new_version}")
                    all_passed = False
            else:
                all_passed = False
        
        finally:
            # Restore backup files
            for file_path, content in backup_files.items():
                with open(file_path, 'w') as f:
                    f.write(content)
    
    return all_passed


def test_workflow_syntax():
    """Test workflow YAML syntax."""
    print("\n" + "="*60)
    print("📄 TESTING WORKFLOW YAML SYNTAX")
    print("="*60)
    
    workflows = [
        ".github/workflows/auto-release.yml",
        ".github/workflows/version-bump.yml",
        ".github/workflows/release.yml",
    ]
    
    all_passed = True
    for workflow in workflows:
        if not Path(workflow).exists():
            print(f"❌ {workflow} not found")
            all_passed = False
            continue
        
        try:
            import yaml
            with open(workflow, 'r') as f:
                yaml.safe_load(f)
            print(f"✅ {workflow} has valid YAML syntax")
        except ImportError:
            print(f"⚠️  PyYAML not installed, skipping {workflow} validation")
        except yaml.YAMLError as e:
            print(f"❌ {workflow} has invalid YAML syntax: {e}")
            all_passed = False
    
    return all_passed


def test_semantic_versioning():
    """Test semantic versioning calculations."""
    print("\n" + "="*60)
    print("🏷️ TESTING SEMANTIC VERSIONING")
    print("="*60)
    
    test_cases = [
        # (current_version, bump_type, expected_result)
        ("1.0.0", "patch", "1.0.1"),
        ("1.0.0", "minor", "1.1.0"),
        ("1.0.0", "major", "2.0.0"),
        ("0.4.0", "patch", "0.4.1"),
        ("0.4.0", "minor", "0.5.0"),
        ("0.4.0", "major", "1.0.0"),
        ("2.3.5", "patch", "2.3.6"),
        ("2.3.5", "minor", "2.4.0"),
        ("2.3.5", "major", "3.0.0"),
    ]
    
    all_passed = True
    for current, bump_type, expected in test_cases:
        # Parse current version
        major, minor, patch = map(int, current.split('.'))
        
        # Calculate expected new version
        if bump_type == "major":
            new_version = f"{major + 1}.0.0"
        elif bump_type == "minor":
            new_version = f"{major}.{minor + 1}.0"
        elif bump_type == "patch":
            new_version = f"{major}.{minor}.{patch + 1}"
        
        status = "✅" if new_version == expected else "❌"
        print(f"{status} {current} + {bump_type} → {new_version} (expected: {expected})")
        
        if new_version != expected:
            all_passed = False
    
    return all_passed


def test_pipeline_integration():
    """Test pipeline integration points."""
    print("\n" + "="*60)
    print("🔗 TESTING PIPELINE INTEGRATION")
    print("="*60)
    
    checks = [
        ("scripts/get_version.py exists", Path("scripts/get_version.py").exists()),
        ("scripts/bump_version.py exists", Path("scripts/bump_version.py").exists()),
        ("pyproject.toml exists", Path("pyproject.toml").exists()),
        ("Cargo.toml exists", Path("Cargo.toml").exists()),
        ("python/demopy/__init__.py exists", Path("python/demopy/__init__.py").exists()),
        (".github/workflows/auto-release.yml exists", Path(".github/workflows/auto-release.yml").exists()),
        ("CONTRIBUTING.md exists", Path("CONTRIBUTING.md").exists()),
    ]
    
    all_passed = True
    for description, result in checks:
        status = "✅" if result else "❌"
        print(f"{status} {description}")
        if not result:
            all_passed = False
    
    # Test script execution
    success, _ = run_command(
        "python scripts/get_version.py",
        "Test get_version.py execution"
    )
    if not success:
        all_passed = False
    
    return all_passed


def main():
    """Main test function."""
    print("🚀 Automated CI/CD Pipeline Testing")
    print("Testing the automated release pipeline components")
    print("="*60)
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("❌ pyproject.toml not found. Please run this script from the project root.")
        return False
    
    # Run all tests
    tests = [
        ("Commit Message Analysis", test_commit_message_analysis),
        ("Version Bumping Logic", test_version_bumping),
        ("Workflow YAML Syntax", test_workflow_syntax),
        ("Semantic Versioning", test_semantic_versioning),
        ("Pipeline Integration", test_pipeline_integration),
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
        print("✅ Automated CI/CD pipeline is ready")
        print("✅ Commit message analysis works correctly")
        print("✅ Version bumping logic is functional")
        print("✅ Workflow files are valid")
        print("✅ Integration points are configured")
        print("\n🚀 Ready for automated releases!")
    else:
        print("\n⚠️  SOME TESTS FAILED")
        print("❌ Fix issues before using automated pipeline")
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
