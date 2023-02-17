from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QToolBar, QMenuBar, QMenu, QAction

from piekit.plugins.base import BasePlugin
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor


class MenuBar(
    BasePlugin,
    ConfigAccessor,
    LocalesAccessor,
    AssetsAccessor,
):
    name = "menubar"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.__menus: dict[str, QMenu] = {}
        self.__menusItems: dict[str, QMenu] = {}

    def init(self) -> None:
        self.menuBar = QMenuBar(self._parent)

        # File menu
        self.addMenu(name="file", text=self.getTranslation("File"))
        self.addMenuItem(menu="file", name="open", text=self.getTranslation("Open file"), icon="bug.svg")

        self._parent.setMenuBar(self.menuBar)

    def addMenu(
        self,
        *,
        name: str = None,
        text: str = None
    ) -> None:
        if name in self.__menus:
            # raise PieException to handle and show error window
            pass

        menu = QMenu(text, self.menuBar)
        self.__menus[name] = menu
        self.__menusItems[name] = {}
        self.menuBar.addMenu(menu)

    def addMenuItem(
        self,
        *,
        menu: str = None,
        name: str = None,
        text: str = None,
        icon: str = None,
        signal: pyqtSignal = None,
    ) -> None:
        if menu not in self.__menus:
            # raise PieException to handle and show error window
            pass

        if name in self.__menusItems:
            # raise PieException to handle and show error window
            pass

        parent = self.__menus.get(menu)

        menuItemAction = QAction(parent=parent, text=text, icon=QIcon(self.getAsset(icon)))
        menuItemAction.setObjectName(name)
        parent.addAction(menuItemAction)

        if signal:
            menuItemAction.triggered.connect(signal)

        setattr(self, menuItemAction.objectName(), menuItemAction)

        self.__menusItems[menu].update({name: menuItemAction})
