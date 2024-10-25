"""Test module for calculator operations."""
from calculator import add, subtract, multiply, divide
from command import (
    AddCommand, SubtractCommand, MultiplyCommand, DivideCommand
)

def test_basic_operations():
    """Test basic arithmetic operations from the calculator module."""
    assert add(2, 3) == 5
    assert subtract(5, 3) == 2
    assert multiply(4, 3) == 12
    assert divide(6, 2) == 3
    assert divide(5, 0) == "Error: Division by zero"

def test_add_command(data_facade):
    """Test AddCommand execution and data storage."""
    cmd = AddCommand(data_facade, 2, 3)
    assert cmd.execute() == 5
    data = data_facade.view_data()
    assert "add" in data
    assert "5" in data

def test_subtract_command(data_facade):
    """Test SubtractCommand execution and data storage."""
    cmd = SubtractCommand(data_facade, 5, 3)
    assert cmd.execute() == 2
    data = data_facade.view_data()
    assert "subtract" in data
    assert "2" in data

def test_multiply_command(data_facade):
    """Test MultiplyCommand execution and data storage."""
    cmd = MultiplyCommand(data_facade, 4, 3)
    assert cmd.execute() == 12
    data = data_facade.view_data()
    assert "multiply" in data
    assert "12" in data

def test_divide_command(data_facade):
    """Test DivideCommand execution and data storage."""
    cmd = DivideCommand(data_facade, 6, 2)
    assert cmd.execute() == 3
    data = data_facade.view_data()
    assert "divide" in data
    assert "3" in data

def test_divide_by_zero_command(data_facade):
    """Test DivideCommand handling of division by zero."""
    cmd = DivideCommand(data_facade, 5, 0)
    assert cmd.execute() == "Error: Division by zero"
    