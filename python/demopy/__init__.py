"""
demopy_gb_jj - A demo PyPI package with Rust extensions

This package demonstrates how to create Python extensions using Rust and PyO3.
"""

__version__ = "0.4.0"

try:
    # Import the Rust extension
    from demopy_gb_jj._rust import (
        hello as _rust_hello,
        add,
        multiply,
        sum_list,
        reverse_string,
        power,
    )
    
    # Use the Rust implementation for hello
    def hello():
        """Return a greeting message from the Rust extension."""
        return _rust_hello()
    
    # Export all functions
    __all__ = [
        "hello",
        "add",
        "multiply",
        "sum_list",
        "reverse_string",
        "power",
        "__version__"
    ]
    
except ImportError:
    # Fallback to pure Python implementation if Rust extension is not available
    def hello():
        """Return a greeting message (pure Python fallback)."""
        return "Hello from demopy_gb_jj (Python fallback)!"
    
    def add(a, b):
        """Add two numbers (pure Python fallback)."""
        return a + b
    
    def multiply(a, b):
        """Multiply two numbers (pure Python fallback)."""
        return a * b
    
    def sum_list(numbers):
        """Sum a list of numbers (pure Python fallback)."""
        return sum(numbers)
    
    def reverse_string(s):
        """Reverse a string (pure Python fallback)."""
        return s[::-1]

    def power(base, exponent):
        """Calculate the power of a number (base^exponent) (pure Python fallback)."""
        return base ** exponent

    __all__ = [
        "hello",
        "add",
        "multiply",
        "sum_list",
        "reverse_string",
        "power",
        "__version__"
    ]
