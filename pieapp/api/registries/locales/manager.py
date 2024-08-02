from pathlib import Path

from pieapp.api.gloader import Global
from pieapp.utils.files import read_json
from pieapp.api.registries.base import BaseRegistry
from pieapp.api.registries.models import SysRegistry, Scope
from pieapp.api.registries.configs.mixins import ConfigAccessorMixin


class LocaleRegistry(BaseRegistry, ConfigAccessorMixin):
    name = SysRegistry.Locales

    def init(self) -> None:
        self._locale = self.get_config("locale.locale", Scope.User, Global.DEFAULT_LOCALE)
        self._translations: dict[str, dict[str, str]] = {}

        self._load_app_locales()
        self._load_plugins_locales(Global.APP_ROOT / Global.PLUGINS_FOLDER_NAME)
        self._load_plugins_locales(Global.USER_ROOT / Global.PLUGINS_FOLDER_NAME)

    def _load_app_locales(self) -> None:
        # Read app/user configuration
        file = Global.APP_ROOT / Global.LOCALES_FOLDER / f"{self._locale}.json"
        self._translations.update({Scope.Shared: read_json(file)})

    def _load_plugins_locales(self, plugins_folder: Path) -> None:
        for plugin_folder in plugins_folder.iterdir():
            file = plugin_folder / Global.LOCALES_FOLDER / f"{self._locale}.json"
            if not file.exists():
                continue

            if not self._translations.get(file.name):
                self._translations[plugin_folder.name] = {}

            self._translations[plugin_folder.name].update(**read_json(file))

    def get(self, scope: str, key: str) -> str:
        if scope not in self._translations:
            return key

        return self._translations[scope].get(key, key)

    def restore(self, *args, **kwargs) -> None:
        self._translations = {}

    @property
    def locale(self):
        return self._locale
