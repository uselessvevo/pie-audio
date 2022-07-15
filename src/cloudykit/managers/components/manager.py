from cloudykit.abstracts.manager import IManager


class ComponentsManager(IManager):
    name = 'components'

    def __init__(self) -> None:
        self._components: dict = {}

    def mount(self, parent=None) -> None:
        pass

    def unmount(self, parent=None) -> None:
        pass

    def reload(self, *args, **kwargs) -> None:
        pass

    def destroy(self, *args, **kwargs) -> None:
        pass
