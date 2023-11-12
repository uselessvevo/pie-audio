from piekit.managers.structs import Section
from piekit.managers.registry import Managers
from piekit.managers.structs import SysManager


def translate(text: str, section: Section.Shared = Section.Shared) -> str:
    return Managers(SysManager.Locales).get(section, text)
