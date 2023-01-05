import typing

from cloudykit.system.manager import System
from cloudykit.objects.mainwindow import MainWindow
from cloudykit.objects.manager import BaseManager
from cloudykit.utils.files import read_json
from cloudykit.utils.modules import import_by_path


class ComponentsManager(BaseManager):
    # TODO: Make a method to get all plugins
    dependencies = ("userconfigs",)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._components = {}

    def mount(self, parent: MainWindow = None) -> None:
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
            self._components[component_inst.name] = component_inst

    def unmount(self, component: "BaseComponent" = None, full_house: bool = False) -> None:
        """
        Unmount managers, services in parent object or all at once
        Args:
            component (object): BaseComponent based object
            full_house (bool): reload all managers, services from all instances
        """
        # Get all plugins and reload them
        # plugins = self._get_all_plugins()

        if component and full_house:
            raise RuntimeError("Can\"t use `component` and `full_house` together")

        if component:
            component.unmount()

        elif full_house:
            for component in self._components.values():
                self._logger.info(f"Unmounting {component.name} from {self.__class__.__name__}")
                component.unmount()

    def reload(self, *components: tuple[str], full_house: bool = False) -> None:
        components = self._components.keys() if full_house else components
        for component in components:
            self._components.get(component)

    def get(self, key, default: typing.Any = None) -> typing.Any:
        return self._components.get(key)
