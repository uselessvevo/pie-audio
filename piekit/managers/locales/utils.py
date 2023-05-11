from typing import Any

from piekit.managers.structs import Sections
from piekit.managers.registry import Managers
from piekit.managers.structs import SysManagers


def get_translation(text: str, section: Sections.Shared = Sections.Shared) -> str:
    return Managers(SysManagers.Locales).get(section, text)


getTranslation = get_translation
