#!/usr/bin/env python3
"""
Line endings test script for Rust formatting issues.

This script checks and fixes line ending issues that can cause rustfmt failures.
"""

import subprocess
import sys
import os
from pathlib import Path


def check_line_endings(file_path):
    """Check what type of line endings a file has."""
    try:
        with open(file_path, 'rb') as f:
            content = f.read()

        crlf_count = content.count(b'\r\n')
        lf_only_count = content.count(b'\n') - crlf_count
        cr_only_count = content.count(b'\r') - crlf_count

        return {
            'crlf': crlf_count,
            'lf': lf_only_count,
            'cr': cr_only_count,
            'total_lines': crlf_count + lf_only_count + cr_only_count
        }
    except Exception as e:
        return {'error': str(e)}


def normalize_line_endings(file_path, target='lf'):
    """Normalize line endings in a file."""
    try:
        with open(file_path, 'rb') as f:
            content = f.read()

        # Convert to LF
        if target == 'lf':
            # First convert CRLF to LF, then CR to LF
            content = content.replace(b'\r\n', b'\n')
            content = content.replace(b'\r', b'\n')
        elif target == 'crlf':
            # First normalize to LF, then convert to CRLF
            content = content.replace(b'\r\n', b'\n')
            content = content.replace(b'\r', b'\n')
            content = content.replace(b'\n', b'\r\n')

        with open(file_path, 'wb') as f:
            f.write(content)

        return True
    except Exception as e:
        print(f"Error normalizing {file_path}: {e}")
        return False


def run_command(cmd, description):
    """Run a command and return success status."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
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


def test_rust_files():
    """Test line endings in Rust files."""
    print("\n" + "="*50)
    print("🦀 RUST FILE LINE ENDING CHECK")
    print("="*50)

    rust_files = list(Path('.').rglob('*.rs'))
    toml_files = list(Path('.').rglob('*.toml'))

    all_files = rust_files + toml_files

    if not all_files:
        print("No Rust or TOML files found")
        return True

    issues_found = False

    for file_path in all_files:
        if file_path.is_file():
            endings = check_line_endings(file_path)

            if 'error' in endings:
                print(f"❌ Error checking {file_path}: {endings['error']}")
                issues_found = True
                continue

            total_lines = endings['total_lines']
            if total_lines == 0:
                print(f"📄 {file_path}: Empty file")
                continue

            if endings['crlf'] > 0:
                print(f"❌ {file_path}: Has {endings['crlf']} CRLF line endings (should be LF)")
                issues_found = True

                # Fix the line endings
                print(f"🔧 Fixing line endings in {file_path}...")
                if normalize_line_endings(file_path, 'lf'):
                    print(f"✅ Fixed line endings in {file_path}")
                else:
                    print(f"❌ Failed to fix line endings in {file_path}")
            elif endings['lf'] > 0:
                print(f"✅ {file_path}: Correct LF line endings ({endings['lf']} lines)")
            else:
                print(f"⚠️  {file_path}: Unusual line endings - CR: {endings['cr']}")

    return not issues_found


def test_rustfmt():
    """Test rustfmt formatting."""
    print("\n" + "="*50)
    print("🎨 RUSTFMT FORMATTING TEST")
    print("="*50)

    # First, apply formatting
    success, _ = run_command("cargo fmt --all", "Apply Rust formatting")
    if not success:
        return False

    # Then check if formatting is correct
    success, _ = run_command("cargo fmt --all -- --check", "Check Rust formatting")
    return success


def test_git_attributes():
    """Test .gitattributes configuration."""
    print("\n" + "="*50)
    print("📝 GIT ATTRIBUTES CHECK")
    print("="*50)

    gitattributes_path = Path('.gitattributes')

    if not gitattributes_path.exists():
        print("❌ .gitattributes file not found")
        return False

    with open(gitattributes_path, 'r') as f:
        content = f.read()

    required_rules = [
        '*.rs text eol=lf',
        '*.toml text eol=lf'
    ]

    missing_rules = []
    for rule in required_rules:
        if rule not in content:
            missing_rules.append(rule)

    if missing_rules:
        print(f"❌ Missing .gitattributes rules: {missing_rules}")
        return False
    else:
        print("✅ .gitattributes has correct line ending rules")
        return True


def main():
    """Main test function."""
    print("🚀 Line Endings and Rust Formatting Test")
    print("This script checks and fixes line ending issues for Rust files")
    print("="*60)

    # Check if we're in the right directory
    if not Path("Cargo.toml").exists():
        print("❌ Cargo.toml not found. Please run this script from the project root.")
        return False

    # Run tests
    tests = [
        ("Git Attributes", test_git_attributes),
        ("Rust File Line Endings", test_rust_files),
        ("Rustfmt Formatting", test_rustfmt),
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
        print("✅ Line endings are correct")
        print("✅ Rust formatting should work in CI")
    else:
        print("\n⚠️  SOME TESTS FAILED")
        print("❌ Fix issues before pushing to GitHub")

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
