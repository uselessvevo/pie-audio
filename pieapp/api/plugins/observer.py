""""
Plugin notification observer
"""
from pieapp.api.exceptions import PieException


class PluginsObserverMixin:

    def __init__(self) -> None:
        self._plugin_event_listeners: dict[str, dict] = {}
        self._plugin_listeners = {}
        self._plugin_teardown_listeners = {}

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
                self._plugin_listeners[plugin_listen] = method_name

            if hasattr(method, "plugin_teardown"):
                plugin_teardown = method.plugin_teardown
                if plugin_teardown not in self.requires + self.optional:
                    raise PieException(
                        f"Method {method_name} of {self} is trying to watch "
                        f"plugin {plugin_teardown}, but that plugin is not "
                        f"listed in `requires` nor `optional`."
                    )
                self._plugin_teardown_listeners[plugin_teardown] = method_name

    def on_plugin_available(self, plugin_name: str) -> None:
        """
        Handle plugin availability and redirect it to plugin-specific
        startup handlers

        Args:
            plugin_name (str): Name of the plugin that was notified as available.
        """
        if plugin_name in self._plugin_listeners:
            method_name = self._plugin_listeners[plugin_name]
            method = getattr(self, method_name)
            method()

    def on_plugin_teardown(self, plugin_name: str):
        """
        Handle plugin teardown and redirect it to plugin-specific teardown
        handlers.
        Args:
            plugin_name (str): Name of the plugin that is going through its teardown process.
        """
        # Call plugin specific handler
        if plugin_name in self._plugin_teardown_listeners:
            method_name = self._plugin_teardown_listeners[plugin_name]
            method = getattr(self, method_name)
            method()
