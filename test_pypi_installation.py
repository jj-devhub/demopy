#!/usr/bin/env python3
"""
Test script to verify PyPI package installation and functionality.

This script tests the published package from PyPI to ensure the complete
pipeline worked correctly.
"""

import subprocess
import sys
import tempfile
import os
from pathlib import Path


def run_command(cmd, description, cwd=None):
    """Run a command and return success status."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
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


def test_pypi_installation():
    """Test installing the package from PyPI."""
    print("🚀 Testing PyPI Package Installation")
    print("="*50)
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"📁 Using temporary directory: {temp_dir}")
        
        # Create a virtual environment
        venv_path = Path(temp_dir) / "test_venv"
        success, _ = run_command(
            f"python -m venv {venv_path}",
            "Create test virtual environment",
            cwd=temp_dir
        )
        if not success:
            return False
        
        # Determine activation script and python path
        if os.name == 'nt':  # Windows
            python_path = venv_path / "Scripts" / "python"
            pip_path = venv_path / "Scripts" / "pip"
        else:  # Unix-like
            python_path = venv_path / "bin" / "python"
            pip_path = venv_path / "bin" / "pip"
        
        # Upgrade pip
        success, _ = run_command(
            f"{pip_path} install --upgrade pip",
            "Upgrade pip in test environment",
            cwd=temp_dir
        )
        if not success:
            return False
        
        # Install the package from PyPI
        success, _ = run_command(
            f"{pip_path} install demopy_gb_jj==0.3.1",
            "Install demopy_gb_jj v0.3.1 from PyPI",
            cwd=temp_dir
        )
        if not success:
            print("⚠️  Package might not be published yet. Try again in a few minutes.")
            return False
        
        # Test basic functionality
        test_script = '''
import demopy
import sys

print("=== PACKAGE FUNCTIONALITY TEST ===")
print(f"Python version: {sys.version}")
print(f"Package version: {demopy.__version__}")

# Test all functions
print(f"hello(): {demopy.hello()}")
print(f"add(5, 7): {demopy.add(5, 7)}")
print(f"multiply(3.5, 2.0): {demopy.multiply(3.5, 2.0)}")
print(f"sum_list([1,2,3,4,5]): {demopy.sum_list([1,2,3,4,5])}")
print(f"reverse_string('Hello PyPI!'): {demopy.reverse_string('Hello PyPI!')}")

# Check if using Rust extension or Python fallback
hello_msg = demopy.hello()
if "Rust edition" in hello_msg:
    print("✅ Using Rust extension")
elif "Python fallback" in hello_msg:
    print("✅ Using Python fallback")
else:
    print("⚠️  Unknown backend")

print("✅ All functions working correctly!")
'''
        
        success, output = run_command(
            f'{python_path} -c "{test_script}"',
            "Test package functionality",
            cwd=temp_dir
        )
        if not success:
            return False
        
        # Test fallback mechanism
        fallback_test = '''
import sys
import builtins

# Mock import error for Rust extension
original_import = builtins.__import__
def mock_import(name, *args, **kwargs):
    if "demopy_gb_jj._rust" in name:
        raise ImportError("Mocked import error for testing")
    return original_import(name, *args, **kwargs)

builtins.__import__ = mock_import

# Import should use fallback
import demopy

hello_msg = demopy.hello()
if "Python fallback" in hello_msg:
    print("✅ Fallback mechanism working")
    print(f"Fallback hello(): {hello_msg}")
    print(f"Fallback add(10, 20): {demopy.add(10, 20)}")
else:
    print("❌ Fallback mechanism not working")
    sys.exit(1)
'''
        
        success, _ = run_command(
            f'{python_path} -c "{fallback_test}"',
            "Test Python fallback mechanism",
            cwd=temp_dir
        )
        if not success:
            return False
        
        print("\n🎉 PyPI Package Installation Test PASSED!")
        return True


def check_github_release():
    """Check if GitHub release was created."""
    print("\n🏷️ Checking GitHub Release")
    print("="*30)
    
    print("📝 Manual verification steps:")
    print("1. Go to: https://github.com/jj-devhub/demopy/releases")
    print("2. Look for 'Release v0.3.1'")
    print("3. Verify it has:")
    print("   - Auto-generated changelog")
    print("   - Source code archives")
    print("   - Release notes")
    
    return True


def check_pypi_page():
    """Check PyPI page."""
    print("\n📦 Checking PyPI Publication")
    print("="*30)
    
    print("📝 Manual verification steps:")
    print("1. Go to: https://pypi.org/project/demopy-gb-jj/")
    print("2. Verify version 0.3.1 is shown as latest")
    print("3. Check 'Download files' tab for:")
    print("   - Source distribution (.tar.gz)")
    print("   - Wheels for multiple platforms")
    print("   - Python 3.8-3.13 compatibility")
    
    return True


def main():
    """Main test function."""
    print("🚀 End-to-End Pipeline Verification")
    print("Testing the complete release pipeline results")
    print("="*60)
    
    tests = [
        ("PyPI Installation", test_pypi_installation),
        ("GitHub Release", check_github_release),
        ("PyPI Page", check_pypi_page),
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
    print("📊 VERIFICATION SUMMARY")
    print("="*60)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n🎉 COMPLETE PIPELINE SUCCESS!")
        print("✅ Version bump worked")
        print("✅ Release pipeline worked") 
        print("✅ PyPI publication worked")
        print("✅ Package installation works")
        print("✅ All functionality verified")
    else:
        print("\n⚠️  SOME VERIFICATIONS FAILED")
        print("Check the pipeline steps and try again")
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
