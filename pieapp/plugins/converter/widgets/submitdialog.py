from __feature__ import snake_case

from pathlib import Path

from PySide6.QtCore import QSize
from PySide6.QtGui import QAction, Qt

from PySide6.QtWidgets import QStyle, QDialogButtonBox
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QGridLayout

from pieapp.api.models.themes import ThemeProperties, IconName
from pieapp.api.registries.locales.helpers import translate
from pieapp.api.registries.configs.mixins import ConfigAccessorMixin
from pieapp.api.registries.themes.mixins import ThemeAccessorMixin
from pieapp.widgets.buttons import Button, ButtonRole
from pieapp.widgets.spacer import Spacer


class SubmitConvertDialog(QDialog, ConfigAccessorMixin, ThemeAccessorMixin):

    def __init__(self, directory: Path, start_converter_signal: "Signal") -> None:
        super().__init__()
        self.set_modal(True)
        self.set_window_title(translate("Start converter"))
        self.set_window_icon(self.get_svg_icon(IconName.Bolt, ThemeProperties.AppIconColor))

        line_edit_action = QAction()
        line_edit_action.set_icon(self.style().standard_icon(QStyle.StandardPixmap.SP_DirIcon))
        # line_edit_action.triggered.connect(self.select_ffmpeg_root_path)

        file_path_button = Button()
        file_path_button.set_icon(self.get_svg_icon(IconName.Folder, prop=ThemeProperties.AppIconColor))
        file_path_button.set_icon_size(QSize(27, 27))
        # start_converter_button.clicked.connect(self._start_downloader_thread)

        file_path_line_edit = QLineEdit()
        file_path_line_edit.set_placeholder_text(translate("Select where output folder will be created"))
        file_path_line_edit.add_action(line_edit_action, QLineEdit.ActionPosition.TrailingPosition)

        accept_button = Button(ButtonRole.Primary)
        accept_button.clicked.connect(start_converter_signal)
        accept_button.set_text(translate("Ok"))

        cancel_button = Button()
        cancel_button.clicked.connect(self.close)
        cancel_button.set_text(translate("Cancel"))

        dialog_button_box = QDialogButtonBox()
        dialog_button_box.add_button(accept_button, QDialogButtonBox.ButtonRole.AcceptRole)
        dialog_button_box.add_button(cancel_button, QDialogButtonBox.ButtonRole.RejectRole)

        grid_layout = QGridLayout()
        grid_layout.set_horizontal_spacing(0)
        grid_layout.set_contents_margins(0, 0, 0, 0)
        grid_layout.add_widget(file_path_line_edit, 0, 0)
        grid_layout.add_widget(Spacer(), 1, 0, Qt.AlignmentFlag.AlignRight)
        grid_layout.add_widget(dialog_button_box, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.set_layout(grid_layout)
        self.exec()
