import typing

from PyQt5.Qt import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget

from pieapp.structs.containers import Containers
from pieapp.structs.workbench import WorkbenchItems
from piekit.plugins.base import PiePlugin

from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor
from piekit.managers.toolbars.mixins import ToolBarAccessor
from piekit.managers.toolbuttons.mixins import ToolButtonAccessor


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
        self.workbench = self.addToolBar(widget, self.name)

        self.workbench.setMovable(False)
        self.workbench.setContextMenuPolicy(Qt.PreventContextMenu)
        self.workbench.setToolButtonStyle(Qt.ToolButtonTextBesideIcon | Qt.AlignLeading)

        self.addToolButton(
            parent=self.workbench,
            section=self.name,
            name=WorkbenchItems.OpenFiles,
            text=self.getTranslation("Open file"),
            tooltip=self.getTranslation("Open file"),
            icon=self.getAssetIcon("open-folder.png")
        )

        self.addToolButton(
            parent=self.workbench,
            section=self.name,
            name=WorkbenchItems.Clear,
            text=self.getTranslation("Clear"),
            tooltip=self.getTranslation("Clear"),
            icon=self.getAssetIcon("recycle-bin.png")
        ).setEnabled(False)

        self.addToolButton(
            parent=self.workbench,
            section=self.name,
            name=WorkbenchItems.Settings,
            text=self.getTranslation("Settings"),
            tooltip=self.getTranslation("Settings"),
            icon=self.getAssetIcon("settings.png")
        )

        self.addToolButton(
            parent=self.workbench,
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
            name=WorkbenchItems.OpenFiles,
            item=self.getToolButton(self.name, WorkbenchItems.OpenFiles)
        )

        self.addToolBarItem(
            section=self.name,
            name=WorkbenchItems.Clear,
            item=self.getToolButton(self.name, WorkbenchItems.Clear)
        )

        self.addToolBarItem(
            section=self.name,
            name=WorkbenchItems.Settings,
            item=self.getToolButton(self.name, WorkbenchItems.Settings)
        )

        self.addToolBarItem(
            section=self.name,
            name=WorkbenchItems.Spacer,
            item=spacer
        )

        self.addToolBarItem(
            section=self.name,
            name=WorkbenchItems.Exit,
            item=self.getToolButton(self.name, WorkbenchItems.Exit)
        )

        self._parent.addToolBar(Qt.TopToolBarArea, self.workbench)


def main(*args, **kwargs) -> typing.Any:
    return Workbench(*args, **kwargs)
