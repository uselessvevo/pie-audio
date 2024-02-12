from typing import Any, Union

from pieapp.api.managers.registry import Managers
from pieapp.api.managers.structs import SysManager, Section


class LocalesAccessorMixin:
    """
    ConfigManager accessor mixin
    """

    def translate(
        self,
        key: Any,
        section: Union[str, Section] = Section.Shared
    ) -> Any:
        return Managers(SysManager.Locales).get(section or self.section, key)
