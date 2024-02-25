from typing import Any, Union

from pieapp.api.managers.registry import Registries
from pieapp.api.managers.structs import SysRegistry, Section


class LocalesAccessorMixin:
    """
    ConfigManager accessor mixin
    """

    def translate(
        self,
        key: Any,
        section: Union[str, Section] = Section.Shared
    ) -> Any:
        return Registries(SysRegistry.Locales).get(section or self.section, key)
