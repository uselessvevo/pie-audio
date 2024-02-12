from __feature__ import snake_case

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QWidget, QFormLayout

from pieapp.api.globals.loader import Global
from pieapp.api.structs.plugins import Plugin
from pieapp.api.managers.structs import Section
from pieapp.api.plugins.confpage import ConfigPage
from pieapp.api.managers.locales.helpers import translate
from pieapp.api.managers.themes.mixins import ThemeAccessorMixin
from pieapp.api.managers.configs.mixins import ConfigAccessorMixin


class AppearanceConfigPage(
    ConfigPage,
    ConfigAccessorMixin,
    ThemeAccessorMixin
):
    name = Plugin.Appearance
    section = Section.Root

    def get_icon(self) -> "QIcon":
        return self.get_svg_icon("icons/app.svg", section=self.name)

    def get_title(self) -> str:
        return translate("Appearance")

    def get_page_widget(self) -> QWidget:
        return self._main_widget

    def init(self) -> None:
        self._main_widget = QWidget()
        self._form_layout = QFormLayout()

        self._locales = Global.LOCALES
        self._cur_locale = self.get_config(
            key="locale.locale",
            default=Global.DEFAULT_LOCALE,
            scope=Section.Root,
            section=Section.User
        )
        self._locales_reversed = {v: k for (k, v) in self._locales.items()}

        self._locales_cbox = QComboBox()
        self._locales_cbox.set_object_name("PreferencesComboBox")
        self._locales_cbox.insert_item(0, self._locales.pop(self._cur_locale))
        self._locales_cbox.add_items([self._locales.get(i) for (i, _) in self._locales.items()])
        self._locales_cbox.currentIndexChanged.connect(self._locales_cbox_connect)

        themes = self.get_themes()
        self._theme_cbox = QComboBox()
        self._theme_cbox.set_object_name("PreferencesComboBox")
        self._theme_cbox.add_items(themes)
        self._theme_cbox.set_current_text(self.get_config(
            "assets.theme", scope=Section.Root, section=Section.User
        ))
        self._theme_cbox.currentIndexChanged.connect(self._theme_cbox_connect)

        self._form_layout.add_row(translate("Language"), self._locales_cbox)
        self._form_layout.add_row(translate("Theme"), self._theme_cbox)
        self._main_widget.set_layout(self._form_layout)

    def _theme_cbox_connect(self) -> None:
        new_theme = self._theme_cbox.current_text()
        self.set_config(
            scope=Section.Root,
            section=Section.User,
            key="assets.theme",
            data=new_theme,
            temp=True
        )
        self.set_modified(True)

    def _locales_cbox_connect(self) -> None:
        new_locale = self._locales_reversed.get(self._locales_cbox.current_text())
        self.set_config(
            scope=Section.Root,
            section=Section.User,
            key="locale.locale",
            data=new_locale,
            temp=True
        )
        self.set_modified(True)

    def accept(self) -> None:
        self.save_config(scope=Section.Root, section=Section.User, temp=True)
        self.set_modified(False)

    def cancel(self) -> None:
        self.restore_config()
