from pathlib import Path
from dotty_dict import Dotty

from cloudykit.utils.files import read_json
from cloudykit.system.manager import System
from cloudykit.objects.manager import BaseManager


class LocalesManager(BaseManager):
    dependencies = ("userconfigs",)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._locale: str = System.registry.userconfigs.get(
            key="locales.locale",
            default=System.config.DEFAULT_LOCALE
        )
        self._files: dict = {}
        self._translations: Dotty = Dotty({})

    def mount(self, root: Path = System.root, section: str = System.config.SHARED_TYPE) -> None:
        files = (root / System.config.LOCALES_FOLDER_NAME / self._locale).rglob("*.json")
        for file in files:
            if not self._translations.get(section):
                self._translations[section] = {}

            self._translations[section].update(**read_json(file))
            self._files.update({str(file): section})

    def unmount(self) -> None:
        self._translations = Dotty({})

    def reload(self) -> None:
        self.unmount()
        self.reload_files(full_house=True)
        self.mount()

    def reload_files(self, *files: tuple[str], full_house: bool = False) -> None:
        files: tuple = self._files.keys() if full_house else files
        files_data = {k: v for (k, v) in self._files.items() if k in files}
        for file, section in files_data.items():
            self._translations[section].update(**read_json(file))
            self._logger.info(f"Reading {file} file for {section} section")
        
    def get(self, key: str, section: str = "shared") -> str:
        try:
            return self._translations[section][key]
        except KeyError:
            return key

    @property
    def locale(self):
        return self._locale
