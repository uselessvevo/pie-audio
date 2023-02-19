import typing
from typing import Union

from piekit.managers.registry import Managers
from piekit.managers.types import SysManagers, SharedSection


class LocalesAccessor:
    """
    Config mixin
    """

    def get_translation(
        self,
        key: typing.Any,
        section: Union[str, SharedSection] = SharedSection
    ) -> typing.Any:
        return Managers.get(SysManagers.Locales).get(self.section or section, key)

    getTranslation = get_translation
