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
        section: Union[str, Section] = Section.Inner
    ) -> Any:
        return Managers(SysManager.Configs).get(self.name, section, key, default)

    def get_shared_config(
        self,
        key: Any,
        default: Any = None,
        section: Union[Section.Inner, Section.User] = Section.Shared
    ) -> Any:
        return Managers(SysManager.Configs).get_shared(section, key, default)

    def set_config(self, key: Any, data: Any) -> None:
        Managers(SysManager.Configs).set(self.name, key, data)

    def delete_config(self, key: Any) -> None:
        Managers(SysManager.Configs).delete(self.name, key)

    def save_config(self, data: dict, create: bool = False) -> None:
        Managers(SysManager.Configs).save(self.name, data, create)

    getConfig = get_config
    getSharedConfig = get_shared_config
    setConfig = set_config
    saveConfig = save_config
    deleteConfig = delete_config
