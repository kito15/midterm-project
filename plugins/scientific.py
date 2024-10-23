import math

class ScientificCalculator:
    def get_description(self):
        return "Scientific calculator functions (power, square root, sin, cos)"
    
    def get_commands(self):
        return {
            'power': self.power,
            'sqrt': self.sqrt,
            'sin': self.sin,
            'cos': self.cos
        }
    
    def power(self, base, exponent):
        try:
            return float(base) ** float(exponent)
        except ValueError:
            return "Error: Invalid numbers"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def sqrt(self, number):
        try:
            num = float(number)
            if num < 0:
                return "Error: Cannot calculate square root of negative number"
            return math.sqrt(num)
        except ValueError:
            return "Error: Invalid number"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def sin(self, angle):
        try:
            return math.sin(float(angle))
        except ValueError:
            return "Error: Invalid number"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def cos(self, angle):
        try:
            return math.cos(float(angle))
        except ValueError:
            return "Error: Invalid number"
        except Exception as e:
            return f"Error: {str(e)}"

# Create plugin instance
plugin_instance = ScientificCalculator()
