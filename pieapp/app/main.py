from __feature__ import snake_case

import os

from PySide6.QtCore import QSettings, Signal, QPoint
from PySide6.QtWidgets import QMainWindow

from pieapp.api.globals import Global
from pieapp.api.models.scopes import Scope
from pieapp.api.models.themes import ThemeProperties, IconName

from pieapp.api.registries.locales.helpers import translate
from pieapp.api.registries.configs.mixins import ConfigAccessorMixin
from pieapp.api.registries.themes.mixins import ThemeAccessorMixin
from pieapp.api.utils.qapp import get_application

from pieapp.widgets.messagebox import MessageBox


class MainWindow(ConfigAccessorMixin, ThemeAccessorMixin, QMainWindow):
    sig_on_before_main_window_show = Signal()
    sig_on_main_window_show = Signal()
    sig_on_main_window_close = Signal()

    def __init__(self) -> None:
        QMainWindow.__init__(self)

        # Set windows taskbar icon
        if os.name == "nt":
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                Global.PIEAPP_ORGANIZATION_DOMAIN
            )

        self.set_minimum_size(*Global.DEFAULT_WINDOW_SIZE)

        settings = QSettings()
        self.restore_geometry(settings.value("geometry", self.save_geometry()))

        self.set_window_title(
            f'{translate("Pie Audio • Simple Audio Editor")} '
            f'({Global.PIEAPP_VERSION} - {Global.PIEAPP_VERSION_STAGE})'
        )
        self.set_window_icon(self.get_svg_icon(IconName.Bolt, prop=ThemeProperties.AppIconColor))

    def init(self) -> None:
        self.sig_on_before_main_window_show.emit()
        self.move_to_primary_screen()
        self.show()
        self.sig_on_main_window_show.emit()

    def close_event(self, event) -> None:
        if self.close_handler(True):
            self.sig_on_main_window_close.emit()
            event.accept()
        else:
            event.ignore()

    def close_handler(self, cancellable: bool = True) -> bool:
        show_exit_dialog = self.get_app_config("config.ui.show_exit_dialog", Scope.User, True)
        if cancellable and show_exit_dialog:
            message_box = MessageBox(
                parent=self,
                window_title=translate("Exit"),
                message_text=translate("Are you sure you want to exit?"),
            )
            message_box.set_check_box_text(translate("Don't show this message again?"))
            message_box.exec()
            if message_box.is_checked():
                self.update_app_config("config.ui.show_exit_dialog", Scope.User, False, True)
                self.sig_on_main_window_close.emit()

            if message_box.clicked_button() == message_box.no_button:
                return False

        settings = QSettings()
        settings.set_value("geometry", self.save_geometry())

        get_application().process_events()

        return True

    def _is_on_visible_screen(self):
        """Detect if the window is placed on a visible screen."""
        x, y = self.geometry().x(), self.geometry().y()
        qapp = get_application().instance()
        current_screen = qapp.screen_at(QPoint(x, y))

        if current_screen is None:
            return False
        else:
            return True

    def move_to_primary_screen(self):
        """Move the window to the primary screen if necessary."""
        if self._is_on_visible_screen():
            return

        qapp = get_application().instance()
        primary_screen_geometry = qapp.primary_screen().available_geometry()
        x, y = primary_screen_geometry.x(), primary_screen_geometry.y()

        if self.is_maximized():
            self.show_normal()

        self.move(QPoint(x, y))

        # With this we want to maximize only the Spyder main window and not the
        # plugin ones, which usually are not maximized.
        if not hasattr(self, "is_window_widget"):
            self.show_maximized()
