"""
Test module for calculator application.
Contains integration tests for basic operations, plugin system, and history management.
"""
import io
import unittest.mock
import pytest
from calculator import PluginManager, main

def test_plugin_manager_initialization():
    """Test the initialization of PluginManager class."""
    manager = PluginManager()
    assert hasattr(manager, 'plugins')
    assert len(manager.plugins) > 0

@pytest.mark.parametrize("input_str,expected", [
    ("add 2 3", "Result: 5"),
    ("subtract 5 3", "Result: 2"),
    ("multiply 4 2", "Result: 8"),
    ("divide 6 2", "Result: 3.0"),
    ("divide 5 0", "Error: Division by zero"),
])
def test_calculator_operations_integration(input_str, expected):
    """Test basic calculator operations through integration testing."""
    with unittest.mock.patch('builtins.input', side_effect=[input_str, 'exit']), \
         unittest.mock.patch('sys.stdout', new=io.StringIO()) as fake_out:
        main()
        assert expected in fake_out.getvalue()

def test_invalid_inputs():
    """Test handling of invalid input commands."""
    with unittest.mock.patch('builtins.input', side_effect=['invalid command', 'exit']), \
         unittest.mock.patch('sys.stdout', new=io.StringIO()) as fake_out:
        main()
        assert "Error" in fake_out.getvalue()

def test_plugin_menu():
    """Test the display of plugin menu."""
    with unittest.mock.patch('builtins.input', side_effect=['menu', 'exit']), \
         unittest.mock.patch('sys.stdout', new=io.StringIO()) as fake_out:
        main()
        assert "Available Plugins" in fake_out.getvalue()

def test_plugin_execution():
    """Test execution of a plugin command."""
    with unittest.mock.patch('builtins.input', side_effect=['use_plugin scientific sqrt 16', 'exit']), \
         unittest.mock.patch('sys.stdout', new=io.StringIO()) as fake_out:
        main()
        assert "Result: 4.0" in fake_out.getvalue()

def test_history_commands():
    """Test various history-related commands."""
    inputs = [
        'add 2 3',
        'save_history',
        'clear_history',
        'load_history',
        'view_history',
        'delete_history',
        'save_history_to_csv test.csv',
        'load_history_from_csv test.csv',
        'exit'
    ]
    with unittest.mock.patch('builtins.input', side_effect=inputs), \
         unittest.mock.patch('sys.stdout', new=io.StringIO()) as fake_out:
        main()
        output = fake_out.getvalue()
        assert "Result: 5" in output
        assert "successfully" in output
        assert "cleared" in output

def test_invalid_commands():
    """Test handling of various invalid command scenarios."""
    inputs = [
        'invalid_op 1 2',
        'add invalid 2',
        'add 1',
        'save_history_to_csv',
        'load_history_from_csv',
        'exit'
    ]
    with unittest.mock.patch('builtins.input', side_effect=inputs), \
         unittest.mock.patch('sys.stdout', new=io.StringIO()) as fake_out:
        main()
        output = fake_out.getvalue()
        assert "Error: Invalid operation" in output
        assert "Error: Please enter valid numbers" in output
        assert "Error: Invalid input format" in output
        assert "Error: Invalid save_history_to_csv command format" in output
        assert "Error: Invalid load_history_from_csv command format" in output

def test_plugin_error_handling():
    """Test error handling in plugin system."""
    inputs = [
        'use_plugin nonexistent command',
        'use_plugin scientific invalid_command',
        'use_plugin',
        'exit'
    ]
    with unittest.mock.patch('builtins.input', side_effect=inputs), \
         unittest.mock.patch('sys.stdout', new=io.StringIO()) as fake_out:
        main()
        output = fake_out.getvalue()
        assert "Plugin 'nonexistent' not found" in output
        assert "Command 'invalid_command' not found" in output
        assert "Error: Invalid input format" in output
