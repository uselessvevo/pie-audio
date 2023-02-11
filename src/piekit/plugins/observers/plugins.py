""" This observer serves """
from piekit.structs.etc import AllPlugins


class PluginObserverMixin:

    def __init__(self) -> None:
        self._plugin_availability_listeners = {}
        self._plugin_unmount_listeners = {}

        for method_name in dir(self):
            method = getattr(self, method_name, None)
            if hasattr(method, "_plugin_listen"):
                plugin_listen = method._plugin_listen

                if plugin_listen not in self.requires + self.optional:
                    raise Exception(
                        f"Method {method_name} of {self} is trying to watch "
                        f"plugin {plugin_listen}, but that plugin is not "
                        f"listed in REQUIRES nor OPTIONAL."
                    )

                self._plugin_availability_listeners[plugin_listen] = method_name

            if hasattr(method, "_plugin_unmount"):
                plugin_unmount = method._plugin_unmount

                if plugin_unmount not in self.requires + self.optional:
                    raise Exception(
                        f"Method {method_name} of {self} is trying to watch "
                        f"plugin {plugin_unmount}, but that plugin is not "
                        f"listed in `requires` nor `optional`."
                    )

                self._plugin_unmount_listeners[plugin_unmount] = method_name

    def on_plugin_available(self, plugin: str) -> None:
        if plugin in self._plugin_availability_listeners:
            method_name = self._plugin_availability_listeners[plugin]
            method = getattr(self, method_name)
            method()

        # Call global plugin handler
        if AllPlugins in self._plugin_availability_listeners:
            method_name = self._plugin_availability_listeners[AllPlugins]
            method = getattr(self, method_name)
            method(plugin)

    def on_plugin_unmount(self, plugin: str) -> None:
        if plugin in self._plugin_unmount_listeners:
            method_name = self._plugin_unmount_listeners[plugin]
            method = getattr(self, method_name)
            method()

    onPluginAvailable = on_plugin_available
    onPluginUnmount = on_plugin_unmount
