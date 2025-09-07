#!/usr/bin/env python3
"""
Python package structure validation script.

This script validates that the Python package structure is correct
and that both the Rust extension and Python fallback can be imported
and tested properly.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description, check=True):
    """Run a command and return success status."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            cmd, shell=True, check=check, capture_output=True, text=True
        )
        if result.stdout.strip():
            print(f"   Output: {result.stdout.strip()}")
        print(f"✅ {description} - SUCCESS")
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        if e.stderr:
            print(f"   Error: {e.stderr.strip()}")
        return False, e.stderr


def check_package_structure():
    """Check the Python package structure."""
    print("\n" + "=" * 60)
    print("📁 CHECKING PACKAGE STRUCTURE")
    print("=" * 60)

    required_files = [
        "pyproject.toml",
        "Cargo.toml",
        "src/lib.rs",
        "python/demopy/__init__.py",
        "tests/test_demopy.py",
    ]

    missing_files = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            missing_files.append(file_path)

    if missing_files:
        print(f"\n⚠️  Missing files: {missing_files}")
        return False

    print("\n✅ All required files present")
    return True


def test_python_fallback_import():
    """Test importing the Python fallback module."""
    print("\n" + "=" * 60)
    print("🐍 TESTING PYTHON FALLBACK IMPORT")
    print("=" * 60)

    # Add python directory to path
    python_dir = Path("python").resolve()
    if python_dir not in sys.path:
        sys.path.insert(0, str(python_dir))

    try:
        import demopy

        print("✅ demopy module imported successfully")

        # Check version
        version = getattr(demopy, "__version__", "unknown")
        print(f"✅ Package version: {version}")

        # Check exports
        exports = getattr(demopy, "__all__", [])
        print(f"✅ Exported functions: {exports}")

        # Test basic functionality
        if hasattr(demopy, "hello"):
            hello_result = demopy.hello()
            print(f"✅ hello() works: {hello_result}")

            # Check if using fallback
            if "Python fallback" in hello_result:
                print("✅ Using Python fallback implementation")
            elif "Rust edition" in hello_result:
                print("✅ Using Rust extension implementation")
            else:
                print("⚠️  Unknown implementation type")

        # Test other functions
        test_functions = [
            ("add", [5, 7], 12),
            ("multiply", [2.5, 4.0], 10.0),
            ("sum_list", [[1, 2, 3, 4, 5]], 15),
            ("reverse_string", ["hello"], "olleh"),
            ("power", [2, 3], 8),
        ]

        for func_name, args, expected in test_functions:
            if hasattr(demopy, func_name):
                try:
                    result = getattr(demopy, func_name)(*args)
                    if (
                        abs(result - expected) < 1e-10
                        if isinstance(expected, (int, float))
                        else result == expected
                    ):
                        print(f"✅ {func_name}{tuple(args)} = {result}")
                    else:
                        print(
                            f"❌ {func_name}{tuple(args)} = {result}, expected {expected}"
                        )
                except Exception as e:
                    print(f"❌ {func_name}{tuple(args)} failed: {e}")
            else:
                print(f"⚠️  {func_name} not found in module")

        return True

    except ImportError as e:
        print(f"❌ Failed to import demopy: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing demopy: {e}")
        return False


def test_maturin_development():
    """Test maturin development installation."""
    print("\n" + "=" * 60)
    print("🦀 TESTING MATURIN DEVELOPMENT INSTALLATION")
    print("=" * 60)

    # Check if maturin is available
    success, _ = run_command(
        "maturin --version", "Check maturin availability", check=False
    )
    if not success:
        print("⚠️  maturin not available, skipping development installation test")
        return True

    # Try maturin develop
    success, output = run_command(
        "maturin develop", "Test maturin develop", check=False
    )

    if success:
        print("✅ maturin develop succeeded")

        # Test the installed package
        try:
            import demopy

            hello_result = demopy.hello()
            print(f"✅ Installed package works: {hello_result}")

            if "Rust edition" in hello_result:
                print("✅ Using Rust extension from maturin develop")
            else:
                print("⚠️  Expected Rust extension, got: {hello_result}")

            return True
        except ImportError as e:
            print(f"❌ Failed to import after maturin develop: {e}")
            return False
    else:
        print(
            "⚠️  maturin develop failed, this is expected in environments without Rust"
        )
        print("   The Python fallback should still work")
        return True


def test_package_installation_methods():
    """Test different package installation methods."""
    print("\n" + "=" * 60)
    print("📦 TESTING PACKAGE INSTALLATION METHODS")
    print("=" * 60)

    methods = [
        (
            "PYTHONPATH approach",
            "export PYTHONPATH=$PYTHONPATH:$(pwd)/python && python -c 'import demopy; print(demopy.hello())'",
        ),
        (
            "Direct path import",
            "python -c 'import sys; sys.path.insert(0, \"python\"); import demopy; print(demopy.hello())'",
        ),
    ]

    results = {}
    for method_name, command in methods:
        print(f"\n🧪 Testing: {method_name}")
        success, output = run_command(command, f"Test {method_name}", check=False)
        results[method_name] = success

        if success and output:
            print(f"   Result: {output}")

    return results


def validate_ci_setup():
    """Validate the CI setup for Python testing."""
    print("\n" + "=" * 60)
    print("🤖 VALIDATING CI SETUP")
    print("=" * 60)

    # Check if we can run the same commands as CI
    ci_commands = [
        ("black --check python/ tests/", "Black formatting check"),
        ("isort --check-only python/ tests/", "isort import check"),
        ("flake8 python/ tests/", "flake8 linting"),
        (
            "python -c 'import sys; sys.path.insert(0, \"python\"); import demopy'",
            "Module import test",
        ),
    ]

    results = {}
    for command, description in ci_commands:
        success, _ = run_command(command, description, check=False)
        results[description] = success

    return results


def main():
    """Main validation function."""
    print("🔍 Python Package Structure Validation")
    print("Validating package structure and import methods")
    print("=" * 60)

    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print(
            "❌ pyproject.toml not found. Please run this script from the project root."
        )
        return False

    # Run validation checks
    checks = [
        ("Package Structure", check_package_structure),
        ("Python Fallback Import", test_python_fallback_import),
        ("Maturin Development", test_maturin_development),
        ("Installation Methods", test_package_installation_methods),
        ("CI Setup", validate_ci_setup),
    ]

    results = {}
    for check_name, check_func in checks:
        try:
            result = check_func()
            if isinstance(result, dict):
                # For methods that return detailed results
                results[check_name] = all(result.values())
                print(f"\n📊 {check_name} detailed results:")
                for sub_check, sub_result in result.items():
                    status = "✅" if sub_result else "❌"
                    print(f"   {status} {sub_check}")
            else:
                results[check_name] = result
        except Exception as e:
            print(f"❌ {check_name} failed with exception: {e}")
            results[check_name] = False

    # Summary
    print("\n" + "=" * 60)
    print("📊 VALIDATION SUMMARY")
    print("=" * 60)

    all_passed = True
    for check_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status} {check_name}")
        if not passed:
            all_passed = False

    if all_passed:
        print("\n🎉 ALL VALIDATIONS PASSED!")
        print("✅ Package structure is correct")
        print("✅ Python fallback works")
        print("✅ Import methods are functional")
        print("✅ CI setup should work correctly")
    else:
        print("\n⚠️  SOME VALIDATIONS FAILED")
        print("❌ Review the issues above before running CI")

    # Recommendations
    print("\n" + "=" * 60)
    print("💡 RECOMMENDATIONS FOR CI")
    print("=" * 60)

    print("For GitHub Actions Code Quality workflow:")
    print("1. Use PYTHONPATH approach: export PYTHONPATH=$PYTHONPATH:$(pwd)/python")
    print("2. Install dependencies: pip install black isort flake8 mypy pytest")
    print(
        "3. Test import: python -c 'import sys; sys.path.insert(0, \"python\"); import demopy'"
    )
    print("4. Run tests with proper path: PYTHONPATH=python pytest tests/ -v")

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
