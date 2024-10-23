import pandas as pd
from datetime import datetime
import json

# History will be stored as a string constant in this file
SAVED_HISTORY = """[{"timestamp": "2024-10-23 19:40:30.826108", "operation": "add", "num1": 1.0, "num2": 2.0, "result": 3.0}, {"timestamp": "2024-10-23 19:40:36.441549", "operation": "subtract", "num1": 2.0, "num2": 3.0, "result": -1.0}, {"timestamp": "2024-10-23 19:40:40.522081", "operation": "multiply", "num1": 2.0, "num2": 5.0, "result": 10.0}, {"timestamp": "2024-10-23 19:40:45.505288", "operation": "divide", "num1": 2.0, "num2": 0.0, "result": "Error: Division by zero"}]"""  # This will be updated when saving history

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: Division by zero"
    return a / b

class CalculatorHistory:
    def __init__(self):
        self.history = pd.DataFrame(columns=['timestamp', 'operation', 'num1', 'num2', 'result'])
        
    def add_record(self, operation, num1, num2, result):
        new_record = pd.DataFrame({
            'timestamp': [str(datetime.now())],
            'operation': [operation],
            'num1': [num1],
            'num2': [num2],
            'result': [result]
        })
        self.history = pd.concat([self.history, new_record], ignore_index=True)
    
    def save_history(self):
        try:
            # Convert the history to a list of dictionaries
            history_data = self.history.to_dict('records')
            # Read the current file content
            with open(__file__, 'r') as file:
                content = file.read()
            
            # Find the SAVED_HISTORY line and replace it
            new_history = json.dumps(history_data)
            new_content = content.replace(
                'SAVED_HISTORY = """[{"timestamp": "2024-10-23 19:40:30.826108", "operation": "add", "num1": 1.0, "num2": 2.0, "result": 3.0}, {"timestamp": "2024-10-23 19:40:36.441549", "operation": "subtract", "num1": 2.0, "num2": 3.0, "result": -1.0}, {"timestamp": "2024-10-23 19:40:40.522081", "operation": "multiply", "num1": 2.0, "num2": 5.0, "result": 10.0}, {"timestamp": "2024-10-23 19:40:45.505288", "operation": "divide", "num1": 2.0, "num2": 0.0, "result": "Error: Division by zero"}]"""',
                f'SAVED_HISTORY = """{new_history}"""'
            ).replace(
                f'SAVED_HISTORY = """{SAVED_HISTORY}"""',
                f'SAVED_HISTORY = """{new_history}"""'
            )
            
            # Write the updated content back to the file
            with open(__file__, 'w') as file:
                file.write(new_content)
            return "History saved successfully"
        except Exception as e:
            return f"Error saving history: {str(e)}"
    
    def load_history(self):
        try:
            # Load history from the SAVED_HISTORY constant
            history_data = json.loads(SAVED_HISTORY)
            if history_data:
                self.history = pd.DataFrame(history_data)
                return "History loaded successfully"
            return "No saved history found"
        except Exception as e:
            return f"Error loading history: {str(e)}"
    
    def view_history(self):
        if len(self.history) == 0:
            return "No calculations in history"
        return str(self.history)
    
    def clear_history(self):
        self.history = pd.DataFrame(columns=['timestamp', 'operation', 'num1', 'num2', 'result'])
        return "History cleared from memory"
    
    def delete_history(self):
        try:
            # Read the current file content
            with open(__file__, 'r') as file:
                content = file.read()
            
            # Reset the SAVED_HISTORY to empty
            new_content = content.replace(
                f'SAVED_HISTORY = """{SAVED_HISTORY}"""',
                'SAVED_HISTORY = """[{"timestamp": "2024-10-23 19:40:30.826108", "operation": "add", "num1": 1.0, "num2": 2.0, "result": 3.0}, {"timestamp": "2024-10-23 19:40:36.441549", "operation": "subtract", "num1": 2.0, "num2": 3.0, "result": -1.0}, {"timestamp": "2024-10-23 19:40:40.522081", "operation": "multiply", "num1": 2.0, "num2": 5.0, "result": 10.0}, {"timestamp": "2024-10-23 19:40:45.505288", "operation": "divide", "num1": 2.0, "num2": 0.0, "result": "Error: Division by zero"}]"""'
            )
            
            # Write the updated content back to the file
            with open(__file__, 'w') as file:
                file.write(new_content)
            
            self.clear_history()
            return "History deleted successfully"
        except Exception as e:
            return f"Error deleting history: {str(e)}"

def main():
    print("Enhanced Calculator REPL with History Management")
    print("Available commands:")
    print("  Calculations: add, subtract, multiply, divide")
    print("  History: save_history, load_history, view_history, clear_history, delete_history")
    print("Format for calculations: operation number1 number2")
    print("Type 'exit' to quit")
    
    history_manager = CalculatorHistory()
    
    while True:
        try:
            # Get user input
            user_input = input("> ").strip().lower()
            
            # Check for exit command
            if user_input == 'exit':
                break
            
            # Handle history commands
            if user_input == 'save_history':
                print(history_manager.save_history())
                continue
            elif user_input == 'load_history':
                print(history_manager.load_history())
                continue
            elif user_input == 'view_history':
                print(history_manager.view_history())
                continue
            elif user_input == 'clear_history':
                print(history_manager.clear_history())
                continue
            elif user_input == 'delete_history':
                print(history_manager.delete_history())
                continue
            
            # Parse input for calculations
            parts = user_input.split()
            if len(parts) != 3:
                print("Error: Invalid input format. Please use: operation number1 number2")
                continue
            
            operation, num1, num2 = parts
            
            # Convert numbers
            try:
                num1 = float(num1)
                num2 = float(num2)
            except ValueError:
                print("Error: Please enter valid numbers")
                continue
            
            # Process operation
            result = None
            if operation == 'add':
                result = add(num1, num2)
            elif operation == 'subtract':
                result = subtract(num1, num2)
            elif operation == 'multiply':
                result = multiply(num1, num2)
            elif operation == 'divide':
                result = divide(num1, num2)
            else:
                print("Error: Invalid operation. Use add, subtract, multiply, or divide")
                continue
            
            # Add to history and print result
            history_manager.add_record(operation, num1, num2, result)
            print(f"Result: {result}")
            
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
