from __feature__ import snake_case

import os

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QMainWindow, QApplication

from pieapp.api.globals import Global
from pieapp.api.managers.structs import Section
from pieapp.api.managers.registry import Managers
from pieapp.api.managers.locales.helpers import translate
from pieapp.api.managers.configs.mixins import ConfigAccessorMixin
from pieapp.api.managers.themes.mixins import ThemeAccessorMixin
from pieapp.widgets.messagebox import MessageCheckBox


class MainWindow(ConfigAccessorMixin, ThemeAccessorMixin, QMainWindow):

    def __init__(self) -> None:
        QMainWindow.__init__(self)

        # Set windows taskbar icon
        if os.name == "nt":
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                Global.PIEAPP_ORGANIZATION_DOMAIN
            )

        self.set_minimum_size(*Global.DEFAULT_MIN_WINDOW_SIZE)

        settings = QSettings()
        self.restore_geometry(settings.value("geometry", self.save_geometry()))

        self.set_window_title(
            f'{translate("Pie Audio • Simple Audio Editor")} '
            f'({Global.PIEAPP_VERSION})'
        )
        self.set_window_icon(self.get_svg_icon("icons/bolt.svg", color="#f5d97f"))

    def close_event(self, event) -> None:
        if self.close_handler(True):
            event.accept()
        else:
            event.ignore()

    def close_handler(self, cancellable: bool = True) -> bool:
        show_exit_dialog = self.get_config(
            key="ui.show_exit_dialog",
            default=True,
            scope=Section.Root,
            section=Section.User
        )
        if cancellable and show_exit_dialog:
            message_box = MessageCheckBox(
                parent=self,
                window_title=translate("Exit"),
                message_text=translate("Are you sure you want to exit?"),
            )
            message_box.set_check_box_text(translate("Don't show this message again?"))
            message_box.exec()
            if message_box.is_checked():
                self.set_config("ui.show_exit_dialog", False, scope=Section.Root, section=Section.User)

            if message_box.clicked_button() == message_box.no_button:
                return False

        settings = QSettings()
        settings.set_value("geometry", self.save_geometry())
        self.save_config(Section.Root, Section.User, create=True)

        QApplication.process_events()
        Managers.shutdown(full_house=True)

        return True
