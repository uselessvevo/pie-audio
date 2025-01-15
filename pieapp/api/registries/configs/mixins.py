from typing import Any

from pieapp.api.globals import Global
from pieapp.api.models.scopes import Scope
from pieapp.api.registries.configs.registry import ConfigRegistry


class ConfigAccessorMixin:
    """
    ConfigRegistry mixin with proxy methods
    """

    @staticmethod
    def _build_file_name_and_key(key: str) -> list[str]:
        return key.split(".", 1)

    # Application config proxy methods

    def get_app_config(
        self,
        key: str = None,
        inner_scope: str = Scope.Inner,
        default: Any = None
    ) -> Any:
        file_name, key = self._build_file_name_and_key(key)
        return self._get_config(Scope.Root, inner_scope, file_name, key, default)

    def update_app_config(
        self,
        key: str = None,
        inner_scope: str = Scope.Inner,
        data: Any = None,
        save: bool = False,
        temp: bool = False,
        create: bool = False
    ) -> Any:
        file_name, key = self._build_file_name_and_key(key)
        return self._update_config(Scope.Root, inner_scope, file_name, key, data, save, temp, create)

    def save_app_config(
        self,
        file_name: str = Global.CONFIG_FILE_NAME,
        inner_scope: str = Scope.Inner,
        create: bool = False
    ) -> Any:
        self._save_config(Scope.Root, inner_scope, file_name, create)

    def restore_app_config(
        self,
        file_name: str = Global.CONFIG_FILE_NAME,
        inner_scope: str = Scope.Inner,
    ) -> Any:
        return self._restore_config(Scope.Root, inner_scope, file_name)

    # Plugin config proxy methods

    def get_plugin_config(
        self,
        key: str = None,
        inner_scope: str = Scope.Inner,
        default: Any = None
    ) -> Any:
        file_name, key = self._build_file_name_and_key(key)
        return self._get_config(self.name, inner_scope, file_name, key, default)

    def update_plugin_config(
        self,
        key: str = None,
        inner_scope: str = Scope.Inner,
        data: Any = None,
        save: bool = False,
        temp: bool = False,
        create: bool = False
    ) -> Any:
        file_name, key = self._build_file_name_and_key(key)
        return self._update_config(self.name, inner_scope, file_name, key, data, save, temp, create)

    def save_plugin_config(
        self,
        file_name: str = Global.CONFIG_FILE_NAME,
        inner_scope: str = Scope.Inner,
        create: bool = False
    ) -> Any:
        self._save_config(self.name, inner_scope, file_name, create)

    def restore_plugin_config(
        self,
        file_name: str = Global.CONFIG_FILE_NAME,
        inner_scope: str = Scope.Inner,
    ) -> Any:
        return self._restore_config(Scope.Root, inner_scope, file_name)

    # Private proxy methods

    def _get_config(
        self,
        scope: str, inner_scope: str,
        file_name: str,
        key: str,
        default: Any
    ) -> Any:
        return ConfigRegistry.get(f"{scope}.{inner_scope}.{file_name}", key, default)

    def _update_config(
        self,
        scope: str,
        inner_scope: str,
        file_name: str,
        key: str,
        data: Any,
        save: bool,
        temp: bool = False,
        create: bool = False
    ) -> Any:
        return ConfigRegistry.update(f"{scope}.{inner_scope}.{file_name}", key, data, temp, save, create)

    def _save_config(
        self,
        scope: str,
        inner_scope: str,
        file_name: str,
        create: bool
    ) -> None:
        return ConfigRegistry.save(f"{scope}.{inner_scope}.{file_name}", f"{file_name}.json", create)

    def _restore_config(
        self,
        scope: str,
        inner_scope: str,
        file_name: str
    ) -> Any:
        return ConfigRegistry.restore(f"{scope}.{inner_scope}.{file_name}")
