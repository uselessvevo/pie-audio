from typing import Any

from PySide6.QtCore import QObject, Signal

from piekit.plugins.plugins import PiePlugin


class PiePluginAPI(QObject):
    name: str = None

    # Notify that API is ready
    sig_plugin_api_ready = Signal()

    def __init__(self, plugin: PiePlugin) -> None:
        super().__init__(plugin)

        self._plugin = plugin

    def prepare(self) -> None:
        self.init()
        self.sig_plugin_api_ready.emit()

    def init(self) -> None:
        pass

    def shutdown(self, *args, **kwargs) -> None:
        pass

    def reload(self, *args, **kwargs) -> None:
        self.init()
        self.shutdown()

    def call(self, method: str, **kwargs) -> Any:
        try:
            return self.__getattribute__(method)(**kwargs)
        except AttributeError:
            raise AttributeError(method)

    @property
    def plugin(self) -> PiePlugin:
        return self._plugin

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}> (id: {id(self)}, parent: {self._plugin})"
