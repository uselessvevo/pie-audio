from typing import Union

from piekit.objects.base import PieObject
from piekit.objects.mixins import MenuMixin
from piekit.objects.mixins import ActionMixin

from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor
from src.piekit.containers.containers import BaseContainer


class BasePlugin(
    PieObject,
    ActionMixin,
    MenuMixin,
    ConfigAccessor,
    LocalesAccessor,
    AssetsAccessor,
):
    # Icon name
    icon: Union[None, str] = "app.svg"

    # By default, description must be written in English
    description: str

    # Container to register on
    container: Union[None, BaseContainer] = None

    def prepareConfigurationPage(self) -> None:
        """ Prepare configuration page widget """
        pass

    # Update methods

    def updateStyle(self) -> None:
        pass

    def updateLocalization(self) -> None:
        pass

    def onCloseEvent(self) -> None:
        self.logger.info("Closing. Goodbye!..")

    def getDescription(self) -> str:
        return self.description or f"{self.__class__.__class__}'s description"
