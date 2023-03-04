""" 
Plugin notification observer 
"""
from piekit.managers.structs import AllPlugins


class PluginsObserverMixin:

    def __init__(self) -> None:
        self._plugin_availability_listeners = {}
        self._plugin_unmount_listeners = {}

        for method_name in dir(self):
            method = getattr(self, method_name, None)
            if hasattr(method, "_plugin_listen"):
                plugin_listen = method._plugin_listen

                if plugin_listen not in self.requires + self.optional:
                    raise PieException(
                        f"Method {method_name} of {self} is trying to watch "
                        f"plugin {plugin_listen}, but that plugin is not "
                        f"listed in `requires` nor `optional`."
                    )

                self._plugin_availability_listeners[plugin_listen] = method_name

            if hasattr(method, "_object_unmount"):
                object_unmount = method._object_unmount

                if object_unmount not in self.requires + self.optional:
                    raise PieException(
                        f"Method {method_name} of {self} is trying to watch "
                        f"plugin {object_unmount}, but that plugin is not "
                        f"listed in `requires` nor `optional`."
                    )

                self._plugin_unmount_listeners[object_unmount] = method_name

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

    def on_plugin_unmount(self, target: str) -> None:
        if target in self._plugin_unmount_listeners:
            method_name = self._plugin_unmount_listeners[target]
            method = getattr(self, method_name)
            method()

    onPluginAvailable = on_plugin_available
    onPluginUnmount = on_plugin_unmount
