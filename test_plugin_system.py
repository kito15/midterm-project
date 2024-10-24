import pytest
from calculator import PluginManager
import os
import sys

def test_plugin_manager_initialization(plugin_manager):
    assert isinstance(plugin_manager, PluginManager)
    assert hasattr(plugin_manager, 'plugins')

def test_plugin_loading(plugin_manager):
    # Scientific calculator plugin should be loaded
    assert 'scientific' in plugin_manager.plugins
    plugin = plugin_manager.plugins['scientific']
    assert hasattr(plugin, 'get_commands')
    assert hasattr(plugin, 'get_description')

def test_plugin_commands(plugin_manager):
    scientific = plugin_manager.plugins['scientific']
    commands = scientific.get_commands()
    assert 'power' in commands
    assert 'sqrt' in commands
    assert 'sin' in commands
    assert 'cos' in commands

def test_plugin_command_execution(plugin_manager):
    result = plugin_manager.execute_command('scientific', 'power', 2, 3)
    assert result == 8.0

    result = plugin_manager.execute_command('scientific', 'sqrt', 16)
    assert result == 4.0

def test_invalid_plugin_commands(plugin_manager):
    result = plugin_manager.execute_command('nonexistent', 'command', 1)
    assert "not found" in result

    result = plugin_manager.execute_command('scientific', 'invalid', 1)
    assert "not found" in result

def test_plugin_error_handling(plugin_manager):
    result = plugin_manager.execute_command('scientific', 'sqrt', -1)
    assert "Error" in result

    result = plugin_manager.execute_command('scientific', 'power', 'invalid', 2)
    assert "Error" in result

def test_scientific_trig_functions(plugin_manager):
    # Test sin
    result = plugin_manager.execute_command('scientific', 'sin', 0)
    assert abs(result) < 0.0001  # sin(0) = 0

    # Test cos
    result = plugin_manager.execute_command('scientific', 'cos', 0)
    assert abs(result - 1) < 0.0001  # cos(0) = 1

def test_scientific_error_cases(plugin_manager):
    # Test invalid input for sin
    result = plugin_manager.execute_command('scientific', 'sin', 'invalid')
    assert "Error" in result

    # Test invalid input for cos
    result = plugin_manager.execute_command('scientific', 'cos', 'invalid')
    assert "Error" in result

def test_plugin_description():
    from plugins.scientific import ScientificCalculator
    calc = ScientificCalculator()
    desc = calc.get_description()
    assert isinstance(desc, str)
    assert len(desc) > 0

def test_scientific_error_handling():
    from plugins.scientific import ScientificCalculator
    calc = ScientificCalculator()
    
    # Test power with invalid inputs
    result = calc.power('invalid', 2)
    assert "Error" in result
    result = calc.power(2, 'invalid')
    assert "Error" in result
    
    # Test sqrt with invalid input
    result = calc.sqrt('invalid')
    assert "Error" in result
    result = calc.sqrt(-1)
    assert "Error" in result
    
    # Test trig functions with invalid inputs
    result = calc.sin('invalid')
    assert "Error" in result
    result = calc.cos('invalid')
    assert "Error" in result

def test_plugin_logging():
    import logging
    from plugins.scientific import ScientificCalculator
    
    # Capture log messages
    with self.assertLogs(level='INFO') as logs:
        calc = ScientificCalculator()
        calc.get_description()
        calc.get_commands()
        calc.power(2, 3)
        calc.sqrt(16)
        calc.sin(0)
        calc.cos(0)
    
    # Verify log messages were created
    assert len(logs.output) > 0
    assert any('INFO' in msg for msg in logs.output)
