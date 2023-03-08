import typing

from PyQt5.QtWidgets import QDialog

from piekit.plugins.base import PiePlugin
from pieapp.structs.plugins import Plugins
from pieapp.structs.containers import Containers
from piekit.managers.menus.mixins import MenuAccessor

from pieapp.structs.workbench import WorkbenchItems
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.locales.mixins import LocalesAccessor
from piekit.managers.toolbars.mixins import ToolBarAccessor
from piekit.managers.toolbuttons.mixins import ToolButtonAccessor
from piekit.managers.plugins.decorators import onPluginAvailable


class Converter(
    PiePlugin,
    MenuAccessor,
    LocalesAccessor,
    AssetsAccessor,
    ToolBarAccessor,
    ToolButtonAccessor
):
    name = Plugins.Converter
    requires = [Containers.Workbench, Containers.MenuBar]

    def init(self) -> None:
        self.dialog = QDialog(self.parent())
        self.dialog.setWindowTitle(self.getTranslation("Convert"))
        self.dialog.setWindowIcon(self.getAssetIcon("go.png"))
        self.dialog.resize(400, 300)

    @onPluginAvailable(target=Containers.Workbench)
    def onWorkbenchAvailable(self) -> None:
        self.addToolButton(
            parent=self.getToolBar(Containers.Workbench),
            section=self.name,
            name=WorkbenchItems.OpenFiles,
            text=self.getTranslation("Open file"),
            tooltip=self.getTranslation("Open file"),
            icon=self.getAssetIcon("open-folder.png")
        )

        self.addToolButton(
            parent=self.getToolBar(Containers.Workbench),
            section=self.name,
            name=WorkbenchItems.Convert,
            text=self.getTranslation("Convert"),
            tooltip=self.getTranslation("Convert"),
            icon=self.getAssetIcon("go.png")
        ).setEnabled(False)

        self.addToolButton(
            parent=self.getToolBar(Containers.Workbench),
            section=self.name,
            name=WorkbenchItems.Clear,
            text=self.getTranslation("Clear"),
            tooltip=self.getTranslation("Clear"),
            icon=self.getAssetIcon("recycle-bin.png")
        ).setEnabled(False)

        self.addToolBarItem(
            section=Containers.Workbench,
            name=WorkbenchItems.Clear,
            item=self.getToolButton(self.name, WorkbenchItems.Clear),
            before=WorkbenchItems.Spacer
        )

        self.addToolBarItem(
            section=Containers.Workbench,
            name=WorkbenchItems.Convert,
            item=self.getToolButton(self.name, WorkbenchItems.Convert),
            before=WorkbenchItems.Spacer
        )

        self.addToolBarItem(
            section=Containers.Workbench,
            name=WorkbenchItems.OpenFiles,
            item=self.getToolButton(self.name, WorkbenchItems.OpenFiles),
            before=WorkbenchItems.Spacer
        )


def main(*args, **kwargs) -> typing.Any:
    return Converter(*args, **kwargs)
