from __feature__ import snake_case

from PySide6.QtGui import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QGridLayout

from pieapp.api.globals import Global
from pieapp.api.models.themes import IconName
from pieapp.api.registries.themes.mixins import ThemeAccessorMixin

from pieapp.widgets.buttons import Button
from pieapp.widgets.buttons import ButtonRole
from pieapp.api.plugins.widgets import DialogType
from pieapp.api.plugins.widgets import PiePluginWidget
from pieapp.api.registries.locales.helpers import translate


class AboutWidget(PiePluginWidget, ThemeAccessorMixin):
    dialog_type = DialogType.Modal

    def init(self) -> None:
        self.resize(400, 300)

        ok_button = Button(ButtonRole.Primary)
        ok_button.set_text(translate("Ok"))
        ok_button.clicked.connect(self.close)

        pixmap = QPixmap()
        icon_path = self.get_file_path(IconName.App)
        pixmap.load(icon_path)

        icon_label = QLabel()
        icon_label.set_pixmap(pixmap)

        description_label = QLabel()
        description_label.set_text(
            f'{translate("Pie Audio • Simple Audio Editor")} '
            f'({Global.PIEAPP_VERSION})'
        )

        github_link_label = QLabel()
        github_link_label.set_open_external_links(True)
        github_link_label.set_text(f"<a href='{Global.PIEAPP_PROJECT_URL}'>{translate('Project URL')}</a>")

        grid_layout = QGridLayout()
        grid_layout.add_widget(icon_label, 0, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        grid_layout.add_widget(description_label, 1, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        grid_layout.add_widget(github_link_label, 2, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        grid_layout.add_widget(ok_button, 3, 0, alignment=Qt.AlignmentFlag.AlignRight)

        self.set_layout(grid_layout)

    def call(self):
        self.show()
