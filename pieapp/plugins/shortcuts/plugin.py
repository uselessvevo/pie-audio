from pieapp.api.models.plugins import SysPlugin
from pieapp.api.models.themes import ThemeProperties, IconName

from pieapp.api.plugins import PiePlugin
from pieapp.api.plugins.helpers import get_plugin
from pieapp.api.plugins.decorators import on_plugin_available
from pieapp.api.plugins.decorators import on_plugin_shutdown

from pieapp.api.registries.locales.helpers import translate
from pieapp.api.registries.themes.mixins import ThemeAccessorMixin

from shortcuts.confpage import ShortcutConfigPage
from shortcuts.confpage import ShortcutBlankConfigPage


class ShortcutsPlugin(PiePlugin, ThemeAccessorMixin):
    name = SysPlugin.ShortcutManager
    requires = [SysPlugin.Preferences]

    def get_name(self) -> str:
        return translate("Shortcuts")

    def get_description(self) -> str:
        return translate("Shortcut manager", scope=self.name)

    def get_plugin_icon(self) -> "QIcon":
        return self.get_svg_icon(
            key=IconName.App,
            scope=self.name,
            prop=ThemeProperties.AppIconColor
        )

    # ConfigPage/Preferences plugin methods

    def on_plugins_ready(self) -> None:
        preferences = get_plugin(SysPlugin.Preferences)
        preferences.update_config_page(ShortcutConfigPage.name, ShortcutConfigPage)

    @on_plugin_available(plugin=SysPlugin.Preferences)
    def _on_preferences_available(self) -> None:
        preferences = get_plugin(SysPlugin.Preferences)
        preferences.register_config_page(ShortcutBlankConfigPage)

    @on_plugin_shutdown(plugin=SysPlugin.Preferences)
    def _on_preferences_teardown(self) -> None:
        preferences = get_plugin(SysPlugin.Preferences)
        preferences.deregister_config_page(ShortcutConfigPage)


def main(parent, plugin_path):
    return ShortcutsPlugin(parent, plugin_path)
