from __feature__ import snake_case

from pieapp.api.models.plugins import SysPlugin

from pieapp.api.plugins.helpers import get_plugin
from pieapp.api.plugins.plugins import PiePlugin
from pieapp.api.registries.menus.mixins import MenuAccessorMixin
from pieapp.api.registries.configs.mixins import ConfigAccessorMixin
from pieapp.api.plugins.decorators import on_plugin_available, on_plugin_shutdown

from menuman.confpage import MenuManagerConfigPage


class MenuManager(PiePlugin, ConfigAccessorMixin, MenuAccessorMixin):
    name = SysPlugin.MenuManager
    requires = [SysPlugin.Preferences]

    # @on_plugin_available(plugin=SysPlugin.Preferences)
    def _on_preferences_available(self) -> None:
        preferences = get_plugin(SysPlugin.Preferences)
        preferences.register_config_page(MenuManagerConfigPage)

    # @on_plugin_shutdown(plugin=SysPlugin.Preferences)
    def _on_preferences_teardown(self) -> None:
        preferences = get_plugin(SysPlugin.Preferences)
        preferences.deregister_config_page(MenuManagerConfigPage)


def main(parent, plugin_path):
    return MenuManager(parent, plugin_path)

