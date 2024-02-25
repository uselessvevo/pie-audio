from typing import Union, Any

from pieapp.api.managers.registry import Registries
from pieapp.api.managers.structs import Section, SysRegistry


def get_config(
    key: Any,
    default: Any = None,
    temp: bool = False,
    scope: Union[str, Section.Root] = None,
    section: Union[Section.Inner, Section.User] = Section.Inner,
) -> Any:
    return Registries(SysRegistry.Configs).get(scope, section, key, default, temp=temp)


def set_config(
    key: Any,
    data: Any,
    temp: bool = False,
    scope: Union[str, Section.Root] = None,
    section: Union[Section.Inner, Section.User] = Section.Inner,
) -> None:
    Registries(SysRegistry.Configs).update(scope, section, key, data, temp=temp)


def delete_config(
    key: Any,
    scope: Union[str, Section.Root] = None,
    section: Union[Section.Inner, Section.User] = Section.Inner,
) -> None:
    Registries(SysRegistry.Configs).delete(scope, section, key)


def save_config(
    scope: Union[str, Section.Root] = None,
    section: Union[Section.Inner, Section.User] = Section.Inner,
    temp: bool = False,
    create: bool = False
) -> None:
    Registries(SysRegistry.Configs).save(scope, section, temp=temp, create=create)


def restore_config(
    key: Any = None,
    scope: Union[str, Section.Root] = None,
    section: Union[Section.Inner, Section.User] = Section.Inner
) -> None:
    Registries(SysRegistry.Configs).restore(scope, section, key)
