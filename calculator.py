import pandas as pd
from datetime import datetime
import json
import os
import sys
import importlib

# History storage
SAVED_HISTORY = """[{"timestamp": "2024-10-23 19:52:04.822577", "operation": "multiply", "num1": 4.0, "num2": 5.0, "result": 20.0}, {"timestamp": "2024-10-23 19:52:09.014594", "operation": "add", "num1": 2.0, "num2": 3.0, "result": 5.0}]"""

class PluginInterface:
    """Base interface that all calculator plugins must implement"""
    def get_commands(self):
        """Return a dictionary of command names and their functions"""
        raise NotImplementedError
    
    def get_description(self):
        """Return plugin description"""
        raise NotImplementedError

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

class PluginManager:
    def __init__(self):
        self.plugins = {}
        self.load_plugins()

    def load_plugins(self):
        """Load all plugins from the plugins directory"""
        # Ensure plugins directory exists
        if not os.path.exists('plugins'):
            os.makedirs('plugins')
            with open(os.path.join('plugins', '__init__.py'), 'w') as f:
                pass
            return

        # Add plugins directory to Python path
        plugins_dir = os.path.abspath('plugins')
        if plugins_dir not in sys.path:
            sys.path.insert(0, plugins_dir)

        # Load each plugin
        for file in os.listdir('plugins'):
            if file.endswith('.py') and file != '__init__.py':
                module_name = file[:-3]
                try:
                    module = importlib.import_module(module_name)
                    if hasattr(module, 'plugin_instance'):
                        self.plugins[module_name] = module.plugin_instance
                        print(f"Loaded plugin: {module_name}")
                except Exception as e:
                    print(f"Error loading plugin {module_name}: {str(e)}")

    def list_plugins(self):
        """List all available plugins and their commands"""
        if not self.plugins:
            return "No plugins available"
        
        output = "Available Plugins:\n"
        for name, plugin in self.plugins.items():
            output += f"\n{name}:\n"
            output += f"  Description: {plugin.get_description()}\n"
            output += "  Commands:\n"
            for cmd in plugin.get_commands().keys():
                output += f"    - {cmd}\n"
        return output

    def execute_command(self, plugin_name, command, *args):
        """Execute a plugin command"""
        if plugin_name not in self.plugins:
            return f"Plugin '{plugin_name}' not found"
        
        plugin = self.plugins[plugin_name]
        commands = plugin.get_commands()
        
        if command not in commands:
            return f"Command '{command}' not found in plugin '{plugin_name}'"
        
        try:
            return commands[command](*args)
        except Exception as e:
            return f"Error executing command: {str(e)}"

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
            history_data = self.history.to_dict('records')
            with open(__file__, 'r') as file:
                content = file.read()
            new_history = json.dumps(history_data)
            new_content = content.replace(
                'SAVED_HISTORY = """[{"timestamp": "2024-10-23 19:52:04.822577", "operation": "multiply", "num1": 4.0, "num2": 5.0, "result": 20.0}, {"timestamp": "2024-10-23 19:52:09.014594", "operation": "add", "num1": 2.0, "num2": 3.0, "result": 5.0}]"""',
                f'SAVED_HISTORY = """{new_history}"""'
            ).replace(
                f'SAVED_HISTORY = """{SAVED_HISTORY}"""',
                f'SAVED_HISTORY = """{new_history}"""'
            )
            with open(__file__, 'w') as file:
                file.write(new_content)
            return "History saved successfully"
        except Exception as e:
            return f"Error saving history: {str(e)}"
    
    def load_history(self):
        try:
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
            with open(__file__, 'r') as file:
                content = file.read()
            new_content = content.replace(
                f'SAVED_HISTORY = """{SAVED_HISTORY}"""',
                'SAVED_HISTORY = """[{"timestamp": "2024-10-23 19:52:04.822577", "operation": "multiply", "num1": 4.0, "num2": 5.0, "result": 20.0}, {"timestamp": "2024-10-23 19:52:09.014594", "operation": "add", "num1": 2.0, "num2": 3.0, "result": 5.0}]"""'
            )
            with open(__file__, 'w') as file:
                file.write(new_content)
            self.clear_history()
            return "History deleted successfully"
        except Exception as e:
            return f"Error deleting history: {str(e)}"

def main():
    print("Enhanced Calculator REPL with Plugin System")
    print("Available commands:")
    print("  Calculations: add, subtract, multiply, divide")
    print("  History: save_history, load_history, view_history, clear_history, delete_history")
    print("  Plugins: menu, use_plugin <plugin_name> <command> [args...]")
    print("Format for calculations: operation number1 number2")
    print("Type 'exit' to quit")
    
    history_manager = CalculatorHistory()
    plugin_manager = PluginManager()
    
    while True:
        try:
            user_input = input("> ").strip().lower()
            
            if user_input == 'exit':
                break
            
            if user_input == 'menu':
                print(plugin_manager.list_plugins())
                continue
            
            if user_input.startswith('use_plugin '):
                parts = user_input.split()
                if len(parts) < 3:
                    print("Error: Invalid plugin command format. Use: use_plugin <plugin_name> <command> [args...]")
                    continue
                plugin_name = parts[1]
                command = parts[2]
                args = parts[3:]
                result = plugin_manager.execute_command(plugin_name, command, *args)
                print(f"Result: {result}")
                continue
            
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
            
            parts = user_input.split()
            if len(parts) != 3:
                print("Error: Invalid input format. Please use: operation number1 number2")
                continue
            
            operation, num1, num2 = parts
            
            try:
                num1 = float(num1)
                num2 = float(num2)
            except ValueError:
                print("Error: Please enter valid numbers")
                continue
            
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
            
            history_manager.add_record(operation, num1, num2, result)
            print(f"Result: {result}")
            
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
