from typing import Union

from piekit.managers.registry import Managers
from piekit.managers.structs import SysManager
from piekit.managers.confpages.structs import ConfigPage


ConfigPagesDict = dict[str, dict]
ConfigPagesList = list[dict[str, ConfigPage]]
ConfigPagesUnion = Union[ConfigPagesList, ConfigPagesDict]


class ConfigPageAccessor:
    """
    Configuration pages accessor. 
    Use this mixin to allow your plugin register other plugins configuration pages
    """

    def get_page(self, section: str, page: str) -> Union[ConfigPage, None]:
        return Managers(SysManager.ConfigPages).get_page(section, page)

    def get_pages(self, section: str) -> Union[list[ConfigPage], list]:
        return Managers(SysManager.ConfigPages).get_pages(section)

    def get_all_confpages(self, as_list: bool = False) -> ConfigPagesUnion:
        return Managers(SysManager.ConfigPages).get_all_pages(as_list=as_list)
