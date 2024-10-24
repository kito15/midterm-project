import pytest
from factory import DataFacade
import pandas as pd
import os

@pytest.fixture
def data_facade():
    facade = DataFacade()
    facade.clear_data()
    return facade

def test_add_record(data_facade):
    data_facade.add_record('add', 2, 3, 5)
    data = data_facade.view_data()
    assert 'add' in data
    assert '2' in data
    assert '3' in data
    assert '5' in data

def test_save_load_csv(data_facade, tmp_path):
    # Add some test data
    data_facade.add_record('add', 2, 3, 5)
    data_facade.add_record('multiply', 4, 5, 20)
    
    # Save to temporary file
    test_file = tmp_path / "test_history.csv"
    result = data_facade.save_to_csv(str(test_file))
    assert "successfully" in result
    assert os.path.exists(test_file)
    
    # Clear and reload
    data_facade.clear_data()
    assert data_facade.view_data() == "No data available"
    
    # Load and verify
    result = data_facade.load_from_csv(str(test_file))
    assert "successfully" in result
    data = data_facade.view_data()
    assert 'add' in data
    assert 'multiply' in data

def test_clear_data(data_facade):
    data_facade.add_record('add', 2, 3, 5)
    assert "add" in data_facade.view_data()
    
    result = data_facade.clear_data()
    assert "cleared" in result
    assert data_facade.view_data() == "No data available"

def test_invalid_file_operations(data_facade):
    result = data_facade.load_from_csv("nonexistent.csv")
    assert "Error" in result

    result = data_facade.save_to_csv("/invalid/path/file.csv")
    assert "Error" in result