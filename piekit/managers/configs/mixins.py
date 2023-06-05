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
        section: Union[Section.Inner, Section.User] = Section.Inner,
    ) -> Any:
        return Managers(SysManager.Configs).get(self.name, section, key, default)

    def get_shared_config(
        self,
        key: Any,
        default: Any = None,
        scope: Union[str, Section.Root] = Section.Root,
        section: Union[Section.Inner, Section.User] = Section.Inner,
    ) -> Any:
        return Managers(SysManager.Configs).get(scope, section, key, default)

    def set_config(
        self,
        key: Any,
        data: Any,
        section: Union[Section.Inner, Section.User] = Section.Inner,
    ) -> None:
        if section in (Section.Shared, Section.Root):
            raise KeyError(f"Can't set protected section \"{section}\"")

        Managers(SysManager.Configs).set(self.name, section, key, data)

    def delete_config(
        self,
        key: Any,
        section: Union[Section.Inner, Section.User] = Section.Inner,
    ) -> None:
        if section in (Section.Shared, Section.Root):
            raise KeyError(f"Can't delete protected section \"{section}\"")

        Managers(SysManager.Configs).delete(self.name, section, key)

    def save_config(
        self,
        section: Union[Section.Inner, Section.User] = Section.Inner,
        create: bool = False
    ) -> None:
        if section in (Section.Shared, Section.Root):
            raise KeyError(f"Can't delete protected section \"{section}\"")
            
        Managers(SysManager.Configs).save(self.name, section, create)

    getConfig = get_config
    getSharedConfig = get_shared_config
    setConfig = set_config
    saveConfig = save_config
    deleteConfig = delete_config
