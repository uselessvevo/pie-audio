from cloudykit.plugins.base import Plugin


class GenericPlugin(Plugin):
    """ Generic plugin """

    def mount(self) -> None:
        """ Basic managers setup """
        from cloudykit.managers.assets.manager import AssetsManager
        from cloudykit.managers.configs.manager import ConfigsManager
        from cloudykit.managers.locales.manager import LocalesManager

        assets = AssetsManager()
        config = ConfigsManager()
        locales = LocalesManager()

        self.managers_registry.mount(config, assets, locales)
