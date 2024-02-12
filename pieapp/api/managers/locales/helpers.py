from pieapp.api.managers.structs import Section
from pieapp.api.managers.registry import Managers
from pieapp.api.managers.structs import SysManager


def translate(text: str, section: Section.Shared = Section.Shared) -> str:
    return Managers(SysManager.Locales).get(section, text)
