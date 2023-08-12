""" 
Plugin notification observer 
"""
from piekit.managers.structs import AllPlugins
from piekit.exceptions import PieException


class PluginsObserverMixin:

    def __init__(self) -> None:
        self._plugin_availability_listeners = {}
        self._plugin_shutdown_listeners = {}

        for method_name in dir(self):
            method = getattr(self, method_name, None)
            if hasattr(method, "plugin_listen"):
                plugin_listen = method.plugin_listen

                if plugin_listen not in self.requires + self.optional:
                    raise PieException(
                        f"Method {method_name} of {self} is trying to watch "
                        f"plugin {plugin_listen}, but that plugin is not "
                        f"listed in `requires` nor `optional`."
                    )

                self._plugin_availability_listeners[plugin_listen] = method_name

            if hasattr(method, "plugin_shutdown"):
                object_shutdown = method.plugin_shutdown

                if object_shutdown not in self.requires + self.optional:
                    raise PieException(
                        f"Method {method_name} of {self} is trying to watch "
                        f"plugin {object_shutdown}, but that plugin is not "
                        f"listed in `requires` nor `optional`."
                    )

                self._plugin_shutdown_listeners[object_shutdown] = method_name

    def on_plugin_available(self, target: str) -> None:
        if target in self._plugin_availability_listeners:
            method_name = self._plugin_availability_listeners[target]
            method = getattr(self, method_name)
            method()

        # Call global plugin handler
        if AllPlugins in self._plugin_availability_listeners:
            method_name = self._plugin_availability_listeners[AllPlugins]
            method = getattr(self, method_name)
            method(target)

    def on_plugin_shutdown(self, target: str) -> None:
        if target in self._plugin_shutdown_listeners:
            method_name = self._plugin_shutdown_listeners[target]
            method = getattr(self, method_name)
            method()

    onPluginAvailable = on_plugin_available
    onPluginShutdown = on_plugin_shutdown
