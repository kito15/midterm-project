"""Test module for data facade functionality."""
import os
import pytest
from factory import DataFacade

@pytest.fixture(name='facade')
def fixture_data_facade():
    """Fixture to provide a DataFacade instance with cleared data."""
    facade = DataFacade()
    facade.clear_data()
    return facade

def test_add_record(facade):
    """Test adding a record to the data facade."""
    facade.add_record('add', 2, 3, 5)
    data = facade.view_data()
    assert 'add' in data
    assert '2' in data
    assert '3' in data
    assert '5' in data

def test_save_load_csv(facade, tmp_path):
    """Test saving and loading data from a CSV file."""
    # Add some test data
    facade.add_record('add', 2, 3, 5)
    facade.add_record('multiply', 4, 5, 20)
    # Save to temporary file
    test_file = tmp_path / "test_history.csv"
    result = facade.save_to_csv(str(test_file))
    assert "successfully" in result
    assert os.path.exists(test_file)
    # Clear and reload
    facade.clear_data()
    assert facade.view_data() == "No data available"
    # Load and verify
    result = facade.load_from_csv(str(test_file))
    assert "successfully" in result
    data = facade.view_data()
    assert 'add' in data
    assert 'multiply' in data

def test_clear_data(facade):
    """Test clearing data from the data facade."""
    facade.add_record('add', 2, 3, 5)
    assert "add" in facade.view_data()
    result = facade.clear_data()
    assert "cleared" in result
    assert facade.view_data() == "No data available"

def test_invalid_file_operations(facade):
    """Test invalid file operations."""
    result = facade.load_from_csv("nonexistent.csv")
    assert "Error" in result
    result = facade.save_to_csv("/invalid/path/file.csv")
    assert "Error" in result

def test_empty_data_operations(facade):
    """Test operations on empty data."""
    # Test operations on empty data
    assert facade.view_data() == "No data available"
    # Test saving empty data
    result = facade.save_to_csv("empty.csv")
    assert "successfully" in result
    # Test loading empty file
    facade.clear_data()
    result = facade.load_from_csv("empty.csv")
    assert "successfully" in result

def test_data_validation(facade):
    """Test data validation with invalid data types."""
    # Test with invalid data types
    facade.add_record(None, None, None, None)
    data = facade.view_data()
    assert 'None' in data
    facade.add_record('invalid', 'not_number', 'not_number', 'not_number')
    data = facade.view_data()
    assert 'invalid' in data
    assert 'not_number' in data

def test_concurrent_operations(facade):
    """Test multiple operations in sequence."""
    # Test multiple operations in sequence
    facade.add_record('add', 1, 2, 3)
    facade.add_record('multiply', 2, 3, 6)
    facade.save_to_csv('test1.csv')
    facade.clear_data()
    facade.load_from_csv('test1.csv')
    data = facade.view_data()
    assert 'add' in data
    assert 'multiply' in data
    # Clean up test file
    if os.path.exists('test1.csv'):
        os.remove('test1.csv')

def test_empty_file_operations(facade):
    """Test operations with non-existent files."""
    # Test operations with non-existent files
    result = facade.load_from_csv('nonexistent.csv')
    assert 'Error' in result
    # Test saving to invalid path
    result = facade.save_to_csv('/invalid/path/test.csv')
    assert 'Error' in result

def test_data_operations_with_empty_dataframe(facade):
    """Test data operations with an empty DataFrame."""
    # Test view_data with empty DataFrame
    facade.clear_data()
    assert facade.view_data() == "No data available"
    # Test save_to_csv with empty DataFrame
    result = facade.save_to_csv('empty.csv')
    assert 'successfully' in result
    # Clean up test file
    if os.path.exists('empty.csv'):
        os.remove('empty.csv')

def test_multiple_records(facade):
    """Test adding multiple records and verifying them."""
    # Add multiple records and verify
    operations = [
        ('add', 1, 2, 3),
        ('subtract', 5, 3, 2),
        ('multiply', 4, 5, 20),
        ('divide', 10, 2, 5)
    ]
    for op, num1, num2, result in operations:
        facade.add_record(op, num1, num2, result)
    data = facade.view_data()
    for op, _, _, _ in operations:
        assert op in data
