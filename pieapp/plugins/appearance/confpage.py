from __feature__ import snake_case

from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QWidget, QFormLayout

from pieapp.api.gloader import Global
from pieapp.api.models.plugins import SysPlugin
from pieapp.api.registries.models import Scope
from pieapp.api.plugins.confpage import ConfigPage
from pieapp.api.registries.locales.helpers import translate
from pieapp.api.registries.themes.mixins import ThemeAccessorMixin
from pieapp.api.registries.configs.mixins import ConfigAccessorMixin


class AppearanceConfigPage(
    ConfigPage,
    ConfigAccessorMixin,
    ThemeAccessorMixin
):
    name = SysPlugin.Appearance
    scope = Scope.Root

    def get_icon(self) -> "QIcon":
        return self.get_svg_icon("icons/app.svg", scope=self.name)

    def get_title(self) -> str:
        return translate("Appearance")

    def get_page_widget(self) -> QWidget:
        return self._main_widget

    def init(self) -> None:
        self._main_widget = QWidget()
        self._form_layout = QFormLayout()

        self._locales = Global.LOCALES
        self._cur_locale = self.get_config("locale.locale", Scope.User, Global.DEFAULT_LOCALE)
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
        self._theme_cbox.set_current_text(self.get_config("assets.theme", Scope.User))
        self._theme_cbox.currentIndexChanged.connect(self._theme_cbox_connect)

        self._form_layout.add_row(translate("Language"), self._locales_cbox)
        self._form_layout.add_row(translate("Theme"), self._theme_cbox)
        self._main_widget.set_layout(self._form_layout)

    def _theme_cbox_connect(self) -> None:
        new_theme = self._theme_cbox.current_text()
        self.update_config("assets.theme", Scope.User, new_theme)
        self.set_modified(True)

    def _locales_cbox_connect(self) -> None:
        new_locale = self._locales_reversed.get(self._locales_cbox.current_text())
        self.update_config("locale.locale", new_locale)
        self.set_modified(True)

    def accept(self) -> None:
        self.save_config(Scope.User)
        self.set_modified(False)

    def cancel(self) -> None:
        self.restore_config(Scope.User)
