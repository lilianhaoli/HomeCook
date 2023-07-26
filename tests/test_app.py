import pytest

# sample function to be tested
def add_numbers(a, b):
    return a + b

# sample tests
def test_add_numbers():
    result = add_numbers(2, 3)
    assert result == 5

def test_add_numbers_negative():
    result = add_numbers(-5, 10)
    assert result == 5

def test_add_numbers_zero():
    result = add_numbers(0, 0)
    assert result == 0
    
if __name__ == '__main__':
    pytest.main()