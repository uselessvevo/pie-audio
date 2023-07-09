from typing import Any, Union

from piekit.managers.registry import Managers
from piekit.managers.structs import SysManager, Section


class ConfigAccessor:
    """
    Config mixin
    """

    def get_config(
        self,
        key: Any,
        default: Any = None,
        temp: bool = False,
        section: Union[Section.Inner, Section.User] = Section.Inner,
    ) -> Any:
        return Managers(SysManager.Configs).get(self.name, section, key, default, temp=temp)

    def get_shared_config(
        self,
        key: Any,
        default: Any = None,
        temp: bool = False,
        scope: Union[str, Section.Root] = Section.Root,
        section: Union[Section.Inner, Section.User] = Section.Inner,
    ) -> Any:
        return Managers(SysManager.Configs).get(scope, section, key, default, temp=temp)

    def set_config(
        self,
        key: Any,
        data: Any,
        temp: bool = False,
        section: Union[Section.Inner, Section.User] = Section.Inner,
    ) -> None:
        Managers(SysManager.Configs).set(self.name, section, key, data, temp=temp)

    def delete_config(
        self,
        key: Any,
        section: Union[Section.Inner, Section.User] = Section.Inner,
    ) -> None:
        Managers(SysManager.Configs).delete(self.name, section, key)

    def save_config(
        self,
        section: Union[Section.Inner, Section.User] = Section.Inner,
        temp: bool = False
    ) -> None:
        Managers(SysManager.Configs).save(self.name, section, temp=temp)

    def restore_config(
        self,
        key: Any = None,
        section: Union[Section.Inner, Section.User] = Section.Inner,
    ) -> None:
        Managers(SysManager.Configs).restore(self.name, section, key)

    getConfig = get_config
    getSharedConfig = get_shared_config
    setConfig = set_config
    saveConfig = save_config
    deleteConfig = delete_config
    restoreConfig = restore_config
