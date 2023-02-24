from piekit.utils.files import read_json
from piekit.system.loader import Config
from piekit.managers.base import BaseManager
from piekit.managers.types import PathConfig, SysManagers
from piekit.managers.registry import Managers


class LocaleManager(BaseManager):
    name = SysManagers.Locales
    dependencies = (SysManagers.Configs,)

    def __init__(self) -> None:
        super().__init__()

        self._locale: str = Managers.configs.get(
            "user", "locales.locale",
            default=Config.DEFAULT_LOCALE
        )
        self._roots: set[PathConfig] = set()
        self._translations: dict[str, dict[str, str]] = {}

    def mount(self, *roots: PathConfig) -> None:
        for root_config in roots:
            self._roots.add(root_config)
            files = (root_config.root / self._locale).rglob(root_config.pattern)
            for file in files:
                section: str = root_config.section

                if not self._translations.get(section):
                    self._translations[section] = {}

                self._translations[file.stem].update(**read_json(str(file)))

    def unmount(self, *args, **kwargs) -> None:
        self._translations = {}

    def reload(self) -> None:
        self.unmount()
        self.mount(*self._roots)

    def get(self, section: str, key: str) -> str:
        if section not in self._translations:
            return key

        return self._translations[section].get(key, key)

    @property
    def locale(self):
        return self._locale
