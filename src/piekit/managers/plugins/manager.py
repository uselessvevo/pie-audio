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
        self._object_dependents: dict[str, dict[str, list[str]]] = {}

        # List of the plugins that the plugin depends on
        self._object_dependencies: dict[str, dict[str, list[str]]] = {}

        # BasePlugin dictionary
        self._objects_registry: dict[str, BasePlugin] = {}

        # BasePlugin dictionary with availability boolean status
        self._object_availability: dict[str, bool] = {}

        self._object_ready: set[str] = set()

    # BaseManager methods

    def mount(self, parent: "MainWindow" = None) -> None:
        """ Mount all built-in plugins, components and user plugins """
        self._mount_plugins(Config.APP_ROOT / Config.PLUGINS_FOLDER, parent)
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
        plugins = plugins if not full_house else self._objects_registry.keys()
        for plugin in plugins:
            self._logger.info(f"Unmounting plugin {plugin} from {self.__class__.__name__}")

            if plugin in self._objects_registry:
                self._unmount_plugin(plugin)
            
    def reload(self, *plugins: str, full_house: bool = False) -> None:
        """ Reload listed or all plugins and components """
        plugins = self._objects_registry.keys() if full_house else plugins
        for plugin in plugins:
            self._logger.info(f"Reloading plugin {plugin} from {self.__class__.__name__}")

            if plugin in self._objects_registry:
                self._reload_plugin(plugin)

    def get(self, key) -> Any:
        """ Get plugin instance by its name """
        return self._objects_registry.get(key)

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
                object_path = folder / plugin.name
                object_manifest = read_json(str(object_path / "manifest.json"))

                # Importing plugin module
                object_module = import_by_path("plugin", str(object_path / "plugin/plugin.py"))

                # Creating plugin instance
                # System.root / System.config.PLUGINS_FOLDER / self.name
                object_instance: BasePlugin = getattr(object_module, object_manifest.get("init"))(parent, object_path)

                self._update_object_info(
                    object_instance.name,
                    object_instance.requires,
                    object_instance.optional
                )

                # Hashing plugin instance
                self._objects_registry[object_instance.name] = object_instance

                object_instance.signalObjectReady.connect(
                    lambda: (
                        self._notify_object_availability(
                            object_instance.name,
                            object_instance.requires,
                            object_instance.optional,
                        ),
                        self._notify_object_availability_on_main(
                            object_instance.name
                        )
                    )
                )

                # Initializing plugin
                object_instance.prepare()

        self._set_objects_ready()

    def _set_objects_ready(self) -> None:
        for pie_object in self._objects_registry:
            if pie_object in self._object_ready:
                continue

            object_instance = self._objects_registry.get(pie_object)

            # BasePlugin is ready
            object_instance.signalObjectReady.emit()

            self._notify_object_dependencies(object_instance.name)

            # Inform about that
            self._logger.info(f"Object {pie_object} is ready!")

            self._object_ready.add(pie_object)

    def _notify_object_availability(
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

        self._object_availability[name] = True

        for plugin in requires + optional:
            if plugin in self._objects_registry:
                object_instance = self._objects_registry[plugin]
                object_instance.on_object_available(name)

    def _notify_object_availability_on_main(self, name: str) -> None:
        object_instance = self._objects_registry.get(name)
        if object_instance:
            object_instance.parent().signalObjectReady.emit(name)

    def _notify_object_dependencies(self, name: str) -> None:
        """ Notify plugin dependencies """
        object_instance = self._objects_registry[name]
        object_dependencies = self._object_dependencies.get(name, {})
        required_plugins = object_dependencies.get("requires", [])
        optional_plugins = object_dependencies.get("optional", [])

        for plugin in required_plugins + optional_plugins:
            if plugin in self._objects_registry:
                if self._object_availability.get(plugin, False):
                    self._logger.debug(f"BasePlugin {plugin} has already loaded")
                    object_instance.on_object_available(plugin)

    def _update_object_info(
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
        object_dependents = self._object_dependents.get(plugin, {})
        object_strict_dependents = object_dependents.get(category, [])
        object_strict_dependents.append(dependent_plugin)
        object_dependents[category] = object_strict_dependents
        self._object_dependents[plugin] = object_dependents

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
        object_dependencies = self._object_dependencies.get(plugin, {})
        object_strict_dependencies = object_dependencies.get(category, [])
        object_strict_dependencies.append(required_plugin)
        object_dependencies[category] = object_strict_dependencies
        self._object_dependencies[plugin] = object_dependencies

    def _notify_object_unmount(self, object_name: str):
        """Notify dependents of a plugin that is going to be unavailable."""
        object_dependents = self._object_dependents.get(object_name, {})
        required_plugins = object_dependents.get("requires", [])
        optional_plugins = object_dependents.get("optional", [])

        for plugin in required_plugins + optional_plugins:
            if plugin in self._objects_registry:
                if self._object_availability.get(plugin, False):
                    self._logger.debug(
                        f"Notifying plugin {plugin} that {object_name} is going to be turned off"
                    )
                    object_instance: BasePlugin = self._objects_registry[plugin]
                    object_instance.on_object_unmount(object_name)

    def _unmount_plugin(self, object_name: str):
        """ Unmount a plugin from its dependencies """
        object_instance: BasePlugin = self._objects_registry[object_name]
        object_dependencies = self._object_dependencies.get(object_name, {})
        required_plugins = object_dependencies.get("requires", [])
        optional_plugins = object_dependencies.get("optional", [])

        for plugin in required_plugins + optional_plugins:
            if plugin in self._objects_registry:
                if self._object_availability.get(plugin, False):
                    self._logger.info(f"Unmounting {object_name} from {plugin}")
                    object_instance.on_object_unmount(plugin)

    # PluginManager public methods

    def is_object_available(self, name: str) -> bool:
        return self._object_availability.get(name, False)

    isPluginAvailable = is_object_available
