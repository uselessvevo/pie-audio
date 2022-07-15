import sys
from typing import Any

from cloudykit.abstracts.manager import IManager
from cloudykit.system.manager import System
from cloudykit.utils.files import read_json
from cloudykit.utils.modules import import_by_path
from cloudykit.utils.logger import DummyLogger


class PluginsManager(IManager):
    """
    Plugin manager is the registry of all app plugins
    """
    name = 'plugins'

    def __init__(self):
        self.logger = DummyLogger('PluginsManager')
        self._plugins_instances = dict()

    def mount(self, parent=None) -> None:
        plugins = (System.root / 'plugins')
        for plugin in plugins.iterdir():
            if plugin.is_dir() and plugin.name not in ('__pycache__',):
                parent.logger.log(f'Mounting plugin "{plugin.name}"')
                plugin_path = System.root / f'plugins/{plugin.name}'
                plugin_manifest = read_json(str(plugin_path / 'manifest.json'))
                plugin_inst = import_by_path('plugin', str(plugin_path / 'plugin/plugin.py'))
                sys.modules[plugin_manifest.get('init')] = plugin_inst
                plugin_inst = getattr(plugin_inst, plugin_manifest.get('init'))(parent)
                plugin_inst.mount()
                self._plugins_instances[plugin_inst.name] = plugin_inst

    def unmount(self, parent=None) -> None:
        if parent:
            parent.unmount()

        else:
            for plugin in self._plugins_instances.values():
                self.logger.log()
                plugin.unmount()

    def reload(self, plugin: str) -> None:
        plugins = self._plugins_instances.get(plugin, self._plugins_instances)
        for name, plugin in plugins.items():
            plugin.reload()

    def get(self, key, default: Any) -> Any:
        self._plugins_instances.get(key)
