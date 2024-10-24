import pandas as pd
import logging

# Configure logging
logger = logging.getLogger(__name__)

class DataFacade:
    def __init__(self):
        self.data = pd.DataFrame(columns=['timestamp', 'operation', 'num1', 'num2', 'result'])

    def add_record(self, operation, num1, num2, result):
        new_record = pd.DataFrame({
            'timestamp': [str(pd.Timestamp.now())],
            'operation': [operation],
            'num1': [num1],
            'num2': [num2],
            'result': [result]
        })
        self.data = pd.concat([self.data, new_record], ignore_index=True)
        logger.info(f"Added record to data: {operation} {num1} {num2} = {result}")

    def save_to_csv(self, filename):
        try:
            self.data.to_csv(filename, index=False)
            logger.info(f"Data saved to {filename} successfully")
            return f"Data saved to {filename} successfully"
        except Exception as e:
            logger.error(f"Error saving data to {filename}: {str(e)}")
            return f"Error saving data to {filename}: {str(e)}"

    def load_from_csv(self, filename):
        try:
            self.data = pd.read_csv(filename)
            logger.info(f"Data loaded from {filename} successfully")
            return f"Data loaded from {filename} successfully"
        except Exception as e:
            logger.error(f"Error loading data from {filename}: {str(e)}")
            return f"Error loading data from {filename}: {str(e)}"

    def view_data(self):
        if len(self.data) == 0:
            logger.info("No data available")
            return "No data available"
        logger.info("Viewing data")
        return str(self.data)

    def clear_data(self):
        self.data = pd.DataFrame(columns=['timestamp', 'operation', 'num1', 'num2', 'result'])
        logger.info("Data cleared from memory")
        return "Data cleared from memory"
