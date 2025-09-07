# Contributing to demopy_gb_jj

Thank you for your interest in contributing to demopy_gb_jj! This document
provides guidelines for contributing to the project.

## 🚀 Automated Release Pipeline

This project uses an **automated CI/CD pipeline** that automatically handles
versioning, building, and publishing based on your commit messages.
Understanding how this works will help you contribute effectively.

### 📝 Commit Message Conventions

We use **semantic commit messages** to automatically determine version bumps
and generate changelogs. Please follow these conventions:

#### **Format:**

```text
<type>: <description>

[optional body]

[optional footer]
```text

#### **Types and Version Impact:**

| Commit Type | Version Bump | Example |
|-------------|--------------|---------|
| `feat:` or `feature:` | **Minor** (0.4.0 → 0.5.0) | `feat: add new functions` |
| `fix:` or `patch:` | **Patch** (0.4.0 → 0.4.1) | `fix: resolve memory leak` |
| `BREAKING CHANGE:` or `major:` | **Major** (0.4.0 → 1.0.0) | `feat: redesign` |
| `chore:`, `docs:`, etc. | **Patch** (0.4.0 → 0.4.1) | `chore: update deps` |

#### **Examples:**

**New Feature (Minor Version Bump):**

```text
feat: add trigonometric functions to Rust extension

- Add sin, cos, tan functions
- Include comprehensive tests
- Update documentation with examples
```text

**Bug Fix (Patch Version Bump):**

```text
fix: resolve division by zero error in multiply function

The multiply function now properly handles edge cases where
one of the operands is zero.

Fixes #123
```text

**Breaking Change (Major Version Bump):**

```python
feat: redesign function signatures for better type safety

BREAKING CHANGE: All function signatures now require explicit
type annotations. This improves type safety but breaks
backward compatibility with versions < 1.0.0.

Migration guide:
- Old: demopy.add(5, 7)
- New: demopy.add(5, 7)  # (no change in usage, but internal types changed)
```text

**Maintenance (Patch Version Bump):**

```

chore: update Rust dependencies to latest versions

- Update maturin to 1.4.0
- Update pyo3 to 0.20.0
- All tests pass with new versions

```text

### 🔄 Automated Workflow Process

When you push commits to the `main` branch:

1. **Analysis**: The system analyzes your commit messages
2. **Version Calculation**: Determines the appropriate version bump
3. **Version Update**: Updates version in all project files
4. **Tag Creation**: Creates a git tag (e.g., `v0.4.1`)
5. **Build**: Builds wheels for all platforms (Ubuntu, Windows, macOS)
6. **Publish**: Publishes to PyPI automatically
7. **Release**: Creates GitHub release with auto-generated changelog

### 🚫 Skipping Automatic Releases

If you want to push changes without triggering a release, include `[skip ci]` in
your commit message:

```python
docs: update README with new examples [skip ci]
```text

Or use commit types that don't trigger releases:

- `docs:` - Documentation changes
- `style:` - Code formatting changes
- `test:` - Test-only changes

## 🛠️ Development Workflow

### **Setting Up Development Environment:**

1. **Clone the repository:**

   ```bash
   git clone https://github.com/jj-devhub/demopy.git
   cd demopy
   ```text

2. **Set up development environment (automated):**

   ```bash
   python scripts/setup_dev_environment.py
   ```text

   Or manually:

   ```bash
   # Install Rust tools
   rustup component add rustfmt clippy

   # Install Python tools
   pip install black isort flake8 mypy pytest pre-commit maturin

   # Set up pre-commit hooks
   pre-commit install
   ```text

3. **Build and install in development mode:**

   ```bash
   maturin develop
   # Or use the Makefile
   make dev-install
   ```text

4. **Run tests:**

   ```bash
   pytest
   # Or use the Makefile
   make test
   ```text

### **Making Changes:**

1. **Create a feature branch:**

   ```bash
   git checkout -b feature/your-feature-name
   ```text

2. **Make your changes** following the coding standards

3. **Test your changes:**

   ```bash
   maturin develop
   pytest
   ```text

4. **Commit with semantic messages:**

   ```bash
   git commit -m "feat: add your new feature"
   ```text

5. **Push and create a pull request:**

   ```bash
   git push origin feature/your-feature-name
   ```text

### **Pull Request Process:**

1. **Ensure all tests pass**
2. **Update documentation** if needed
3. **Use semantic commit messages** in your PR
4. **Describe the changes** in the PR description
5. **Wait for review** and address feedback

## 📦 Manual Release Process

If you need to manually trigger a release:

1. **Go to GitHub Actions**: `https://github.com/jj-devhub/demopy/actions`
2. **Select "Manual Version Bump"** workflow
3. **Click "Run workflow"**
4. **Choose version bump type** (patch, minor, major)
5. **Optionally specify custom version**

## 🧪 Testing

### **Running Tests Locally:**

```bash
# Install in development mode
maturin develop

# Run Python tests
pytest

# Run Rust tests
cargo test
```text

### **Testing Different Python Versions:**

```bash
# Test with specific Python version
python3.8 -m pytest
python3.9 -m pytest
python3.10 -m pytest
```text

## 📋 Code Standards

### **Automated Code Quality:**

Our project uses automated code formatting and quality checks:

- **Pre-commit hooks**: Automatically format and check code before commits
- **CI/CD pipeline**: Runs comprehensive quality checks on every push
- **Make commands**: Easy access to all quality tools

### **Python Code:**

- **Formatting**: Automatically formatted with `black` (88 char line length)
- **Import sorting**: Automatically sorted with `isort`
- **Linting**: Checked with `flake8`
- **Type checking**: Optional `mypy` type checking
- **Testing**: Use `pytest` for all tests
- **Security**: Scanned with `safety` and `bandit`

### **Rust Code:**

- **Formatting**: Automatically formatted with `cargo fmt`
- **Linting**: Checked with `cargo clippy` (warnings as errors)
- **Testing**: Comprehensive test coverage required
- **Security**: Audited with `cargo audit`
- **Documentation**: Document all public APIs

### **Quality Commands:**

```bash
# Format all code
make format

# Run all linters
make lint

# Run all tests
make test

# Run all quality checks
make check

# Simulate CI pipeline locally
make ci
```text

### **Commit Messages:**

- Use semantic commit message format
- Keep the first line under 50 characters
- Use imperative mood ("add" not "added")
- Reference issues when applicable
- **Pre-commit hooks will check your commit message format**

## 🐛 Reporting Issues

When reporting issues:

1. **Use the issue templates** if available
2. **Provide clear reproduction steps**
3. **Include system information** (OS, Python version, etc.)
4. **Include error messages** and stack traces
5. **Describe expected vs actual behavior**

## 📄 License

By contributing to this project, you agree that your contributions will be
licensed under the MIT License.

## 🤝 Code of Conduct

Please be respectful and inclusive in all interactions.
We want this to be a welcoming community for everyone.

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Email**: Contact the maintainers directly if needed

Thank you for contributing to demopy_gb_jj! 🎉
