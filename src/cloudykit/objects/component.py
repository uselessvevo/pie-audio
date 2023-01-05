from PyQt5.QtCore import pyqtSignal, QObject

from cloudykit.system.manager import System
from cloudykit.system.registry import ManagersRegistry


class BaseComponent(QObject):
    name: str
    description: str
    version: tuple[int, int, int] = (0, 1, 0)

    signalComponentReady = pyqtSignal(str)
    signalComponentLoading = pyqtSignal(str)
    signalComponentReloading = pyqtSignal(str)

    signalOnMainWindowClose = pyqtSignal(bool)
    signalExceptionOccurred = pyqtSignal(dict)

    signalOnComponentClose = pyqtSignal()
    signalOnComponentMoved = pyqtSignal("QMoveEvent")
    signalOnComponentResized = pyqtSignal("QResizeEvent")

    def __init__(self, parent):
        super().__init__(parent)

    def mount(self) -> None:
        raise NotImplementedError("Method `mount` must be implemented")

    def unmount(self) -> None:
        pass

    def register(self, **kwargs) -> None:
        raise NotImplementedError("Method `register` must be implemented")

    def unregister(self):
        raise NotImplementedError("Method `unregister` must be implemented")

    @property
    def registry(self) -> ManagersRegistry:
        return System.registry
