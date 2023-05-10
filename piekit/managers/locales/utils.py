from typing import Any

from piekit.managers.registry import Managers
from piekit.managers.structs import SysManagers


def get_translation(text: str, default: Any) -> str:
    return Managers(SysManagers.Locales).get(text, default)


getTranslation = get_translation
