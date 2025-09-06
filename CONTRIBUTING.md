# Contributing to demopy_gb_jj

Thank you for your interest in contributing to demopy_gb_jj! This document provides guidelines for contributing to the project.

## 🚀 Automated Release Pipeline

This project uses an **automated CI/CD pipeline** that automatically handles versioning, building, and publishing based on your commit messages. Understanding how this works will help you contribute effectively.

### 📝 Commit Message Conventions

We use **semantic commit messages** to automatically determine version bumps and generate changelogs. Please follow these conventions:

#### **Format:**
```
<type>: <description>

[optional body]

[optional footer]
```

#### **Types and Version Impact:**

| Commit Type | Version Bump | Example |
|-------------|--------------|---------|
| `feat:` or `feature:` | **Minor** (0.4.0 → 0.5.0) | `feat: add new mathematical functions` |
| `fix:` or `patch:` | **Patch** (0.4.0 → 0.4.1) | `fix: resolve memory leak in Rust extension` |
| `BREAKING CHANGE:` or `major:` | **Major** (0.4.0 → 1.0.0) | `feat: redesign API (BREAKING CHANGE)` |
| `chore:`, `docs:`, `style:`, `refactor:`, `perf:`, `test:` | **Patch** (0.4.0 → 0.4.1) | `chore: update dependencies` |

#### **Examples:**

**New Feature (Minor Version Bump):**
```
feat: add trigonometric functions to Rust extension

- Add sin, cos, tan functions
- Include comprehensive tests
- Update documentation with examples
```

**Bug Fix (Patch Version Bump):**
```
fix: resolve division by zero error in multiply function

The multiply function now properly handles edge cases where
one of the operands is zero.

Fixes #123
```

**Breaking Change (Major Version Bump):**
```
feat: redesign function signatures for better type safety

BREAKING CHANGE: All function signatures now require explicit
type annotations. This improves type safety but breaks
backward compatibility with versions < 1.0.0.

Migration guide:
- Old: demopy.add(5, 7)
- New: demopy.add(5, 7)  # (no change in usage, but internal types changed)
```

**Maintenance (Patch Version Bump):**
```
chore: update Rust dependencies to latest versions

- Update maturin to 1.4.0
- Update pyo3 to 0.20.0
- All tests pass with new versions
```

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

If you want to push changes without triggering a release, include `[skip ci]` in your commit message:

```
docs: update README with new examples [skip ci]
```

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
   ```

2. **Install development dependencies:**
   ```bash
   pip install maturin pytest
   ```

3. **Build and install in development mode:**
   ```bash
   maturin develop
   ```

4. **Run tests:**
   ```bash
   pytest
   ```

### **Making Changes:**

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the coding standards

3. **Test your changes:**
   ```bash
   maturin develop
   pytest
   ```

4. **Commit with semantic messages:**
   ```bash
   git commit -m "feat: add your new feature"
   ```

5. **Push and create a pull request:**
   ```bash
   git push origin feature/your-feature-name
   ```

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
```

### **Testing Different Python Versions:**
```bash
# Test with specific Python version
python3.8 -m pytest
python3.9 -m pytest
python3.10 -m pytest
```

## 📋 Code Standards

### **Python Code:**
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for all public functions
- Include tests for new functionality

### **Rust Code:**
- Follow standard Rust formatting (`cargo fmt`)
- Use `cargo clippy` for linting
- Write comprehensive tests
- Document public APIs

### **Commit Messages:**
- Use semantic commit message format
- Keep the first line under 50 characters
- Use imperative mood ("add" not "added")
- Reference issues when applicable

## 🐛 Reporting Issues

When reporting issues:

1. **Use the issue templates** if available
2. **Provide clear reproduction steps**
3. **Include system information** (OS, Python version, etc.)
4. **Include error messages** and stack traces
5. **Describe expected vs actual behavior**

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

## 🤝 Code of Conduct

Please be respectful and inclusive in all interactions. We want this to be a welcoming community for everyone.

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Email**: Contact the maintainers directly if needed

Thank you for contributing to demopy_gb_jj! 🎉
