"""Test module for logging system functionality."""
import os
import pytest
from singleton import Logger
from strategy import FileLoggerStrategy, ConsoleLoggerStrategy

def test_logger_singleton():
    logger1 = Logger()
    logger2 = Logger()
    assert logger1 is logger2

def test_file_logger_strategy():
    test_log_file = "test.log"
    strategy = FileLoggerStrategy(test_log_file)
    logger = Logger()
    logger.set_strategy(strategy)
    
    test_message = "Test log message"
    logger.log(test_message, "INFO")
    
    assert os.path.exists(test_log_file)
    with open(test_log_file, 'r') as f:
        content = f.read()
        assert test_message in content
    
    # Cleanup
    os.remove(test_log_file)

def test_console_logger_strategy(capsys):
    strategy = ConsoleLoggerStrategy()
    logger = Logger()
    logger.set_strategy(strategy)
    
    test_message = "Test console message"
    logger.log(test_message, "INFO")
    
    captured = capsys.readouterr()
    assert test_message in captured.out
