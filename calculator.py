import os
import logging
import pandas as pd
from datetime import datetime
import json
import sys
import importlib
from command import AddCommand, SubtractCommand, MultiplyCommand, DivideCommand, SaveHistoryCommand, LoadHistoryCommand, ViewHistoryCommand, ClearHistoryCommand
from singleton import logger_instance, HistoryManager
from strategy import CSVHistoryStrategy, FileLoggerStrategy, ConsoleLoggerStrategy

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_FILE = os.getenv('LOG_FILE', None)

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT, filename=LOG_FILE)
logger = logger_instance.get_logger()

# History storage
SAVED_HISTORY = """[{"timestamp": "2024-10-23 20:06:49.299196", "operation": "add", "num1": 1.0, "num2": 2.0, "result": 3.0}, {"timestamp": "2024-10-23 20:06:52.850854", "operation": "add", "num1": 2.0, "num2": 3.0, "result": 5.0}, {"timestamp": "2024-10-23 20:06:56.819044", "operation": "subtract", "num1": 2.0, "num2": 3.0, "result": -1.0}, {"timestamp": "2024-10-23 20:07:00.402757", "operation": "multiply", "num1": 2.0, "num2": 3.0, "result": 6.0}]"""

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
        logger.info("Loading plugins from the plugins directory")
        # Ensure plugins directory exists
        if not os.path.exists('plugins'):
            os.makedirs('plugins')
            with open(os.path.join('plugins', '__init__.py'), 'w') as f:
                pass
            logger.info("Plugins directory created")
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
                    module = importlib.import_module(f'plugins.{module_name}')
                    if hasattr(module, 'plugin_instance'):
                        self.plugins[module_name] = module.plugin_instance
                        logger.info(f"Loaded plugin: {module_name}")
                except Exception as e:
                    logger.error(f"Error loading plugin {module_name}: {str(e)}")

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
            logger.error(f"Plugin '{plugin_name}' not found")
            return f"Plugin '{plugin_name}' not found"

        plugin = self.plugins[plugin_name]
        commands = plugin.get_commands()

        if command not in commands:
            logger.error(f"Command '{command}' not found in plugin '{plugin_name}'")
            return f"Command '{command}' not found in plugin '{plugin_name}'"

        try:
            result = commands[command](*args)
            logger.info(f"Executed command '{command}' in plugin '{plugin_name}' with result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error executing command: {str(e)}")
            return f"Error executing command: {str(e)}"

def main():
    logger.info("Enhanced Calculator REPL with Plugin System started")
    print("Hey there! Welcome to the Enhanced Calculator REPL with Plugin System 🚀")
    print("Here are the commands you can use:")
    print("  Calculations: add, subtract, multiply, divide")
    print("  History: save_history, load_history, view_history, clear_history, delete_history, save_history_to_csv <filename>, load_history_from_csv <filename>")
    print("  Plugins: menu, use_plugin <plugin_name> <command> [args...]")
    print("Format for calculations: operation number1 number2")
    print("Type 'exit' to quit")

    history_manager = HistoryManager()
    plugin_manager = PluginManager()

    while True:
        try:
            user_input = input("> ").strip()
            if not user_input:
                continue
            logger.info(f"User input: {user_input}")

            if user_input == 'exit':
                logger.info("User exited the calculator")
                break

            if user_input == 'menu':
                logger.info("User requested plugin menu")
                print(plugin_manager.list_plugins())
                continue

            if user_input.startswith('use_plugin '):
                parts = user_input.split()
                if len(parts) < 3:
                    logger.warning("Invalid plugin command format")
                    print("Error: Invalid plugin command format. Use: use_plugin <plugin_name> <command> [args...]")
                    continue
                plugin_name = parts[1]
                command = parts[2]
                args = parts[3:]
                logger.info(f"User executed plugin command: {plugin_name} {command} {args}")
                result = plugin_manager.execute_command(plugin_name, command, *args)
                print(f"Result: {result}")
                continue

            if user_input == 'save_history':
                logger.info("User requested to save history")
                command = SaveHistoryCommand(history_manager, 'history.csv')
                print(command.execute())
                continue
            elif user_input == 'load_history':
                logger.info("User requested to load history")
                command = LoadHistoryCommand(history_manager, 'history.csv')
                print(command.execute())
                continue
            elif user_input == 'view_history':
                logger.info("User requested to view history")
                command = ViewHistoryCommand(history_manager)
                print(command.execute())
                continue
            elif user_input == 'clear_history':
                logger.info("User requested to clear history")
                command = ClearHistoryCommand(history_manager)
                print(command.execute())
                continue
            elif user_input == 'delete_history':
                logger.info("User requested to delete history")
                print(history_manager.clear_data())
                continue
            elif user_input.startswith('save_history_to_csv '):
                parts = user_input.split()
                if len(parts) != 2:
                    logger.warning("Invalid save_history_to_csv command format")
                    print("Error: Invalid save_history_to_csv command format. Use: save_history_to_csv <filename>")
                    continue
                filename = parts[1]
                logger.info(f"User requested to save history to CSV: {filename}")
                command = SaveHistoryCommand(history_manager, filename)
                print(command.execute())
                continue
            elif user_input.startswith('load_history_from_csv '):
                parts = user_input.split()
                if len(parts) != 2:
                    logger.warning("Invalid load_history_from_csv command format")
                    print("Error: Invalid load_history_from_csv command format. Use: load_history_from_csv <filename>")
                    continue
                filename = parts[1]
                logger.info(f"User requested to load history from CSV: {filename}")
                command = LoadHistoryCommand(history_manager, filename)
                print(command.execute())
                continue

            if user_input.startswith('use_plugin '):
                parts = user_input.split()
                if len(parts) < 3:
                    logger.warning("Invalid plugin command format")
                    print("Error: Invalid plugin command format. Use: use_plugin <plugin_name> <command> [args...]")
                    continue
                plugin_name = parts[1]
                command = parts[2]
                args = parts[3:]
                try:
                    args = [float(arg) for arg in args]
                    result = plugin_manager.execute_command(plugin_name, command, *args)
                    print(f"Result: {result}")
                except ValueError:
                    result = plugin_manager.execute_command(plugin_name, command, *args)
                    print(f"Result: {result}")
                continue

            parts = user_input.split()
            if len(parts) != 3 or parts[0] not in ['add', 'subtract', 'multiply', 'divide']:
                logger.error("Invalid input format")
                print("Error: Invalid input format. Use: operation number1 number2")
                continue
                
            operation, num1, num2 = parts

            try:
                num1 = float(num1)
                num2 = float(num2)
            except ValueError:
                logger.error("Invalid numbers entered")
                print("Error: Please enter valid numbers")
                continue

            command = None
            if operation == 'add':
                command = AddCommand(history_manager, num1, num2)
            elif operation == 'subtract':
                command = SubtractCommand(history_manager, num1, num2)
            elif operation == 'multiply':
                command = MultiplyCommand(history_manager, num1, num2)
            elif operation == 'divide':
                command = DivideCommand(history_manager, num1, num2)
            else:
                logger.error("Invalid operation")
                print("Error: Invalid operation. Use add, subtract, multiply, or divide")
                continue

            result = command.execute()
            logger.info(f"User executed {operation} command with result: {result}")
            print(f"Result: {result}")

        except Exception as e:
            logger.error(f"Error: {str(e)}")
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
