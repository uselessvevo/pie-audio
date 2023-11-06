from typing import Union

from PySide6.QtWidgets import QWidget, QPushButton, QGridLayout

from piekit.globals import Global
from pieapp.structs.plugins import Plugin
from piekit.plugins.plugins import PiePlugin
from piekit.managers.themes.mixins import ThemeAccessorMixin
from piekit.plugins.mixins import ContainerRegisterAccessorMixin


class TestPluginChild(
    PiePlugin, 
    ThemeAccessorMixin,
    ContainerRegisterAccessorMixin
):
    """
    This plugin made to check how `ContainerRegister` mixins works
    """
    
    name = Plugin.TestPluginChild
    section = Plugin.TestPluginChild
    requires = [Plugin.TestPluginChild]

    def init(self) -> None:
        self._main_layout = QGridLayout()
        self._widget = QWidget(self._parent)
        self._test_button = QPushButton(self._widget)
        self._test_button.set_text("Click me")
        self._test_button.clicked.connect(self.test_button_connect)
        self._test_button.set_icon(self.get_svg_icon("icons/delete.svg"))
        self._main_layout.add_widget(self._test_button, 0, 0)
        self._widget.set_layout(self._main_layout)

        # TODO: Check if it works
        self.register_on(Plugin.TestPlugin, self._widget)

    def test_button_connect(self) -> None:
        self._logger.debug(f"{self.name}'s button clicked")


def main(parent: "QMainWindow", plugin_path: "Path") -> Union[PiePlugin, None]:
    if Global.TEST_PLUGIN_ENABLE:
        return TestPluginChild(parent, plugin_path)
