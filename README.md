# demopy_gb_jj

A minimal Rust-based Python extension using PyO3 bindings with automated CI/CD
pipeline.

[![CI](https://github.com/jj-devhub/demopy/actions/workflows/ci.yml/badge.svg)](https://github.com/jj-devhub/demopy/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/demopy-gb-jj.svg)](https://badge.fury.io/py/demopy-gb-jj)
[![Python versions](https://img.shields.io/pypi/pyversions/demopy-gb-jj.svg)](https://pypi.org/project/demopy-gb-jj/)

## Features

- **Rust-Python Integration**: High-performance Rust functions exposed to Python
via PyO3
- **Fallback Support**: Pure Python implementations when Rust extension is
unavailable
- **Automated CI/CD**: GitHub Actions workflows for testing, building, and
publishing
- **Version Management**: Automated version bumping across all project files
- **Cross-Platform**: Supports Windows, macOS, and Linux
- **Multiple Python Versions**: Compatible with Python 3.8-3.13

## Installation

### From PyPI (Recommended)

```bash
pip install demopy_gb_jj
```text

### From Source

```bash
# Clone the repository
git clone https://github.com/jj-devhub/demopy.git
cd demopy

# Install Rust (if not already installed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install Python dependencies
pip install maturin

# Build and install the package
maturin develop
```text

## Usage

```python
import demopy

# Basic functions
print(demopy.hello())  # "Hello from demopy_gb_jj (Rust edition)!"
print(demopy.add(2, 3))  # 5
print(demopy.multiply(2.5, 4.0))  # 10.0

# List operations
numbers = [1, 2, 3, 4, 5]
print(demopy.sum_list(numbers))  # 15

# String operations
print(demopy.reverse_string("Hello, World!"))  # "!dlroW ,olleH"

# Version info
print(demopy.__version__)  # Current version
```text

## Development

### Prerequisites

- Python 3.8 or higher (tested up to 3.13)
- Rust 1.70 or higher
- Git

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/jj-devhub/demopy.git
cd demopy

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install maturin pytest

# Set up pre-commit hooks for code quality (recommended)
python scripts/setup_pre_commit.py

# Build the extension in development mode
maturin develop

# Run tests
pytest tests/ -v
cargo test
```text

### Code Quality

This project uses automated code quality enforcement through pre-commit hooks:

```bash
# Set up pre-commit hooks (one-time setup)
python scripts/setup_pre_commit.py

# Hooks run automatically on git commit
git commit -m "your changes"  # Hooks auto-format and check code
```text

**Available quality tools:**

- **Black**: Python code formatting (88-char line length)
- **isort**: Import statement sorting
- **flake8**: Python linting and PEP 8 compliance
- **mypy**: Static type checking (optional)
- **cargo fmt**: Rust code formatting
- **cargo clippy**: Rust linting

See [docs/PRE_COMMIT_HOOKS.md](docs/PRE_COMMIT_HOOKS.md) for detailed information.

### Project Structure

```text
demopy/
├── .github/workflows/     # GitHub Actions CI/CD
├── docs/                  # Documentation
├── python/demopy/         # Python package source
├── src/                   # Rust source code
├── tests/                 # Test files
├── scripts/               # Utility scripts
├── .pre-commit-config.yaml # Pre-commit hooks configuration
├── Cargo.toml            # Rust package configuration
├── pyproject.toml        # Python package configuration
└── README.md
```text

### Version Management

This project uses automated version management. To bump the version:

#### Using GitHub Actions (Recommended)

1. Go to the "Actions" tab in your GitHub repository
2. Select "Version Bump" workflow
3. Click "Run workflow"
4. Choose the bump type (patch/minor/major) or specify a custom version
5. The workflow will automatically:
   - Update version numbers in all files
   - Create a commit and tag
   - Trigger the release workflow
   - Publish to PyPI

#### Manual Version Bumping

```bash
# Bump patch version (0.2.5 -> 0.2.6)
python scripts/bump_version.py patch

# Bump minor version (0.2.5 -> 0.3.0)
python scripts/bump_version.py minor

# Bump major version (0.2.5 -> 1.0.0)
python scripts/bump_version.py major

# Set specific version
python scripts/bump_version.py 1.2.3
```text

### Testing

```bash
# Run Python tests
pytest tests/ -v

# Run Rust tests
cargo test

# Run linting
cargo fmt --all -- --check
cargo clippy -- -D warnings

# Test pure Python fallback
python -c "
import sys
sys.path.insert(0, 'python')
import builtins
original_import = builtins.__import__
def mock_import(name, *args, **kwargs):
    if 'demopy_gb_jj._rust' in name:
        raise ImportError('Mocked')
    return original_import(name, *args, **kwargs)
builtins.__import__ = mock_import
import demopy
print(demopy.hello())
"
```text

### Building and Publishing

The project uses GitHub Actions for automated building and publishing:

1. **Continuous Integration**: Runs on every push and pull request
   - Tests across multiple OS and Python versions
   - Builds the Rust extension
   - Runs both Rust and Python tests

2. **Release Workflow**: Triggers on version tags
   - Builds wheels for all platforms
   - Creates source distribution
   - Publishes to PyPI
   - Creates GitHub release with changelog

3. **Version Bump Workflow**: Manual trigger for version management
   - Updates version across all files
   - Creates commit and tag
   - Triggers release workflow

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run the test suite (`pytest tests/ && cargo test`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Architecture

### Rust Extension

The Rust code in `src/lib.rs` implements high-performance functions using PyO3:

- **hello()**: Returns a greeting message
- **add(a, b)**: Adds two integers
- **multiply(a, b)**: Multiplies two floats
- **sum_list(numbers)**: Sums a list of integers
- **reverse_string(s)**: Reverses a string

### Python Wrapper

The Python module in `python/demopy/__init__.py` provides:

- Import handling with fallback to pure Python
- Consistent API regardless of backend
- Version information
- Proper error handling

### Fallback Mechanism

If the Rust extension fails to load, the package automatically falls back to
pure Python implementations, ensuring the package works even in environments
where the Rust extension cannot be built or loaded.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE)
file for details.

## Changelog

See [Releases](https://github.com/jj-devhub/demopy/releases) for a detailed changelog.

A demo PyPI package for CI/CD publishing.
