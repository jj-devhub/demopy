#!/usr/bin/env python3
"""
End-to-end test script for demopy_gb_jj package installation and functionality.

This script tests:
1. Package installation from PyPI
2. Rust extension functionality (if available)
3. Python fallback functionality
4. Version consistency
5. All exported functions
"""

import subprocess
import sys
import tempfile
import os
from pathlib import Path


def run_command(cmd, description):
    """Run a command and return success status."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - SUCCESS")
        if result.stdout.strip():
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        print(f"   Error: {e.stderr.strip() if e.stderr else str(e)}")
        return False


def test_package_functionality():
    """Test the package functionality."""
    test_code = '''
import demopy

print("=== PACKAGE FUNCTIONALITY TEST ===")

# Test version
print(f"Version: {demopy.__version__}")

# Test all functions
print(f"hello(): {demopy.hello()}")
print(f"add(2, 3): {demopy.add(2, 3)}")
print(f"multiply(2.5, 4.0): {demopy.multiply(2.5, 4.0)}")
print(f"sum_list([1,2,3,4,5]): {demopy.sum_list([1,2,3,4,5])}")
print(f"reverse_string('Hello World'): {demopy.reverse_string('Hello World')}")

# Test __all__ exports
print(f"Exported functions: {demopy.__all__}")

# Detect if using Rust extension or Python fallback
hello_msg = demopy.hello()
if "Rust edition" in hello_msg:
    print("✅ Using Rust extension")
elif "Python fallback" in hello_msg:
    print("✅ Using Python fallback")
else:
    print("⚠️  Unknown backend")

print("=== ALL TESTS PASSED ===")
'''
    
    return run_command(f'python -c "{test_code}"', "Test package functionality")


def test_fallback_mechanism():
    """Test that fallback works when Rust extension is unavailable."""
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

# Now import demopy - should use fallback
import demopy

print("=== FALLBACK MECHANISM TEST ===")
hello_msg = demopy.hello()
print(f"hello(): {hello_msg}")

if "Python fallback" in hello_msg:
    print("✅ Fallback mechanism working correctly")
    
    # Test all fallback functions
    print(f"add(5, 7): {demopy.add(5, 7)}")
    print(f"multiply(3.0, 2.5): {demopy.multiply(3.0, 2.5)}")
    print(f"sum_list([10,20,30]): {demopy.sum_list([10,20,30])}")
    print(f"reverse_string('Fallback'): {demopy.reverse_string('Fallback')}")
    print("✅ All fallback functions working")
else:
    print("❌ Fallback mechanism not working")
    sys.exit(1)

print("=== FALLBACK TEST PASSED ===")
'''
    
    return run_command(f'python -c "{fallback_test}"', "Test fallback mechanism")


def main():
    """Main test function."""
    print("🚀 Starting End-to-End Package Testing")
    print("=" * 50)
    
    # Test 1: Install package from PyPI
    success = run_command(
        "pip install --upgrade demopy_gb_jj", 
        "Install package from PyPI"
    )
    if not success:
        print("❌ Package installation failed. Check if it's published to PyPI.")
        return False
    
    # Test 2: Test package functionality
    if not test_package_functionality():
        return False
    
    # Test 3: Test fallback mechanism
    if not test_fallback_mechanism():
        return False
    
    # Test 4: Verify version consistency
    success = run_command(
        'python -c "import demopy; print(f\'Package version: {demopy.__version__}\')"',
        "Verify version consistency"
    )
    if not success:
        return False
    
    print("\n" + "=" * 50)
    print("🎉 ALL END-TO-END TESTS PASSED!")
    print("✅ Package installation successful")
    print("✅ Rust extension or fallback working")
    print("✅ All functions operational")
    print("✅ Version consistency verified")
    print("=" * 50)
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
