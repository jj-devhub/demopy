#!/usr/bin/env python3
"""
Development environment setup script for demopy_gb_jj.

This script sets up all the necessary tools for development including:
- Pre-commit hooks
- Rust formatting and linting tools
- Python formatting and linting tools
- Development dependencies
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
            print(f"   {result.stdout.strip()}")
        print(f"✅ {description} - SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        if e.stderr:
            print(f"   Error: {e.stderr.strip()}")
        return False


def check_rust_installed():
    """Check if Rust is installed."""
    try:
        result = subprocess.run(["rustc", "--version"], capture_output=True, text=True)
        print(f"✅ Rust installed: {result.stdout.strip()}")
        return True
    except FileNotFoundError:
        print("❌ Rust not found. Please install Rust from https://rustup.rs/")
        return False


def setup_rust_tools():
    """Set up Rust formatting and linting tools."""
    print("\n" + "=" * 50)
    print("🦀 SETTING UP RUST TOOLS")
    print("=" * 50)

    if not check_rust_installed():
        return False

    # Install rustfmt and clippy
    success = True
    success &= run_command("rustup component add rustfmt", "Install rustfmt")
    success &= run_command("rustup component add clippy", "Install clippy")

    # Install additional Rust tools using our installation script
    success &= run_command(
        "python scripts/install_rust_tools.py --mode dev",
        "Install Rust development tools",
        check=False,
    )

    return success


def setup_python_tools():
    """Set up Python formatting and linting tools."""
    print("\n" + "=" * 50)
    print("🐍 SETTING UP PYTHON TOOLS")
    print("=" * 50)

    # Install Python development tools
    tools = [
        "black",  # Code formatter
        "isort",  # Import sorter
        "flake8",  # Linter
        "mypy",  # Type checker
        "pytest",  # Testing framework
        "pre-commit",  # Pre-commit hooks
        "maturin",  # Rust-Python integration
        "safety",  # Security scanner
        "bandit",  # Security linter
    ]

    success = True
    for tool in tools:
        success &= run_command(f"pip install {tool}", f"Install {tool}")

    return success


def setup_precommit_hooks():
    """Set up pre-commit hooks."""
    print("\n" + "=" * 50)
    print("🪝 SETTING UP PRE-COMMIT HOOKS")
    print("=" * 50)

    success = True
    success &= run_command("pre-commit install", "Install pre-commit hooks")
    success &= run_command(
        "pre-commit install --hook-type commit-msg", "Install commit-msg hooks"
    )

    # Run pre-commit on all files to set up the environment
    print("🔄 Running pre-commit on all files (this may take a while)...")
    run_command(
        "pre-commit run --all-files", "Run pre-commit on all files", check=False
    )

    return success


def setup_git_hooks():
    """Set up additional git hooks."""
    print("\n" + "=" * 50)
    print("📝 SETTING UP GIT HOOKS")
    print("=" * 50)

    # Create a commit message template
    commit_template = """# <type>: <description>
#
# Types:
#   feat:     New feature (minor version bump)
#   fix:      Bug fix (patch version bump)
#   docs:     Documentation changes
#   style:    Code style changes (formatting, etc.)
#   refactor: Code refactoring
#   perf:     Performance improvements
#   test:     Adding or updating tests
#   chore:    Maintenance tasks
#   BREAKING CHANGE: Major version bump
#
# Examples:
#   feat: add power function for exponentiation calculations
#   fix: resolve memory leak in multiply function
#   docs: update README with new examples
#   BREAKING CHANGE: redesign API for better type safety
#
# Use [skip ci] to skip CI/CD pipeline
"""

    try:
        with open(".gitmessage", "w") as f:
            f.write(commit_template)

        run_command(
            "git config commit.template .gitmessage", "Set commit message template"
        )
        print("✅ Git commit template created")
        return True
    except Exception as e:
        print(f"❌ Failed to create git commit template: {e}")
        return False


def run_initial_checks():
    """Run initial code quality checks."""
    print("\n" + "=" * 50)
    print("🔍 RUNNING INITIAL QUALITY CHECKS")
    print("=" * 50)

    # First validate Python package structure
    success = run_command(
        "python scripts/test_python_structure.py",
        "Validate Python package structure",
        check=False,
    )
    if not success:
        print("⚠️  Python package structure validation failed, but continuing...")

    checks = [
        ("cargo fmt --all -- --check", "Check Rust formatting"),
        (
            "cargo clippy --all-targets --all-features -- -D warnings",
            "Run Rust linting",
        ),
        ("cargo test", "Run Rust tests"),
        ("black --check python/ tests/", "Check Python formatting"),
        ("isort --check-only python/ tests/", "Check Python import sorting"),
        ("flake8 python/ tests/", "Run Python linting"),
        (
            "PYTHONPATH=python python -c 'import demopy; print(\"Python fallback works:\", demopy.hello())'",
            "Test Python fallback import",
        ),
    ]

    results = []
    for cmd, description in checks:
        success = run_command(cmd, description, check=False)
        results.append((description, success))

    print("\n" + "=" * 50)
    print("📊 QUALITY CHECK RESULTS")
    print("=" * 50)

    all_passed = True
    for description, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status} {description}")
        if not success:
            all_passed = False

    if all_passed:
        print("\n🎉 All quality checks passed!")
    else:
        print(
            "\n⚠️  Some quality checks failed. Run the individual commands to see details."
        )

    return all_passed


def main():
    """Main setup function."""
    print("🚀 Development Environment Setup for demopy_gb_jj")
    print("=" * 60)

    # Check if we're in the right directory
    if not Path("Cargo.toml").exists() or not Path("pyproject.toml").exists():
        print("❌ Please run this script from the project root directory.")
        return False

    # Run setup steps
    steps = [
        ("Rust Tools", setup_rust_tools),
        ("Python Tools", setup_python_tools),
        ("Pre-commit Hooks", setup_precommit_hooks),
        ("Git Hooks", setup_git_hooks),
        ("Initial Quality Checks", run_initial_checks),
    ]

    results = {}
    for step_name, step_func in steps:
        try:
            results[step_name] = step_func()
        except Exception as e:
            print(f"❌ {step_name} failed with exception: {e}")
            results[step_name] = False

    # Summary
    print("\n" + "=" * 60)
    print("📊 SETUP SUMMARY")
    print("=" * 60)

    all_passed = True
    for step_name, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{status} {step_name}")
        if not success:
            all_passed = False

    if all_passed:
        print("\n🎉 DEVELOPMENT ENVIRONMENT SETUP COMPLETE!")
        print("✅ All tools installed and configured")
        print("✅ Pre-commit hooks active")
        print("✅ Code quality checks passing")
        print("\n📝 Next steps:")
        print("  1. Make changes to your code")
        print("  2. Commit with semantic messages (feat:, fix:, etc.)")
        print("  3. Pre-commit hooks will automatically format and check your code")
        print("  4. Push to trigger the automated CI/CD pipeline")
    else:
        print("\n⚠️  SETUP INCOMPLETE")
        print("❌ Some steps failed. Please review the errors above.")
        print("💡 You may need to install missing dependencies manually.")

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
