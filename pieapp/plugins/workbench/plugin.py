from __feature__ import snake_case

from typing import Union

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QSizePolicy, QWidget, QGridLayout

from piekit.layouts.structs import Layout
from pieapp.structs.containers import Container
from pieapp.structs.workbench import WorkbenchItem
from piekit.managers.layouts.mixins import LayoutsAccessorMixin
from piekit.plugins.plugins import PiePlugin

from piekit.managers.assets.mixins import AssetsAccessorMixin
from piekit.managers.configs.mixins import ConfigAccessorMixin
from piekit.managers.locales.mixins import LocalesAccessorMixin
from piekit.managers.toolbars.mixins import ToolBarAccessorMixin
from piekit.managers.toolbuttons.mixins import ToolButtonAccessorMixin


class Workbench(
    PiePlugin,
    ConfigAccessorMixin, LocalesAccessorMixin, AssetsAccessorMixin,
    ToolBarAccessorMixin, ToolButtonAccessorMixin, LayoutsAccessorMixin,
):
    name = Container.Workbench

    def init(self) -> None:
        self._workbench = self.add_toolbar(name=self.name)
        self._workbench_layout = QGridLayout()
        self._workbench_layout.add_widget(self._workbench)
        self.get_layout(Layout.Main).add_layout(self._workbench_layout, 0, 0, Qt.AlignmentFlag.AlignTop)

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


def main(*args, **kwargs) -> Union[PiePlugin, None]:
    return Workbench(*args, **kwargs)