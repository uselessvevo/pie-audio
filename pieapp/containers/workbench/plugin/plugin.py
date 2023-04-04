import typing

from PySide6.QtWidgets import QSizePolicy, QWidget

from pieapp.structs.containers import Containers
from pieapp.structs.workbench import WorkbenchItems
from piekit.plugins.plugins import PiePlugin

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
        self.widget = QWidget()
        self.widget.setObjectName("Workbench")
        self.workbench = self.addToolBar(self.widget, self.name)

        self.addToolButton(
            parent=self.workbench,
            section=self.name,
            name=WorkbenchItems.Exit,
            text=self.getTranslation("Exit"),
            tooltip=self.getTranslation("Exit"),
            icon=self.getAssetIcon("exit.png"),
            triggered=self.parent().close
        )

        spacer = QWidget()
        spacer.setObjectName(WorkbenchItems.Spacer)
        spacer.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
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

        self.parent().mainLayout.addWidget(self.workbench, 0, 0)


def main(*args, **kwargs) -> typing.Any:
    return Workbench(*args, **kwargs)
