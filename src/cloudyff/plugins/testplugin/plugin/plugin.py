from cloudykit.plugins.plugin import GenericPlugin


class TestPlugin(GenericPlugin):
    name = 'testplugin'

    def init(self) -> None:
        pass

    def refresh(self):
        pass
