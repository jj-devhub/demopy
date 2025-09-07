#!/usr/bin/env python3
"""
Pre-commit hooks setup script for demopy_gb_jj.

This script installs and configures pre-commit hooks for automatic code quality
enforcement in the demopy_gb_jj Rust-Python extension project.
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


def check_prerequisites():
    """Check if required tools are available."""
    print("\n" + "=" * 60)
    print("🔍 CHECKING PREREQUISITES")
    print("=" * 60)

    prerequisites = [
        ("python --version", "Python installation"),
        ("pip --version", "pip package manager"),
        ("git --version", "Git version control"),
    ]

    all_good = True
    for cmd, description in prerequisites:
        success, _ = run_command(cmd, f"Check {description}", check=False)
        if not success:
            all_good = False

    return all_good


def install_pre_commit():
    """Install pre-commit package."""
    print("\n" + "=" * 60)
    print("📦 INSTALLING PRE-COMMIT")
    print("=" * 60)

    # Check if pre-commit is already installed
    success, _ = run_command(
        "pre-commit --version", "Check pre-commit installation", check=False
    )
    if success:
        print("✅ pre-commit is already installed")
        return True

    # Install pre-commit
    success, _ = run_command(
        "pip install pre-commit", "Install pre-commit package", check=False
    )
    if not success:
        print("❌ Failed to install pre-commit")
        return False

    # Verify installation
    success, _ = run_command(
        "pre-commit --version", "Verify pre-commit installation", check=False
    )
    return success


def install_hooks():
    """Install pre-commit hooks."""
    print("\n" + "=" * 60)
    print("🪝 INSTALLING PRE-COMMIT HOOKS")
    print("=" * 60)

    # Install hooks
    success, _ = run_command(
        "pre-commit install", "Install pre-commit hooks", check=False
    )
    if not success:
        return False

    # Install commit message hooks (optional)
    success, _ = run_command(
        "pre-commit install --hook-type commit-msg",
        "Install commit message hooks",
        check=False,
    )
    # Don't fail if this doesn't work, it's optional

    return True


def update_hooks():
    """Update pre-commit hooks to latest versions."""
    print("\n" + "=" * 60)
    print("🔄 UPDATING HOOK VERSIONS")
    print("=" * 60)

    success, _ = run_command(
        "pre-commit autoupdate", "Update hook versions", check=False
    )
    return success


def test_hooks():
    """Test pre-commit hooks on all files."""
    print("\n" + "=" * 60)
    print("🧪 TESTING PRE-COMMIT HOOKS")
    print("=" * 60)

    print("Running pre-commit on all files (this may take a while)...")
    success, output = run_command(
        "pre-commit run --all-files", "Test all hooks", check=False
    )

    if success:
        print("✅ All hooks passed!")
    else:
        print("⚠️  Some hooks failed or made changes.")
        print(
            "This is normal for the first run - hooks may auto-fix formatting issues."
        )
        print("\nHook output:")
        print(output)

        # Run again to see if issues are resolved
        print("\nRunning hooks again to verify fixes...")
        success2, _ = run_command(
            "pre-commit run --all-files", "Re-test all hooks", check=False
        )
        if success2:
            print("✅ All hooks now pass after auto-fixes!")
        else:
            print("⚠️  Some issues still remain. Please review the output above.")

    return success


def show_usage_info():
    """Show information about using pre-commit hooks."""
    print("\n" + "=" * 60)
    print("📋 PRE-COMMIT HOOKS USAGE")
    print("=" * 60)

    print(
        """
🎯 How Pre-commit Hooks Work:
   • Hooks run automatically before each git commit
   • They check and auto-fix code quality issues
   • Commits are blocked if critical issues are found
   • Auto-fixable issues (formatting) are corrected automatically

🛠️  Available Hooks:
   • Black: Auto-formats Python code (88 char line length)
   • isort: Sorts and organizes Python imports
   • flake8: Lints Python code for PEP 8 compliance
   • mypy: Static type checking (optional)
   • cargo fmt: Formats Rust code
   • cargo clippy: Lints Rust code
   • General: Trailing whitespace, YAML/TOML validation, etc.

📁 Target Directories:
   • python/ - Python fallback implementation
   • tests/ - Test files
   • scripts/ - Utility scripts
   • src/ - Rust source code (for Rust hooks)

🚀 Common Commands:
   • git commit -m "message"  # Runs hooks automatically
   • pre-commit run --all-files  # Run hooks on all files
   • pre-commit run <hook-id>  # Run specific hook
   • pre-commit skip  # Skip hooks for one commit (not recommended)

⚙️  Configuration Files:
   • .pre-commit-config.yaml - Hook configuration
   • pyproject.toml - Tool-specific settings (black, isort, flake8, mypy)

💡 Tips:
   • Let hooks auto-fix formatting issues, then commit again
   • Review any remaining issues flagged by linters
   • Use 'git add' after auto-fixes to stage the changes
   • Check CI pipeline - it runs the same quality checks
"""
    )


def main():
    """Main setup function."""
    print("🛠️  Pre-commit Hooks Setup for demopy_gb_jj")
    print("Setting up automatic code quality enforcement")
    print("=" * 60)

    # Check if we're in the right directory
    if not Path(".pre-commit-config.yaml").exists():
        print("❌ .pre-commit-config.yaml not found.")
        print("   Please run this script from the project root directory.")
        return False

    # Run setup steps
    steps = [
        ("Prerequisites Check", check_prerequisites),
        ("Install pre-commit", install_pre_commit),
        ("Install hooks", install_hooks),
        ("Update hooks", update_hooks),
        ("Test hooks", test_hooks),
    ]

    results = {}
    for step_name, step_func in steps:
        try:
            results[step_name] = step_func()
        except Exception as e:
            print(f"❌ {step_name} failed with exception: {e}")
            results[step_name] = False

    # Show usage information
    show_usage_info()

    # Summary
    print("\n" + "=" * 60)
    print("📊 SETUP SUMMARY")
    print("=" * 60)

    all_passed = True
    for step_name, passed in results.items():
        status = "✅ SUCCESS" if passed else "❌ FAILED"
        print(f"{status} {step_name}")
        if not passed:
            all_passed = False

    if all_passed:
        print("\n🎉 PRE-COMMIT HOOKS SETUP COMPLETE!")
        print("✅ Hooks are installed and ready to use")
        print("✅ Code quality will be enforced automatically")
        print("✅ Next commit will trigger the hooks")
    else:
        print("\n⚠️  SETUP INCOMPLETE")
        print("❌ Some steps failed - please review the errors above")
        print(
            "💡 You may need to install missing dependencies or fix configuration issues"
        )

    print("\n🚀 Next Steps:")
    print("   1. Make some changes to Python files")
    print("   2. Run 'git add .' to stage changes")
    print("   3. Run 'git commit -m \"test: verify pre-commit hooks\"'")
    print("   4. Watch the hooks automatically check and fix your code!")

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
