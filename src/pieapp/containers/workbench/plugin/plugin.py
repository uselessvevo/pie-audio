import typing

from PyQt5.Qt import Qt
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QToolBar, QWidget

from pieapp.structs.containers import Containers
from piekit.managers.toolbars.mixins import ToolBarAccessor
from piekit.managers.toolbuttons.mixins import ToolButtonAccessor
from piekit.managers.structs import WorkbenchItems
from piekit.plugins.base import PiePlugin
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor


class Workbench(
    PiePlugin,
    ConfigAccessor,
    LocalesAccessor,
    AssetsAccessor,
    ToolBarAccessor,
    ToolButtonAccessor,
):
    name = Containers.Workbench

    def init(self) -> None:
        widget = QWidget()
        self.toolBar = self.addToolBar(widget, self.name)
        self.toolBar.setMovable(False)
        self.toolBar.setIconSize(QtCore.QSize(27, 27))
        self.toolBar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.toolBar.setOrientation(Qt.Vertical)
        self.toolBar.setSizePolicy(QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum
        ))

        self.addToolButton(
            parent=self.toolBar,
            section=self.name,
            name=WorkbenchItems.Settings,
            text=self.getTranslation("Settings"),
            tooltip=self.getTranslation("Settings"),
            icon=self.getAssetIcon("settings.png")
        )

        self.addToolButton(
            parent=self.toolBar,
            section=self.name,
            name=WorkbenchItems.Exit,
            text=self.getTranslation("Exit"),
            tooltip=self.getTranslation("Exit"),
            icon=self.getAssetIcon("exit.png"),
            triggered=self.parent().close
        )

        spacer = QtWidgets.QWidget()
        spacer.setObjectName(WorkbenchItems.Spacer)
        spacer.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )

        self.addToolBarItem(
            section=self.name,
            name=WorkbenchItems.Spacer,
            item=spacer
        )

        self.addToolBarItem(
            section=self.name,
            name=WorkbenchItems.Settings,
            item=self.getToolButton(self.name, WorkbenchItems.Settings)
        )

        self.addToolBarItem(
            section=self.name,
            name=WorkbenchItems.Exit,
            item=self.getToolButton(self.name, WorkbenchItems.Exit)
        )

        self._parent.addToolBar(Qt.LeftToolBarArea, self.toolBar)


def main(*args, **kwargs) -> typing.Any:
    return Workbench(*args, **kwargs)
