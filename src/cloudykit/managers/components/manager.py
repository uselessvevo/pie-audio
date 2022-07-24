from cloudykit.abstracts.manager import IManager


class ComponentsManager(IManager):
    name = 'components'

    def __init__(self, parent=None) -> None:
        self._parent = parent
        self._components: dict = {}

    def mount(self) -> None:
        pass

    def unmount(self, *args, **kwargs) -> None:
        pass

    def reload(self, *args, **kwargs) -> None:
        pass

    def destroy(self, *args, **kwargs) -> None:
        pass
