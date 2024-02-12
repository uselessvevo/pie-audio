from typing import Any, Union

from pieapp.api.managers.registry import Managers
from pieapp.api.managers.structs import SysManager, Section


class ConfigAccessorMixin:
    """
    Config mixin made for PiePlugin based plugins/containers
    """

    def get_config(
        self,
        key: Any,
        default: Any = None,
        temp: bool = False,
        scope: Union[str, Section.Root] = None,
        section: Union[Section.Inner, Section.User] = Section.Inner,
    ) -> Any:
        return Managers(SysManager.Configs).get(scope or self.name, section, key, default, temp=temp)

    def set_config(
        self,
        key: Any,
        data: Any,
        temp: bool = False,
        scope: Union[str, Section.Root] = None,
        section: Union[Section.Inner, Section.User] = Section.Inner,
    ) -> None:
        Managers(SysManager.Configs).set(scope or self.name, section, key, data, temp=temp)

    def delete_config(
        self,
        key: Any,
        scope: Union[str, Section.Root] = None,
        section: Union[Section.Inner, Section.User] = Section.Inner,
    ) -> None:
        Managers(SysManager.Configs).delete(scope or self.name, section, key)

    def save_config(
        self,
        scope: Union[str, Section.Root] = None,
        section: Union[Section.Inner, Section.User] = Section.Inner,
        temp: bool = False,
        create: bool = False
    ) -> None:
        Managers(SysManager.Configs).save(scope or self.name, section, temp=temp, create=create)

    def restore_config(
        self,
        key: Any = None,
        scope: Union[str, Section.Root] = None,
        section: Union[Section.Inner, Section.User] = Section.Inner,
    ) -> None:
        Managers(SysManager.Configs).restore(scope or self.name, section, key)
