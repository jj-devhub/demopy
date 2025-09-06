"""
Tests for demopy_gb_jj package

These tests verify both the Rust extension and Python fallback implementations.
"""

import pytest
import sys
from pathlib import Path

# Add the python directory to the path so we can import demopy
sys.path.insert(0, str(Path(__file__).parent.parent / "python"))

import demopy


class TestBasicFunctionality:
    """Test basic functionality of the demopy package."""
    
    def test_hello(self):
        """Test the hello function."""
        result = demopy.hello()
        assert isinstance(result, str)
        assert "demopy_gb_jj" in result
        # Should contain either "Rust edition" or "Python fallback"
        assert any(phrase in result for phrase in ["Rust edition", "Python fallback"])
    
    def test_add(self):
        """Test the add function."""
        assert demopy.add(2, 3) == 5
        assert demopy.add(-1, 1) == 0
        assert demopy.add(0, 0) == 0
        assert demopy.add(100, 200) == 300
    
    def test_multiply(self):
        """Test the multiply function."""
        assert demopy.multiply(2.0, 3.0) == 6.0
        assert demopy.multiply(-1.0, 1.0) == -1.0
        assert demopy.multiply(0.0, 100.0) == 0.0
        assert demopy.multiply(2.5, 4.0) == 10.0
    
    def test_sum_list(self):
        """Test the sum_list function."""
        assert demopy.sum_list([1, 2, 3, 4, 5]) == 15
        assert demopy.sum_list([]) == 0
        assert demopy.sum_list([-1, -2, -3]) == -6
        assert demopy.sum_list([100]) == 100
    
    def test_reverse_string(self):
        """Test the reverse_string function."""
        assert demopy.reverse_string("hello") == "olleh"
        assert demopy.reverse_string("") == ""
        assert demopy.reverse_string("a") == "a"
        assert demopy.reverse_string("12345") == "54321"
        assert demopy.reverse_string("Hello, World!") == "!dlroW ,olleH"


class TestVersionInfo:
    """Test version information."""
    
    def test_version_exists(self):
        """Test that version information is available."""
        assert hasattr(demopy, "__version__")
        assert isinstance(demopy.__version__, str)
        assert len(demopy.__version__) > 0
    
    def test_version_format(self):
        """Test that version follows semantic versioning format."""
        import re
        version_pattern = r'^\d+\.\d+\.\d+$'
        assert re.match(version_pattern, demopy.__version__)


class TestModuleStructure:
    """Test module structure and exports."""
    
    def test_all_exports(self):
        """Test that __all__ is properly defined."""
        assert hasattr(demopy, "__all__")
        expected_exports = {
            "hello",
            "add", 
            "multiply",
            "sum_list",
            "reverse_string",
            "__version__"
        }
        assert set(demopy.__all__) == expected_exports
    
    def test_all_functions_callable(self):
        """Test that all exported functions are callable."""
        for func_name in demopy.__all__:
            if func_name != "__version__":
                func = getattr(demopy, func_name)
                assert callable(func), f"{func_name} should be callable"


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_add_large_numbers(self):
        """Test addition with large numbers."""
        large_num = 2**32
        result = demopy.add(large_num, large_num)
        assert result == 2 * large_num
    
    def test_multiply_precision(self):
        """Test multiplication precision with floats."""
        result = demopy.multiply(0.1, 0.2)
        # Allow for floating point precision issues
        assert abs(result - 0.02) < 1e-10
    
    def test_sum_list_large(self):
        """Test sum_list with a large list."""
        large_list = list(range(1000))
        expected = sum(large_list)
        assert demopy.sum_list(large_list) == expected
    
    def test_reverse_string_unicode(self):
        """Test reverse_string with unicode characters."""
        unicode_str = "Hello 🌍 World! 🚀"
        result = demopy.reverse_string(unicode_str)
        expected = unicode_str[::-1]
        assert result == expected


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
