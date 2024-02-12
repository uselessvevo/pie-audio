from pieapp.api.plugins import PieObject
from pieapp.api.structs.plugins import Plugin
from pieapp.api.plugins.helpers import get_plugin
from pieapp.api.plugins.decorators import on_plugin_event

from appearance.confpage import AppearanceConfigPage


class Appearance(PieObject):
    name = Plugin.Appearance
    requires = [Plugin.Preferences]

    def get_config_page(self) -> "ConfigPage":
        return AppearanceConfigPage()

    @on_plugin_event(target=Plugin.Preferences)
    def _on_preferences_available(self) -> None:
        preferences = get_plugin(Plugin.Preferences)
        preferences.register_config_page(self)

    @on_plugin_event(target=Plugin.Preferences, event="on_teardown")
    def _on_preferences_teardown(self) -> None:
        preferences = get_plugin(Plugin.Preferences)
        preferences.deregister_config_page(self)


def main(parent: "QMainWindow", plugin_path: "Path"):
    return Appearance(parent, plugin_path)
