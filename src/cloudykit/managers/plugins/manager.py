import sys
from typing import Any

from cloudykit.abstracts.manager import IManager
from cloudykit.system.manager import System
from cloudykit.utils.files import read_json
from cloudykit.utils.modules import import_by_path
from cloudykit.utils.logger import DummyLogger


logger = DummyLogger('PluginsManager')


class PluginsManager(IManager):
    """
    Plugin manager is the registry of all app plugins
    """
    name = 'plugins'

    def __init__(self):
        self._plugins_instances = dict()

    def mount(self, parent=None) -> None:
        plugins = (System.root / 'plugins')
        for plugin in plugins.iterdir():
            if plugin.is_dir() and plugin.name not in ('__pycache__',):
                logger.log(f'Mounting plugin "{plugin.name}" in {self.__class__.__name__}')

                # Reading data from plugin/manifest.json
                plugin_path = System.root / f'plugins/{plugin.name}'
                plugin_manifest = read_json(str(plugin_path / 'manifest.json'))

                # Importing needed plugin and manually putting it in `sys.modules`
                plugin_inst = import_by_path('plugin', str(plugin_path / 'plugin/plugin.py'))
                sys.modules[plugin_manifest.get('init')] = plugin_inst

                # Initializing class
                plugin_inst = getattr(plugin_inst, plugin_manifest.get('init'))(parent)
                plugin_inst.mount()

                # Hashing plugin instance
                self._plugins_instances[plugin_inst.name] = plugin_inst

    def unmount(self, parent=None, full_house=False) -> None:
        """
        Unmount managers, services in parent object or all at once
        Args:
            parent (object): parent object, f.e: `Plugin`
            full_house (bool): reload all managers, services from all instances
        """
        if parent:
            parent.unmount()
        else:
            for plugin in self._plugins_instances.values():
                logger.log(f'Unmounting {parent.name} from {self.__class__.__name__}')
                plugin.unmount()

    def reload(self, plugin: str) -> None:
        plugins = self._plugins_instances.get(plugin, self._plugins_instances)
        for name, plugin in plugins.items():
            plugin.reload()

    def get(self, key, default: Any) -> Any:
        return self._plugins_instances.get(key)
