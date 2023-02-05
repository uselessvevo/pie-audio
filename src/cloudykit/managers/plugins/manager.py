from pathlib import Path
from typing import Any

from PyQt5.QtCore import pyqtSignal

from cloudykit.plugins.base import BasePlugin
from cloudykit.utils.modules import import_by_path
from cloudykit.utils.files import read_json, write_json

from cloudykit.system import System
from cloudykit.managers.base import BaseManager


class PluginsManager(BaseManager):
    """
    This manager is the plugin registry.
    Based on Spyder's `SpyderPluginRegistry`
    """
    name = "plugins"
    dependencies = ("configs", "locales",)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # List of plugins that depend on it
        self._plugin_dependents: dict[str, dict[str, list[str]]] = {}

        # List of the plugins that the plugin depends on
        self._plugin_dependencies: dict[str, dict[str, list[str]]] = {}

        # Plugin dictionary
        self._plugins_registry: dict[str, BasePlugin] = {}

        # Plugin dictionary with availability boolean status
        self._plugin_availability: dict[str, bool] = {}

    def mount(self, parent: "MainWindow" = None) -> None:
        self._mount_plugins(System.root / System.config.PLUGINS_FOLDER, parent)
        self._mount_plugins(System.user_root / System.config.USER_PLUGINS_FOLDER, parent)

    def unmount(self, *plugins: "BasePlugin", full_house: bool = False) -> None:
        """
        Unmount managers, services in parent object or all at once
        Args:
            plugins (objects): BasePlugin based object
            full_house (bool): reload all managers, services from all instances
        """
        plugins = plugins if not full_house else self._plugins_registry.values()
        for plugin in plugins:
            self._logger.info(f"Unmounting plugin {plugin.name} from {self.__class__.__name__}")

            if plugin:
                plugin.unmount()

    def _mount_plugins(self, folder: "Path", parent: "MainWindow" = None) -> None:
        if not folder.exists():
            folder.mkdir()

        if not (folder / "manifest.json").exists():
            write_json(str(folder / "manifest.json"), [])

        plugins_loading_order = System.config.PLUGINS_LOADING_ORDER
        plugins_folders = (
            i.name for i in list(folder.iterdir())
            if not i.is_file()
            and i.is_dir()
            and i.name not in ("__pycache__", "__init__.py")
        )

        ordered_folders = (i for _, i in sorted(zip(plugins_folders, plugins_loading_order)))
        ordered_folders = (Path(folder, i) for i in ordered_folders)

        for plugin in ordered_folders:
            if plugin.is_dir() and plugin.name not in ("__pycache__",) and parent:
                self._logger.info(f"Mounting plugin `{plugin.name}` in `{parent.__class__.__name__}`")

                # Reading data from `plugin/manifest.json`
                plugin_path = folder / plugin.name
                plugin_manifest = read_json(str(plugin_path / "manifest.json"))

                # Importing plugin module
                plugin_module = import_by_path("plugin", str(plugin_path / "plugin/plugin.py"))

                # Creating plugin instance
                # System.root / System.config.PLUGINS_FOLDER / self.name
                plugin_instance = getattr(plugin_module, plugin_manifest.get("init"))(parent, plugin_path)

                self.update_plugin_info(
                    plugin_instance.name, 
                    plugin_instance.requires, 
                    plugin_instance.optional
                )

                # Hashing plugin instance
                self._plugins_registry[plugin_instance.name] = plugin_instance

                plugin_instance.signalPluginReady.connect(
                    lambda: self.notify_plugin_availability(
                        plugin_instance.name,
                        plugin_instance.requires,
                        plugin_instance.optional,
                    )
                )

                self.notify_plugin_dependencies(plugin_instance.name)

                # Initializing plugin
                plugin_instance.init()

    def notify_plugin_availability(
        self,
        name: str,
        requires: list[str] = None,
        optional: list[str] = None,
    ) -> None:
        """
        Notify dependent plugins that our plugin is available

        Args:
            name (str): plugin name
            requires (list[str]): list of required plugins
            optional (list[str]): list of optional plugins
        """
        requires = requires or []
        optional = optional or []

        self._plugin_availability[name] = True

        for plugin in requires + optional:
            if plugin in self._plugins_registry:
                plugin_instance = self._plugins_registry[plugin]
                plugin_instance.on_plugin_available(name)
                
    def notify_plugin_dependencies(self, name: str) -> None:
        plugin_instance = self._plugins_registry[name]
        plugin_dependencies = self._plugin_dependencies.get(name, {})
        required_plugins = plugin_dependencies.get("requires", [])
        optional_plugins = plugin_dependencies.get("optional", [])

        for plugin in required_plugins + optional_plugins:
            if plugin in self._plugins_registry:
                if self._plugin_availability.get(plugin, False):
                    self._logger.debug(f"Plugin {plugin} has already loaded")
                    plugin_instance.on_plugin_available(plugin)
                    
    def update_plugin_info(
        self, 
        name: str, 
        required_plugins: list[str], 
        optional_plugins: list[str]
    ) -> None:
        """Update the dependencies and dependents of `plugin_name`."""
        for plugin in required_plugins:
            self.update_dependencies(name, plugin, "requires")
            self.update_dependents(plugin, name, "requires")

        for plugin in optional_plugins:
            self.update_dependencies(name, plugin, "optional")
            self.update_dependents(plugin, name, "optional")

    def update_dependents(self, plugin: str, dependent_plugin: str, key: str) -> None:
        """ Add `dependent_plugin` to the list of dependents of `plugin` """
        plugin_dependents = self._plugin_dependents.get(plugin, {})
        plugin_strict_dependents = plugin_dependents.get(key, [])
        plugin_strict_dependents.append(dependent_plugin)
        plugin_dependents[key] = plugin_strict_dependents
        self._plugin_dependents[plugin] = plugin_dependents

    def update_dependencies(self, plugin: str, required_plugin: str, key: str) -> None:
        """ Add `required_plugin` to the list of dependencies of `plugin` """
        plugin_dependencies = self._plugin_dependencies.get(plugin, {})
        plugin_strict_dependencies = plugin_dependencies.get(key, [])
        plugin_strict_dependencies.append(required_plugin)
        plugin_dependencies[key] = plugin_strict_dependencies
        self._plugin_dependencies[plugin] = plugin_dependencies

    def is_plugin_available(self, name: str) -> bool:
        return self._plugin_availability.get(name, False)

    def reload(self, *plugins: tuple[str], full_house: bool = False) -> None:
        plugins = self._plugins_registry.keys() if full_house else plugins
        for plugin in plugins:
            self._plugins_registry.get(plugin)

    def get(self, key, default: Any = None) -> Any:
        return self._plugins_registry.get(key)
