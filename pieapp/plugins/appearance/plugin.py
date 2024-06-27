from __feature__ import snake_case

from pieapp.api.plugins import PiePlugin
from pieapp.api.models.plugins import SysPlugin
from pieapp.api.plugins.helpers import get_plugin
from pieapp.api.plugins.decorators import on_plugin_ready
from pieapp.api.plugins.decorators import on_plugin_shutdown

from appearance.confpage import AppearanceConfigPage


class Appearance(PiePlugin):
    name = SysPlugin.Appearance
    requires = [SysPlugin.Preferences]

    @staticmethod
    def get_config_page() -> AppearanceConfigPage:
        return AppearanceConfigPage()

    @on_plugin_ready(plugin=SysPlugin.Preferences)
    def _on_preferences_available(self) -> None:
        preferences = get_plugin(SysPlugin.Preferences)
        preferences.register_config_page(self)

    @on_plugin_shutdown(plugin=SysPlugin.Preferences)
    def _on_preferences_teardown(self) -> None:
        preferences = get_plugin(SysPlugin.Preferences)
        preferences.deregister_config_page(self)


def main(parent: "QMainWindow", plugin_path: "Path"):
    return Appearance(parent, plugin_path)
