from typing import Any, Union

from piekit.managers.registry import Managers
from piekit.managers.structs import SysManager, Section


class LocalesAccessorMixin:
    """
    ConfigManager accessor mixin
    """

    def get_translation(
        self,
        key: Any,
        section: Union[str, Section] = Section.Shared
    ) -> Any:
        return Managers(SysManager.Locales).get(section or self.section, key)

    getTranslation = get_translation
