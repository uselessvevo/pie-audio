from typing import Any
from pathlib import Path

from piekit.mainwindow.main import MainWindow
from piekit.managers.types import SysManagers
from piekit.objects.base import PieObject
from piekit.managers.base import BaseManager
from piekit.system.loader import Config
from piekit.utils.modules import import_by_path
from piekit.utils.files import read_json, write_json


class ObjectManager(BaseManager):
    """
    This manager is the PieObjects registry.
    Based on SpyderPluginRegistry from the Spyder IDE project
    """
    name = SysManagers.Objects
    dependencies = (SysManagers.Configs, SysManagers.Locales)

    def __init__(self) -> None:
        super().__init__()

        # List of PieObjects that depend on it
        self._object_dependents: dict[str, dict[str, list[str]]] = {}

        # List of the PieObjects that the PieObjects depends on
        self._object_dependencies: dict[str, dict[str, list[str]]] = {}

        # PieObject dictionary
        self._objects_registry: dict[str, PieObject] = {}

        # PieObjects dictionary with availability boolean status
        self._object_availability: dict[str, bool] = {}

        self._object_ready: set[str] = set()

    # BaseManager methods

    def mount(self, parent: "MainWindow" = None) -> None:
        """ Mount all built-in or site PieObjects, components and user pie_objects """
        self._mount_objects_from_packages(Config.APP_ROOT / Config.CONTAINERS_FOLDER, parent)
        self._mount_objects_from_packages(Config.APP_ROOT / Config.PLUGINS_FOLDER, parent)
        self._mount_objects_from_packages(Config.USER_ROOT / Config.USER_PLUGINS_FOLDER, parent)

    def unmount(self, *pie_objects: str, full_house: bool = False) -> None:
        """
        Unmount managers, services in parent object or all at once

        Args:
            pie_objects (objects): PieObject based classes
            full_house (bool): reload all managers, services from all instances

        TODO: Notify all objects to unmount all dependencies
        """
        pie_objects = pie_objects if not full_house else self._objects_registry.keys()
        for pie_object in pie_objects:
            self._logger.info(f"Unmounting {pie_object} from {self.__class__.__name__}")

            if pie_object in self._objects_registry:
                self._unmount_object(pie_object)

        # List of PieObjects that depend on it
        self._object_dependents: dict[str, dict[str, list[str]]] = {}

        # List of the PieObjects that the PieObjects depends on
        self._object_dependencies: dict[str, dict[str, list[str]]] = {}

        # PieObject dictionary
        self._objects_registry: dict[str, PieObject] = {}

        # PieObjects dictionary with availability boolean status
        self._object_availability: dict[str, bool] = {}

        self._object_ready: set[str] = set()
            
    def reload(self, *pie_objects: str, full_house: bool = False) -> None:
        """ Reload listed or all objects and components """
        self.unmount(*pie_objects, full_house=full_house)
        for pie_object in self._objects_registry:
            object_instance = self._objects_registry.get(pie_object)
            self._initialize_object(object_instance)

    def get(self, key) -> Any:
        """ Get PieObject instance by its name """
        return self._objects_registry.get(key)

    # ObjectManager protected methods

    def _mount_objects_from_packages(self, folder: "Path", parent: MainWindow = None) -> None:
        if not folder.exists():
            folder.mkdir()

        for package in folder.iterdir():
            if package.is_dir() and package.name not in ("__pycache__",) and parent:
                self._logger.info(f"Reading package data from {package.name}")

                # Reading data from `<object>/manifest.json`
                object_path = folder / package.name
                object_manifest = read_json(str(object_path / "manifest.json"))

                # Importing PieObject module
                object_module = import_by_path("plugin", str(object_path / "plugin/plugin.py"))

                # Creating PieObject instance
                object_instance: PieObject = getattr(object_module, object_manifest.get("init"))(parent, object_path)

                self._initialize_object(object_instance)

        self._set_objects_ready()

    def _set_objects_ready(self) -> None:
        for pie_object in self._objects_registry:
            if pie_object in self._object_ready:
                continue

            object_instance = self._objects_registry.get(pie_object)

            # PieObject is ready
            object_instance.signalObjectReady.emit()

            self._notify_object_dependencies(object_instance.name)

            # Inform about that
            self._logger.info(f"{object_instance.type.capitalize()} {object_instance.name} is ready!")

            self._object_ready.add(pie_object)

    def _initialize_object(self, object_instance: PieObject) -> None:
        self._logger.info(f"Preparing {object_instance.type} {object_instance.name}")

        self._update_object_info(
            object_instance.name,
            object_instance.requires,
            object_instance.optional
        )

        # Hashing PieObject instance
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

        # Preparing `PieObject` instance
        object_instance.prepare()

    def _notify_object_availability(
        self,
        name: str,
        requires: list[str] = None,
        optional: list[str] = None,
    ) -> None:
        """
        Notify dependent PieObjects that our PieObject is available

        Args:
            name (str): PieObject name
            requires (list[str]): list of required PieObjects
            optional (list[str]): list of optional PieObjects
        """
        requires = requires or []
        optional = optional or []

        self._object_availability[name] = True

        for pie_object in requires + optional:
            if pie_object in self._objects_registry:
                object_instance = self._objects_registry[pie_object]
                object_instance.on_object_available(name)

    def _notify_object_availability_on_main(self, name: str) -> None:
        object_instance = self._objects_registry.get(name)
        if object_instance:
            object_instance.parent().signalObjectReady.emit(name)

    def _notify_object_dependencies(self, name: str) -> None:
        """ Notify PieObjects dependencies """
        object_instance = self._objects_registry[name]
        object_dependencies = self._object_dependencies.get(name, {})
        required_objects = object_dependencies.get("requires", [])
        optional_objects = object_dependencies.get("optional", [])

        for pie_object in required_objects + optional_objects:
            if pie_object in self._objects_registry:
                if self._object_availability.get(pie_object, False):
                    self._logger.debug(f"{object_instance.type.capitalize()} {pie_object} has already loaded")
                    object_instance.on_object_available(pie_object)

    def _update_object_info(
        self,
        name: str,
        required_objects: list[str],
        optional_objects: list[str]
    ) -> None:
        """
        Update the PieObject dependencies and dependents
        """
        for pie_object in required_objects:
            self._update_dependencies(name, pie_object, "requires")
            self._update_dependents(pie_object, name, "requires")

        for pie_object in optional_objects:
            self._update_dependencies(name, pie_object, "optional")
            self._update_dependents(pie_object, name, "optional")

    def _update_dependents(
        self,
        pie_object: str,
        dependent_plugin: str,
        category: str
    ) -> None:
        """
        Add dependent pie_object to the pie_object's list of dependents

        Args:
            pie_object (str): object name
            dependent_plugin (str): dependent pie_object
            category (str): required or optional category of pie_objects
        """
        object_dependents = self._object_dependents.get(pie_object, {})
        object_strict_dependents = object_dependents.get(category, [])
        object_strict_dependents.append(dependent_plugin)
        object_dependents[category] = object_strict_dependents
        self._object_dependents[pie_object] = object_dependents

    def _update_dependencies(
        self,
        pie_object: str,
        required_pie_object: str,
        category: str
    ) -> None:
        """
        Add required pie_object to the pie_object's list of dependencies

        Args:
            pie_object (str): pie_object name
            required_pie_object (str): required pie_object
            category (str): required or optional category of pie_objects
        """
        object_dependencies = self._object_dependencies.get(pie_object, {})
        object_strict_dependencies = object_dependencies.get(category, [])
        object_strict_dependencies.append(required_pie_object)
        object_dependencies[category] = object_strict_dependencies
        self._object_dependencies[pie_object] = object_dependencies

    def _notify_object_unmount(self, object_name: str):
        """Notify dependents of a pie_object that is going to be unavailable."""
        object_dependents = self._object_dependents.get(object_name, {})
        required_objects = object_dependents.get("requires", [])
        optional_objects = object_dependents.get("optional", [])

        for pie_object in required_objects + optional_objects:
            if pie_object in self._objects_registry:
                if self._object_availability.get(pie_object, False):
                    object_instance: PieObject = self._objects_registry[pie_object]
                    self._logger.debug(
                        f"Notifying {object_instance.type.capitalize()} "
                        f"that {object_name} is going to be turned off"
                    )
                    object_instance.on_object_unmount(object_name)

    def _unmount_object(self, object_name: str):
        """ Unmount a pie_object from its dependencies """
        object_instance: PieObject = self._objects_registry[object_name]
        object_dependencies = self._object_dependencies.get(object_name, {})
        required_objects = object_dependencies.get("requires", [])
        optional_objects = object_dependencies.get("optional", [])

        for pie_object in required_objects + optional_objects:
            if pie_object in self._objects_registry:
                if self._object_availability.get(pie_object, False):
                    self._logger.info(f"Unmounting {object_name} from {pie_object}")
                    object_instance.on_object_unmount(pie_object)

    # ObjectManager public methods

    def is_object_available(self, name: str) -> bool:
        return self._object_availability.get(name, False)

    isObjectAvailable = is_object_available
