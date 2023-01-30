from typing import Any

from cloudykit.system.types import PathConfig
from cloudykit.utils.files import read_json, write_json
from cloudykit.utils.modules import import_by_path

from cloudykit.system.manager import System
from cloudykit.managers.base import BaseManager
from cloudykit.appwindow.main import AppWindow


class PluginsManager(BaseManager):
    """
    Plugin manager is the registry of all app plugins
    """
    name = "plugins"
    dependencies = ("configs", "locales",)  # "components"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._dictionary: dict = {}

    def mount(self, parent: AppWindow = None) -> None:
        self._mount_plugins(System.root / System.config.PLUGINS_FOLDER, parent)
        self._mount_plugins(System.user_root / System.config.USER_PLUGINS_FOLDER, parent)

    def _mount_plugins(self, folder: "Path", parent: "AppWindow" = None) -> None:
        if not folder.exists():
            folder.mkdir()

        if not (folder / "manifest.json").exists():
            write_json(str(folder / "manifest.json"), [])

        for plugin in folder.iterdir():
            if plugin.is_dir() and plugin.name not in ("__pycache__",) and parent:
                self._logger.info(f"Mounting plugin `{plugin.name}` in `{parent.__class__.__name__}`")

                # Reading data from `plugin/manifest.json`
                plugin_path = folder / plugin.name
                plugin_manifest = read_json(str(plugin_path / "manifest.json"))

                # Importing plugin module
                plugin_module = import_by_path("plugin", str(plugin_path / "plugin/plugin.py"))

                # Creating plugin instance
                plugin_instance = getattr(plugin_module, plugin_manifest.get("init"))(parent)

                # Load locales, configs and components for our plugin
                System.registry.configs.mount(PathConfig(plugin_path, section=plugin_instance.name))
                System.registry.locales.mount(PathConfig(plugin_path, section=plugin_instance.name))

                # System.registry.components.mount()
                # System.registry.assets.mount()

                # Initializing plugin
                plugin_instance.init()

                # Hashing plugin instance
                self._dictionary[plugin_instance.name] = plugin_instance

    def unmount(self, *plugins: "BasePlugin", full_house: bool = False) -> None:
        """
        Unmount managers, services in parent object or all at once
        Args:
            plugin (object): BasePlugin based object
            full_house (bool): reload all managers, services from all instances
        """
        plugins = plugins if not full_house else self._dictionary.values()
        for plugin in plugins:
            self._logger.info(f"Unmounting {plugin.name} from {self.__class__.__name__}")

            if plugin:
                System.registry.configs.delete(plugin.name)
                System.registry.locales.delete(plugin.name)
                plugin.unmount()

    def reload(self, *plugins: tuple[str], full_house: bool = False) -> None:
        plugins = self._dictionary.keys() if full_house else plugins
        for plugin in plugins:
            self._dictionary.get(plugin)

    def get(self, key, default: Any = None) -> Any:
        return self._dictionary.get(key)
