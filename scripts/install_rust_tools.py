#!/usr/bin/env python3
"""
Rust tools installation script for CI/CD workflows.

This script manages the installation of Rust tools in a way that handles
existing installations gracefully and provides proper error handling.
"""

import subprocess
import sys
import os
import json
from pathlib import Path


def run_command(cmd, description, check=True, capture_output=True):
    """Run a command and return success status and output."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            check=check, 
            capture_output=capture_output, 
            text=True
        )
        if capture_output and result.stdout.strip():
            print(f"   Output: {result.stdout.strip()}")
        if check:
            print(f"✅ {description} - SUCCESS")
        return True, result.stdout.strip() if capture_output else ""
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        if capture_output and e.stderr:
            print(f"   Error: {e.stderr.strip()}")
        return False, e.stderr.strip() if capture_output else ""


def check_tool_installed(tool_name):
    """Check if a cargo tool is installed."""
    success, _ = run_command(f"command -v {tool_name}", f"Check if {tool_name} is installed", check=False)
    return success


def get_tool_version(tool_name):
    """Get the version of an installed tool."""
    success, output = run_command(f"{tool_name} --version", f"Get {tool_name} version", check=False)
    if success:
        return output.split()[1] if len(output.split()) > 1 else "unknown"
    return None


def install_cargo_tool(tool_name, install_args="--locked", force_reinstall=False):
    """Install a cargo tool with proper error handling."""
    print(f"\n📦 Installing Rust tool: {tool_name}")
    print("-" * 40)
    
    # Check if already installed
    if not force_reinstall and check_tool_installed(tool_name):
        version = get_tool_version(tool_name)
        print(f"✅ {tool_name} already installed (version: {version})")
        return True
    
    # Try normal installation
    install_cmd = f"cargo install {tool_name} {install_args}"
    print(f"Running: {install_cmd}")
    
    success, output = run_command(install_cmd, f"Install {tool_name}", check=False)
    
    if success:
        version = get_tool_version(tool_name)
        print(f"✅ {tool_name} installed successfully (version: {version})")
        return True
    
    # If normal installation failed, try with --force
    if "already exists in destination" in output:
        print(f"⚠️  {tool_name} binary already exists, trying with --force...")
        force_cmd = f"cargo install {tool_name} {install_args} --force"
        print(f"Running: {force_cmd}")
        
        success, _ = run_command(force_cmd, f"Force install {tool_name}", check=False)
        if success:
            version = get_tool_version(tool_name)
            print(f"✅ {tool_name} force-installed successfully (version: {version})")
            return True
    
    print(f"❌ Failed to install {tool_name}")
    return False


def install_development_tools():
    """Install all development tools needed for the project."""
    print("🛠️  Installing Rust Development Tools")
    print("="*50)
    
    # Define tools to install
    tools = [
        ("cargo-machete", "--locked", "Detect unused dependencies"),
        ("cargo-audit", "--locked", "Security vulnerability scanner"),
        ("cargo-outdated", "--locked", "Check for outdated dependencies"),
        ("cargo-deny", "--locked", "Cargo plugin for linting dependencies"),
        ("cargo-tarpaulin", "--locked", "Code coverage tool"),
    ]
    
    results = {}
    for tool_name, args, description in tools:
        print(f"\n🔧 {tool_name}: {description}")
        results[tool_name] = install_cargo_tool(tool_name, args)
    
    return results


def install_ci_tools():
    """Install only the tools needed for CI/CD."""
    print("🤖 Installing CI/CD Tools")
    print("="*30)
    
    # Essential tools for CI
    ci_tools = [
        ("cargo-machete", "--locked", "Unused dependency detection"),
        ("cargo-audit", "--locked", "Security audit"),
    ]
    
    results = {}
    for tool_name, args, description in ci_tools:
        print(f"\n🔧 {tool_name}: {description}")
        results[tool_name] = install_cargo_tool(tool_name, args)
    
    return results


def list_installed_tools():
    """List all installed cargo tools."""
    print("\n📋 Installed Cargo Tools")
    print("="*30)
    
    # Get list of installed cargo tools
    success, output = run_command("cargo install --list", "List installed tools", check=False)
    
    if success:
        lines = output.split('\n')
        tools = []
        for line in lines:
            if line and not line.startswith(' '):
                tool_info = line.split()
                if len(tool_info) >= 2:
                    tool_name = tool_info[0]
                    version = tool_info[1].strip('v:')
                    tools.append((tool_name, version))
        
        if tools:
            print("Installed tools:")
            for tool_name, version in tools:
                print(f"  ✅ {tool_name} (v{version})")
        else:
            print("No cargo tools installed")
    else:
        print("❌ Failed to list installed tools")


def clean_tool_cache():
    """Clean cargo tool cache to resolve conflicts."""
    print("\n🧹 Cleaning Cargo Cache")
    print("="*25)
    
    cache_dirs = [
        "~/.cargo/registry/cache",
        "~/.cargo/registry/index",
        "~/.cargo/git/db",
    ]
    
    for cache_dir in cache_dirs:
        expanded_dir = os.path.expanduser(cache_dir)
        if os.path.exists(expanded_dir):
            success, _ = run_command(f"rm -rf {expanded_dir}", f"Clean {cache_dir}", check=False)
            if success:
                print(f"✅ Cleaned {cache_dir}")
            else:
                print(f"⚠️  Failed to clean {cache_dir}")
        else:
            print(f"ℹ️  {cache_dir} does not exist")


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Install Rust tools for development and CI/CD")
    parser.add_argument("--mode", choices=["dev", "ci", "list", "clean"], default="ci",
                       help="Installation mode: dev (all tools), ci (CI tools only), list (show installed), clean (clean cache)")
    parser.add_argument("--force", action="store_true", help="Force reinstall all tools")
    parser.add_argument("--tool", help="Install specific tool only")
    
    args = parser.parse_args()
    
    if args.mode == "list":
        list_installed_tools()
        return True
    
    if args.mode == "clean":
        clean_tool_cache()
        return True
    
    if args.tool:
        print(f"🔧 Installing specific tool: {args.tool}")
        success = install_cargo_tool(args.tool, force_reinstall=args.force)
        return success
    
    # Install tools based on mode
    if args.mode == "dev":
        results = install_development_tools()
    else:  # ci mode
        results = install_ci_tools()
    
    # Summary
    print("\n" + "="*50)
    print("📊 INSTALLATION SUMMARY")
    print("="*50)
    
    success_count = sum(1 for success in results.values() if success)
    total_count = len(results)
    
    for tool_name, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{status} {tool_name}")
    
    print(f"\n📈 Results: {success_count}/{total_count} tools installed successfully")
    
    if success_count == total_count:
        print("🎉 All tools installed successfully!")
        list_installed_tools()
        return True
    else:
        print("⚠️  Some tools failed to install")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
