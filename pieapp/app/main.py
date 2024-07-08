import uuid
from pathlib import Path

from __feature__ import snake_case

import os

from PySide6.QtCore import QSettings, Signal
from PySide6.QtWidgets import QMainWindow, QApplication

from pieapp.api.gloader import Global
from pieapp.api.models.themes import ThemeProperties
from pieapp.api.plugins import Plugins
from pieapp.api.registries.models import Scope
from pieapp.api.registries.registry import Registry
from pieapp.api.registries.locales.helpers import translate
from pieapp.api.registries.configs.mixins import ConfigAccessorMixin
from pieapp.api.registries.themes.mixins import ThemeAccessorMixin
from pieapp.helpers.files import delete_directory, create_temp_directory
from pieapp.widgets.messagebox import MessageCheckBox


class MainWindow(ConfigAccessorMixin, ThemeAccessorMixin, QMainWindow):
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

        self.set_minimum_size(*Global.DEFAULT_MIN_WINDOW_SIZE)

        settings = QSettings()
        self.restore_geometry(settings.value("geometry", self.save_geometry()))

        self.set_window_title(
            f'{translate("Pie Audio • Simple Audio Editor")} '
            f'({Global.PIEAPP_VERSION} - {Global.PIEAPP_VERSION_STAGE})'
        )
        self.set_window_icon(self.get_svg_icon(
            key="icons/bolt.svg",
            color=self.get_theme_property(ThemeProperties.AppIconColor)
        ))

    def init(self) -> None:
        root_temp_directory = self.get_config(
            "folders.temp_directory",
            Scope.User,
            Global.USER_ROOT / Global.DEFAULT_TEMP_FOLDER_NAME
        )
        workflow_temp_directory = create_temp_directory(root_temp_directory)
        self.update_config("workflow.temp_directory", Scope.User, str(workflow_temp_directory), temp=True)
        Plugins.init_plugins()
        self.sig_on_main_window_show.emit()

    def close_event(self, event) -> None:
        if self.close_handler(True):
            self.sig_on_main_window_close.emit()
            temp_directory = self.get_config("workflow.temp_directory", Scope.User)
            delete_directory(temp_directory)
            event.accept()
        else:
            event.ignore()

    def close_handler(self, cancellable: bool = True) -> bool:
        show_exit_dialog = self.get_config("ui.show_exit_dialog", Scope.User, True)
        if cancellable and show_exit_dialog:
            message_box = MessageCheckBox(
                parent=self,
                window_title=translate("Exit"),
                message_text=translate("Are you sure you want to exit?"),
            )
            message_box.set_check_box_text(translate("Don't show this message again?"))
            message_box.exec()
            if message_box.is_checked():
                self.update_config("ui.show_exit_dialog", Scope.User, False, True)

            if message_box.clicked_button() == message_box.no_button:
                return False

        settings = QSettings()
        settings.set_value("geometry", self.save_geometry())

        QApplication.process_events()

        return True
