""" 
Plugin notification observer 
"""
from piekit.exceptions import PieException


class PluginsObserverMixin:

    def __init__(self) -> None:
        self._plugin_event_listeners: dict[str, dict] = {}

        for method_name in dir(self):
            method = getattr(self, method_name, None)
            if hasattr(method, "event_listen"):
                data = method.event_listen
                if data.get("target") not in self.requires + self.optional:
                    raise PieException(
                        f"Method {method_name} of {self} is trying to watch "
                        f"plugin {data.get('target')}, but that plugin is not "
                        f"listed in `requires` nor `optional`."
                    )
                self._plugin_event_listeners[f"{data['target']}.{data['event']}"] = {"method": method, **data}

    def on_plugin_event(self, target: str, event: str = None) -> None:
        event = event if event else "plugin_ready"
        target = f"{target}.{event}"
        if target in self._plugin_event_listeners:
            event = self._plugin_event_listeners[target]
            event["method"]()

    @property
    def subscribed_events(self) -> set[str]:
        return set(self._plugin_event_listeners.keys())
