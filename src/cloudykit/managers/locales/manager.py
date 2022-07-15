from dotty_dict import Dotty

from cloudykit.abstracts.manager import IManager
from cloudykit.system.manager import System
from cloudykit.utils.files import read_json


class LocalesManager(IManager):
    name = 'locales'

    def __init__(self) -> None:
        self._locale: str = None
        self._dictionary: Dotty = None

    def init(self, *args, **kwargs) -> None:
        self._locale = System.get(
            key='user.current_locale',
            default=System.get('locales.default_locale')
        )
        self._dictionary: Dotty = Dotty({})
        self.read(System.root / 'locales' / self._locale)

    def mount(self, parent=None) -> None:
        """ Mount object """
        files = (parent.root / 'plugin/configs').rglob('*.json')
        for file in files:
            if parent.name in self._dictionary:
                raise KeyError(f'Plugin "{parent.name}" already mounted')
            self._dictionary[parent.name] = read_json(file)

    def unmount(self, parent=None) -> None:
        self._dictionary.pop(parent.name)
        
    def get(self, key: str) -> str:
        return self._dictionary.get(key, key)

    def read(self, root: str):
        root = System.root / root / 'plugin/locales' / self._locale
        dictionary = {}

        for trans_file in root.glob('*.json'):
            dictionary.update(**read_json(trans_file))

        self._dictionary = Dotty(dictionary)

    @property
    def locale(self):
        return self._locale
