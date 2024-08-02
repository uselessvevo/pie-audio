from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget, QStatusBar

from pieapp.api.exceptions import PieException
from pieapp.api.models.indexes import Index
from pieapp.api.models.plugins import SysPlugin
from pieapp.api.models.statusbar import MessageStatus

from pieapp.api.plugins.plugins import PiePlugin
from pieapp.api.registries.locales.helpers import translate
from pieapp.api.registries.themes.mixins import ThemeAccessorMixin
from pieapp.utils.qt import get_main_window
from pieapp.widgets.iconlabel import IconLabel


class StatusBar(PiePlugin, ThemeAccessorMixin):
    name = SysPlugin.StatusBar
    requires = [SysPlugin.Layout]

    def init(self) -> None:
        self._sb_widgets: dict[str, QWidget] = {}
        self._sb_perm_widgets: dict[str, QWidget] = {}

        self._status_bar = QStatusBar()
        self._status_bar.set_object_name("MainStatusBar")

        self._status_bar_icon = IconLabel()
        self._status_bar.add_widget(self._status_bar_icon)

        main_window = get_main_window()
        main_window.set_status_bar(self._status_bar)

    def on_plugins_ready(self) -> None:
        self.show_message(translate("Plugins are ready"), MessageStatus.Info, 1000)

    def show_message(self, message: str, status: str = MessageStatus.NoStatus, msec: int = None) -> None:
        if status != MessageStatus.NoStatus:
            self._status_bar_icon.set_icon(self.get_svg_icon(f"icons/{status}.svg"))
            self._status_bar_icon.set_text(message)
            self._status_bar_icon.start_clear_timer(msec)
        else:
            self._status_bar.show_message(message)

    def insert_widget(self, name: str, widget: QObject, side: int = Index.Start) -> None:
        if name in self._sb_widgets:
            raise PieException(f"Status bar widget \"{name}\" is already registered")

        self._sb_widgets[name] = widget
        self._status_bar.insert_widget(side, widget)

    def insert_permanent_widget(self, name: str, widget: QObject, side: int = Index.Start) -> None:
        if name in self._sb_widgets:
            raise PieException(f"Status bar widget \"{name}\" is already registered")

        self._sb_perm_widgets[name] = widget
        self._status_bar.insert_permanent_widget(side, widget)


def main(parent: "QMainWindow", plugin_path: "Path"):
    return StatusBar(parent, plugin_path)
