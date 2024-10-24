import pytest
from plugins.scientific import ScientificCalculator
from calculator import PluginManager

@pytest.fixture
def plugin_manager():
    return PluginManager()

def test_plugin_loading(plugin_manager):
    plugins = plugin_manager.list_plugins()
    assert "scientific" in plugins
    assert "Scientific calculator functions (power, square root, sin, cos)" in plugins

def test_plugin_command_execution(plugin_manager):
    result = plugin_manager.execute_command('scientific', 'power', 2, 3)
    assert result == 8

    result = plugin_manager.execute_command('scientific', 'sqrt', 16)
    assert result == 4

    result = plugin_manager.execute_command('scientific', 'sin', 0)
    assert result == 0

    result = plugin_manager.execute_command('scientific', 'cos', 0)
    assert result == 1

def test_plugin_command_error(plugin_manager):
    result = plugin_manager.execute_command('scientific', 'invalid_command')
    assert "Command 'invalid_command' not found in plugin 'scientific'" in result

    result = plugin_manager.execute_command('nonexistent_plugin', 'power', 2, 3)
    assert "Plugin 'nonexistent_plugin' not found" in result
