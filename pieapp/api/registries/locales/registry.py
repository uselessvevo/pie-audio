from pathlib import Path

from pieapp.api.globals import Global
from pieapp.api.utils.files import read_json
from pieapp.api.registries.base import BaseRegistry
from pieapp.api.registries.sysregs import SysRegistry
from pieapp.api.models.scopes import Scope
from pieapp.api.registries.configs.mixins import ConfigAccessorMixin


class LocalesRegistryClass(BaseRegistry, ConfigAccessorMixin):
    name = SysRegistry.Locales

    def init(self) -> None:
        self._locale = self.get_app_config("config.locale", Scope.User, Global.DEFAULT_LOCALE)
        self._translations: dict[str, dict[str, str]] = {}

        self.load_app_locales()
        self.load_plugins_locales(Global.APP_ROOT / Global.PLUGINS_DIR_NAME)
        self.load_plugins_locales(Global.USER_ROOT / Global.PLUGINS_DIR_NAME)

    def load_app_locales(self) -> None:
        # Read app/user configuration
        file = Global.APP_ROOT / Global.LOCALES_DIR / f"{self._locale}.json"
        self._translations.update({Scope.Shared: read_json(file)})

    def load_plugins_locales(self, plugins_folder: Path) -> None:
        for plugin_folder in plugins_folder.iterdir():
            file = plugin_folder / Global.LOCALES_DIR / f"{self._locale}.json"
            if not file.exists():
                continue

            if not self._translations.get(file.name):
                self._translations[plugin_folder.name] = {}

            self._translations[plugin_folder.name].update(**read_json(file))

    def get(self, scope: str, key: str) -> str:
        if scope not in self._translations:
            return key

        return self._translations[scope].get(key, key)

    def restore(self) -> None:
        self._translations = {}

    @property
    def locale(self):
        return self._locale


LocaleRegistry = LocalesRegistryClass()
