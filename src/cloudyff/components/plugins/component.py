from cloudykit.abstracts.component import IComponent
from cloudykit.managers.plugins.manager import PluginsManager


class PluginsComponent(IComponent):

    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent
        self._pluginManager = PluginsManager()

    def mount(self):
        self._pluginManager.mount()

    def init(self):
        pass
