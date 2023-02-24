from piekit.objects.base import PieObject
from piekit.objects.types import ObjectTypes


class PieContainer(PieObject):
    type = ObjectTypes.Container

    def addOn(self, container: str) -> None:
        pass

    def removeFrom(self, container: str) -> None:
        pass


class DockablePieContainer(PieContainer):
    pass
