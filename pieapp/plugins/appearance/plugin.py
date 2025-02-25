from __feature__ import snake_case

from pieapp.api.plugins import PiePlugin
from pieapp.api.models.plugins import SysPlugin
from pieapp.api.plugins.helpers import get_plugin
from pieapp.api.plugins.decorators import on_plugin_available
from pieapp.api.plugins.decorators import on_plugin_shutdown

from appearance.confpage import AppearanceConfigPage


class AppearancePlugin(PiePlugin):
    name = SysPlugin.Appearance
    requires = [SysPlugin.Preferences]

    @on_plugin_available(plugin=SysPlugin.Preferences)
    def _on_preferences_available(self) -> None:
        preferences = get_plugin(SysPlugin.Preferences)
        preferences.register_config_page(AppearanceConfigPage)

    @on_plugin_shutdown(plugin=SysPlugin.Preferences)
    def _on_preferences_teardown(self) -> None:
        preferences = get_plugin(SysPlugin.Preferences)
        preferences.deregister_config_page(AppearanceConfigPage)


def main(parent, plugin_path):
    return AppearancePlugin(parent, plugin_path)
