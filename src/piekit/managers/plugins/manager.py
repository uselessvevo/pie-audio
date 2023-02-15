from typing import Any
from pathlib import Path

from piekit.mainwindow.main import MainWindow
from piekit.plugins.base import BasePlugin
from piekit.managers.base import BaseManager
from piekit.system.loader import Config
from piekit.utils.modules import import_by_path
from piekit.utils.files import read_json, write_json


class PluginManager(BaseManager):
    """
    This manager is the plugin registry.
    Based on Spyder's `SpyderPluginRegistry`
    """
    name = "plugins"
    dependencies = ("configs", "locales",)

    def __init__(self) -> None:
        super().__init__()

        # List of plugins that depend on it
        self._plugin_dependents: dict[str, dict[str, list[str]]] = {}

        # List of the plugins that the plugin depends on
        self._plugin_dependencies: dict[str, dict[str, list[str]]] = {}

        # BasePlugin dictionary
        self._plugins_registry: dict[str, BasePlugin] = {}

        # BasePlugin dictionary with availability boolean status
        self._plugin_availability: dict[str, bool] = {}

    # BaseManager methods

    def mount(self, parent: "MainWindow" = None) -> None:
        """ Mount all built-in plugins, components and user plugins """
        self._mount_plugins(Config.APP_ROOT / Config.PLUGINS_FOLDER, parent)
        self._mount_plugins(Config.APP_ROOT / Config.COMPONENTS_FOLDER, parent)
        self._mount_plugins(Config.APP_ROOT / Config.CONTAINERS_FOLDER, parent)
        self._mount_plugins(Config.USER_ROOT / Config.USER_PLUGINS_FOLDER, parent)

    def unmount(self, *plugins: str, full_house: bool = False) -> None:
        """ Unmount listed or all plugins and components """
        """
        TODO: Notify all plugins to unmount all dependencies

        Unmount managers, services in parent object or all at once

        Args:
            plugins (objects): BasePlugin based object
            full_house (bool): reload all managers, services from all instances
        """
        plugins = plugins if not full_house else self._plugins_registry.keys()
        for plugin in plugins:
            self._logger.info(f"Unmounting plugin {plugin} from {self.__class__.__name__}")

            if plugin in self._plugins_registry:
                self._unmount_plugin(plugin)
            
    def reload(self, *plugins: str, full_house: bool = False) -> None:
        """ Reload listed or all plugins and components """
        plugins = self._plugins_registry.keys() if full_house else plugins
        for plugin in plugins:
            self._logger.info(f"Reloading plugin {plugin} from {self.__class__.__name__}")

            if plugin in self._plugins_registry:
                self._reload_plugin(plugin)

    def get(self, key) -> Any:
        """ Get plugin instance by its name """
        return self._plugins_registry.get(key)

    # PluginManager protected methods

    def _mount_plugins(self, folder: "Path", parent: MainWindow = None) -> None:
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
                # System.root / System.config.PLUGINS_FOLDER / self.name
                plugin_instance: BasePlugin = getattr(plugin_module, plugin_manifest.get("init"))(parent, plugin_path)

                self._update_plugin_info(
                    plugin_instance.name,
                    plugin_instance.requires,
                    plugin_instance.optional
                )

                # Hashing plugin instance
                self._plugins_registry[plugin_instance.name] = plugin_instance

                plugin_instance.signalPluginReady.connect(
                    lambda: (
                        self._notify_plugin_availability(
                            plugin_instance.name,
                            plugin_instance.requires,
                            plugin_instance.optional,
                        ),
                        self._notify_plugin_availability_on_main(
                            plugin_instance.name
                        )
                    )
                )

                # Initializing plugin
                plugin_instance.prepare()

                self._notify_plugin_dependencies(plugin_instance.name)

    def _notify_plugin_availability(
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

    def _notify_plugin_availability_on_main(self, name: str) -> None:
        plugin_instance = self._plugins_registry.get(name)
        if plugin_instance:
            plugin_instance.parent().signalPluginReady.emit(name)

    def _notify_plugin_dependencies(self, name: str) -> None:
        """ Notify plugin dependencies """
        plugin_instance = self._plugins_registry[name]
        plugin_dependencies = self._plugin_dependencies.get(name, {})
        required_plugins = plugin_dependencies.get("requires", [])
        optional_plugins = plugin_dependencies.get("optional", [])

        for plugin in required_plugins + optional_plugins:
            if plugin in self._plugins_registry:
                if self._plugin_availability.get(plugin, False):
                    self._logger.debug(f"BasePlugin {plugin} has already loaded")
                    plugin_instance.on_plugin_available(plugin)

    def _update_plugin_info(
        self,
        name: str,
        required_plugins: list[str],
        optional_plugins: list[str]
    ) -> None:
        """
        Update the plugin dependencies and dependents
        """
        for plugin in required_plugins:
            self._update_dependencies(name, plugin, "requires")
            self._update_dependents(plugin, name, "requires")

        for plugin in optional_plugins:
            self._update_dependencies(name, plugin, "optional")
            self._update_dependents(plugin, name, "optional")

    def _update_dependents(
        self,
        plugin: str,
        dependent_plugin: str,
        category: str
    ) -> None:
        """
        Add dependent plugin to the plugin's list of dependents

        Args:
            plugin (str): plugin name
            dependent_plugin (str): dependent plugin
            category (str): required or optional category of plugins
        """
        plugin_dependents = self._plugin_dependents.get(plugin, {})
        plugin_strict_dependents = plugin_dependents.get(category, [])
        plugin_strict_dependents.append(dependent_plugin)
        plugin_dependents[category] = plugin_strict_dependents
        self._plugin_dependents[plugin] = plugin_dependents

    def _update_dependencies(
        self,
        plugin: str,
        required_plugin: str,
        category: str
    ) -> None:
        """
        Add required plugin to the plugin's list of dependencies

        Args:
            plugin (str): plugin name
            required_plugin (str): required plugin
            category (str): required or optional category of plugins
        """
        plugin_dependencies = self._plugin_dependencies.get(plugin, {})
        plugin_strict_dependencies = plugin_dependencies.get(category, [])
        plugin_strict_dependencies.append(required_plugin)
        plugin_dependencies[category] = plugin_strict_dependencies
        self._plugin_dependencies[plugin] = plugin_dependencies

    def _notify_plugin_unmount(self, plugin_name: str):
        """Notify dependents of a plugin that is going to be unavailable."""
        plugin_dependents = self._plugin_dependents.get(plugin_name, {})
        required_plugins = plugin_dependents.get("requires", [])
        optional_plugins = plugin_dependents.get("optional", [])

        for plugin in required_plugins + optional_plugins:
            if plugin in self._plugins_registry:
                if self._plugin_availability.get(plugin, False):
                    self._logger.debug(
                        f"Notifying plugin {plugin} that {plugin_name} is going to be turned off"
                    )
                    plugin_instance: BasePlugin = self._plugins_registry[plugin]
                    plugin_instance.on_plugin_unmount(plugin_name)

    def _unmount_plugin(self, plugin_name: str):
        """ Unmount a plugin from its dependencies """
        plugin_instance: BasePlugin = self._plugins_registry[plugin_name]
        plugin_dependencies = self._plugin_dependencies.get(plugin_name, {})
        required_plugins = plugin_dependencies.get("requires", [])
        optional_plugins = plugin_dependencies.get("optional", [])

        for plugin in required_plugins + optional_plugins:
            if plugin in self._plugins_registry:
                if self._plugin_availability.get(plugin, False):
                    self._logger.info(f"Unmounting {plugin_name} from {plugin}")
                    plugin_instance.on_plugin_unmount(plugin)

    # PluginManager public methods

    def is_plugin_available(self, name: str) -> bool:
        return self._plugin_availability.get(name, False)

    isPluginAvailable = is_plugin_available
