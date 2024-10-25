"""Facade module for data management operations.

This module provides a facade pattern implementation for managing operational data,
including storage, retrieval, and manipulation of numerical operations data.
"""
import logging
from typing import Optional

import pandas as pd

# Configure logging
logger = logging.getLogger(__name__)

class DataFacade:
    """Manages data operations including storage, retrieval, and manipulation of numerical operations.
    
    Provides methods for adding records, saving/loading from CSV files, viewing data,
    and clearing stored data. Uses pandas DataFrame for data storage.
    """

    def __init__(self):
        """Initialize DataFacade with empty DataFrame with predefined columns."""
        self.data = pd.DataFrame(columns=['timestamp', 'operation', 'num1', 'num2', 'result'])

    def add_record(self, operation: str, num1: float, num2: float, result: float) -> None:
        """Add a new operation record to the data store.

        Args:
            operation: The mathematical operation performed
            num1: First number in the operation
            num2: Second number in the operation
            result: Result of the operation
        """
        new_record = pd.DataFrame({
            'timestamp': [str(pd.Timestamp.now())],
            'operation': [operation],
            'num1': [num1],
            'num2': [num2],
            'result': [result]
        })
        self.data = pd.concat([self.data, new_record], ignore_index=True)
        logger.info("Added record to data: %(op)s %(n1)s %(n2)s = %(res)s",
                   {'op': operation, 'n1': num1, 'n2': num2, 'res': result})

    def save_to_csv(self, filename: str) -> str:
        """Save current data to a CSV file.

        Args:
            filename: Path to the output CSV file

        Returns:
            Status message indicating success or failure
        """
        try:
            self.data.to_csv(filename, index=False)
            logger.info("Data saved to %s successfully", filename)
            return f"Data saved to {filename} successfully"
        except (IOError, PermissionError) as e:
            logger.error("Error saving data to %(filename)s: %(error)s",
                        {'filename': filename, 'error': str(e)})
            return f"Error saving data to {filename}: {str(e)}"

    def load_from_csv(self, filename: str) -> str:
        """Load data from a CSV file.

        Args:
            filename: Path to the input CSV file

        Returns:
            Status message indicating success or failure
        """
        try:
            self.data = pd.read_csv(filename)
            logger.info("Data loaded from %s successfully", filename)
            return f"Data loaded from {filename} successfully"
        except (IOError, FileNotFoundError) as e:
            logger.error("Error loading data from %(filename)s: %(error)s",
                        {'filename': filename, 'error': str(e)})
            return f"Error loading data from {filename}: {str(e)}"

    def view_data(self) -> str:
        """Return string representation of current data.

        Returns:
            String representation of the data or status message if empty
        """
        if len(self.data) == 0:
            logger.info("No data available")
            return "No data available"
        logger.info("Viewing data")
        return str(self.data)

    def clear_data(self) -> str:
        """Clear all data from memory.

        Returns:
            Confirmation message
        """
        self.data = pd.DataFrame(columns=['timestamp', 'operation', 'num1', 'num2', 'result'])
        logger.info("Data cleared from memory")
        return "Data cleared from memory"
    