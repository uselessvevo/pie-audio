from typing import Any

from PySide6.QtCore import QObject

from piekit.plugins.plugins import PiePlugin


class PiePluginAPI(QObject):

    def __init__(self, parent: PiePlugin) -> None:
        super().__init__(parent)

        self._parent = parent

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
    def parent(self) -> PiePlugin:
        return self._parent

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}> (id: {id(self)}, parent: {self._parent})"
