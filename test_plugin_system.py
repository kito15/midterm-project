"""Test module for the plugin system of the calculator application."""

import logging
import math
from calculator import PluginManager
from plugins.scientific import ScientificCalculator

def test_plugin_manager_initialization(plugin_manager):
    """Test if plugin manager initializes correctly."""
    assert isinstance(plugin_manager, PluginManager)
    assert hasattr(plugin_manager, 'plugins')

def test_plugin_loading(plugin_manager):
    """Test if plugins are loaded correctly."""
    # Scientific calculator plugin should be loaded
    assert 'scientific' in plugin_manager.plugins
    plugin = plugin_manager.plugins['scientific']
    assert hasattr(plugin, 'get_commands')
    assert hasattr(plugin, 'get_description')

def test_plugin_commands(plugin_manager):
    """Test if plugin commands are available."""
    scientific = plugin_manager.plugins['scientific']
    commands = scientific.get_commands()
    assert 'power' in commands
    assert 'sqrt' in commands
    assert 'sin' in commands
    assert 'cos' in commands

def test_plugin_command_execution(plugin_manager):
    """Test if plugin commands execute correctly."""
    result = plugin_manager.execute_command('scientific', 'power', 2, 3)
    assert result == 8.0

    result = plugin_manager.execute_command('scientific', 'sqrt', 16)
    assert result == 4.0

def test_invalid_plugin_commands(plugin_manager):
    """Test handling of invalid plugin commands."""
    result = plugin_manager.execute_command('nonexistent', 'command', 1)
    assert "not found" in result

    result = plugin_manager.execute_command('scientific', 'invalid', 1)
    assert "not found" in result

def test_plugin_error_handling(plugin_manager):
    """Test error handling in plugin execution."""
    result = plugin_manager.execute_command('scientific', 'sqrt', -1)
    assert "Error" in result

    result = plugin_manager.execute_command('scientific', 'power', 'invalid', 2)
    assert "Error" in result

def test_scientific_trig_functions(plugin_manager):
    """Test trigonometric functions of scientific calculator."""
    # Test sin
    result = plugin_manager.execute_command('scientific', 'sin', 0)
    assert abs(result) < 0.0001  # sin(0) = 0

    # Test cos
    result = plugin_manager.execute_command('scientific', 'cos', 0)
    assert abs(result - 1) < 0.0001  # cos(0) = 1

def test_scientific_error_cases(plugin_manager):
    """Test error cases in scientific calculator functions."""
    # Test invalid input for sin
    result = plugin_manager.execute_command('scientific', 'sin', 'invalid')
    assert "Error" in result

    # Test invalid input for cos
    result = plugin_manager.execute_command('scientific', 'cos', 'invalid')
    assert "Error" in result

def test_plugin_description():
    """Test plugin description functionality."""
    calc = ScientificCalculator()
    desc = calc.get_description()
    assert isinstance(desc, str)
    assert len(desc) > 0

def test_scientific_error_handling():
    """Test error handling in scientific calculator."""
    calc = ScientificCalculator()
    # Test power with invalid inputs
    result = calc.power('invalid', 2)
    assert "Error: Invalid numbers" in result
    result = calc.power(2, 'invalid')
    assert "Error: Invalid numbers" in result
    result = calc.power(None, 2)
    assert "Error" in result
    # Test sqrt with invalid input
    result = calc.sqrt('invalid')
    assert "Error: Invalid number" in result
    result = calc.sqrt(-1)
    assert "Error: Cannot calculate square root of negative number" in result
    result = calc.sqrt(None)
    assert "Error" in result
    # Test trig functions with invalid inputs
    result = calc.sin('invalid')
    assert "Error: Invalid number" in result
    result = calc.sin(None)
    assert "Error" in result
    result = calc.cos('invalid')
    assert "Error: Invalid number" in result
    result = calc.cos(None)
    assert "Error" in result
def test_scientific_edge_cases():
    """Test edge cases in scientific calculator."""
    calc = ScientificCalculator()
    # Test power with zero and one
    assert calc.power(0, 5) == 0.0
    assert calc.power(1, 1000) == 1.0
    assert calc.power(2, 0) == 1.0
    # Test sqrt with zero and one
    assert calc.sqrt(0) == 0.0
    assert calc.sqrt(1) == 1.0
    # Test trig functions with special angles
    assert abs(calc.sin(math.pi)) < 1e-10  # sin(π) ≈ 0
    assert abs(calc.cos(math.pi) + 1) < 1e-10  # cos(π) ≈ -1

def test_plugin_logging(caplog):
    """Test logging functionality of plugins."""
    # Set log level
    caplog.set_level(logging.INFO)
    # Execute operations that generate logs
    calc = ScientificCalculator()
    calc.get_description()
    calc.get_commands()
    calc.power(2, 3)
    calc.sqrt(16)
    calc.sin(0)
    calc.cos(0)
    # Verify log messages were created
    assert len(caplog.records) > 0
    assert any(record.levelname == 'INFO' for record in caplog.records)
