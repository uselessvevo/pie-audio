import os
import sys
from typing import Any
from pathlib import Path

from piekit.managers.registry import Managers
from piekit.utils.modules import import_by_path
from piekit.mainwindow.main import MainWindow

from piekit.config import Config
from piekit.plugins.plugins import PiePlugin
from piekit.managers.base import BaseManager
from piekit.managers.structs import SysManagers


class PluginManager(BaseManager):
    """
    This manager is the PiePlugins registry.
    Based on SpyderPluginRegistry from the Spyder IDE project
    """
    name = SysManagers.Plugins
    dependencies = (SysManagers.Configs, SysManagers.Locales)

    def __init__(self) -> None:
        super().__init__()

        # List of PiePlugins that depend on it
        self._plugin_dependents: dict[str, dict[str, list[str]]] = {}

        # List of the PiePlugins that the PiePlugins depends on
        self._plugin_dependencies: dict[str, dict[str, list[str]]] = {}

        # PiePlugin dictionary
        self._plugins_registry: dict[str, PiePlugin] = {}

        # PiePlugins dictionary with availability boolean status
        self._plugin_availability: dict[str, bool] = {}

    # BaseManager methods

    def init(self, parent: "MainWindow" = None) -> None:
        """ Initialize all built-in or site PiePlugins, components and user plugins """
        self._initialize_from_packages(Config.APP_ROOT / Config.CONTAINERS_FOLDER, parent)
        self._initialize_from_packages(Config.APP_ROOT / Config.PLUGINS_FOLDER, parent)
        self._initialize_from_packages(Config.USER_ROOT / Config.USER_PLUGINS_FOLDER, parent)

    def shutdown(self, *plugins: str, full_house: bool = False) -> None:
        """
        Shutdown managers, services in parent object or all at once

        Args:
            plugins (objects): PiePlugin based classes
            full_house (bool): reload all managers, services from all instances
        """
        plugins = plugins if not full_house else self._plugins_registry.keys()
        for plugin in plugins:
            self._logger.info(f"Shutting down {plugin} from {self.__class__.__name__}")

            if plugin in self._plugins_registry:
                self._shutdown_plugin(plugin)

        # List of PiePlugins that depend on it
        self._plugin_dependents: dict[str, dict[str, list[str]]] = {}

        # List of the PiePlugins that the PiePlugins depends on
        self._plugin_dependencies: dict[str, dict[str, list[str]]] = {}

        # PiePlugin dictionary
        self._plugins_registry: dict[str, PiePlugin] = {}

        # PiePlugins dictionary with availability boolean status
        self._plugin_availability: dict[str, bool] = {}

    def reload(self, *plugins: str, full_house: bool = False) -> None:
        """ Reload listed or all objects and components """
        self.shutdown(*plugins, full_house=full_house)
        for plugin in self._plugins_registry:
            plugin_instance = self._plugins_registry.get(plugin)
            self._initialize_plugin(plugin_instance)

    def get(self, key) -> Any:
        """ Get PiePlugin instance by its name """
        return self._plugins_registry.get(key)

    # PluginManager protected methods

    def _initialize_from_packages(self, folder: "Path", parent: MainWindow = None) -> None:
        if not folder.exists():
            folder.mkdir()

        for package in folder.iterdir():
            if package.is_dir() and package.name not in ("__pycache__",) and parent:
                self._logger.info(f"Reading package data from {package.name}")

                # Plugin path: pieapp/plugins/<plugin name>
                plugin_path = folder / package.name

                # Add our plugin into sys.path
                sys.path.append(os.path.abspath(str(plugin_path)))

                # Importing plugin module
                plugin_module = import_by_path("plugin", str(plugin_path / "plugin/plugin.py"))
                if (plugin_path / "plugin/config.py").exists():
                    config_module = import_by_path("config", str(plugin_path / "plugin/config.py"))
                    Config.load_module(config_module)

                # Initializing plugin instance
                plugin_instance: PiePlugin = getattr(plugin_module, "main")(parent, plugin_path)

                self._initialize_plugin(plugin_instance)

    def _initialize_plugin(self, plugin_instance: PiePlugin) -> None:
        self._logger.info(f"Preparing {plugin_instance.type} {plugin_instance.name}")

        self._update_plugin_info(
            plugin_instance.name,
            plugin_instance.requires,
            plugin_instance.optional
        )

        # Hashing PiePlugin instance
        self._plugins_registry[plugin_instance.name] = plugin_instance

        plugin_instance.signalPluginReady.connect(
            lambda: (
                self._notify_plugin_availability(plugin_instance.name),
                self._notify_plugin_availability_on_main(plugin_instance.name)
            )
        )

        # Preparing `PiePlugin` instance
        plugin_instance.prepare()

        # PiePlugin is ready
        plugin_instance.signalPluginReady.emit()

        self._notify_plugin_dependencies(plugin_instance.name)

        # Inform about that
        self._logger.info(f"{plugin_instance.type.capitalize()} {plugin_instance.name} is ready!")

    def _notify_plugin_availability(
        self,
        name: str,
    ) -> None:
        """
        Notify dependent PiePlugins that our PiePlugin is available

        Args:
            name (str): PiePlugin name
        """
        self._plugin_availability[name] = True

        # Notify plugin dependents
        plugin_dependents = self._plugin_dependents.get(name, {})
        required_plugins = plugin_dependents.get('requires', [])
        optional_plugins = plugin_dependents.get('optional', [])

        for plugin in required_plugins + optional_plugins:
            if plugin in self._plugins_registry:
                plugin_instance = self._plugins_registry[plugin]
                plugin_instance.on_plugin_available(name)

    def _notify_plugin_availability_on_main(self, name: str) -> None:
        plugin_instance = self._plugins_registry.get(name)
        if plugin_instance:
            plugin_instance.parent().signalPluginReady.emit(name)

    def _notify_plugin_dependencies(self, name: str) -> None:
        """ Notify PiePlugins dependencies """
        plugin_instance = self._plugins_registry[name]
        plugin_dependencies = self._plugin_dependencies.get(name, {})
        required_plugins = plugin_dependencies.get("requires", [])
        optional_plugins = plugin_dependencies.get("optional", [])

        for plugin in required_plugins + optional_plugins:
            if plugin in self._plugins_registry:
                if self._plugin_availability.get(plugin, False):
                    self._logger.debug(f"{plugin_instance.type.capitalize()} {plugin} has already loaded")
                    plugin_instance.on_plugin_available(plugin)

    def _update_plugin_info(
        self,
        name: str,
        required_plugins: list[str],
        optional_plugins: list[str]
    ) -> None:
        """
        Update the PiePlugin dependencies and dependents
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
            plugin (str): object name
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

    def _notify_plugin_shutting_down(self, plugin_name: str):
        """Notify dependents of a plugin that is going to be unavailable."""
        plugin_dependents = self._plugin_dependents.get(plugin_name, {})
        required_plugins = plugin_dependents.get("requires", [])
        optional_plugins = plugin_dependents.get("optional", [])

        for plugin in required_plugins + optional_plugins:
            if plugin in self._plugins_registry:
                if self._plugin_availability.get(plugin, False):
                    plugin_instance: PiePlugin = self._plugins_registry[plugin]
                    self._logger.debug(
                        f"Notifying {plugin_instance.type.capitalize()} "
                        f"that {plugin_name} is going to be turned off"
                    )
                    plugin_instance.on_plugin_shutdown(plugin_name)

    def _shutdown_plugin(self, plugin_name: str):
        """ Shutdown a plugin from its dependencies """
        plugin_instance: PiePlugin = self._plugins_registry[plugin_name]
        plugin_dependencies = self._plugin_dependencies.get(plugin_name, {})
        required_plugins = plugin_dependencies.get("requires", [])
        optional_plugins = plugin_dependencies.get("optional", [])

        for plugin in required_plugins + optional_plugins:
            if plugin in self._plugins_registry:
                if self._plugin_availability.get(plugin, False):
                    self._logger.info(f"Shutting down {plugin_name} from {plugin}")
                    plugin_instance.on_plugin_shutdown(plugin)

    # PluginManager public methods

    def is_plugin_available(self, name: str) -> bool:
        return self._plugin_availability.get(name, False)

    isPluginAvailable = is_plugin_available
