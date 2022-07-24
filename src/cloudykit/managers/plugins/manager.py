import sys
from typing import Any, Tuple

from cloudykit.abstracts.manager import IManager
from cloudykit.managers.system.manager import System
from cloudykit.utils.files import read_json
from cloudykit.utils.modules import import_by_path
from cloudykit.utils.logger import DummyLogger


logger = DummyLogger('PluginsManager')


class PluginsManager(IManager):
    """
    Plugin manager is the registry of all app plugins
    """
    name = 'plugins'

    def __init__(self, parent=None):
        self._parent = parent
        self._plugins_instances = dict()

    def mount(self) -> None:
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
                plugin_inst = getattr(plugin_inst, plugin_manifest.get('init'))(self._parent)
                plugin_inst.mount()

                # Hashing plugin instance
                self._plugins_instances[plugin_inst.name] = plugin_inst

    def unmount(self, plugin: "Plugin" = None, full_house: bool = False) -> None:
        """
        Unmount managers, services in parent object or all at once
        Args:
            plugin (object):
            full_house (bool): reload all managers, services from all instances
        """
        if plugin and full_house:
            raise RuntimeError('Can\'t use `plugin` and `full_house` together')

        if plugin:
            plugin.unmount()
        elif full_house:
            for plugin in self._plugins_instances.values():
                logger.log(f'Unmounting {plugin.name} from {self.__class__.__name__}')
                plugin.unmount()

    def reload(self, *plugins: Tuple[str], full_house: bool = False) -> None:
        plugins = self._plugins_instances.keys() if full_house else plugins
        for plugin in plugins:
            self._plugins_instances.get(plugin)

    def get(self, key, default: Any) -> Any:
        return self._plugins_instances.get(key)
