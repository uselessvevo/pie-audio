from pieapp.api.registries.models import Scope
from pieapp.api.registries.registry import Registry
from pieapp.api.registries.models import SysRegistry


def translate(text: str, *args, scope: Scope.Shared = Scope.Shared) -> str:
    result: str = Registry(SysRegistry.Locales).get(scope, text)
    return result % args
