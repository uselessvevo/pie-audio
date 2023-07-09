from piekit.managers.confpages.structs import ConfigurationPage
from piekit.managers.confpages.manager import ConfigPageManager


class ConfigurationPageAccessor:
    """
    Configuration pages accessor. 
    Use this mixin to allow your plugin register other plugins configuration pages
    """

    def add_section(self, section: str) -> None:
        pass

    def remove_section(self, section: str) -> None:
        pass

    def add_page(self, section: str, page: ConfigurationPage) -> None:
        pass

    def remove_page(self, section: str, page: ConfigurationPage) -> None:
        pass

    def get_all_sections(self) -> list[str]:
        pass

    def get_all_pages(self) -> list[ConfigurationPage]:
        pass
