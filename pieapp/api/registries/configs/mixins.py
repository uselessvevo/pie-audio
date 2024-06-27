from typing import Any

from pieapp.api.registries.registry import Registry
from pieapp.api.registries.models import SysRegistry, Scope


class ConfigAccessorMixin:
    """
    ConfigRegistry mixin with proxy methods
    """

    # Root config proxy methods

    def get_config(self, key: str = None, inner_scope: str = Scope.Inner, default: Any = None) -> Any:
        return self._get_config(Scope.Root, inner_scope, key, default)

    def update_config(self, key: str = None, inner_scope: str = Scope.Inner, data: Any = None,
                      save: bool = False, temp: bool = False, create: bool = False) -> Any:
        return self._update_config(Scope.Root, inner_scope, key, data, save, temp, create)

    def save_config(self, inner_scope: str = Scope.Inner, create: bool = False) -> Any:
        self._save_config(Scope.Root, inner_scope, create)

    def restore_config(self, inner_scope: str = Scope.Inner) -> Any:
        return self._restore_config(Scope.Root, inner_scope)

    # Plugin config proxy methods

    def get_plugin_config(self, key: str = None, inner_scope: str = Scope.Inner, default: Any = None) -> Any:
        return self._get_config(self.name, inner_scope, key, default)

    def update_plugin_config(self, key: str = None, inner_scope: str = Scope.Inner, data: Any = None,
                             save: bool = False, temp: bool = False, create: bool = False) -> Any:
        return self._update_config(self.name, inner_scope, key, data, save, temp, create)

    def save_plugin_config(self, inner_scope: str = Scope.Inner, create: bool = False) -> Any:
        self._save_config(self.name, inner_scope, create)

    def restore_plugin_config(self, inner_scope: str = Scope.Inner) -> Any:
        return self._restore_config(Scope.Root, inner_scope)

    # Private proxy methods

    def _save_config(self, scope: str, inner_scope: str, create) -> None:
        return Registry(SysRegistry.Configs).save(f"{scope}.{inner_scope}", create)

    def _get_config(self, scope: str, inner_scope: str, key: str, default: Any) -> Any:
        return Registry(SysRegistry.Configs).get(f"{scope}.{inner_scope}", key, default)

    def _update_config(self, scope: str, inner_scope: str, key: str, data: Any,
                       save: bool, temp: bool = False, create: bool = False) -> Any:
        return Registry(SysRegistry.Configs).update(f"{scope}.{inner_scope}", key, data, temp, save, create)

    def _restore_config(self, scope: str, inner_scope: str) -> Any:
        return Registry(SysRegistry.Configs).restore(f"{scope}.{inner_scope}")
