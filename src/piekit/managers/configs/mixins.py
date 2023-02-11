from typing import Any, Union

from piekit.structs.etc import SharedSection
from piekit.managers.registry import Managers
from piekit.structs.managers import SysManagersEnum


class ConfigAccessor:
    """
    Config mixin
    """

    def get_config(
        self,
        key: Any,
        default: Any = None,
        section: Union[str, SharedSection] = SharedSection
    ) -> Any:
        return Managers.get(SysManagersEnum.Configs).get(self.section or section, key, default)

    def set_config(self, key: Any, data: Any) -> None:
        Managers.get(SysManagersEnum.Configs).set(self.section, key, data)

    def delete_config(self, key: Any) -> None:
        Managers.get(SysManagersEnum.Configs).delete(self.section, key)

    getConfig = get_config
    setConfig = set_config
    deleteConfig = delete_config
