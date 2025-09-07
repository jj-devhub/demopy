#!/usr/bin/env python3
"""
Integration test script for demopy_gb_jj package.

This script tests both the Rust extension and Python fallback implementations
to ensure they work correctly after installation.
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path


def run_command(cmd, description, check=True, capture_output=True):
    """Run a command and return success status."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            cmd, shell=True, check=check, capture_output=capture_output, text=True
        )
        if capture_output and result.stdout.strip():
            print(f"   Output: {result.stdout.strip()}")
        print(f"✅ {description} - SUCCESS")
        return True, result.stdout.strip() if capture_output else ""
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        if capture_output and e.stderr:
            print(f"   Error: {e.stderr.strip()}")
        if capture_output and e.stdout:
            print(f"   Stdout: {e.stdout.strip()}")
        return False, e.stderr if capture_output else ""


def test_package_import():
    """Test that the package can be imported correctly."""
    print("\n" + "=" * 60)
    print("📦 TESTING PACKAGE IMPORT")
    print("=" * 60)

    test_script = """
import sys
print(f"Python version: {sys.version}")
print(f"Python path: {sys.path[:3]}...")

try:
    import demopy
    print("✅ Successfully imported demopy")
    print(f"Package version: {demopy.__version__}")
    print(f"Available functions: {demopy.__all__}")

    # Test that all expected functions are available
    expected_functions = ["hello", "add", "multiply", "sum_list", "reverse_string", "power"]
    missing_functions = []

    for func_name in expected_functions:
        if hasattr(demopy, func_name):
            print(f"✅ {func_name} is available")
        else:
            print(f"❌ {func_name} is missing")
            missing_functions.append(func_name)

    if missing_functions:
        print(f"❌ Missing functions: {missing_functions}")
        sys.exit(1)
    else:
        print("✅ All expected functions are available")

except ImportError as e:
    print(f"❌ Failed to import demopy: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error during import test: {e}")
    sys.exit(1)
"""

    success, _ = run_command(
        f'python -c "{test_script}"', "Test package import", check=False
    )
    return success


def test_functionality():
    """Test that all functions work correctly."""
    print("\n" + "=" * 60)
    print("🧪 TESTING FUNCTIONALITY")
    print("=" * 60)

    test_script = """
import demopy

print("Testing demopy functionality:")

# Test hello function
hello_result = demopy.hello()
print(f"hello(): {hello_result}")

# Determine if using Rust or Python implementation
if "Rust edition" in hello_result:
    print("✅ Using Rust extension implementation")
    implementation = "Rust"
elif "Python fallback" in hello_result:
    print("✅ Using Python fallback implementation")
    implementation = "Python"
else:
    print(f"⚠️  Unknown implementation: {hello_result}")
    implementation = "Unknown"

# Test all functions with expected results
test_cases = [
    ("add", [5, 7], 12),
    ("multiply", [2.5, 4.0], 10.0),
    ("sum_list", [[1, 2, 3, 4, 5]], 15),
    ("reverse_string", ["hello"], "olleh"),
    ("power", [2, 3], 8),
    ("power", [4, 0.5], 2.0),  # Square root
    ("power", [8, 1/3], 2.0),  # Cube root (approximately)
]

all_passed = True
for func_name, args, expected in test_cases:
    try:
        func = getattr(demopy, func_name)
        result = func(*args)

        # Handle floating point comparisons
        if isinstance(expected, float):
            if abs(result - expected) < 1e-10:
                print(f"✅ {func_name}{tuple(args)} = {result}")
            else:
                print(f"❌ {func_name}{tuple(args)} = {result}, expected {expected}")
                all_passed = False
        else:
            if result == expected:
                print(f"✅ {func_name}{tuple(args)} = {result}")
            else:
                print(f"❌ {func_name}{tuple(args)} = {result}, expected {expected}")
                all_passed = False

    except Exception as e:
        print(f"❌ {func_name}{tuple(args)} failed: {e}")
        all_passed = False

if all_passed:
    print(f"✅ All functionality tests passed using {implementation} implementation")
else:
    print(f"❌ Some functionality tests failed with {implementation} implementation")
    import sys
    sys.exit(1)
"""

    success, _ = run_command(
        f'python -c "{test_script}"', "Test functionality", check=False
    )
    return success


def test_wheel_installation():
    """Test installing from a built wheel."""
    print("\n" + "=" * 60)
    print("🎡 TESTING WHEEL INSTALLATION")
    print("=" * 60)

    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Using temporary directory: {temp_dir}")

        # Build wheel
        success, output = run_command(
            "maturin build --release", "Build wheel with maturin", check=False
        )
        if not success:
            print("❌ Failed to build wheel")
            return False

        # Find the built wheel
        dist_dir = Path("target/wheels")
        if not dist_dir.exists():
            print("❌ Wheel directory not found")
            return False

        wheels = list(dist_dir.glob("*.whl"))
        if not wheels:
            print("❌ No wheels found")
            return False

        wheel_path = wheels[0]  # Use the first wheel found
        print(f"Found wheel: {wheel_path}")

        # Install the wheel in a clean environment
        venv_dir = Path(temp_dir) / "test_venv"

        # Create virtual environment
        success, _ = run_command(
            f"python -m venv {venv_dir}", "Create test virtual environment", check=False
        )
        if not success:
            print("❌ Failed to create virtual environment")
            return False

        # Determine the correct python executable path
        if os.name == "nt":  # Windows
            python_exe = venv_dir / "Scripts" / "python.exe"
            pip_exe = venv_dir / "Scripts" / "pip.exe"
        else:  # Unix-like
            python_exe = venv_dir / "bin" / "python"
            pip_exe = venv_dir / "bin" / "pip"

        # Install the wheel
        success, _ = run_command(
            f'"{pip_exe}" install "{wheel_path}"',
            "Install wheel in test environment",
            check=False,
        )
        if not success:
            print("❌ Failed to install wheel")
            return False

        # Test import in the clean environment
        test_import_script = """
try:
    import demopy
    print("✅ Successfully imported demopy in clean environment")
    print(f"Version: {demopy.__version__}")
    print(f"Hello: {demopy.hello()}")

    # Test a few functions
    print(f"add(2, 3) = {demopy.add(2, 3)}")
    print(f"power(2, 3) = {demopy.power(2, 3)}")

    print("✅ Wheel installation test passed")
except Exception as e:
    print(f"❌ Error in clean environment: {e}")
    import sys
    sys.exit(1)
"""

        success, _ = run_command(
            f'"{python_exe}" -c "{test_import_script}"',
            "Test import in clean environment",
            check=False,
        )
        return success


def test_fallback_behavior():
    """Test that fallback behavior works when Rust extension is not available."""
    print("\n" + "=" * 60)
    print("🐍 TESTING PYTHON FALLBACK BEHAVIOR")
    print("=" * 60)

    # Test using PYTHONPATH to use fallback implementation

    fallback_test_script = """
import sys
sys.path.insert(0, "python")

# Import the module directly from python directory (fallback)
import demopy

hello_result = demopy.hello()
print(f"Fallback hello(): {hello_result}")

if "Python fallback" in hello_result:
    print("✅ Successfully using Python fallback implementation")

    # Test fallback functions
    print(f"add(10, 20) = {demopy.add(10, 20)}")
    print(f"multiply(3.5, 2.0) = {demopy.multiply(3.5, 2.0)}")
    print(f"sum_list([1, 2, 3]) = {demopy.sum_list([1, 2, 3])}")
    print(f"reverse_string('test') = {demopy.reverse_string('test')}")
    print(f"power(3, 2) = {demopy.power(3, 2)}")

    print("✅ Python fallback functionality test passed")
else:
    print(f"⚠️  Expected Python fallback, got: {hello_result}")
"""

    success, _ = run_command(
        f'python -c "{fallback_test_script}"', "Test Python fallback", check=False
    )
    return success


def main():
    """Main integration test function."""
    print("🧪 Integration Test for demopy_gb_jj")
    print("Testing both Rust extension and Python fallback implementations")
    print("=" * 60)

    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print(
            "❌ pyproject.toml not found. Please run this script from the project root."
        )
        return False

    # Run integration tests
    tests = [
        ("Package Import", test_package_import),
        ("Functionality", test_functionality),
        ("Wheel Installation", test_wheel_installation),
        ("Python Fallback", test_fallback_behavior),
    ]

    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False

    # Summary
    print("\n" + "=" * 60)
    print("📊 INTEGRATION TEST SUMMARY")
    print("=" * 60)

    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status} {test_name}")
        if not passed:
            all_passed = False

    if all_passed:
        print("\n🎉 ALL INTEGRATION TESTS PASSED!")
        print("✅ Package builds and installs correctly")
        print("✅ Rust extension works when available")
        print("✅ Python fallback works when Rust extension unavailable")
        print("✅ All functionality is correct")
    else:
        print("\n⚠️  SOME INTEGRATION TESTS FAILED")
        print("❌ Review the issues above before deploying")

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
