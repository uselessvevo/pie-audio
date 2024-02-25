from typing import Any, Union

from pieapp.api.managers.registry import Registries
from pieapp.api.managers.structs import SysRegistry, Section


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
        return Registries(SysRegistry.Configs).get(scope or self.name, section, key, default, temp=temp)

    def set_config(
        self,
        key: Any,
        data: Any,
        temp: bool = False,
        scope: Union[str, Section.Root] = None,
        section: Union[Section.Inner, Section.User] = Section.Inner,
    ) -> None:
        Registries(SysRegistry.Configs).update(scope or self.name, section, key, data, temp=temp)

    def delete_config(
        self,
        key: Any,
        scope: Union[str, Section.Root] = None,
        section: Union[Section.Inner, Section.User] = Section.Inner,
    ) -> None:
        Registries(SysRegistry.Configs).delete(scope or self.name, section, key)

    def save_config(
        self,
        scope: Union[str, Section.Root] = None,
        section: Union[Section.Inner, Section.User] = Section.Inner,
        temp: bool = False,
        create: bool = False
    ) -> None:
        Registries(SysRegistry.Configs).save(scope or self.name, section, temp=temp, create=create)

    def restore_config(
        self,
        key: Any = None,
        scope: Union[str, Section.Root] = None,
        section: Union[Section.Inner, Section.User] = Section.Inner,
    ) -> None:
        Registries(SysRegistry.Configs).restore(scope or self.name, section, key)
