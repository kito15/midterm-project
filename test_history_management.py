import pytest
import os
import pandas as pd
from command import SaveHistoryCommand, LoadHistoryCommand, ViewHistoryCommand, ClearHistoryCommand

def test_save_history_command(sample_history_data, test_csv_file):
    cmd = SaveHistoryCommand(sample_history_data, test_csv_file)
    result = cmd.execute()
    assert "successfully" in result
    assert os.path.exists(test_csv_file)

def test_load_history_command(sample_history_data, test_csv_file):
    # First save some data
    SaveHistoryCommand(sample_history_data, test_csv_file).execute()
    
    # Clear and reload
    sample_history_data.clear_data()
    cmd = LoadHistoryCommand(sample_history_data, test_csv_file)
    result = cmd.execute()
    assert "successfully" in result
    
    # Verify data
    data = sample_history_data.view_data()
    assert "add" in data
    assert "multiply" in data

def test_view_history_command(sample_history_data):
    cmd = ViewHistoryCommand(sample_history_data)
    result = cmd.execute()
    assert "add" in result
    assert "multiply" in result

def test_clear_history_command(sample_history_data):
    cmd = ClearHistoryCommand(sample_history_data)
    result = cmd.execute()
    assert "cleared" in result
    assert sample_history_data.view_data() == "No data available"

def test_invalid_file_operations(history_manager):
    cmd = LoadHistoryCommand(history_manager, "nonexistent.csv")
    result = cmd.execute()
    assert "Error" in result

    cmd = SaveHistoryCommand(history_manager, "/invalid/path/file.csv")
    result = cmd.execute()
    assert "Error" in result
