import typing
from typing import Union

from piekit.managers.registry import Managers
from piekit.managers.structs import SysManagers, Sections


class LocalesAccessor:
    """
    Config mixin
    """

    def get_translation(
        self,
        key: typing.Any,
        section: Union[str, Sections] = Sections.Shared
    ) -> typing.Any:
        return Managers(SysManagers.Locales).get(self.section or section, key)

    getTranslation = get_translation
