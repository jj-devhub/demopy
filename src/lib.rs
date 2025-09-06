use pyo3::prelude::*;
use pyo3::types::PyModule;

/// A simple function that returns a greeting message
#[pyfunction]
fn hello() -> String {
    "Hello from demopy_gb_jj (Rust edition)!".to_string()
}

/// A function that adds two numbers
#[pyfunction]
fn add(a: i64, b: i64) -> i64 {
    a + b
}

/// A function that multiplies two numbers
#[pyfunction]
fn multiply(a: f64, b: f64) -> f64 {
    a * b
}

/// A function that processes a list of numbers and returns their sum
#[pyfunction]
fn sum_list(numbers: Vec<i64>) -> i64 {
    numbers.iter().sum()
}

/// A function that reverses a string
#[pyfunction]
fn reverse_string(s: String) -> String {
    s.chars().rev().collect()
}

/// A function that calculates the power of a number (base^exponent)
#[pyfunction]
fn power(base: f64, exponent: f64) -> f64 {
    base.powf(exponent)
}

/// A Python module implemented in Rust.
#[pymodule]
fn demopy_gb_jj(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hello, m)?)?;
    m.add_function(wrap_pyfunction!(add, m)?)?;
    m.add_function(wrap_pyfunction!(multiply, m)?)?;
    m.add_function(wrap_pyfunction!(sum_list, m)?)?;
    m.add_function(wrap_pyfunction!(reverse_string, m)?)?;
    m.add_function(wrap_pyfunction!(power, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(add(2, 3), 5);
        assert_eq!(add(-1, 1), 0);
        assert_eq!(add(0, 0), 0);
    }

    #[test]
    fn test_multiply() {
        assert_eq!(multiply(2.0, 3.0), 6.0);
        assert_eq!(multiply(-1.0, 1.0), -1.0);
        assert_eq!(multiply(0.0, 100.0), 0.0);
    }

    #[test]
    fn test_sum_list() {
        assert_eq!(sum_list(vec![1, 2, 3, 4, 5]), 15);
        assert_eq!(sum_list(vec![]), 0);
        assert_eq!(sum_list(vec![-1, -2, -3]), -6);
    }

    #[test]
    fn test_reverse_string() {
        assert_eq!(reverse_string("hello".to_string()), "olleh");
        assert_eq!(reverse_string("".to_string()), "");
        assert_eq!(reverse_string("a".to_string()), "a");
    }

    #[test]
    fn test_hello() {
        let result = hello();
        assert!(result.contains("demopy_gb_jj"));
        assert!(result.contains("Rust edition"));
    }

    #[test]
    fn test_power() {
        // Basic power calculations
        assert_eq!(power(2.0, 3.0), 8.0);
        assert_eq!(power(5.0, 2.0), 25.0);
        assert_eq!(power(10.0, 0.0), 1.0);

        // Edge cases
        assert_eq!(power(0.0, 5.0), 0.0);
        assert_eq!(power(1.0, 100.0), 1.0);
        assert_eq!(power(-2.0, 3.0), -8.0);
        assert_eq!(power(-2.0, 2.0), 4.0);

        // Fractional exponents (square root, cube root)
        assert!((power(4.0, 0.5) - 2.0).abs() < 1e-10);
        assert!((power(8.0, 1.0/3.0) - 2.0).abs() < 1e-10);

        // Negative exponents
        assert!((power(2.0, -1.0) - 0.5).abs() < 1e-10);
        assert!((power(4.0, -0.5) - 0.5).abs() < 1e-10);
    }
}
