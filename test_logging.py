import pytest
from singleton import logger_instance
import logging

@pytest.fixture
def logger():
    return logger_instance.get_logger()

def test_logger_info(logger, caplog):
    with caplog.at_level(logging.INFO):
        logger.info("This is an info message")
        assert "This is an info message" in caplog.text

def test_logger_error(logger, caplog):
    with caplog.at_level(logging.ERROR):
        logger.error("This is an error message")
        assert "This is an error message" in caplog.text

def test_logger_debug(logger, caplog):
    with caplog.at_level(logging.DEBUG):
        logger.debug("This is a debug message")
        assert "This is a debug message" in caplog.text
