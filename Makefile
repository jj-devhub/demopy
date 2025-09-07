# Makefile for demopy_gb_jj development
#
# Common commands:
#   make setup     - Set up development environment
#   make format    - Format all code (Rust + Python)
#   make lint      - Run all linters
#   make test      - Run all tests
#   make check     - Run all quality checks
#   make build     - Build the package
#   make clean     - Clean build artifacts

.PHONY: help setup format lint test check build clean install dev-install

# Default target
help:
	@echo "🚀 demopy_gb_jj Development Commands"
	@echo "=================================="
	@echo ""
	@echo "Setup:"
	@echo "  make setup        Set up development environment"
	@echo "  make install      Install package in current environment"
	@echo "  make dev-install  Install package in development mode"
	@echo ""
	@echo "Code Quality:"
	@echo "  make format       Format all code (Rust + Python)"
	@echo "  make lint         Run all linters"
	@echo "  make test         Run all tests"
	@echo "  make check        Run all quality checks"
	@echo ""
	@echo "Build:"
	@echo "  make build        Build wheels and source distribution"
	@echo "  make clean        Clean build artifacts"
	@echo ""
	@echo "Development:"
	@echo "  make pre-commit   Run pre-commit on all files"
	@echo "  make security     Run security scans"
	@echo "  make docs         Generate documentation"

# Setup development environment
setup:
	@echo "🔧 Setting up development environment..."
	python scripts/setup_dev_environment.py

# Format all code
format:
	@echo "🎨 Formatting code..."
	@echo "📝 Formatting Rust code..."
	cargo fmt --all
	@echo "🐍 Formatting Python code..."
	black python/ tests/ scripts/
	isort python/ tests/ scripts/

# Run all linters
lint:
	@echo "🔍 Running linters..."
	@echo "🦀 Rust linting..."
	cargo clippy --all-targets --all-features -- -D warnings
	@echo "🐍 Python linting..."
	flake8 python/ tests/ scripts/
	@echo "📄 YAML linting..."
	yamllint .github/workflows/ .pre-commit-config.yaml || true

# Run all tests
test:
	@echo "🧪 Running tests..."
	@echo "🦀 Rust tests..."
	cargo test --verbose
	@echo "🐍 Python tests..."
	PYTHONPATH=python pytest tests/ -v

# Run all quality checks
check: format lint test
	@echo "✅ All quality checks completed"

# Build the package
build:
	@echo "📦 Building package..."
	maturin build --release
	@echo "✅ Build completed. Wheels available in target/wheels/"

# Install package in current environment
install:
	@echo "📥 Installing package..."
	pip install .

# Install package in development mode
dev-install:
	@echo "🔧 Installing package in development mode..."
	maturin develop

# Clean build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	cargo clean
	rm -rf target/
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Clean completed"

# Run pre-commit on all files
pre-commit:
	@echo "🪝 Running pre-commit hooks..."
	pre-commit run --all-files

# Run security scans
security:
	@echo "🔒 Running security scans..."
	@echo "🦀 Rust security audit..."
	cargo audit || true
	@echo "🐍 Python security scan..."
	safety check || true
	bandit -r python/ || true

# Generate documentation
docs:
	@echo "📚 Generating documentation..."
	@echo "🦀 Rust documentation..."
	cargo doc --no-deps --open
	@echo "🐍 Python documentation..."
	# Add Python doc generation here if needed

# Quick development cycle
dev: format lint test
	@echo "🚀 Development cycle completed"

# Release preparation
release-check: check security
	@echo "🚀 Release preparation checks completed"
	@echo "✅ Ready for release!"

# CI simulation (run what CI runs)
ci:
	@echo "🤖 Simulating CI pipeline..."
	@echo "1️⃣ Code formatting check..."
	cargo fmt --all -- --check
	@echo "2️⃣ Rust linting..."
	cargo clippy --all-targets --all-features -- -D warnings
	@echo "3️⃣ Rust tests..."
	cargo test
	@echo "4️⃣ Python formatting check..."
	black --check python/ tests/ scripts/
	isort --check-only python/ tests/ scripts/
	@echo "5️⃣ Python linting..."
	flake8 python/ tests/ scripts/
	@echo "6️⃣ Python tests..."
	PYTHONPATH=python pytest tests/ -v
	@echo "7️⃣ Build test..."
	maturin build --release
	@echo "✅ CI simulation completed successfully!"

# Show current status
status:
	@echo "📊 Project Status"
	@echo "================"
	@echo "🦀 Rust version:"
	@rustc --version
	@echo "🐍 Python version:"
	@python --version
	@echo "📦 Package version:"
	@python scripts/get_version.py
	@echo "🔧 Git status:"
	@git status --porcelain | head -10

# Install development dependencies
deps:
	@echo "📦 Installing development dependencies..."
	pip install black isort flake8 mypy pytest pre-commit maturin safety bandit
	rustup component add rustfmt clippy
	python scripts/install_rust_tools.py --mode dev

# Install CI dependencies only
deps-ci:
	@echo "🤖 Installing CI dependencies..."
	pip install black isort flake8 pytest maturin
	rustup component add rustfmt clippy
	python scripts/install_rust_tools.py --mode ci

# List installed Rust tools
tools-list:
	@echo "📋 Listing installed Rust tools..."
	python scripts/install_rust_tools.py --mode list

# Clean Rust tool cache
tools-clean:
	@echo "🧹 Cleaning Rust tool cache..."
	python scripts/install_rust_tools.py --mode clean

# Validate Python package structure
validate-python:
	@echo "🔍 Validating Python package structure..."
	python scripts/test_python_structure.py

# Test Python fallback only
test-python-fallback:
	@echo "🐍 Testing Python fallback implementation..."
	PYTHONPATH=python python -c "import demopy; print('Version:', demopy.__version__); print('Hello:', demopy.hello())"

# Pre-commit hooks management
setup-hooks:
	@echo "🪝 Setting up pre-commit hooks..."
	python scripts/setup_pre_commit.py

install-hooks:
	@echo "📦 Installing pre-commit hooks..."
	pip install pre-commit
	pre-commit install

update-hooks:
	@echo "🔄 Updating pre-commit hooks..."
	pre-commit autoupdate

run-hooks:
	@echo "🧪 Running pre-commit hooks on all files..."
	pre-commit run --all-files

skip-hooks:
	@echo "⚠️  Skipping pre-commit hooks for next commit..."
	@echo "Use: git commit --no-verify -m 'your message'"
