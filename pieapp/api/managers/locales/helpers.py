from pieapp.api.managers.structs import Section
from pieapp.api.managers.registry import Registries
from pieapp.api.managers.structs import SysRegistry


def translate(text: str, section: Section.Shared = Section.Shared) -> str:
    return Registries(SysRegistry.Locales).get(section, text)
