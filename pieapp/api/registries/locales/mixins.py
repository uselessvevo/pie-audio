from typing import Any, Union

from pieapp.api.registries.registry import Registry
from pieapp.api.registries.models import SysRegistry, Scope


class LocalesAccessorMixin:
    """
    ConfigManager accessor mixin
    """

    def translate(
        self,
        key: Any,
        scope: Union[str, Scope] = Scope.Shared
    ) -> Any:
        return Registry(SysRegistry.Locales).get(scope or self.scope, key)
