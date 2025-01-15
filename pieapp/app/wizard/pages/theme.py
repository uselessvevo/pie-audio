from __feature__ import snake_case

from PySide6.QtGui import Qt

from PySide6 import QtWidgets

from pieapp.api.models.scopes import Scope
from pieapp.api.registries.locales.helpers import translate
from pieapp.api.registries.configs.mixins import ConfigAccessorMixin


class ThemeWizardPage(ConfigAccessorMixin, QtWidgets.QWizardPage):
    scope = Scope.Shared

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self._current_theme: str = None

        grid_layout = QtWidgets.QGridLayout()

        theme_label = QtWidgets.QLabel(translate("Select theme"))
        theme_label.set_style_sheet("QLabel{font-size: 25pt; padding-bottom: 20px;}")

        rb_light_theme = QtWidgets.QRadioButton()
        rb_light_theme.toggled.connect(self.on_radio_button_click)
        rb_light_theme.set_style_sheet("QRadioButton {font-size: 15pt;}")
        rb_light_theme.set_text(translate("Light theme"))
        rb_light_theme.set_checked(True)
        rb_light_theme.theme = "light theme"

        rb_dark_theme = QtWidgets.QRadioButton()
        rb_dark_theme.toggled.connect(self.on_radio_button_click)
        rb_dark_theme.set_style_sheet("QRadioButton {font-size: 15pt;}")
        rb_dark_theme.set_text(translate("Dark theme"))
        rb_dark_theme.theme = "dark theme"

        grid_layout.add_widget(theme_label, 0, 0, Qt.AlignmentFlag.AlignTop)
        grid_layout.add_widget(rb_light_theme, 1, 0, Qt.AlignmentFlag.AlignLeft)
        grid_layout.add_widget(rb_dark_theme, 1, 1, Qt.AlignmentFlag.AlignLeft)

        self.set_layout(grid_layout)

    def on_radio_button_click(self) -> None:
        radio_button = self.sender()
        if radio_button.is_checked():
            self._current_theme = getattr(radio_button, "theme", "light theme")

    def finish(self) -> None:
        self.update_app_config("config.theme", Scope.User, self._current_theme, True)
