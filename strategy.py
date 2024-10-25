"""Strategy module implementing various logging and history strategies."""
import pandas as pd

class HistoryStrategy:
    """Base class for implementing history storage strategies."""
    def save(self, data, filename):
        """Save data to a file using the implemented strategy.
        
        Args:
            data: The data to be saved
            filename (str): Path to the target file
        """
        raise NotImplementedError

    def load(self, filename):
        """Load data from a file using the implemented strategy.
        
        Args:
            filename (str): Path to the source file
            
        Returns:
            The loaded data
        """
        raise NotImplementedError

class CSVHistoryStrategy(HistoryStrategy):
    """Strategy for saving and loading history data in CSV format."""
    def save(self, data, filename):
        """Save data to a CSV file.
        
        Args:
            data (pandas.DataFrame): The data to be saved
            filename (str): Path to the target CSV file
        """
        data.to_csv(filename, index=False)

    def load(self, filename):
        """Load data from a CSV file.
        
        Args:
            filename (str): Path to the source CSV file
            
        Returns:
            pandas.DataFrame: The loaded data
        """
        return pd.read_csv(filename)

class LoggerStrategy:
    """Base class for implementing logging strategies."""
    def log(self, message, level):
        """Log a message with the specified level.
        
        Args:
            message (str): The message to log
            level (str): The logging level
        """
        raise NotImplementedError
    
    def clear_logs(self):
        """Clear all logs."""
        raise NotImplementedError

class FileLoggerStrategy(LoggerStrategy):
    """Strategy for logging messages to a file."""
    def __init__(self, filename):
        """Initialize the file logger.
        
        Args:
            filename (str): Path to the log file
        """
        self.filename = filename

    def log(self, message, level):
        """Log a message to a file with the specified level.
        
        Args:
            message (str): The message to log
            level (str): The logging level
        """
        with open(self.filename, 'a', encoding='utf-8') as file:
            file.write(f"{level}: {message}\n")
            
    def clear_logs(self):
        """Clear the log file."""
        with open(self.filename, 'w', encoding='utf-8') as file:
            pass

class ConsoleLoggerStrategy(LoggerStrategy):
    """Strategy for logging messages to the console."""
    def log(self, message, level):
        """Log a message to the console with the specified level.
        
        Args:
            message (str): The message to log
            level (str): The logging level
        """
        print(f"{level}: {message}")
    
    def clear_logs(self):
        """Clear console logs (no-op for console logging)."""
        raise NotImplementedError

class Logger:
    """Main logger class that uses different logging strategies."""
    def __init__(self):
        """Initialize the logger with no strategy."""
        self.strategy = None

    def set_strategy(self, strategy):
        """Set the logging strategy.
        
        Args:
            strategy (LoggerStrategy): The logging strategy to use
        """
        self.strategy = strategy

    def log(self, message, level):
        """Log a message using the current strategy.
        
        Args:
            message (str): The message to log
            level (str): The logging level
        """
        if self.strategy:
            self.strategy.log(message, level)
        else:
            print(f"{level}: {message}")  # Default console logging
            