from typing import Union

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget

from pieapp.api.models.plugins import SysPlugin
from pieapp.api.plugins.confpage import ConfigPage
from pieapp.api.models.scopes import Scope
from pieapp.api.registries.locales.helpers import translate


class MenuManagerConfigPage(ConfigPage):
    name = SysPlugin.MenuManager
    root = Scope.Shared

    def get_title(self) -> str:
        return translate("Menu manager")

    def get_icon(self) -> Union[QIcon, None]:
        pass

    def get_page_widget(self) -> QWidget:
        pass
