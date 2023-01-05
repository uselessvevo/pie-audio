from dotty_dict import Dotty

from cloudykit.utils.files import read_json
from cloudykit.system.manager import System
from cloudykit.objects.manager import BaseManager


class LocalesManager(BaseManager):
    dependencies = ("userconfigs",)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._locale = System.registry.userconfigs.get(
            key="locales.locale",
            default=System.config.DEFAULT_LOCALE
        )
        self._translations: dict = {}

    def mount(self, section: str = "shared") -> None:
        files = (System.root / System.config.LOCALES_FOLDER / self._locale).rglob("*.json")
        for file in files:
            if not self._translations.get(section):
                self._translations[section] = {}

            self._translations[section]["$FILE$"] = file.name
            self._translations[section].update(**read_json(file))

    def unmount(self, *args, **kwargs) -> None:
        self._translations = Dotty({})

    def reload(self, *args, **kwargs) -> None:
        self.unmount()
        self.mount()
        
    def get(self, key: str, section: str = "shared") -> str:
        try:
            return self._translations[section][key]
        except KeyError:
            return key

    def read(self, root: str = None, section: str = "shared"):
        root = System.root / root / System.config.LOCALES_FOLDER / self._locale
        dictionary = {}

        for trans_file in root.glob("*.json"):
            dictionary.update(**read_json(trans_file))

        self._translations[section] = dictionary

    @property
    def locale(self):
        return self._locale
