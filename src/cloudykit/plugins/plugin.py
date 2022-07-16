from cloudykit.plugins.base import Plugin


class GenericPlugin(Plugin):
    """ Generic plugin """

    def mount(self) -> None:
        self.managers_registry.mount(
            'cloudykit.managers.assets.manager.AssetsManager',
            'cloudykit.managers.configs.manager.ConfigsManager',
            'cloudykit.managers.locales.manager.LocalesManager'
        )
