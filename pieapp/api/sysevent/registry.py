from PySide6.QtCore import QObject, Signal

from pieapp.api.gloader import Global


class SystemEventRegistry(QObject):

    def __init__(self) -> None:
        super(SystemEventRegistry, self).__init__()

        # List of signals that depend on it
        self._signals_dependents: dict[str, dict] = {}

        # List of the signals that the signals depends on
        self._signals_dependencies: dict[str, dict[str, list[str]]] = {}

        # Signal dictionary
        self._signals_registry: dict[str, dict] = {}

    @staticmethod
    def _get_object_signals(target: QObject) -> list[str]:
        """
        Collect signals names that starts with `SIGNAL_PREFIX (sig_/sig)` prefix
        """
        signals: list[str] = []
        for signal_name in dir(target):
            if (signal_name.startswith(Global.PLUGINS_SIGNAL_PREFIX)
                    and signal_name not in Global.PLUGINS_PRIVATE_SIGNALS):
                signal_instance = getattr(target, signal_name, None)
                if isinstance(signal_instance, Signal):
                    signals.append(signal_name)

        return signals

    def _notify_object_event(self, target_name: QObject, signals: set[str]) -> None:
        object_dependents = self._signals_dependents.get(target_name, {})
        required_plugins = object_dependents.get("requires", [])
        optional_plugins = object_dependents.get("optional", [])

        for plugin in required_plugins + optional_plugins:
            if plugin in self._signals_registry:
                object_instance = self._signals_registry[plugin]
                for signal in signals:
                    object_instance.on_system_event(target_name, signal)
