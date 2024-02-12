from __feature__ import snake_case

from typing import Any
from types import ModuleType

import sys
from pathlib import Path
from version_parser import Version

from PySide6.QtCore import Signal, QObject

from pieapp.api.exceptions import PieException
from pieapp.api.globals import Global
from pieapp.api.plugins.plugins import PiePlugin
from pieapp.api.plugins.types import PluginType
from pieapp.helpers.modules import import_by_path
from pieapp.helpers.qt import get_main_window
from pieapp.helpers.logger import logger


class PluginRegistry(QObject):
    """
    Based on SpyderPluginRegistry from the Spyder IDE project
    """
    sig_plugins_ready = Signal()

    def __init__(self) -> None:
        super(PluginRegistry, self).__init__()

        # Just a logger
        self._logger = logger

        # List of PiePlugins that depend on it
        self._plugin_dependents: dict[str, dict[str, list[str]]] = {}

        # List of the PiePlugins that the PiePlugins depends on
        self._plugin_dependencies: dict[str, dict[str, list[str]]] = {}

        # PiePlugin dictionary
        self._plugin_registry: dict[str, PiePlugin] = {}

        # PiePlugins dictionary with availability boolean status
        self._plugin_availability: dict[str, bool] = {}

        # Dictionary with plugin name to its type
        self._plugins_types_registry: dict[PluginType, set[str]] = {k.value: set() for k in PluginType}

    def init_plugins(self) -> None:
        """ Initialize all built-in or third-party PiePlugins, components and user plugins """
        main_window = get_main_window()
        if not main_window:
            raise PieException(f"Can't find an initialized QMainWindow instance")

        # Initialize plugins then
        self._initialize_from_packages(Global.APP_ROOT / Global.PLUGINS_FOLDER, main_window)
        self._initialize_from_packages(Global.USER_ROOT / Global.PLUGINS_FOLDER, main_window)

    def shutdown_plugins(self, *plugins: str, full_house: bool = False) -> None:
        """
        Shutdown managers, services in parent object or all at once

        Args:
            plugins (objects): PiePlugin based classes
            full_house (bool): reload all managers, services from all instances
        """
        plugins = plugins if not full_house else self._plugin_registry.keys()
        for plugin in plugins:
            self._logger.debug(f"Shutting down plugin \"{plugin}\" from {self.__class__.__name__}")
            if plugin in self._plugin_registry:
                self._shutdown_plugin(plugin)

    def reload_plugins(self, *plugins: str, full_house: bool = False) -> None:
        """ Reload listed or all objects and components """
        self.shutdown(*plugins, full_house=full_house)
        for plugin in self._plugin_registry:
            plugin_instance = self._plugin_registry.get(plugin)
            self._initialize_plugin(plugin_instance)

    def delete_plugin(
        self,
        plugin_name: str,
        teardown: bool = False,
        check_can_delete: bool = False
    ) -> bool:
        plugin_instance = self._plugin_registry.get(plugin_name)
        if not plugin_instance:
            return False

        if check_can_delete:
            can_delete = plugin_instance.can_close()
            if not can_delete:
                return False
        
        try:
            plugin_instance.delete_later()
        except RuntimeError:
            pass

        if teardown:
            # Disconnect plugin from other plugins
            self._shutdown_plugin(plugin_name)

            # Disconnect depending on plugins from the plugin to delete
            self._notify_plugin_shutdown(plugin_name)

        try:
            plugin_instance.on_close()
        except Exception:
            pass

        return True

    def get_plugin(self, plugin_name: str) -> Any:
        """ Get PiePlugin instance by its name """
        if plugin_name in self._plugin_registry:
            return self._plugin_registry[plugin_name]

        raise PieException(f"Plugin \"{plugin_name}\" was not found")

    # Prepare methods

    def _initialize_from_packages(self, folder: "Path", parent: "QMainWindow" = None) -> None:
        if not folder.exists():
            self._logger.warning(f"Plugins folder {folder.name} doesn't exist")
            return

        sys.path.insert(0, folder.as_posix())

        for package in folder.iterdir():
            if package.is_dir() and package.name not in ("__pycache__",):
                self._logger.debug(f"Preparing plugin {package.name}")

                # Plugin path: pieapp/plugins/<plugin name>
                plugin_path = folder / package.name

                if (plugin_path / "globals.py").exists():
                    Global.load_by_path(plugin_path / "globals.py")

                # Add our plugin into sys.path
                plugin_package_module = import_by_path(str(plugin_path / "__init__.py"))
                try:
                    self._check_versions(plugin_package_module)
                except AttributeError:
                    self.delete_plugin(package.name)

                # Importing plugin module
                plugin_module = import_by_path(str(plugin_path / "plugin.py"))

                # Initializing plugin instance
                plugin_instance: PiePlugin = getattr(plugin_module, "main")(parent, plugin_path)
                if plugin_instance:
                    self._initialize_plugin(plugin_instance)

    def _check_versions(self, plugin_package: ModuleType) -> None:
        """
        Check application/pieapp, piekit and plugin version
        """
        sys_pieapp_version = Version(Global.PIEAPP_VERSION)
        sys_piekit_version = Version(Global.PIEKIT_VERSION)

        if not plugin_package.version:
            raise AttributeError(f"Plugin {plugin_package.name} must have `version` attribute")

        plugin_pieapp_version = Version(plugin_package.pieapp_version)
        plugin_piekit_version = Version(plugin_package.piekit_version)

        if sys_pieapp_version.get_major_version() != plugin_pieapp_version.get_major_version():
            raise AttributeError(f"Application version ({sys_pieapp_version}) is not compatible with plugin"
                                 f"{plugin_package.name} version ({plugin_package.PIEAPP_VERSION})")

        if sys_piekit_version != plugin_piekit_version:
            raise AttributeError(f"PieKit version ({sys_piekit_version}) is not compatible with plugin"
                                 f"{plugin_package.name} version ({plugin_package.piekit_version})")

    def _initialize_plugin(self, plugin_instance: PiePlugin) -> None:
        self._logger.debug(f"Initializing plugin {plugin_instance.name}")

        self._update_plugin_info(
            plugin_instance.name,
            plugin_instance.requires,
            plugin_instance.optional
        )

        # Hashing PiePlugin instance
        self._plugin_registry[plugin_instance.name] = plugin_instance
        self._plugins_types_registry[plugin_instance.type.value].add(plugin_instance.name)

        if hasattr(plugin_instance, "on_main_window_show"):
            plugin_instance.sig_on_main_window_show.connect(plugin_instance.on_main_window_show)
        if hasattr(plugin_instance, "on_main_window_close"):
            plugin_instance.sig_on_main_window_close.connect(plugin_instance.on_main_window_close)

        plugin_signals = self._get_plugin_signals(plugin_instance)
        for signal_name in plugin_signals:
            signal_instance = getattr(plugin_instance, signal_name)
            signal_instance.connect(lambda: self._notify_plugin_event(
                plugin_instance.name, set(map(lambda v: v.replace("sig_", ""), plugin_signals))
            ))

        plugin_instance.sig_plugin_ready.connect(lambda: (
            self._notify_plugin_dependencies(plugin_instance.name),
            self._notify_plugin_availability(plugin_instance.name)
        ))

        try:
            plugin_instance.prepare()
        except Exception as e:
            print("Error: ", plugin_instance.name, str(e))
            self.delete_plugin(plugin_instance.name)

    def _get_plugin_signals(self, plugin_instance: PiePlugin) -> list[str]:
        """
        Collect signals names that starts with `PLUGINS_SIGNAL_PREFIX (sig_/sig)` prefix
        """
        signals: list[str] = []
        for signal_name in dir(plugin_instance):
            if (
                signal_name.startswith(Global.PLUGINS_SIGNAL_PREFIX)
                and signal_name not in Global.PLUGINS_PRIVATE_SIGNALS
            ):
                signal_instance = getattr(plugin_instance, signal_name, None)
                if isinstance(signal_instance, Signal):
                    signals.append(signal_name)

        return signals

    # Notification methods

    def _notify_plugin_event(self, name: str, signals: set[str] = None) -> None:
        plugin_dependents = self._plugin_dependents.get(name, {})
        required_plugins = plugin_dependents.get("requires", [])
        optional_plugins = plugin_dependents.get("optional", [])

        for plugin in required_plugins + optional_plugins:
            if plugin in self._plugin_registry:
                plugin_instance = self._plugin_registry[plugin]
                for signal in signals:
                    plugin_instance.on_plugin_event(name, signal)

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
        required_plugins = plugin_dependents.get("requires", [])
        optional_plugins = plugin_dependents.get("optional", [])

        for plugin in required_plugins + optional_plugins:
            if plugin in self._plugin_registry:
                plugin_instance = self._plugin_registry[plugin]
                plugin_instance.on_plugin_event(name)

    def _notify_plugin_dependencies(self, name: str) -> None:
        """ Notify PiePlugins dependencies """
        plugin_instance = self._plugin_registry[name]
        plugin_dependencies = self._plugin_dependencies.get(name, {})
        required_plugins = plugin_dependencies.get("requires", [])
        optional_plugins = plugin_dependencies.get("optional", [])

        for plugin in required_plugins + optional_plugins:
            if plugin in self._plugin_registry:
                if self._plugin_availability.get(plugin, False):
                    self._logger.debug(f"Plugin {plugin} has already loaded")
                    plugin_instance.on_plugin_event(plugin)

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

    def _notify_plugin_shutdown(self, plugin_name: str):
        """
        Notify dependents of a plugin that is going to be unavailable.

        Args:
            plugin_name (str): Plugin name
        """
        plugin_dependents = self._plugin_dependents.get(plugin_name, {})
        required_plugins = plugin_dependents.get("requires", [])
        optional_plugins = plugin_dependents.get("optional", [])

        for plugin in required_plugins + optional_plugins:
            if plugin in self._plugin_registry:
                if self._plugin_availability.get(plugin, False):
                    plugin_instance: PiePlugin = self._plugin_registry[plugin]
                    self._logger.debug(
                        f"Notifying {plugin_instance.type.value.capitalize()} "
                        f"that {plugin_name} is going to be turned off"
                    )
                    plugin_instance.on_plugin_event(plugin_name, "plugin_shutdown")

    def _shutdown_plugin(self, plugin_name: str):
        """ Shutdown a plugin from its dependencies """
        plugin_instance: PiePlugin = self._plugin_registry[plugin_name]
        plugin_dependencies = self._plugin_dependencies.get(plugin_name, {})
        required_plugins = plugin_dependencies.get("requires", [])
        optional_plugins = plugin_dependencies.get("optional", [])

        for plugin in required_plugins + optional_plugins:
            if plugin in self._plugin_registry:
                if self._plugin_availability.get(plugin, False):
                    self._logger.debug(f"Shutting down {plugin_name} from {plugin}")
                    plugin_instance.on_plugin_event(plugin, "plugin_shutdown")

    # PluginManager public methods

    def is_plugin_available(self, name: str) -> bool:
        return self._plugin_availability.get(name, False)


Plugins = PluginRegistry()
