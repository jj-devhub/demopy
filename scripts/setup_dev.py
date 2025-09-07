#!/usr/bin/env python3
"""
Development setup script for demopy_gb_jj

This script sets up the development environment by:
1. Checking for required tools (Python, Rust, etc.)
2. Installing Python dependencies
3. Building the Rust extension
4. Running tests to verify everything works

Usage:
    python scripts/setup_dev.py
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd, description, check=True):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            cmd, shell=True, check=check, capture_output=True, text=True
        )
        if result.stdout:
            print(f"   {result.stdout.strip()}")
        if result.stderr and not check:
            print(f"   Warning: {result.stderr.strip()}")
        print(f"✅ {description} completed")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Command: {cmd}")
        print(f"   Error: {e.stderr.strip() if e.stderr else str(e)}")
        return None


def check_tool(cmd, name, install_hint):
    """Check if a tool is available."""
    print(f"🔍 Checking for {name}...")
    result = run_command(f"{cmd} --version", f"Check {name}", check=False)
    if result and result.returncode == 0:
        print(f"✅ {name} is available")
        return True
    else:
        print(f"❌ {name} is not available")
        print(f"   Install hint: {install_hint}")
        return False


def main():
    """Main setup function."""
    print("🚀 Setting up demopy_gb_jj development environment\n")

    # Change to project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    print(f"📁 Working directory: {project_root.absolute()}\n")

    # Check required tools
    tools_ok = True

    if not check_tool("python", "Python", "Install from https://python.org"):
        tools_ok = False

    if not check_tool("cargo", "Rust/Cargo", "Install from https://rustup.rs"):
        tools_ok = False

    if not check_tool("git", "Git", "Install from https://git-scm.com"):
        tools_ok = False

    if not tools_ok:
        print(
            "\n❌ Some required tools are missing. Please install them and try again."
        )
        sys.exit(1)

    print("\n" + "=" * 50)
    print("📦 Installing Python dependencies")
    print("=" * 50)

    # Install Python dependencies
    if not run_command("pip install --upgrade pip", "Upgrade pip"):
        sys.exit(1)

    if not run_command("pip install maturin pytest", "Install Python dependencies"):
        sys.exit(1)

    print("\n" + "=" * 50)
    print("🦀 Building Rust extension")
    print("=" * 50)

    # Build Rust extension
    if not run_command("maturin develop", "Build Rust extension"):
        print("\n❌ Failed to build Rust extension. This might be due to:")
        print("   - Missing Rust toolchain")
        print("   - Missing system dependencies")
        print("   - Compilation errors")
        sys.exit(1)

    print("\n" + "=" * 50)
    print("🧪 Running tests")
    print("=" * 50)

    # Run Rust tests
    if not run_command("cargo test", "Run Rust tests"):
        print("⚠️  Rust tests failed, but continuing...")

    # Run Python tests
    if not run_command("pytest tests/ -v", "Run Python tests"):
        print("⚠️  Python tests failed, but continuing...")

    print("\n" + "=" * 50)
    print("🎉 Development environment setup complete!")
    print("=" * 50)

    print("\nNext steps:")
    print(
        "1. Try importing the package: python -c 'import demopy; print(demopy.hello())'"
    )
    print("2. Run tests: pytest tests/ -v")
    print("3. Run Rust tests: cargo test")
    print("4. Format code: cargo fmt")
    print("5. Check linting: cargo clippy")
    print("\nHappy coding! 🚀")


if __name__ == "__main__":
    main()
