from piekit.plugins.plugins import PiePlugin
from piekit.plugins.types import PluginTypes
from piekit.managers.registry import Managers
from piekit.managers.structs import SysManager


class ContainerRegisterAccessor:
    """
    Main window accessor mixin
    """

    def register_on(self, container: str, target: PiePlugin) -> PiePlugin:
        """
        Register plugin on certain container by its name
        
        Args:
            container (str): name of the container
            target (PiePlugin): plugin instance

        Returns:
            A container instance
        """
        if not isinstance(target, PiePlugin):
            raise TypeError(f"Target {target.name} is not a `PiePlugin` based instance")
            
        if Managers(SysManager.Plugins).plugin_has_type(PluginTypes.Container):
            raise KeyError(f"Container {container} doesn't exist on {self.__class__.__name__}")

        container_instance = Managers(SysManager.Plugins).get(container)
        container_instance.register_target(target)

        return container_instance
    
    def remove_from(self, container: str, target: str) -> PiePlugin:
        """
        Remove/unregister plugin from the container by its name
        
        Args:
            container (str): name of the container
            target (str): plugin name

        Returns:
            A container instance
        """
        if Managers(SysManager.Plugins).plugin_has_type(PluginTypes.Container):
            raise KeyError(f"Container {container} doesn't exist on {self.__class__.__name__}")

        container_instance = Managers(SysManager.Plugins).get(container)
        container_instance.remove_target(target)

        return container_instance
