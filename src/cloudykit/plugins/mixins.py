from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QAction, QMenu, QMenuBar


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
