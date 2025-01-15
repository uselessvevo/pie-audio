from typing import Any, Union

from pieapp.api.models.scopes import Scope
from pieapp.api.registries.locales.registry import LocaleRegistry


class LocalesAccessorMixin:
    """
    ConfigManager accessor mixin
    """

    def translate(
        self,
        key: Any,
        scope: str = Scope.Shared
    ) -> Any:
        return LocaleRegistry.get(scope or self.scope, key)
