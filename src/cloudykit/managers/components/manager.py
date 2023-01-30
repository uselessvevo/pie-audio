import typing

from cloudykit.system.manager import System
from cloudykit.appwindow.main import AppWindow
from cloudykit.managers.base import BaseManager
from cloudykit.utils.files import read_json
from cloudykit.utils.modules import import_by_path


class ComponentsManager(BaseManager):
    name = "components"
    dependencies = ("configs",)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._dictionary = {}

    def mount(self, parent: AppWindow = None) -> None:
        for component in (System.root / System.config.COMPONENTS_FOLDER).iterdir():
            self._logger.warning(f"Mounting component `{component.name}` in `{parent.__class__.__name__}`")

            # Reading data from `component/manifest.json`
            component_path = System.root / f"components/{component.name}"
            component_manifest = read_json(str(component_path / "manifest.json"))

            # Importing component module
            component_module = import_by_path("component", str(component_path / "component/component.py"))

            # Creating component instance
            component_inst = getattr(component_module, component_manifest.get("init"))(parent)

            # Initializing component
            component_inst.init()

            # Hashing component instance
            self._dictionary[component_inst.name] = component_inst

    def unmount(self, *components: "BaseComponent", full_house: bool = False) -> None:
        """
        Unmount managers, services in parent object or all at once
        Args:
            component (object): BaseComponent based object
            full_house (bool): reload all managers, services from all instances
        """
        # TODO: Get all plugins to unmount them all
        # >>> plugins = self._get_all_plugins()
        components = components if not full_house else self._dictionary.values()
        for component in components:
            self._logger.info(f"Unmounting {component.name} from {self.__class__.__name__}")

            if component:
                plugin.unmount()

    def reload(self, *components: tuple[str], full_house: bool = False) -> None:
        components = self._dictionary.keys() if full_house else components
        for component in components:
            self._dictionary.get(component)

    def get(self, key, default: typing.Any = None) -> typing.Any:
        return self._dictionary.get(key)
