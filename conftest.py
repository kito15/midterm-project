import pytest
import os
import pandas as pd
from calculator import PluginManager, HistoryManager
from singleton import Logger
from factory import DataFacade

@pytest.fixture
def plugin_manager():
    return PluginManager()

@pytest.fixture
def history_manager():
    manager = HistoryManager()
    manager.clear_data()  # Ensure clean state
    return manager

@pytest.fixture
def data_facade():
    facade = DataFacade()
    facade.clear_data()  # Ensure clean state
    return facade

@pytest.fixture
def test_csv_file():
    filename = "test_history.csv"
    yield filename
    # Cleanup after test
    if os.path.exists(filename):
        os.remove(filename)

@pytest.fixture
def sample_history_data(history_manager):
    history_manager.add_record('add', 2, 3, 5)
    history_manager.add_record('multiply', 4, 5, 20)
    return history_manager
