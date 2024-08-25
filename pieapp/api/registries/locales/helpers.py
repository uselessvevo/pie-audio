from pieapp.api.registries.locales.manager import Locales
from pieapp.api.registries.models import Scope


def translate(text: str, *args, scope: Scope.Shared = Scope.Shared) -> str:
    result: str = Locales.get(scope, text)
    return result % args
