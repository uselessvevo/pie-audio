from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QAction, QMenu, QMenuBar


class ComponentMixin:
    """
    Use this mixin to register your object
    on the `BaseComponent` based objects
    """
    signalQuitRequested = pyqtSignal()
    signalRestartRequested = pyqtSignal()
    signalExceptionOccurred = pyqtSignal(dict)

    signalOnComponentClose = pyqtSignal()
    signalOnComponentMoved = pyqtSignal("QMoveEvent")
    signalOnComponentResized = pyqtSignal("QResizeEvent")

    def prepareComponentSignals(self) -> None:
        self.signalQuitRequested.connect(self._parent)
        self.signalRestartRequested.connect(self._parent)
        self.signalExceptionOccurred.connect(self._parent)

    def placeOn(self, target: str, **kwargs) -> None:
        """
        Register/render widget on one
        of the listed components of `MainWindow`

        Args:
            target (str): registered component name
            kwargs (dict): component's `register` method parameters
        """
        self._parent.placeOn(self, target, **kwargs)

    def removeFrom(self, target: str) -> None:
        """
        Remover/de-render widget from `MainWindow` component(-s)

        Args:
            target (str): registered component name
        """
        self._parent.removeFrom(self, target)


class ActionMixin:

    def registerAction(self, text: str, icon: QIcon, func: callable, *funcargs, **funckwargs) -> None:
        action = QAction(text, icon, self)
        action.triggered.connect(func(*funcargs, **funckwargs))


class MenuMixin:

    def __init__(self) -> None:
        self.__menus: dict = {}
        self.__menuBars: dict = {}
        self.menuBar = QMenuBar(self)

    def createMenu(self, name: str, menu: str, text: str, icon: QIcon) -> QMenu:
        if self.__menus.get(name):
            raise AttributeError(f"Menu named {menu} is already registered")

        menu = QMenu(self, text, icon)
        self.menuBar.addMenu(menu)
        self.__menus.update({name: menu})
        return menu

    @property
    def menus(self) -> dict:
        return self.__menus
