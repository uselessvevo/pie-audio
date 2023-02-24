from piekit.containers.containers import PieContainer
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor


class Settings(
    PieContainer,
    ConfigAccessor,
    LocalesAccessor,
    AssetsAccessor,
):
    name = "settings"

    def init(self) -> None:
        pass
