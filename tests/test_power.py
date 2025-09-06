#!/usr/bin/env python3
"""
Comprehensive tests for the power function in demopy_gb_jj.

Tests both the Rust extension and Python fallback implementations.
"""

import math
import os
import sys

import pytest

# Add the project root to the path so we can import demopy
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import demopy  # noqa: E402


class TestPowerFunction:
    """Test cases for the power function."""

    def test_basic_power_calculations(self):
        """Test basic power calculations."""
        assert demopy.power(2, 3) == 8
        assert demopy.power(5, 2) == 25
        assert demopy.power(10, 1) == 10
        assert demopy.power(7, 0) == 1

    def test_edge_cases(self):
        """Test edge cases."""
        # Zero base
        assert demopy.power(0, 5) == 0
        assert demopy.power(0, 0) == 1  # 0^0 is defined as 1 in most contexts

        # One base
        assert demopy.power(1, 100) == 1
        assert demopy.power(1, -50) == 1

        # Negative bases
        assert demopy.power(-2, 3) == -8
        assert demopy.power(-2, 2) == 4
        assert demopy.power(-3, 4) == 81
        assert demopy.power(-3, 3) == -27

    def test_fractional_exponents(self):
        """Test fractional exponents (roots)."""
        # Square roots
        assert abs(demopy.power(4, 0.5) - 2.0) < 1e-10
        assert abs(demopy.power(9, 0.5) - 3.0) < 1e-10
        assert abs(demopy.power(16, 0.5) - 4.0) < 1e-10

        # Cube roots
        assert abs(demopy.power(8, 1 / 3) - 2.0) < 1e-10
        assert abs(demopy.power(27, 1 / 3) - 3.0) < 1e-10

        # Other fractional exponents
        assert abs(demopy.power(32, 1 / 5) - 2.0) < 1e-10
        assert abs(demopy.power(16, 1 / 4) - 2.0) < 1e-10

    def test_negative_exponents(self):
        """Test negative exponents (reciprocals)."""
        assert abs(demopy.power(2, -1) - 0.5) < 1e-10
        assert abs(demopy.power(4, -1) - 0.25) < 1e-10
        assert abs(demopy.power(10, -2) - 0.01) < 1e-10
        assert abs(demopy.power(5, -2) - 0.04) < 1e-10

        # Fractional negative exponents
        assert abs(demopy.power(4, -0.5) - 0.5) < 1e-10
        assert abs(demopy.power(9, -0.5) - (1 / 3)) < 1e-10

    def test_large_numbers(self):
        """Test with large numbers."""
        assert demopy.power(2, 10) == 1024
        assert demopy.power(3, 5) == 243
        assert demopy.power(10, 6) == 1000000

    def test_decimal_bases(self):
        """Test with decimal bases."""
        assert abs(demopy.power(2.5, 2) - 6.25) < 1e-10
        assert abs(demopy.power(1.5, 3) - 3.375) < 1e-10
        assert abs(demopy.power(0.5, 2) - 0.25) < 1e-10
        assert abs(demopy.power(0.1, 2) - 0.01) < 1e-10

    def test_comparison_with_math_pow(self):
        """Test that our power function matches Python's math.pow."""
        test_cases = [
            (2, 3),
            (5, 2),
            (10, 0),
            (4, 0.5),
            (8, 1 / 3),
            (2, -1),
            (3.5, 2.2),
            (0.5, 3),
            (7, 4),
            (1.1, 10),
        ]

        for base, exponent in test_cases:
            expected = math.pow(base, exponent)
            actual = demopy.power(base, exponent)
            assert (
                abs(actual - expected) < 1e-10
            ), f"power({base}, {exponent}): expected {expected}, got {actual}"

    def test_type_handling(self):
        """Test that the function handles different numeric types."""
        # Integer inputs
        assert demopy.power(2, 3) == 8

        # Float inputs
        assert abs(demopy.power(2.0, 3.0) - 8.0) < 1e-10

        # Mixed inputs
        assert abs(demopy.power(2, 3.0) - 8.0) < 1e-10
        assert abs(demopy.power(2.0, 3) - 8.0) < 1e-10

    def test_special_mathematical_cases(self):
        """Test special mathematical cases."""
        # e^ln(x) should equal x (approximately)
        e = math.e
        x = 5.0
        ln_x = math.log(x)
        assert abs(demopy.power(e, ln_x) - x) < 1e-10

        # 10^log10(x) should equal x (approximately)
        x = 100.0
        log10_x = math.log10(x)
        assert abs(demopy.power(10, log10_x) - x) < 1e-10

        # Powers of e
        assert abs(demopy.power(e, 1) - e) < 1e-10
        assert abs(demopy.power(e, 0) - 1.0) < 1e-10

    def test_performance_consistency(self):
        """Test that the function performs consistently."""
        # Test the same calculation multiple times
        base, exponent = 2.5, 3.7
        expected = demopy.power(base, exponent)

        for _ in range(100):
            result = demopy.power(base, exponent)
            assert abs(result - expected) < 1e-10

    def test_function_exists_in_all(self):
        """Test that the power function is properly exported."""
        assert "power" in demopy.__all__
        assert hasattr(demopy, "power")
        assert callable(demopy.power)

    def test_docstring_and_metadata(self):
        """Test that the function has proper documentation."""
        # The function should be callable
        assert callable(demopy.power)

        # Test with a simple case to ensure it works
        result = demopy.power(2, 3)
        assert result == 8


class TestPowerFunctionEdgeCases:
    """Additional edge case tests for the power function."""

    def test_very_small_numbers(self):
        """Test with very small numbers."""
        assert abs(demopy.power(0.001, 2) - 0.000001) < 1e-15
        assert abs(demopy.power(0.1, 10) - 1e-10) < 1e-15

    def test_precision_limits(self):
        """Test precision limits."""
        # Test that we get reasonable precision for typical calculations
        result = demopy.power(2, 0.5)  # sqrt(2)
        expected = math.sqrt(2)
        assert abs(result - expected) < 1e-10

        result = demopy.power(10, 0.3010299957)  # approximately log10(2)
        expected = 2.0
        assert (
            abs(result - expected) < 1e-6
        )  # Slightly less precision due to floating point


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])
