from __feature__ import snake_case

from typing import Union

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QGridLayout, QSizePolicy

from pieapp.structs.layouts import Layout
from pieapp.structs.plugins import Plugin
from piekit.managers.layouts.mixins import LayoutsAccessorMixin
from piekit.managers.menus.mixins import MenuAccessorMixin
from piekit.plugins.plugins import PiePlugin

from piekit.managers.icons.mixins import IconAccessorMixin
from piekit.managers.configs.mixins import ConfigAccessorMixin
from piekit.managers.locales.mixins import LocalesAccessorMixin
from piekit.managers.toolbars.mixins import ToolBarAccessorMixin
from piekit.managers.toolbuttons.mixins import ToolButtonAccessorMixin


class Workbench(
    PiePlugin, LocalesAccessorMixin,
    LayoutsAccessorMixin, ToolBarAccessorMixin,
):
    name = Plugin.Workbench
    optional = [Plugin.MenuBar]

    def init(self) -> None:
        self._workbench = self.add_toolbar(name=self.name)
        self._workbench.set_fixed_height(50)
        self._workbench.set_contents_margins(6, 0, 10, 0)
        self._workbench.set_size_policy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))

        self._workbench_layout = QGridLayout()
        self._workbench_layout.add_widget(self._workbench)
        self.get_layout(Layout.Main).add_layout(self._workbench_layout, 0, 0, Qt.AlignmentFlag.AlignTop)


def main(parent: "QMainWindow", plugin_path: "Path") -> Union[PiePlugin, None]:
    return Workbench(parent, plugin_path)
