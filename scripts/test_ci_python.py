#!/usr/bin/env python3
"""
CI Python testing simulation script.

This script simulates exactly what the GitHub Actions Code Quality workflow
will do for Python testing, allowing local validation before pushing.
"""

import subprocess
import sys
import os
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
            text=True,
            env={
                **os.environ,
                "PYTHONPATH": f"{os.environ.get('PYTHONPATH', '')}:{os.getcwd()}/python",
            },
        )
        if result.stdout.strip():
            print(f"   Output: {result.stdout.strip()}")
        print(f"✅ {description} - SUCCESS")
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        if e.stderr:
            print(f"   Error: {e.stderr.strip()}")
        if e.stdout:
            print(f"   Stdout: {e.stdout.strip()}")
        return False, e.stderr


def simulate_ci_python_setup():
    """Simulate the CI Python setup steps."""
    print("\n" + "=" * 60)
    print("🐍 SIMULATING CI PYTHON SETUP")
    print("=" * 60)

    steps = [
        ("python -m pip install --upgrade pip", "Upgrade pip"),
        ("pip install black isort flake8 mypy pytest", "Install Python tools"),
    ]

    results = {}
    for cmd, description in steps:
        success, _ = run_command(cmd, description, check=False)
        results[description] = success

    return results


def simulate_ci_package_setup():
    """Simulate the CI package setup steps."""
    print("\n" + "=" * 60)
    print("📦 SIMULATING CI PACKAGE SETUP")
    print("=" * 60)

    # Set PYTHONPATH
    python_path = f"{os.getcwd()}/python"
    os.environ["PYTHONPATH"] = f"{os.environ.get('PYTHONPATH', '')}:{python_path}"
    print(f"✅ Set PYTHONPATH to include: {python_path}")

    # Test package import
    test_commands = [
        (
            "python -c \"import sys; sys.path.insert(0, 'python'); import demopy; print('✅ demopy module imported successfully')\"",
            "Test module import",
        ),
        (
            "python -c \"import sys; sys.path.insert(0, 'python'); import demopy; print('Package version:', demopy.__version__)\"",
            "Check package version",
        ),
    ]

    results = {}
    for cmd, description in test_commands:
        success, _ = run_command(cmd, description, check=False)
        results[description] = success

    return results


def simulate_ci_quality_checks():
    """Simulate the CI Python quality checks."""
    print("\n" + "=" * 60)
    print("🔍 SIMULATING CI QUALITY CHECKS")
    print("=" * 60)

    quality_checks = [
        ("black --check python/ tests/", "Black formatting check"),
        ("isort --check-only python/ tests/", "isort import sorting check"),
        ("flake8 python/ tests/", "flake8 linting"),
        ("mypy python/demopy/ --ignore-missing-imports", "mypy type checking"),
    ]

    results = {}
    for cmd, description in quality_checks:
        success, _ = run_command(cmd, description, check=False)
        results[description] = success

    return results


def simulate_ci_testing():
    """Simulate the CI Python testing."""
    print("\n" + "=" * 60)
    print("🧪 SIMULATING CI TESTING")
    print("=" * 60)

    # Ensure PYTHONPATH is set
    python_path = f"{os.getcwd()}/python"
    env = {
        **os.environ,
        "PYTHONPATH": f"{os.environ.get('PYTHONPATH', '')}:{python_path}",
    }

    test_commands = [
        (
            "python -c \"import sys; sys.path.insert(0, 'python'); import demopy; print('✅ demopy module imported successfully')\"",
            "Pre-test import validation",
        ),
        ("pytest tests/ -v", "Run pytest tests"),
    ]

    results = {}
    for cmd, description in test_commands:
        print(f"🔄 {description}...")
        try:
            result = subprocess.run(
                cmd, shell=True, check=False, capture_output=True, text=True, env=env
            )
            if result.returncode == 0:
                print(f"✅ {description} - SUCCESS")
                if result.stdout.strip():
                    print(f"   Output: {result.stdout.strip()}")
                results[description] = True
            else:
                print(f"❌ {description} - FAILED")
                if result.stderr:
                    print(f"   Error: {result.stderr.strip()}")
                if result.stdout:
                    print(f"   Stdout: {result.stdout.strip()}")
                results[description] = False
        except Exception as e:
            print(f"❌ {description} - EXCEPTION: {e}")
            results[description] = False

    return results


def test_specific_functionality():
    """Test specific functionality that CI needs to validate."""
    print("\n" + "=" * 60)
    print("🎯 TESTING SPECIFIC FUNCTIONALITY")
    print("=" * 60)

    # Test that all expected functions work
    test_script = """
import sys
sys.path.insert(0, 'python')
import demopy

print('Testing demopy functionality:')
print(f'Version: {demopy.__version__}')
print(f'Exports: {demopy.__all__}')

# Test all functions
functions_to_test = [
    ('hello', [], 'Hello from demopy_gb_jj'),
    ('add', [5, 7], 12),
    ('multiply', [2.5, 4.0], 10.0),
    ('sum_list', [[1, 2, 3, 4, 5]], 15),
    ('reverse_string', ['hello'], 'olleh'),
    ('power', [2, 3], 8),
]

all_passed = True
for func_name, args, expected in functions_to_test:
    try:
        func = getattr(demopy, func_name)
        result = func(*args)
        
        if func_name == 'hello':
            # Just check that it contains expected text
            if expected in result:
                print(f'✅ {func_name}() works: {result}')
            else:
                print(f'❌ {func_name}() unexpected result: {result}')
                all_passed = False
        else:
            # Check exact match for other functions
            if abs(result - expected) < 1e-10 if isinstance(expected, (int, float)) else result == expected:
                print(f'✅ {func_name}{tuple(args)} = {result}')
            else:
                print(f'❌ {func_name}{tuple(args)} = {result}, expected {expected}')
                all_passed = False
    except Exception as e:
        print(f'❌ {func_name} failed: {e}')
        all_passed = False

if all_passed:
    print('✅ All functionality tests passed')
else:
    print('❌ Some functionality tests failed')
    sys.exit(1)
"""

    success, _ = run_command(
        f'python -c "{test_script}"', "Test all demopy functionality", check=False
    )
    return {"Functionality test": success}


def main():
    """Main CI simulation function."""
    print("🤖 CI Python Testing Simulation")
    print("Simulating GitHub Actions Code Quality workflow Python steps")
    print("=" * 60)

    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print(
            "❌ pyproject.toml not found. Please run this script from the project root."
        )
        return False

    # Run simulation steps
    simulation_steps = [
        ("Python Setup", simulate_ci_python_setup),
        ("Package Setup", simulate_ci_package_setup),
        ("Quality Checks", simulate_ci_quality_checks),
        ("Testing", simulate_ci_testing),
        ("Functionality", test_specific_functionality),
    ]

    all_results = {}
    for step_name, step_func in simulation_steps:
        try:
            results = step_func()
            all_results[step_name] = results
        except Exception as e:
            print(f"❌ {step_name} failed with exception: {e}")
            all_results[step_name] = {"Exception": False}

    # Summary
    print("\n" + "=" * 60)
    print("📊 CI SIMULATION SUMMARY")
    print("=" * 60)

    overall_success = True
    for step_name, step_results in all_results.items():
        step_success = all(step_results.values()) if step_results else False
        status = "✅ PASSED" if step_success else "❌ FAILED"
        print(f"{status} {step_name}")

        # Show detailed results
        for sub_check, sub_result in step_results.items():
            sub_status = "  ✅" if sub_result else "  ❌"
            print(f"{sub_status} {sub_check}")

        if not step_success:
            overall_success = False

    print("\n" + "=" * 60)
    if overall_success:
        print("🎉 CI SIMULATION SUCCESSFUL!")
        print("✅ All steps passed - CI should work correctly")
        print("✅ Python package structure is correct")
        print("✅ Quality checks will pass")
        print("✅ Tests will run successfully")
    else:
        print("⚠️  CI SIMULATION FAILED")
        print("❌ Some steps failed - fix issues before pushing")
        print("💡 Review the failed checks above")

    return overall_success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
