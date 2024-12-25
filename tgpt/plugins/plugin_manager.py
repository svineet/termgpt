import os
import importlib.util

PLUGINS = {}

class PluginManager:
    @staticmethod
    def load_plugins():
        plugin_dir = os.path.dirname(__file__)
        for filename in os.listdir(plugin_dir):
            if filename.endswith(".py") and filename != "plugin_manager.py":
                module_name = filename[:-3]
                module_path = os.path.join(plugin_dir, filename)
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, "Plugin"):
                    plugin = module.Plugin()
                    PLUGINS[plugin.tag] = plugin

    @staticmethod
    def get_plugins():
        return PLUGINS
