import typing
from typing import Union

from piekit.managers.registry import Managers
from piekit.structs.etc import SharedSection
from piekit.structs.managers import SysManagersEnum


class LocalesAccessor:
    """
    Config mixin
    """

    def get_translation(
        self,
        key: typing.Any,
        section: Union[str, SharedSection] = SharedSection
    ) -> typing.Any:
        return Managers.get(SysManagersEnum.Locales).get(self.section or section, key)

    getTranslation = get_translation
