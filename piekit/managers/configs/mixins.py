from typing import Any, Union

from piekit.managers.registry import Managers
from piekit.managers.structs import SysManagers, Sections


class ConfigAccessor:
    """
    Config mixin
    """

    def get_config(
        self,
        key: Any,
        default: Any = None,
        section: Union[str, Sections] = Sections.Shared
    ) -> Any:
        return Managers(SysManagers.Configs).get(section or self.name, key, default)

    def set_config(self, key: Any, data: Any) -> None:
        Managers(SysManagers.Configs).set(self.name, key, data)

    def delete_config(self, key: Any) -> None:
        Managers(SysManagers.Configs).delete(self.name, key)

    getConfig = get_config
    setConfig = set_config
    deleteConfig = delete_config
