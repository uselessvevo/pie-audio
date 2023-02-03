from typing import Any, Union

from cloudykit.system.manager import System
from cloudykit.managers.configs.manager import ConfigManager
from cloudykit.system.types import SharedSection


class ConfigAccessor:
    """
    Config mixin
    """

    def __init__(self, section: str) -> None:
        self._section = section
        self._config: ConfigManager = System.registry.configs

    def get_config(
        self,
        key: Any,
        default: Any = None,
        section: Union[str, SharedSection] = SharedSection
    ) -> Any:
        return self._config.get(self._section, key, default)

    def set_config(self, key: Any, data: Any) -> None:
        self._config.set(self._section, key, data)

    def delete_config(self, key: Any) -> None:
        self._config.delete(self._section, key)

    getConfig = get_config
    setConfig = set_config
    deleteConfig = delete_config

    @property
    def config(self) -> ConfigManager:
        return self._config
