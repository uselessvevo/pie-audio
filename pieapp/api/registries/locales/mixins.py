from typing import Any, Union

from pieapp.api.registries.locales.manager import Locales
from pieapp.api.registries.models import Scope


class LocalesAccessorMixin:
    """
    ConfigManager accessor mixin
    """

    def translate(
        self,
        key: Any,
        scope: Union[str, Scope] = Scope.Shared
    ) -> Any:
        return Locales.get(scope or self.scope, key)
