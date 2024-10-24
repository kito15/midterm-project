import math
import logging

# Configure logging
logger = logging.getLogger(__name__)

class ScientificCalculator:
    def get_description(self):
        logger.info("Getting description for ScientificCalculator")
        return "Scientific calculator functions (power, square root, sin, cos)"
    
    def get_commands(self):
        logger.info("Getting commands for ScientificCalculator")
        return {
            'power': self.power,
            'sqrt': self.sqrt,
            'sin': self.sin,
            'cos': self.cos
        }
    
    def power(self, base, exponent):
        logger.info(f"Executing power command with base: {base}, exponent: {exponent}")
        try:
            return float(base) ** float(exponent)
        except ValueError:
            logger.error("Invalid numbers for power command")
            return "Error: Invalid numbers"
        except Exception as e:
            logger.error(f"Error executing power command: {str(e)}")
            return f"Error: {str(e)}"
    
    def sqrt(self, number):
        logger.info(f"Executing sqrt command with number: {number}")
        try:
            num = float(number)
            if num < 0:
                logger.error("Cannot calculate square root of negative number")
                return "Error: Cannot calculate square root of negative number"
            return math.sqrt(num)
        except ValueError:
            logger.error("Invalid number for sqrt command")
            return "Error: Invalid number"
        except Exception as e:
            logger.error(f"Error executing sqrt command: {str(e)}")
            return f"Error: {str(e)}"
    
    def sin(self, angle):
        logger.info(f"Executing sin command with angle: {angle}")
        try:
            return math.sin(float(angle))
        except ValueError:
            logger.error("Invalid number for sin command")
            return "Error: Invalid number"
        except Exception as e:
            logger.error(f"Error executing sin command: {str(e)}")
            return f"Error: {str(e)}"
    
    def cos(self, angle):
        logger.info(f"Executing cos command with angle: {angle}")
        try:
            return math.cos(float(angle))
        except ValueError:
            logger.error("Invalid number for cos command")
            return "Error: Invalid number"
        except Exception as e:
            logger.error(f"Error executing cos command: {str(e)}")
            return f"Error: {str(e)}"

# Create plugin instance
plugin_instance = ScientificCalculator()
