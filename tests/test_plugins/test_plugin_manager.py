import unittest
from tgpt.plugins.plugin_manager import PluginManager

class TestPluginManager(unittest.TestCase):
    def test_load_plugins(self):
        PluginManager.load_plugins()
        plugins = PluginManager.get_plugins()
        self.assertIn("@web", plugins)
        self.assertIn("@example", plugins)
