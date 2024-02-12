from __feature__ import snake_case

from PySide6 import QtWidgets

from pieapp.helpers.qt import restart_application
from pieapp.api.managers.configs.mixins import ConfigAccessorMixin
from pieapp.api.managers.locales.helpers import translate
from pieapp.api.managers.registry import Managers
from pieapp.api.managers.structs import Section, SysManager


class ThemeWizardPage(
    ConfigAccessorMixin,
    QtWidgets.QWizardPage
):
    section = Section.Shared

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.combo_box = QtWidgets.QComboBox()
        self.combo_box.set_style_sheet("QComboBox{font-size: 12pt;}")
        self.combo_box.add_items(Managers(SysManager.Themes).get_themes())
        self.combo_box.currentIndexChanged.connect(self.finish)

        self._cur_theme = self.get_config(
            key="assets.theme",
            default=Managers(SysManager.Themes).get_theme(),
            scope=Section.Root,
            section=Section.User
        )

        theme_label = QtWidgets.QLabel(translate("Select theme"))
        theme_label.set_style_sheet("QLabel{font-size: 25pt; padding-bottom: 20px;}")

        layout = QtWidgets.QVBoxLayout()
        layout.add_widget(theme_label)
        layout.add_widget(self.combo_box)
        self.set_layout(layout)

    def finish(self):
        new_theme = self.combo_box.current_text()
        self.set_config(
            scope=Section.Root,
            section=Section.User,
            key="assets.theme",
            data=new_theme
        )
        self.save_config(
            scope=Section.Root,
            section=Section.User
        )

        if self._cur_theme != new_theme:
            restart_application()

        return self.combo_box.current_text()
