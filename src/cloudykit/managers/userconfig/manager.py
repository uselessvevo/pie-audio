from dotty_dict import Dotty

from cloudykit.abstracts.manager import IManager


class UserConfigsManager(IManager):
    name = 'user_config'

    def __init__(self) -> None:
        self._user_config: Dotty = None

    def init(self, *args, **kwargs) -> None:
        self._user_config = Dotty({})

    def mount(self, parent=None) -> None:
        pass

    def unmount(self, parent=None) -> None:
        pass
