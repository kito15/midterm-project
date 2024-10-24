import pytest
import pandas as pd
from calculator import add, subtract, multiply, divide, HistoryManager, logger_instance, main, PluginManager  # Import PluginManager
from unittest.mock import patch
from io import StringIO
import sys
import logging  # Import logging module

@pytest.fixture
def history_manager():
    return HistoryManager()

@pytest.fixture
def plugin_manager():
    return PluginManager()

def test_addition():
    result = add(1, 2)
    assert result == 3

def test_subtraction():
    result = subtract(5, 3)
    assert result == 2

def test_multiplication():
    result = multiply(4, 3)
    assert result == 12

def test_division():
    result = divide(10, 2)
    assert result == 5

def test_division_by_zero():
    result = divide(10, 0)
    assert result == "Error: Division by zero"

def test_history_saving(history_manager):
    history_manager.add_record('add', 1, 2, 3)
    history_manager.add_record('subtract', 5, 3, 2)
    history_manager.save_to_csv('test_history.csv')
    df = pd.read_csv('test_history.csv')
    assert len(df) == 2
    assert df.iloc[0]['operation'] == 'add'
    assert df.iloc[0]['num1'] == 1
    assert df.iloc[0]['num2'] == 2
    assert df.iloc[0]['result'] == 3
    assert df.iloc[1]['operation'] == 'subtract'
    assert df.iloc[1]['num1'] == 5
    assert df.iloc[1]['num2'] == 3
    assert df.iloc[1]['result'] == 2

def test_history_loading(history_manager):
    history_manager.add_record('add', 1, 2, 3)
    history_manager.add_record('subtract', 5, 3, 2)
    history_manager.save_to_csv('test_history.csv')
    history_manager.clear_data()
    history_manager.load_from_csv('test_history.csv')
    df = history_manager.view_data()
    assert len(df) == 2
    assert df.iloc[0]['operation'] == 'add'
    assert df.iloc[0]['num1'] == 1
    assert df.iloc[0]['num2'] == 2
    assert df.iloc[0]['result'] == 3
    assert df.iloc[1]['operation'] == 'subtract'
    assert df.iloc[1]['num1'] == 5
    assert df.iloc[1]['num2'] == 3
    assert df.iloc[1]['result'] == 2

def test_history_viewing(history_manager):
    history_manager.add_record('add', 1, 2, 3)
    history_manager.add_record('subtract', 5, 3, 2)
    result = history_manager.view_data()
    assert "add" in result
    assert "subtract" in result
    assert "1" in result
    assert "2" in result
    assert "3" in result
    assert "5" in result

def test_history_clearing(history_manager):
    history_manager.add_record('add', 1, 2, 3)
    history_manager.add_record('subtract', 5, 3, 2)
    history_manager.clear_data()
    df = history_manager.view_data()
    assert len(df) == 0

def test_repl_addition(capsys):
    user_input = "add 1 2\nexit\n"
    expected_output = "Result: 3.0\n"
    with patch('builtins.input', side_effect=user_input.splitlines()):
        main()
        captured = capsys.readouterr()
        assert expected_output in captured.out

def test_repl_subtraction(capsys):
    user_input = "subtract 5 3\nexit\n"
    expected_output = "Result: 2.0\n"
    with patch('builtins.input', side_effect=user_input.splitlines()):
        main()
        captured = capsys.readouterr()
        assert expected_output in captured.out

def test_repl_multiplication(capsys):
    user_input = "multiply 4 3\nexit\n"
    expected_output = "Result: 12.0\n"
    with patch('builtins.input', side_effect=user_input.split()):
        main()
        captured = capsys.readouterr()
        assert expected_output in captured.out

def test_repl_division(capsys):
    user_input = "divide 10 2\nexit\n"
    expected_output = "Result: 5.0\n"
    with patch('builtins.input', side_effect=user_input.split()):
        main()
        captured = capsys.readouterr()
        assert expected_output in captured.out

def test_repl_division_by_zero(capsys):
    user_input = "divide 10 0\nexit\n"
    expected_output = "Result: Error: Division by zero\n"
    with patch('builtins.input', side_effect=user_input.split()):
        main()
        captured = capsys.readouterr()
        assert expected_output in captured.out

def test_repl_save_history(capsys):
    user_input = "add 1 2\nsave_history\nexit\n"
    expected_output = "Data saved to history.csv successfully\n"
    with patch('builtins.input', side_effect=user_input.split()):
        main()
        captured = capsys.readouterr()
        assert expected_output in captured.out

def test_repl_load_history(capsys):
    user_input = "add 1 2\nsave_history\nload_history\nexit\n"
    expected_output = "Data loaded from history.csv successfully\n"
    with patch('builtins.input', side_effect=user_input.split()):
        main()
        captured = capsys.readouterr()
        assert expected_output in captured.out

def test_repl_view_history(capsys):
    user_input = "add 1 2\nview_history\nexit\n"
    expected_output = "timestamp,operation,num1,num2,result\n"
    with patch('builtins.input', side_effect=user_input.split()):
        main()
        captured = capsys.readouterr()
        assert expected_output in captured.out

def test_repl_clear_history(capsys):
    user_input = "add 1 2\nclear_history\nview_history\nexit\n"
    expected_output = "No data available\n"
    with patch('builtins.input', side_effect=user_input.split()):
        main()
        captured = capsys.readouterr()
        assert expected_output in captured.out

def test_repl_delete_history(capsys):
    user_input = "add 1 2\ndelete_history\nview_history\nexit\n"
    expected_output = "No data available\n"
    with patch('builtins.input', side_effect=user_input.split()):
        main()
        captured = capsys.readouterr()
        assert expected_output in captured.out

def test_repl_save_history_to_csv(capsys):
    user_input = "add 1 2\nsave_history_to_csv test_history.csv\nexit\n"
    expected_output = "Data saved to test_history.csv successfully\n"
    with patch('builtins.input', side_effect=user_input.split()):
        main()
        captured = capsys.readouterr()
        assert expected_output in captured.out

def test_repl_load_history_from_csv(capsys):
    user_input = "add 1 2\nsave_history_to_csv test_history.csv\nload_history_from_csv test_history.csv\nexit\n"
    expected_output = "Data loaded from test_history.csv successfully\n"
    with patch('builtins.input', side_effect=user_input.split()):
        main()
        captured = capsys.readouterr()
        assert expected_output in captured.out

def test_repl_use_plugin_power(capsys):
    user_input = "use_plugin scientific power 2 3\nexit\n"
    expected_output = "Result: 8.0\n"
    with patch('builtins.input', side_effect=user_input.split()):
        main()
        captured = capsys.readouterr()
        assert expected_output in captured.out

def test_repl_use_plugin_sqrt(capsys):
    user_input = "use_plugin scientific sqrt 16\nexit\n"
    expected_output = "Result: 4.0\n"
    with patch('builtins.input', side_effect=user_input.split()):
        main()
        captured = capsys.readouterr()
        assert expected_output in captured.out

def test_repl_use_plugin_sin(capsys):
    user_input = "use_plugin scientific sin 0\nexit\n"
    expected_output = "Result: 0.0\n"
    with patch('builtins.input', side_effect=user_input.split()):
        main()
        captured = capsys.readouterr()
        assert expected_output in captured.out

def test_repl_use_plugin_cos(capsys):
    user_input = "use_plugin scientific cos 0\nexit\n"
    expected_output = "Result: 1.0\n"
    with patch('builtins.input', side_effect=user_input.split()):
        main()
        captured = capsys.readouterr()
        assert expected_output in captured.out

def test_repl_use_plugin_invalid_command(capsys):
    user_input = "use_plugin scientific invalid_command\nexit\n"
    expected_output = "Command 'invalid_command' not found in plugin 'scientific'\n"
    with patch('builtins.input', side_effect=user_input.split()):
        main()
        captured = capsys.readouterr()
        assert expected_output in captured.out

def test_repl_use_nonexistent_plugin(capsys):
    user_input = "use_plugin nonexistent_plugin power 2 3\nexit\n"
    expected_output = "Plugin 'nonexistent_plugin' not found\n"
    with patch('builtins.input', side_effect=user_input.split()):
        main()
        captured = capsys.readouterr()
        assert expected_output in captured.out
