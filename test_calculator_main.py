import pytest
from calculator import PluginManager, main
from unittest.mock import patch
import io
import sys

def test_plugin_manager_initialization():
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
    with patch('builtins.input', side_effect=[input_str, 'exit']), \
         patch('sys.stdout', new=io.StringIO()) as fake_out:
        main()
        assert expected in fake_out.getvalue()

def test_invalid_inputs():
    with patch('builtins.input', side_effect=['invalid command', 'exit']), \
         patch('sys.stdout', new=io.StringIO()) as fake_out:
        main()
        assert "Error" in fake_out.getvalue()

def test_plugin_menu():
    with patch('builtins.input', side_effect=['menu', 'exit']), \
         patch('sys.stdout', new=io.StringIO()) as fake_out:
        main()
        assert "Available Plugins" in fake_out.getvalue()

def test_plugin_execution():
    with patch('builtins.input', side_effect=['use_plugin scientific sqrt 16', 'exit']), \
         patch('sys.stdout', new=io.StringIO()) as fake_out:
        main()
        assert "Result: 4.0" in fake_out.getvalue()

def test_history_commands():
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
    with patch('builtins.input', side_effect=inputs), \
         patch('sys.stdout', new=io.StringIO()) as fake_out:
        main()
        output = fake_out.getvalue()
        assert "Result: 5" in output
        assert "successfully" in output
        assert "cleared" in output

def test_invalid_commands():
    inputs = [
        'invalid_op 1 2',
        'add invalid 2',
        'add 1',
        'save_history_to_csv',
        'load_history_from_csv',
        'exit'
    ]
    with patch('builtins.input', side_effect=inputs), \
         patch('sys.stdout', new=io.StringIO()) as fake_out:
        main()
        output = fake_out.getvalue()
        assert "Error: Invalid operation" in output
        assert "Error: Please enter valid numbers" in output
        assert "Error: Invalid input format" in output
        assert "Error: Invalid save_history_to_csv command format" in output
        assert "Error: Invalid load_history_from_csv command format" in output

def test_plugin_error_handling():
    inputs = [
        'use_plugin nonexistent command',
        'use_plugin scientific invalid_command',
        'use_plugin',
        'exit'
    ]
    with patch('builtins.input', side_effect=inputs), \
         patch('sys.stdout', new=io.StringIO()) as fake_out:
        main()
        output = fake_out.getvalue()
        assert "Plugin 'nonexistent' not found" in output
        assert "Command 'invalid_command' not found" in output
        assert "Error: Invalid plugin command format" in output
