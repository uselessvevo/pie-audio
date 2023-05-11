from __feature__ import snake_case

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
        self.workbench = self.add_toolbar(self.widget, self.name)

        self.add_tool_button(
            parent=self.workbench,
            section=self.name,
            name=WorkbenchItems.Exit,
            text=self.get_translation("Exit"),
            tooltip=self.get_translation("Exit"),
            icon=self.get_asset_icon("exit.png"),
            triggered=self.parent().close
        )

        spacer = QWidget()
        spacer.set_object_name(WorkbenchItems.Spacer)
        spacer.set_size_policy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        self.add_toolbar_item(
            section=self.name,
            name=WorkbenchItems.Spacer,
            item=spacer
        )

        self.add_toolbar_item(
            section=self.name,
            name=WorkbenchItems.Exit,
            item=self.get_tool_button(self.name, WorkbenchItems.Exit)
        )

        self.parent().main_layout.add_widget(self.workbench, 0, 0)


def main(*args, **kwargs) -> typing.Any:
    return Workbench(*args, **kwargs)
