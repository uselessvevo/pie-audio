from pathlib import Path

from pieapp.api.gloader import Global
from pieapp.helpers.files import read_json
from pieapp.api.registries.base import BaseRegistry
from pieapp.api.registries.models import SysRegistry, Scope
from pieapp.api.registries.configs.mixins import ConfigAccessorMixin


class LocaleRegistry(BaseRegistry, ConfigAccessorMixin):
    name = SysRegistry.Locales

    def __init__(self) -> None:
        self._locale = self.get_config("locale.locale", Scope.User, Global.DEFAULT_LOCALE)
        self._roots: set[Path] = set()
        self._translations: dict[str, dict[str, str]] = {}

    def init(self) -> None:
        self._load_app_locales()
        self._load_plugins_locales(Global.APP_ROOT / Global.PLUGINS_FOLDER_NAME)
        self._load_plugins_locales(Global.USER_ROOT / Global.PLUGINS_FOLDER_NAME)

    def _load_app_locales(self) -> None:
        # Read app/user configuration
        self._roots.add(Global.APP_ROOT)

        for file in (Global.APP_ROOT / Global.LOCALES_FOLDER / self._locale).rglob("*.json"):
            scope = Scope.Shared
            if not self._translations.get(scope):
                self._translations[scope] = {}

            self._translations[file.stem].update(**read_json(file))

    def _load_plugins_locales(self, plugins_folder: Path) -> None:
        for plugin_folder in plugins_folder.iterdir():
            self._roots.add(plugin_folder)

            for file in (plugin_folder / Global.LOCALES_FOLDER / self._locale).rglob("*.json"):
                if not self._translations.get(file.name):
                    self._translations[file.stem] = {}

                self._translations[file.stem].update(**read_json(file))

    def shutdown(self, *args, **kwargs) -> None:
        self._translations = {}

    def reload(self) -> None:
        self.shutdown()
        self.init()

    def get(self, scope: str, key: str) -> str:
        if scope not in self._translations:
            return key

        return self._translations[scope].get(key, key)

    @property
    def locale(self):
        return self._locale
