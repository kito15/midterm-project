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

def main():
    print("Simple Calculator REPL")
    print("Available commands: add, subtract, multiply, divide")
    print("Format: operation number1 number2")
    print("Type 'exit' to quit")
    
    while True:
        try:
            # Get user input
            user_input = input("> ").strip().lower()
            
            # Check for exit command
            if user_input == 'exit':
                break
            
            # Parse input
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
            
            # Print result
            print(f"Result: {result}")
            
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
