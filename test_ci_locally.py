#!/usr/bin/env python3
"""
Local CI test script to verify fixes before pushing to GitHub.

This script simulates the CI workflow steps locally to catch issues early.
"""

import subprocess
import sys
import os
import tempfile
import shutil
from pathlib import Path


def run_command(cmd, description, cwd=None, shell=True):
    """Run a command and return success status."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            cmd,
            shell=shell,
            check=True,
            capture_output=True,
            text=True,
            cwd=cwd
        )
        print(f"✅ {description} - SUCCESS")
        if result.stdout.strip():
            print(f"   Output: {result.stdout.strip()}")
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        print(f"   Error: {e.stderr.strip() if e.stderr else str(e)}")
        if e.stdout:
            print(f"   Stdout: {e.stdout.strip()}")
        return False, e.stderr


def test_rust_components():
    """Test Rust compilation and tests."""
    print("\n" + "="*50)
    print("🦀 TESTING RUST COMPONENTS")
    print("="*50)

    # Test Rust compilation
    success, _ = run_command("cargo check", "Rust compilation check")
    if not success:
        return False

    # Test Rust tests
    success, _ = run_command("cargo test", "Rust unit tests")
    if not success:
        return False

    # Test Rust linting
    success, _ = run_command("cargo fmt --all -- --check", "Rust formatting check")
    if not success:
        print("⚠️  Rust formatting issues found. Run 'cargo fmt' to fix.")

    success, _ = run_command("cargo clippy -- -D warnings", "Rust linting")
    if not success:
        print("⚠️  Rust linting issues found.")

    return True


def test_python_components():
    """Test Python components with virtual environment."""
    print("\n" + "="*50)
    print("🐍 TESTING PYTHON COMPONENTS")
    print("="*50)

    # Create temporary virtual environment
    with tempfile.TemporaryDirectory() as temp_dir:
        venv_path = Path(temp_dir) / "test_venv"

        # Create virtual environment
        success, _ = run_command(
            f"python -m venv {venv_path}",
            "Create virtual environment"
        )
        if not success:
            return False

        # Determine activation script path
        if os.name == 'nt':  # Windows
            activate_script = venv_path / "Scripts" / "activate.bat"
            pip_path = venv_path / "Scripts" / "pip"
            python_path = venv_path / "Scripts" / "python"
        else:  # Unix-like
            activate_script = venv_path / "bin" / "activate"
            pip_path = venv_path / "bin" / "pip"
            python_path = venv_path / "bin" / "python"

        # Install dependencies in virtual environment
        success, _ = run_command(
            f"{pip_path} install --upgrade pip",
            "Upgrade pip in venv"
        )
        if not success:
            return False

        success, _ = run_command(
            f"{pip_path} install maturin pytest",
            "Install dependencies in venv"
        )
        if not success:
            return False

        # Build Python extension
        success, _ = run_command(
            f"{python_path} -m maturin develop",
            "Build Python extension with maturin"
        )
        if not success:
            print("⚠️  Maturin develop failed. This might be expected in some environments.")
            # Continue with fallback testing

        # Test Python tests
        success, _ = run_command(
            f"{python_path} -m pytest tests/ -v",
            "Run Python tests"
        )
        if not success:
            return False

        # Test Python fallback
        fallback_test = '''
import sys
sys.path.insert(0, "python")
import builtins
original_import = builtins.__import__
def mock_import(name, *args, **kwargs):
    if "demopy_gb_jj._rust" in name:
        raise ImportError("Mocked import error")
    return original_import(name, *args, **kwargs)
builtins.__import__ = mock_import

import demopy
assert "Python fallback" in demopy.hello()
assert demopy.add(2, 3) == 5
print("Pure Python fallback test passed!")
'''

        success, _ = run_command(
            f'{python_path} -c "{fallback_test}"',
            "Test Python fallback mechanism"
        )
        if not success:
            return False

    return True


def test_workflow_syntax():
    """Test GitHub Actions workflow syntax."""
    print("\n" + "="*50)
    print("⚙️  TESTING WORKFLOW SYNTAX")
    print("="*50)

    workflow_files = [
        ".github/workflows/ci.yml",
        ".github/workflows/release.yml",
        ".github/workflows/version-bump.yml"
    ]

    for workflow_file in workflow_files:
        if Path(workflow_file).exists():
            # Basic YAML syntax check
            try:
                import yaml
                with open(workflow_file, 'r') as f:
                    yaml.safe_load(f)
                print(f"✅ {workflow_file} - Valid YAML syntax")
            except ImportError:
                print(f"⚠️  PyYAML not installed, skipping YAML validation for {workflow_file}")
            except yaml.YAMLError as e:
                print(f"❌ {workflow_file} - Invalid YAML syntax: {e}")
                return False
        else:
            print(f"⚠️  {workflow_file} not found")

    return True


def main():
    """Main test function."""
    print("🚀 Starting Local CI Testing")
    print("This script simulates the GitHub Actions CI workflow locally")
    print("="*60)

    # Check if we're in the right directory
    if not Path("Cargo.toml").exists():
        print("❌ Cargo.toml not found. Please run this script from the project root.")
        return False

    # Test components
    tests = [
        ("Workflow Syntax", test_workflow_syntax),
        ("Rust Components", test_rust_components),
        ("Python Components", test_python_components),
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
        print("✅ Ready to push to GitHub")
        print("✅ CI workflow should work correctly")
    else:
        print("\n⚠️  SOME TESTS FAILED")
        print("❌ Fix issues before pushing to GitHub")
        print("❌ CI workflow may fail")

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
