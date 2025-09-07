# Pre-commit Hooks for demopy_gb_jj

This document explains the pre-commit hooks configuration for the demopy_gb_jj Rust-Python extension project, which automatically enforces code quality standards.

## 🎯 Overview

Pre-commit hooks automatically run code quality checks before each git commit, ensuring consistent code formatting and catching issues early in the development process.

## 🛠️ Available Hooks

### Python Code Quality Tools

| Tool | Purpose | Auto-fix | Block Commit |
|------|---------|----------|--------------|
| **Black** | Code formatting (88-char line length) | ✅ Yes | ❌ No |
| **isort** | Import statement sorting and organization | ✅ Yes | ❌ No |
| **flake8** | PEP 8 linting and code quality checks | ❌ No | ✅ Yes |
| **mypy** | Static type checking (optional) | ❌ No | ✅ Yes |

### Rust Code Quality Tools

| Tool | Purpose | Auto-fix | Block Commit |
|------|---------|----------|--------------|
| **cargo fmt** | Rust code formatting | ✅ Yes | ❌ No |
| **cargo clippy** | Rust linting with warnings as errors | ❌ No | ✅ Yes |
| **cargo test** | Run Rust tests | ❌ No | ✅ Yes |

### General File Quality

| Tool | Purpose | Auto-fix | Block Commit |
|------|---------|----------|--------------|
| **trailing-whitespace** | Remove trailing whitespace | ✅ Yes | ❌ No |
| **end-of-file-fixer** | Ensure files end with newline | ✅ Yes | ❌ No |
| **check-yaml** | Validate YAML syntax | ❌ No | ✅ Yes |
| **check-toml** | Validate TOML syntax | ❌ No | ✅ Yes |
| **check-merge-conflict** | Check for merge conflict markers | ❌ No | ✅ Yes |
| **check-added-large-files** | Prevent large files (>1MB) | ❌ No | ✅ Yes |
| **markdownlint** | Markdown formatting and linting | ✅ Yes | ❌ No |

## 📁 Target Directories

### Python Hooks Target:
- `python/` - Python fallback implementation
- `tests/` - Test files
- `scripts/` - Utility scripts

### Rust Hooks Target:
- `src/` - Rust source code
- `Cargo.toml` - Rust configuration

### Excluded Directories:
- `.venv/` - Virtual environment
- `target/` - Rust build artifacts
- `__pycache__/` - Python cache
- `.git/` - Git metadata

## 🚀 Quick Setup

### Option 1: Automated Setup (Recommended)
```bash
# Run the setup script
python scripts/setup_pre_commit.py

# Or use make command
make setup-hooks
```

### Option 2: Manual Setup
```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Test hooks
pre-commit run --all-files
```

## ⚙️ Configuration Files

### `.pre-commit-config.yaml`
Main configuration file defining all hooks, their versions, and settings.

### `pyproject.toml` Tool Sections
```toml
[tool.black]
line-length = 88
target-version = ['py38', 'py39', 'py310', 'py311', 'py312', 'py313']

[tool.isort]
profile = "black"
line_length = 88
src_paths = ["python", "tests", "scripts"]

[tool.flake8]
max-line-length = 88
extend-ignore = ["E203", "W503"]

[tool.mypy]
python_version = "3.8"
ignore_missing_imports = true
files = ["python", "tests", "scripts"]
```

## 🔄 Daily Usage

### Normal Commit Process
```bash
# Make your changes
git add .

# Commit (hooks run automatically)
git commit -m "your commit message"

# If hooks auto-fix files, add and commit again
git add .
git commit -m "your commit message"
```

### Common Scenarios

#### Scenario 1: Auto-fixable Issues
```bash
$ git commit -m "fix: update function"
Black................................................Passed
isort................................................Passed
# Files were reformatted, commit again
$ git add .
$ git commit -m "fix: update function"
```

#### Scenario 2: Linting Errors
```bash
$ git commit -m "fix: update function"
flake8...............................................Failed
# Fix the linting errors manually, then commit
```

#### Scenario 3: Emergency Bypass (Not Recommended)
```bash
# Skip hooks for one commit only
git commit --no-verify -m "emergency fix"
```

## 🛠️ Management Commands

### Makefile Commands
```bash
make setup-hooks      # Complete setup with testing
make install-hooks    # Install pre-commit only
make update-hooks     # Update hook versions
make run-hooks        # Run hooks on all files
make skip-hooks       # Show how to skip hooks
```

### Direct Pre-commit Commands
```bash
pre-commit run --all-files           # Run all hooks on all files
pre-commit run black                 # Run specific hook
pre-commit run --files python/*.py  # Run on specific files
pre-commit autoupdate               # Update hook versions
pre-commit uninstall                # Remove hooks
```

## 🔧 Troubleshooting

### Common Issues

#### Hook Installation Failed
```bash
# Reinstall pre-commit
pip uninstall pre-commit
pip install pre-commit
pre-commit install
```

#### Hooks Not Running
```bash
# Check if hooks are installed
ls -la .git/hooks/

# Reinstall if missing
pre-commit install
```

#### Formatting Conflicts
```bash
# Run formatters manually
black python/ tests/ scripts/
isort python/ tests/ scripts/

# Then commit
git add .
git commit -m "your message"
```

#### Type Checking Errors
```bash
# Run mypy manually to see detailed errors
mypy python/ tests/ scripts/

# Fix type issues or add type: ignore comments
```

### Performance Issues

#### Slow Hook Execution
```bash
# Update to latest versions
pre-commit autoupdate

# Clean and reinstall
pre-commit clean
pre-commit install
```

## 📊 Integration with CI/CD

The pre-commit hooks use the same tools and configurations as the CI/CD pipeline:

- **Code Quality workflow** runs the same checks
- **Integration tests** verify the same standards
- **Release pipeline** ensures quality before publishing

This ensures consistency between local development and automated testing.

## 🎯 Benefits

### For Developers
- ✅ **Automatic formatting** - No manual code formatting needed
- ✅ **Early error detection** - Catch issues before CI/CD
- ✅ **Consistent style** - All code follows the same standards
- ✅ **Reduced review time** - Fewer formatting-related comments

### For the Project
- ✅ **Code quality assurance** - Maintain high standards automatically
- ✅ **Reduced CI failures** - Catch issues locally first
- ✅ **Professional appearance** - Consistent, well-formatted codebase
- ✅ **Easy onboarding** - New contributors get instant feedback

## 📚 Additional Resources

- [Pre-commit Documentation](https://pre-commit.com/)
- [Black Documentation](https://black.readthedocs.io/)
- [isort Documentation](https://pycqa.github.io/isort/)
- [flake8 Documentation](https://flake8.pycqa.org/)
- [mypy Documentation](https://mypy.readthedocs.io/)

## 🤝 Contributing

When contributing to this project:

1. **Set up hooks** using `python scripts/setup_pre_commit.py`
2. **Let hooks auto-fix** formatting issues
3. **Address linting errors** manually
4. **Test your changes** with `make test`
5. **Commit with confidence** knowing quality is enforced

The pre-commit hooks ensure that all contributions maintain the project's high code quality standards automatically!
