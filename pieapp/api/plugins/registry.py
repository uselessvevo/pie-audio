from __feature__ import snake_case

from types import ModuleType

import sys
from pathlib import Path
from version_parser import Version

from PySide6.QtCore import Signal, QObject

from pieapp.api.exceptions import PieError
from pieapp.api.globals import Global
from pieapp.api.models.plugins import SysPlugin
from pieapp.api.plugins.plugins import PiePlugin
from pieapp.api.plugins.types import PluginType
from pieapp.api.utils.modules import import_by_path
from pieapp.api.utils.qt import get_main_window
from pieapp.api.utils.logger import logger


class PluginRegistryClass(QObject):
    """
    Based on SpyderPluginRegistry from the Spyder IDE project
    """
    plugins_ready = Signal()
    plugins_teardown = Signal()

    def __init__(self) -> None:
        super(PluginRegistryClass, self).__init__()

        # MainWindow reference
        self._main_window: "QMainWindow" = None

        # List of PiePlugins that depend on it
        self._plugin_dependents: dict[str, dict[str, list[str]]] = {}

        # List of the PiePlugins that the PiePlugins depends on
        self._plugin_dependencies: dict[str, dict[str, list[str]]] = {}

        # PiePlugin dictionary
        self._plugin_registry: dict[str, PiePlugin] = {}

        # PiePlugins dictionary with availability boolean status
        self._plugin_availability: dict[str, bool] = {}

        self._plugin_type_registry: dict[str, set] = {k: set() for k in PluginType.fields()}

    def init_globals(self) -> None:
        """
        Collect all "globals.py" files before the core registries start
        """

    def init_plugins(self) -> None:
        """ Initialize all built-in or third-party PiePlugins, components and user plugins """
        self._main_window = get_main_window()
        if not self._main_window:
            raise PieError(f"Can't find an initialized QMainWindow instance")

        # Initialize plugins then
        self.initialize_from_packages(Global.APP_ROOT / Global.PLUGINS_DIR_NAME)
        self.initialize_from_packages(Global.USER_ROOT / Global.PLUGINS_DIR_NAME)
        self.plugins_ready.emit()

    def shutdown_plugins(self, *plugins: str, all_plugins: bool = False) -> None:
        """
        Shutdown managers, services in parent object or all at once

        Args:
            plugins (objects): PiePlugin based classes
            all_plugins (bool): reload all managers, services from all instances
        """
        plugins = plugins if not all_plugins else self._plugin_registry.keys()
        for plugin in plugins:
            logger.debug(f"Shutting down plugin \"{plugin}\" from {self.__class__.__name__}")
            if plugin in self._plugin_registry:
                self.shutdown_plugin(plugin)

    def reload_plugins(self, *plugins: str, all_plugins: bool = False) -> None:
        """ Reload listed or all objects and components """
        self.shutdown_plugins(*plugins, all_plugins=all_plugins)
        for plugin in self._plugin_registry:
            plugin_instance = self._plugin_registry.get(plugin)
            self.initialize_plugin(plugin_instance)

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
            self.shutdown_plugin(plugin_name)

            # Disconnect depending on plugins from the plugin to delete
            self._notify_plugin_shutdown(plugin_name)

        try:
            plugin_instance.on_close()
        except Exception as e:
            logger.critical(str(e))

        return True

    def get_plugin(self, plugin_name: str) -> PiePlugin:
        """ Get PiePlugin instance by its name """
        return self._plugin_registry.get(plugin_name, None)

    def get_plugins(self) -> list[PiePlugin]:
        return list(self._plugin_registry.values())

    # Prepare methods

    def check_versions(self, plugin_package: ModuleType) -> None:
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

    def initialize_from_packages(self, folder: "Path") -> None:
        if not folder.exists():
            logger.warning(f"Plugins folder {folder.name} doesn't exist")
            return

        sys.path.insert(0, folder.as_posix())

        for package in folder.iterdir():
            if package.is_dir() and package.name not in ("__pycache__",):
                logger.debug(f"Preparing plugin {package.name}")

                # Plugin path: pieapp/plugins/<plugin name>
                plugin_path = folder / package.name

                if (plugin_path / "globals.py").exists():
                    Global.load_by_path(plugin_path / "globals.py")

                # Add our plugin into sys.path
                plugin_package_module = import_by_path(str(plugin_path / "__init__.py"))
                try:
                    self.check_versions(plugin_package_module)
                except AttributeError:
                    self.delete_plugin(package.name)

                # Importing plugin module
                plugin_module = import_by_path(str(plugin_path / "plugin.py"))

                # Initializing plugin instance
                plugin_instance = getattr(plugin_module, "main")(self._main_window, plugin_path)
                # if plugin_instance.name in (SysPlugin.Converter, SysPlugin.MetadataEditor):
                #     continue
                if plugin_instance:
                    self.initialize_plugin(plugin_instance)

    def shutdown_plugin(self, plugin_name: str):
        """ Shutdown a plugin from its dependencies """
        plugin_instance = self._plugin_registry[plugin_name]
        plugin_dependencies = self._plugin_dependencies.get(plugin_name, {})
        required_plugins = plugin_dependencies.get("requires", [])
        optional_plugins = plugin_dependencies.get("optional", [])

        for plugin in required_plugins + optional_plugins:
            if plugin in self._plugin_registry:
                if self._plugin_availability.get(plugin, False):
                    logger.debug(f"Shutting down {plugin_name} from {plugin}")
                    plugin_instance.on_plugin_teardown(plugin)

    # Notification methods

    def initialize_plugin(self, plugin_instance: PiePlugin) -> None:
        logger.debug(f"Initializing plugin {plugin_instance.name}")

        self._update_plugin_info(
            plugin_instance.name,
            plugin_instance.requires,
            plugin_instance.optional
        )

        # Hash plugin instance
        self._plugin_registry[plugin_instance.name] = plugin_instance
        self._plugin_type_registry[plugin_instance.type].add(plugin_instance.name)

        # Connect registry with plugin instance
        self.plugins_ready.connect(plugin_instance.sig_reg_plugins_ready)
        self.plugins_teardown.connect(plugin_instance.sig_reg_plugins_teardown)

        self._main_window.sig_on_main_window_close.connect(plugin_instance.sig_on_main_window_close)
        self._main_window.sig_on_main_window_show.connect(plugin_instance.sig_on_main_window_show)
        self._main_window.sig_on_before_main_window_show.connect(plugin_instance.sig_on_before_main_window_show)

        # Connect plugin observer signals
        plugin_instance.sig_plugin_ready.connect(lambda: (
            self._notify_plugin_dependencies(plugin_instance.name),
            self._notify_plugin_availability(plugin_instance.name)
        ))

        try:
            plugin_instance.prepare()
        except Exception as e:
            logger.debug(f"Error {plugin_instance.name}: {e!s}")
            self.delete_plugin(plugin_instance.name)
            raise e

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
                plugin_instance.on_plugin_available(name)

    def _notify_plugin_dependencies(self, name: str) -> None:
        """ Notify PiePlugins dependencies """
        plugin_instance = self._plugin_registry[name]
        plugin_dependencies = self._plugin_dependencies.get(name, {})
        required_plugins = plugin_dependencies.get("requires", [])
        optional_plugins = plugin_dependencies.get("optional", [])

        for plugin in required_plugins + optional_plugins:
            if plugin in self._plugin_registry:
                if self._plugin_availability.get(plugin, False):
                    logger.debug(f"Plugin {plugin} has already loaded")
                    plugin_instance.on_plugin_available(plugin)

    def _update_plugin_info(
        self,
        plugin_name: str,
        required_plugins: list[str],
        optional_plugins: list[str]
    ) -> None:
        """
        Update the PiePlugin dependencies and dependents
        """
        for plugin in required_plugins:
            self._update_dependencies(plugin_name, plugin, "requires")
            self._update_dependents(plugin, plugin_name, "requires")

        for plugin in optional_plugins:
            self._update_dependencies(plugin_name, plugin, "optional")
            self._update_dependents(plugin, plugin_name, "optional")

    def _update_dependents(
        self,
        plugin_name: str,
        dependent_plugin: str,
        category: str
    ) -> None:
        """
        Add dependent plugin to the plugin's list of dependents

        Args:
            plugin_name (str): object name
            dependent_plugin (str): dependent plugin
            category (str): required or optional category of plugins
        """
        plugin_dependents = self._plugin_dependents.get(plugin_name, {})
        plugin_strict_dependents = plugin_dependents.get(category, [])
        plugin_strict_dependents.append(dependent_plugin)
        plugin_dependents[category] = plugin_strict_dependents
        self._plugin_dependents[plugin_name] = plugin_dependents

    def _update_dependencies(
        self,
        plugin_name: str,
        required_plugin: str,
        category: str
    ) -> None:
        """
        Add required plugin to the plugin's list of dependencies

        Args:
            plugin_name (str): plugin name
            required_plugin (str): required plugin
            category (str): required or optional category of plugins
        """
        plugin_dependencies = self._plugin_dependencies.get(plugin_name, {})
        plugin_strict_dependencies = plugin_dependencies.get(category, [])
        plugin_strict_dependencies.append(required_plugin)
        plugin_dependencies[category] = plugin_strict_dependencies
        self._plugin_dependencies[plugin_name] = plugin_dependencies

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
                    plugin_instance = self._plugin_registry[plugin]
                    logger.debug(
                        f"Notifying {plugin_instance.type.value.capitalize()} "
                        f"that {plugin_name} is going to be turned off"
                    )
                    plugin_instance.on_plugin_teardown(plugin_name)

    # PluginManager public methods

    def is_plugin_available(self, plugin_name: str) -> bool:
        return self._plugin_availability.get(plugin_name, False)


PluginRegistry = PluginRegistryClass()
