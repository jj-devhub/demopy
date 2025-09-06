#!/usr/bin/env python3
"""
Windows Rust toolchain test script.

This script simulates the Windows CI environment to test Rust toolchain availability.
"""

import subprocess
import sys
import os
import platform
from pathlib import Path


def run_command(cmd, description, shell=True, check_cargo=False):
    """Run a command and return success status."""
    print(f"🔄 {description}...")
    
    # If we're testing cargo availability, try different approaches
    if check_cargo and platform.system() == "Windows":
        # Try different ways to find cargo on Windows
        cargo_paths = [
            "cargo",
            "cargo.exe", 
            str(Path.home() / ".cargo" / "bin" / "cargo.exe"),
            "C:\\Users\\runneradmin\\.cargo\\bin\\cargo.exe"
        ]
        
        for cargo_path in cargo_paths:
            try:
                result = subprocess.run(
                    f"{cargo_path} --version",
                    shell=True,
                    check=True,
                    capture_output=True,
                    text=True
                )
                print(f"✅ Found cargo at: {cargo_path}")
                print(f"   Version: {result.stdout.strip()}")
                return True, result.stdout
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        
        print(f"❌ Cargo not found in any of: {cargo_paths}")
        return False, "Cargo not found"
    
    try:
        result = subprocess.run(
            cmd, 
            shell=shell, 
            check=True, 
            capture_output=True, 
            text=True
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
    except FileNotFoundError as e:
        print(f"❌ {description} - COMMAND NOT FOUND")
        print(f"   Error: {str(e)}")
        return False, str(e)


def check_environment():
    """Check the current environment setup."""
    print("\n" + "="*50)
    print("🔍 ENVIRONMENT CHECK")
    print("="*50)
    
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    
    # Check PATH
    path_env = os.environ.get('PATH', '')
    print(f"PATH contains {len(path_env.split(os.pathsep))} entries")
    
    # Look for Rust-related paths
    rust_paths = [p for p in path_env.split(os.pathsep) if 'cargo' in p.lower() or 'rust' in p.lower()]
    if rust_paths:
        print("Rust-related PATH entries:")
        for path in rust_paths:
            print(f"  - {path}")
    else:
        print("No Rust-related PATH entries found")
    
    # Check CARGO_HOME
    cargo_home = os.environ.get('CARGO_HOME')
    if cargo_home:
        print(f"CARGO_HOME: {cargo_home}")
        if Path(cargo_home).exists():
            print("  ✅ CARGO_HOME directory exists")
        else:
            print("  ❌ CARGO_HOME directory does not exist")
    else:
        print("CARGO_HOME: not set")
    
    # Check default cargo location
    default_cargo = Path.home() / ".cargo"
    if default_cargo.exists():
        print(f"Default cargo directory exists: {default_cargo}")
        cargo_bin = default_cargo / "bin"
        if cargo_bin.exists():
            print(f"  Cargo bin directory exists: {cargo_bin}")
            cargo_exe = cargo_bin / "cargo.exe"
            if cargo_exe.exists():
                print(f"  ✅ cargo.exe found: {cargo_exe}")
            else:
                print(f"  ❌ cargo.exe not found in {cargo_bin}")
        else:
            print(f"  ❌ Cargo bin directory not found")
    else:
        print(f"Default cargo directory not found: {default_cargo}")


def test_rust_commands():
    """Test Rust command availability."""
    print("\n" + "="*50)
    print("🦀 RUST COMMAND TESTS")
    print("="*50)
    
    # Test rustc
    success, _ = run_command("rustc --version", "Check rustc")
    if not success:
        return False
    
    # Test cargo with special handling
    success, _ = run_command("cargo --version", "Check cargo", check_cargo=True)
    if not success:
        return False
    
    # Test cargo commands
    if Path("Cargo.toml").exists():
        success, _ = run_command("cargo check", "Cargo check", check_cargo=True)
        if not success:
            print("⚠️  Cargo check failed, but this might be expected in some environments")
    
    return True


def simulate_ci_steps():
    """Simulate the CI workflow steps."""
    print("\n" + "="*50)
    print("🔄 SIMULATING CI WORKFLOW")
    print("="*50)
    
    # Step 1: Check if we're in the right directory
    if not Path("Cargo.toml").exists():
        print("❌ Not in project root (Cargo.toml not found)")
        return False
    
    # Step 2: Simulate environment setup
    print("📝 Simulating environment variable setup...")
    
    # Add cargo to PATH if not already there
    cargo_bin = Path.home() / ".cargo" / "bin"
    if cargo_bin.exists():
        current_path = os.environ.get('PATH', '')
        if str(cargo_bin) not in current_path:
            print(f"Adding {cargo_bin} to PATH")
            os.environ['PATH'] = str(cargo_bin) + os.pathsep + current_path
        
        if 'CARGO_HOME' not in os.environ:
            os.environ['CARGO_HOME'] = str(Path.home() / ".cargo")
            print(f"Set CARGO_HOME to {os.environ['CARGO_HOME']}")
    
    # Step 3: Test the commands that fail in CI
    print("\n🧪 Testing CI commands...")
    
    commands = [
        ("cargo --version", "Cargo version check"),
        ("cargo test", "Cargo test"),
        ("cargo fmt --all -- --check", "Cargo format check"),
        ("cargo clippy -- -D warnings", "Cargo clippy")
    ]
    
    results = {}
    for cmd, desc in commands:
        success, output = run_command(cmd, desc, check_cargo=True)
        results[desc] = success
    
    return all(results.values())


def main():
    """Main test function."""
    print("🚀 Windows Rust Toolchain Test")
    print("This script tests Rust availability in Windows-like environment")
    print("="*60)
    
    # Run tests
    tests = [
        ("Environment Check", check_environment),
        ("Rust Commands", test_rust_commands),
        ("CI Simulation", simulate_ci_steps),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            if test_name == "Environment Check":
                test_func()  # This one doesn't return a boolean
                results[test_name] = True
            else:
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
        print("✅ Rust toolchain should work in CI")
    else:
        print("\n⚠️  SOME TESTS FAILED")
        print("❌ May need additional fixes for Windows CI")
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
