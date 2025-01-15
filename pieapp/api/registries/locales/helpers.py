from pieapp.api.models.scopes import Scope
from pieapp.api.registries.locales.registry import LocaleRegistry


def translate(text: str, *args, scope: Scope.Shared = Scope.Shared) -> str:
    result: str = LocaleRegistry.get(scope, text)
    return result % args
