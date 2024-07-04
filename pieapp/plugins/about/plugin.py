from __feature__ import snake_case

from PySide6.QtGui import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QGridLayout

from pieapp.api.gloader import Global
from pieapp.api.models.themes import ThemeProperties
from pieapp.api.registries.locales.helpers import translate
from pieapp.api.models.menus import MainMenu
from pieapp.api.models.plugins import SysPlugin

from pieapp.widgets.buttons import Button
from pieapp.widgets.buttons import ButtonRole

from pieapp.api.plugins.plugins import PiePlugin
from pieapp.api.plugins.decorators import on_plugin_available

from pieapp.api.registries.models import Scope
from pieapp.api.registries.menus.mixins import MenuAccessorMixin
from pieapp.api.registries.themes.mixins import ThemeAccessorMixin


class About(PiePlugin, MenuAccessorMixin, ThemeAccessorMixin):
    name = SysPlugin.About
    requires = [SysPlugin.MainMenuBar]

    def get_plugin_icon(self) -> "QIcon":
        return self.get_svg_icon(
            key="icons/app.svg",
            scope=self.name,
            color=self.get_theme_property(ThemeProperties.AppIconColor)
        )

    def call(self) -> None:
        self._dialog = QDialog(self._parent)
        self._dialog.set_modal(True)
        self._dialog.set_window_title(translate("About"))
        self._dialog.set_window_icon(self.get_plugin_icon())
        self._dialog.resize(400, 300)

        ok_button = Button(ButtonRole.Primary)
        ok_button.set_text(translate("Ok"))
        ok_button.clicked.connect(self._dialog.close)

        pixmap = QPixmap()
        pixmap.load(self.get_file_path("icons/app.svg"))

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

        self._dialog.set_layout(grid_layout)
        self._dialog.show()

    @on_plugin_available(plugin=SysPlugin.MainMenuBar)
    def on_menu_bar_available(self) -> None:
        self.add_menu_item(
            scope=Scope.Shared,
            menu=MainMenu.Help,
            name="about",
            text=translate("About"),
            triggered=self.call,
            icon=self.get_svg_icon("icons/info.svg"),
        )


def main(parent: "QMainWindow", plugin_path: "Path"):
    return About(parent, plugin_path)
