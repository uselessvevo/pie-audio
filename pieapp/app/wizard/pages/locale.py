from __feature__ import snake_case

from PySide6 import QtWidgets

from pieapp.api.gloader import Global
from pieapp.utils.qt import restart_application
from pieapp.api.registries.configs.mixins import ConfigAccessorMixin
from pieapp.api.registries.locales.helpers import translate
from pieapp.api.registries.models import Scope


class LocaleWizardPage(
    ConfigAccessorMixin,
    QtWidgets.QWizardPage
):
    scope = Scope.Shared

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self._parent = parent
        self._locales = Global.LOCALES
        self._cur_locale = self.get_config("locale.locale", Scope.User, default=Global.DEFAULT_LOCALE)
        self._locales_reversed = {v: k for (k, v) in self._locales.items()}

        self.combo_box = QtWidgets.QComboBox()
        self.combo_box.set_style_sheet("QComboBox{font-size: 15pt;}")
        self.combo_box.insert_item(0, self._locales.pop(self._cur_locale))
        self.combo_box.add_items([self._locales.get(i) for (i, _) in self._locales.items()])
        self.combo_box.currentIndexChanged.connect(self.finish)

        self.locale_label = QtWidgets.QLabel(translate("Select locale"))
        self.locale_label.set_style_sheet("QLabel{font-size: 25pt; padding-bottom: 20px;}")

        layout = QtWidgets.QVBoxLayout()
        layout.add_widget(self.locale_label)
        layout.add_widget(self.combo_box)
        self.set_layout(layout)

    def finish(self):
        new_locale = self._locales_reversed.get(self.combo_box.current_text())
        self.update_config("locale", Scope.User, {"locale": new_locale})
        self.save_config(Scope.User)
        if self._cur_locale != new_locale:
            restart_application()

        return new_locale
