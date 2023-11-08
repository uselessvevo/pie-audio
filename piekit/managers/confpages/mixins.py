from typing import Union

from piekit.managers.registry import Managers
from piekit.managers.structs import SysManager
from piekit.managers.confpages.structs import ConfigPage


ConfigPagesDict = dict[str, dict]
ConfigPagesList = list[dict[str, ConfigPage]]
ConfigPagesUnion = Union[ConfigPagesList, ConfigPagesDict]


class ConfigPageAccessorMixin:
    """
    Configuration pages accessor. 
    Use this mixin to allow your plugin register other plugins configuration pages
    """

    def get_page(self, section: str, page: str) -> Union[ConfigPage, None]:
        return Managers(SysManager.ConfigPages).get_page(section, page)

    def get_pages(self, section: str) -> Union[list[ConfigPage], list]:
        return Managers(SysManager.ConfigPages).get_pages(section)

    def get_confpages_dict(self) -> dict[str, ConfigPage]:
        return Managers(SysManager.ConfigPages).get_all_pages(as_list=False)

    def get_confpages_list(self) -> list[ConfigPage]:
        return Managers(SysManager.ConfigPages).get_all_pages(as_list=True)