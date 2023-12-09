from typing import Union

from piekit.managers.structs import Section

from piekit.managers.confpages.structs import ConfigPage

from PySide6.QtWidgets import QWidget, QPushButton, QGridLayout


class TestPluginConfigPage(ConfigPage):
    name = "test-configuration-page"
    root = Section.Root

    def init(self) -> None:
        self._main_grid = QGridLayout()

        self._widget = QWidget()
        self._button = QPushButton(self._widget)
        self._button.set_text("Press me")

        self._main_grid.add_widget(self._button, 0, 0)
        self._widget.set_layout(self._main_grid)

    def get_page_widget(self) -> QWidget:
        return self._widget

    def get_title(self) -> str:
        return "Test configuration page"

    def accept(self) -> None:
        print("Accepted")

    def cancel(self) -> None:
        print("Canceled")


def main(*args, **kwargs) -> Union[ConfigPage, None]:
    return TestPluginConfigPage(*args, **kwargs)
