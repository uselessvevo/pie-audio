import typing
from typing import Union

from piekit.managers.registry import Managers
from piekit.managers.structs import SysManager, Section


class LocalesAccessor:
    """
    Config mixin
    """

    def get_translation(
        self,
        key: typing.Any,
        section: Union[str, Section] = Section.Shared
    ) -> typing.Any:
        return Managers(SysManager.Locales).get(self.section or section, key)

    getTranslation = get_translation
