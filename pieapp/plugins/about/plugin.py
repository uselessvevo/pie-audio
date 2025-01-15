from pieapp.api.models.plugins import SysPlugin

from pieapp.api.models.scopes import Scope
from pieapp.api.models.menus import MainMenu

from pieapp.api.models.themes import IconName
from pieapp.api.models.themes import ThemeProperties

from pieapp.api.plugins.mixins import WidgetsAccessorMixins
from pieapp.api.plugins.plugins import PiePlugin
from pieapp.api.plugins.decorators import on_plugin_available

from pieapp.api.registries.locales.helpers import translate
from pieapp.api.registries.themes.mixins import ThemeAccessorMixin

from about.widgets.mainwidget import AboutWidget


class About(PiePlugin, ThemeAccessorMixin, WidgetsAccessorMixins):
    name = SysPlugin.About
    widget_class = AboutWidget
    requires = [SysPlugin.MainMenuBar]

    def get_plugin_icon(self) -> "QIcon":
        return self.get_svg_icon(IconName.App, self.name, prop=ThemeProperties.AppIconColor)

    @staticmethod
    def get_title() -> str:
        return translate("About")

    @on_plugin_available(plugin=SysPlugin.MainMenuBar)
    def on_menu_bar_available(self) -> None:
        self.add_menu_item(
            scope=Scope.Shared,
            menu=MainMenu.Help,
            name=self.name,
            text=self.get_title(),
            triggered=self.get_widget().call,
            icon=self.get_svg_icon(IconName.App, self.name),
        )


def main(parent, plugin_path):
    return About(parent, plugin_path)
