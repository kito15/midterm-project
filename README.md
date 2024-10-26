# Video Demonstration: [watch video] https://drive.google.com/file/d/1QD7zsTKO1xI5XxmKG2766rSz0RkTJelz/view?usp=sharing

# Enhanced Calculator with Plugin System

A calculator implementation featuring a modular architecture, command pattern implementation, data persistence, and an extensible plugin system.

## Core Components

### Calculator Application
The core calculator provides basic arithmetic operations through a command-based interface:
```python
# Basic arithmetic operations
add(a, b)      # Addition
subtract(a, b)  # Subtraction
multiply(a, b)  # Multiplication
divide(a, b)    # Division with zero-division protection
```

### Data Management
Data operations are handled through a facade pattern implementation (`DataFacade`):

```python
facade = DataFacade()
facade.add_record("add", 2, 3, 5)
facade.save_to_csv("history.csv")
```

The facade manages:
- Operation recording with timestamps
- CSV import/export functionality
- In-memory data storage using pandas DataFrame
- Data clearing and viewing operations

## Architecture

### Command Pattern Implementation
Operations are encapsulated as command objects, providing a uniform interface for execution:

```python
class Command:
    def execute(self):
        raise NotImplementedError

class AddCommand(Command):
    def __init__(self, facade, num1, num2):
        self.facade = facade
        self.num1 = num1
        self.num2 = num2

    def execute(self):
        self.result = self.num1 + self.num2
        self.facade.add_record('add', self.num1, self.num2, self.result)
        return self.result
```

Benefits:
- Consistent operation interface
- Automatic history recording
- Easy addition of new operations

### Plugin System Architecture
The plugin system provides extensibility through a standardized interface:

```python
class PluginInterface:
    def get_commands(self):
        """Return a dictionary of command names and their functions"""
        raise NotImplementedError

    def get_description(self):
        """Return plugin description"""
        raise NotImplementedError
```

Plugin Manager features:
- Dynamic plugin loading from `plugins` directory
- Command registration and execution
- Plugin listing and information retrieval

### Data Management
The `DataFacade` class implements:

1. Data Storage
```python
self.data = pd.DataFrame(columns=[
    'timestamp', 'operation', 'num1', 'num2', 'result'
])
```

2. Record Management
```python
def add_record(self, operation: str, num1: float, num2: float, result: float):
    new_record = pd.DataFrame({
        'timestamp': [str(pd.Timestamp.now())],
        'operation': [operation],
        'num1': [num1],
        'num2': [num2],
        'result': [result]
    })
    self.data = pd.concat([self.data, new_record], ignore_index=True)
```

### Logging System
Comprehensive logging implementation:

```python
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_FILE = os.getenv('LOG_FILE', None)

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT, filename=LOG_FILE)
```

Features:
- Configurable log levels via environment variables
- File and console logging support
- Structured log format
- Operation tracking and error logging

## Usage

### Basic Operations
```sh
> add 2 3
Result: 5

> multiply 4 5
Result: 20
```

### History Management
```sh
> save_history_to_csv history.csv
> load_history_from_csv history.csv
> view_history
> clear_history
```

### Plugin System
```sh
> menu                    # List available plugins
> use_plugin name command # Execute plugin command
```

## Configuration

### Environment Variables
- `LOG_LEVEL`: Set logging detail level (DEBUG|INFO|WARNING|ERROR)
- `LOG_FILE`: Specify log file path

### Data Storage
Default history structure:
```python
{
    "timestamp": "2024-10-23 20:06:49.299196",
    "operation": "add",
    "num1": 1.0,
    "num2": 2.0,
    "result": 3.0
}
```
### Error Handling: LBYL and EAFP

This calculator application applies both *Look Before You Leap* (LBYL) and *Easier to Ask for Forgiveness than Permission* (EAFP):
- **LBYL**: Checks, such as `if num2 == 0`, prevent errors before they occur.
- **EAFP**: Uses `try-except` to handle unexpected input issues, allowing the program to manage errors gracefully.

```python
try:
    num1 = float(num1)
    num2 = float(num2)
    if operation == 'divide' and num2 == 0:
        raise ValueError("Cannot divide by zero")
    result = execute_operation(operation, num1, num2)
    print(f"Result: {result}")
except ValueError as e:
    print(f"Input Error: {e}")
except Exception as e:
    print(f"Unexpected Error: {e}")
```

## Error Handling

The system implements comprehensive error handling:
- Input validation for numerical operations
- File operation error handling
- Plugin loading and execution error management
- Division by zero protection
- Invalid command detection

## Dependencies
- Python 3.x
- pandas: Data management and CSV operations
- importlib: Dynamic plugin loading
- logging: System-wide logging functionality

## Testing
Created test cases covering:
- Basic arithmetic operations
- Command pattern implementation
- Plugin system functionality
- Data persistence operations
- Error handling scenarios

### Setup and Running Tests

```bash

# Install test dependencies

pip install pytest pytest-cov

# Run all tests

pytest

# Run tests with coverage report

pytest --cov=.

```
