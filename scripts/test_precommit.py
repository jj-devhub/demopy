# Test file to verify pre-commit hooks


def test_function():
    x = 1 + 2
    y = 3 + 4
    return x + y


def another_function(a, b, c):
    result = a + b + c
    return result


def good_function():
    return "test"


if __name__ == "__main__":
    print("Testing pre-commit hooks")
    print("Result:", test_function())
    print("Another result:", another_function(1, 2, 3))
    print("Good function:", good_function())
