from cloudykit.plugins.base import BasePlugin
from cloudykit.plugins.mixins import MenuMixin
from cloudykit.plugins.mixins import ActionMixin
from cloudykit.plugins.mixins import ToolButtonMixin
from cloudykit.plugins.mixins import ManagersMixin


class GenericPlugin(
    ManagersMixin,
    MenuMixin,
    ToolButtonMixin,
    ActionMixin,
    BasePlugin,
):
    """ Generic plugin """

    def init(self) -> None:
        pass
