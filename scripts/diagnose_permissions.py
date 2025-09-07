#!/usr/bin/env python3
"""
GitHub Actions permissions diagnostic script.

This script helps diagnose and troubleshoot GitHub Actions permission issues
that prevent the automated CI/CD pipeline from pushing commits and tags.
"""

import subprocess
import sys
import os
import json
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


def check_git_configuration():
    """Check git configuration for authentication."""
    print("\n" + "=" * 60)
    print("🔧 CHECKING GIT CONFIGURATION")
    print("=" * 60)

    checks = [
        ("git config user.name", "Check git user name"),
        ("git config user.email", "Check git user email"),
        ("git remote -v", "Check git remotes"),
        ("git status", "Check git status"),
    ]

    results = {}
    for cmd, description in checks:
        success, output = run_command(cmd, description, check=False)
        results[description] = (success, output)

    return results


def check_github_token_permissions():
    """Check GitHub token permissions if available."""
    print("\n" + "=" * 60)
    print("🔑 CHECKING GITHUB TOKEN PERMISSIONS")
    print("=" * 60)

    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        print("❌ GITHUB_TOKEN environment variable not found")
        print("   This is expected when running locally")
        return False

    print("✅ GITHUB_TOKEN found in environment")

    # Try to make a GitHub API call to check permissions
    try:
        import requests

        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json",
        }

        # Check token scopes
        response = requests.get("https://api.github.com/user", headers=headers)
        if response.status_code == 200:
            scopes = response.headers.get("X-OAuth-Scopes", "").split(", ")
            print(f"✅ Token scopes: {scopes}")

            # Check repository access
            repo_response = requests.get(
                "https://api.github.com/repos/jj-devhub/demopy", headers=headers
            )
            if repo_response.status_code == 200:
                repo_data = repo_response.json()
                permissions = repo_data.get("permissions", {})
                print(f"✅ Repository permissions: {permissions}")
                return True
            else:
                print(f"❌ Cannot access repository: {repo_response.status_code}")
                return False
        else:
            print(f"❌ Token validation failed: {response.status_code}")
            return False

    except ImportError:
        print("⚠️  requests library not available, skipping API checks")
        return None
    except Exception as e:
        print(f"❌ Error checking token permissions: {e}")
        return False


def check_workflow_permissions():
    """Check workflow file permissions configuration."""
    print("\n" + "=" * 60)
    print("📄 CHECKING WORKFLOW PERMISSIONS")
    print("=" * 60)

    workflow_file = Path(".github/workflows/auto-release.yml")
    if not workflow_file.exists():
        print("❌ auto-release.yml workflow file not found")
        return False

    try:
        import yaml

        with open(workflow_file, "r") as f:
            workflow_data = yaml.safe_load(f)

        permissions = workflow_data.get("permissions", {})
        if permissions:
            print("✅ Workflow permissions configured:")
            for perm, value in permissions.items():
                print(f"   {perm}: {value}")

            # Check for required permissions
            required_perms = ["contents", "actions"]
            missing_perms = []
            for perm in required_perms:
                if perm not in permissions or permissions[perm] != "write":
                    missing_perms.append(perm)

            if missing_perms:
                print(f"⚠️  Missing or insufficient permissions: {missing_perms}")
                return False
            else:
                print("✅ All required permissions present")
                return True
        else:
            print("❌ No permissions block found in workflow")
            print("   Add this to your workflow file:")
            print(
                """
permissions:
  contents: write
  actions: write
  packages: write
"""
            )
            return False

    except ImportError:
        print("⚠️  PyYAML not available, cannot parse workflow file")
        return None
    except Exception as e:
        print(f"❌ Error parsing workflow file: {e}")
        return False


def check_repository_settings():
    """Provide guidance on repository settings."""
    print("\n" + "=" * 60)
    print("⚙️  REPOSITORY SETTINGS CHECKLIST")
    print("=" * 60)

    print("Please verify these settings in your GitHub repository:")
    print()

    settings_checklist = [
        (
            "Workflow Permissions",
            [
                "Go to: https://github.com/jj-devhub/demopy/settings/actions",
                "Under 'Workflow permissions', select 'Read and write permissions'",
                "Check 'Allow GitHub Actions to create and approve pull requests'",
                "Click 'Save'",
            ],
        ),
        (
            "Branch Protection",
            [
                "Go to: https://github.com/jj-devhub/demopy/settings/branches",
                "If you have branch protection rules for 'main':",
                "  - Ensure 'Include administrators' allows automation",
                "  - Consider adding 'github-actions[bot]' to bypass restrictions",
                "  - Or disable 'Restrict pushes that create files'",
            ],
        ),
        (
            "Repository Secrets",
            [
                "Go to: https://github.com/jj-devhub/demopy/settings/secrets/actions",
                "If using Personal Access Token:",
                "  - Ensure PERSONAL_ACCESS_TOKEN secret exists",
                "  - Token should have 'repo' and 'workflow' scopes",
                "If using PyPI publishing:",
                "  - Ensure PYPI_API_TOKEN secret exists",
            ],
        ),
    ]

    for category, steps in settings_checklist:
        print(f"📋 {category}:")
        for step in steps:
            print(f"   {step}")
        print()


def simulate_git_operations():
    """Simulate git operations that the workflow performs."""
    print("\n" + "=" * 60)
    print("🧪 SIMULATING GIT OPERATIONS")
    print("=" * 60)

    print("⚠️  This will create test commits and tags. Use with caution!")
    response = input("Continue with simulation? (y/N): ").strip().lower()

    if response != "y":
        print("Simulation cancelled")
        return True

    # Create a test branch for simulation
    test_branch = "test-permissions-simulation"

    operations = [
        (f"git checkout -b {test_branch}", "Create test branch"),
        ("echo 'test' > test-permissions.txt", "Create test file"),
        ("git add test-permissions.txt", "Stage test file"),
        ("git commit -m 'test: permission simulation [skip ci]'", "Create test commit"),
        ("git push origin " + test_branch, "Push test branch"),
        ("git tag test-permission-tag", "Create test tag"),
        ("git push origin test-permission-tag", "Push test tag"),
        ("git checkout main", "Return to main branch"),
        ("git branch -D " + test_branch, "Delete test branch"),
        ("git push origin --delete " + test_branch, "Delete remote test branch"),
        ("git tag -d test-permission-tag", "Delete local test tag"),
        ("git push origin --delete test-permission-tag", "Delete remote test tag"),
    ]

    success_count = 0
    for cmd, description in operations:
        success, _ = run_command(cmd, description, check=False)
        if success:
            success_count += 1

    print(
        f"\n📊 Simulation Results: {success_count}/{len(operations)} operations succeeded"
    )

    if success_count == len(operations):
        print(
            "✅ All git operations successful - permissions likely configured correctly"
        )
        return True
    else:
        print("❌ Some git operations failed - check permissions and authentication")
        return False


def main():
    """Main diagnostic function."""
    print("🔍 GitHub Actions Permissions Diagnostic")
    print("Diagnosing permission issues for automated CI/CD pipeline")
    print("=" * 60)

    # Check if we're in the right directory
    if not Path(".github/workflows").exists():
        print("❌ .github/workflows directory not found")
        print("   Please run this script from the repository root")
        return False

    # Run diagnostic checks
    checks = [
        ("Git Configuration", check_git_configuration),
        ("GitHub Token Permissions", check_github_token_permissions),
        ("Workflow Permissions", check_workflow_permissions),
        ("Repository Settings", check_repository_settings),
    ]

    results = {}
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"❌ {check_name} failed with exception: {e}")
            results[check_name] = False

    # Optional simulation
    print("\n" + "=" * 60)
    print("🧪 OPTIONAL: GIT OPERATIONS SIMULATION")
    print("=" * 60)
    print("This will test actual git push operations to verify permissions")

    simulate = input("Run git operations simulation? (y/N): ").strip().lower()
    if simulate == "y":
        results["Git Operations Simulation"] = simulate_git_operations()

    # Summary
    print("\n" + "=" * 60)
    print("📊 DIAGNOSTIC SUMMARY")
    print("=" * 60)

    for check_name, result in results.items():
        if result is True:
            status = "✅ PASSED"
        elif result is False:
            status = "❌ FAILED"
        else:
            status = "⚠️  SKIPPED"
        print(f"{status} {check_name}")

    # Recommendations
    print("\n" + "=" * 60)
    print("💡 RECOMMENDATIONS")
    print("=" * 60)

    failed_checks = [name for name, result in results.items() if result is False]

    if not failed_checks:
        print("🎉 All checks passed! Your permissions should be configured correctly.")
        print("If you're still experiencing issues:")
        print("  1. Check GitHub Actions logs for specific error messages")
        print("  2. Verify repository settings match the checklist above")
        print("  3. Try the git operations simulation")
    else:
        print("⚠️  Issues found. Recommended actions:")
        print("  1. Review the failed checks above")
        print("  2. Follow the repository settings checklist")
        print(
            "  3. Consider using a Personal Access Token if GITHUB_TOKEN insufficient"
        )
        print("  4. Check the GitHub Actions Setup Guide: docs/GITHUB_ACTIONS_SETUP.md")

    return len(failed_checks) == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
