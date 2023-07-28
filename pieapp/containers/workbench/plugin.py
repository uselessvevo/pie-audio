from __feature__ import snake_case

from typing import Union

from PySide6.QtWidgets import QSizePolicy, QWidget

from pieapp.structs.containers import Container
from pieapp.structs.workbench import WorkbenchItem
from piekit.plugins.plugins import PiePlugin

from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor
from piekit.managers.toolbars.mixins import ToolBarAccessor
from piekit.managers.toolbuttons.mixins import ToolButtonAccessor


class Workbench(
    PiePlugin,
    ToolBarAccessor, ToolButtonAccessor,
    ConfigAccessor, LocalesAccessor, AssetsAccessor,
):
    name = Container.Workbench

    def init(self) -> None:
        self._workbench = self.add_toolbar(self._parent, self.name)

        self.add_tool_button(
            section=self.name,
            name=WorkbenchItem.Exit,
            text=self.get_translation("Exit"),
            tooltip=self.get_translation("Exit"),
            icon=self.get_asset_icon("exit.png"),
            triggered=self._parent.close
        )

        spacer = QWidget()
        spacer.set_object_name(WorkbenchItem.Spacer)
        spacer.set_size_policy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        self.add_toolbar_item(
            section=self.name,
            name=WorkbenchItem.Spacer,
            item=spacer
        )

        self.add_toolbar_item(
            section=self.name,
            name=WorkbenchItem.Exit,
            item=self.get_tool_button(self.name, WorkbenchItem.Exit)
        )

        self._parent.workbench_layout.add_widget(self._workbench, 0, 0)


def main(*args, **kwargs) -> Union[PiePlugin, None]:
    return Workbench(*args, **kwargs)
