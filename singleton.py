"""Singleton module implementing logger and history manager."""
import logging
from factory import DataFacade

class SingletonMeta(type):
    """Metaclass that implements the singleton pattern.
    
    Ensures only one instance of a class is created and provides global access to it.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Logger(metaclass=SingletonMeta):
    """Singleton logger class that provides centralized logging functionality.
    
    This class implements a flexible logging system that can use different logging
    strategies while ensuring only one logger instance exists.
    """
    def __init__(self):
        """Initialize logger with default configuration."""
        self.strategy = None
        self.logger = logging.getLogger(__name__)

    def set_strategy(self, strategy):
        """Set the logging strategy to be used.
        
        Args:
            strategy: A logging strategy object that implements the log method.
        """
        self.strategy = strategy

    def log(self, message, level):
        """Log a message with the specified level.
        
        Args:
            message (str): The message to be logged.
            level (str): The logging level (e.g., 'INFO', 'ERROR', 'DEBUG').
        """
        if self.strategy:
            self.strategy.log(message, level)
        else:
            self.logger.log(getattr(logging, level), message)

    def get_logger(self):
        """Return the underlying logger instance.
        
        Returns:
            logging.Logger: The configured logger instance.
        """
        return self.logger

class HistoryManager(metaclass=SingletonMeta):
    """Singleton class for managing calculation history.
    
    Provides functionality to store, retrieve, and manage calculation records
    using a data facade pattern.
    """
    def __init__(self):
        """Initialize HistoryManager with a DataFacade instance."""
        self.facade = DataFacade()

    def add_record(self, operation, num1, num2, result):
        """Add a new calculation record.
        
        Args:
            operation (str): The mathematical operation performed.
            num1 (float): First operand.
            num2 (float): Second operand.
            result (float): Result of the operation.
        """
        self.facade.add_record(operation, num1, num2, result)

    def save_to_csv(self, filename):
        """Save calculation history to a CSV file.
        
        Args:
            filename (str): Path to the CSV file.
            
        Returns:
            bool: True if save was successful, False otherwise.
        """
        return self.facade.save_to_csv(filename)

    def load_from_csv(self, filename):
        """Load calculation history from a CSV file.
        
        Args:
            filename (str): Path to the CSV file.
            
        Returns:
            bool: True if load was successful, False otherwise.
        """
        return self.facade.load_from_csv(filename)

    def view_data(self):
        """Retrieve all calculation records.
        
        Returns:
            list: List of calculation records.
        """
        return self.facade.view_data()

    def clear_data(self):
        """Clear all calculation records.
        
        Returns:
            bool: True if clearing was successful, False otherwise.
        """
        return self.facade.clear_data()

# Create an instance of Logger
logger_instance = Logger()
