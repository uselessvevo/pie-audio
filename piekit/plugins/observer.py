""" 
Plugin notification observer 
"""
from piekit.managers.structs import AllPlugins
from piekit.exceptions import PieException


class PluginsObserverMixin:

    def __init__(self) -> None:
        self._plugin_event_listeners = {}
        self._plugin_availability_listeners = {}
        self._plugin_shutdown_listeners = {}

        for method_name in dir(self):
            method = getattr(self, method_name, None)
            if hasattr(method, "event_listen"):
                event_listen = method.event_listen
                if event_listen.get("target") not in self.requires + self.optional:
                    raise PieException(
                        f"Method {method_name} of {self} is trying to watch "
                        f"plugin {event_listen.get('target')}, but that plugin is not "
                        f"listed in `requires` nor `optional`."
                    )
                self._plugin_event_listeners[event_listen.get("target")] = {"method": method, **event_listen}

    def on_plugin_event(self, target: str) -> None:
        if target in self._plugin_event_listeners:
            event = self._plugin_event_listeners[target]
            event["method"]()
