from cloudykit.abstracts.component import IComponent
from cloudykit.objects.registry import ManagerRegistry


class MenuComponent(IComponent):
    name = 'cloudyff_menu'

    def __init__(self, parent=None) -> None:
        self._managers = ManagerRegistry(self, as_mixin=True)

    def mount(self, parent=None) -> None:
        self._managers.mount(
            'cloudykit.managers.assets.manager.AssetsManager',
            'cloudykit.managers.configs.manager.ConfigsManager',
            'cloudykit.managers.locales.manager.LocalesManager'
        )

    def unmount(self, parent=None) -> None:
        pass

    def register(self, obj: object) -> None:
        pass
