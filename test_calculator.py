import pytest
from calculator import add, subtract, multiply, divide, HistoryManager, logger_instance, main

@pytest.fixture
def history_manager():
    return HistoryManager()

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
