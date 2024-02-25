from __feature__ import snake_case

from PySide6 import QtWidgets

from pieapp.api.managers.structs import Section
from pieapp.api.managers.locales.helpers import translate
from pieapp.api.managers.configs.mixins import ConfigAccessorMixin


class ThemeWizardPage(ConfigAccessorMixin, QtWidgets.QWizardPage):
    section = Section.Shared

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self._current_theme: str = None

        rb_hbox = QtWidgets.QHBoxLayout()
        self._rb_dark_theme = QtWidgets.QRadioButton()
        self._rb_dark_theme.toggled.connect(self.on_radio_button_click)
        self._rb_dark_theme.set_style_sheet("QRadioButton {font-size: 15pt;}")
        self._rb_dark_theme.set_text(translate("Dark theme"))
        self._rb_dark_theme.set_checked(True)
        self._rb_dark_theme.theme = "dark theme"

        self._rb_light_theme = QtWidgets.QRadioButton()
        self._rb_light_theme.toggled.connect(self.on_radio_button_click)
        self._rb_light_theme.set_style_sheet("QRadioButton {font-size: 15pt;}")
        self._rb_light_theme.set_text(translate("Light theme"))
        self._rb_light_theme.theme = "light theme"

        rb_hbox.add_widget(self._rb_dark_theme)
        rb_hbox.add_widget(self._rb_light_theme)

        theme_label = QtWidgets.QLabel(translate("Select theme"))
        theme_label.set_style_sheet("QLabel{font-size: 25pt; padding-bottom: 20px;}")

        layout = QtWidgets.QVBoxLayout()
        layout.add_layout(rb_hbox)
        self.set_layout(layout)

    def on_radio_button_click(self) -> None:
        radio_button = self.sender()
        if radio_button.is_checked():
            self._current_theme = getattr(radio_button, "theme", "dark theme")

    def finish(self) -> None:
        self.set_config(
            scope=Section.Root,
            section=Section.User,
            key="assets.theme",
            data=self._current_theme
        )
        self.save_config(
            scope=Section.Root,
            section=Section.User
            )

