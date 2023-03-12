import typing

from PyQt5.QtWidgets import QDialog

from pieapp.structs.containers import Containers
from pieapp.structs.menus import Menus
from piekit.managers.menus.mixins import MenuAccessor
from piekit.managers.plugins.decorators import onPluginAvailable
from piekit.managers.structs import Sections
from piekit.managers.toolbars.mixins import ToolBarAccessor
from piekit.managers.toolbuttons.mixins import ToolButtonAccessor
from piekit.plugins.plugins import PiePlugin
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor


class Settings(
    PiePlugin,
    ConfigAccessor,
    LocalesAccessor,
    AssetsAccessor,
    MenuAccessor,
    ToolBarAccessor,
    ToolButtonAccessor,
):
    name = Containers.Settings
    requires = [Containers.MenuBar, Containers.Workbench]

    def init(self) -> None:
        self.dialog = QDialog(self.parent())
        self.dialog.setWindowTitle(self.getTranslation("Settings"))
        self.dialog.setWindowIcon(self.getAssetIcon("settings.png"))
        self.dialog.resize(500, 320)

    @onPluginAvailable(target=Containers.MenuBar)
    def onMenuBarAvailable(self) -> None:
        self.addMenuItem(
            section=Sections.Shared,
            menu=Menus.File,
            name="settings",
            text=self.getTranslation("Settings"),
            triggered=self.dialog.show,
            icon=self.getAssetIcon("settings.png")
        )


def main(*args, **kwargs) -> typing.Any:
    return Settings(*args, **kwargs)
