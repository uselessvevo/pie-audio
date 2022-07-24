from dotty_dict import Dotty

from cloudykit.abstracts.manager import IManager
from cloudykit.managers.system.manager import System
from cloudykit.utils.files import read_json


class LocalesManager(IManager):
    name = 'locales'

    def __init__(self, parent=None) -> None:
        self._parent = parent
        self._locale = System.userconfig.get(
            key='locales.locale',
            default=System.config.get('locales.default_locale')
        )
        self._dictionary: Dotty = Dotty({})

    def mount(self) -> None:
        """ Mount object """
        files = (self._parent.root / 'locales' / self._locale).rglob('*.json')
        for file in files:
            self._dictionary.update(**read_json(file))

    def unmount(self, *args, **kwargs) -> None:
        self._dictionary = Dotty({})

    def reload(self, *args, **kwargs) -> None:
        self.unmount()
        self.mount()
        
    def get(self, key: str) -> str:
        return self._dictionary.get(key, key)

    def read(self, root: str):
        root = System.root / root / 'locales' / self._locale
        dictionary = {}

        for trans_file in root.glob('*.json'):
            dictionary.update(**read_json(trans_file))

        self._dictionary = Dotty(dictionary)

    @property
    def locale(self):
        return self._locale
