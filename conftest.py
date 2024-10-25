"""Test fixtures module for the calculator application."""

import os
import pytest
from calculator import PluginManager, HistoryManager
from factory import DataFacade

@pytest.fixture
def plugin_manager():
    """Create and return a clean PluginManager instance for testing.
    
    Returns:
        PluginManager: A new instance of the plugin manager.
    """
    return PluginManager()

@pytest.fixture
def history_manager():
    """Create and return a clean HistoryManager instance for testing.
    
    Returns:
        HistoryManager: A new instance of the history manager with cleared data.
    """
    manager = HistoryManager()
    manager.clear_data()  # Ensure clean state
    return manager

@pytest.fixture
def data_facade():
    """Create and return a clean DataFacade instance for testing.
    
    Returns:
        DataFacade: A new instance of the data facade with cleared data.
    """
    facade = DataFacade()
    facade.clear_data()  # Ensure clean state
    return facade

@pytest.fixture
def test_csv_file():
    """Create a temporary CSV file for testing and clean it up afterwards.
    
    Yields:
        str: The name of the temporary CSV file.
    """
    filename = "test_history.csv"
    yield filename
    # Cleanup after test
    if os.path.exists(filename):
        os.remove(filename)

@pytest.fixture
def sample_history_data():
    """Create a HistoryManager instance with sample test data.
    
    Returns:
        HistoryManager: A history manager instance populated with sample records.
    """
    test_manager = HistoryManager()
    test_manager.add_record('add', 2, 3, 5)
    test_manager.add_record('multiply', 4, 5, 20)
    return test_manager
