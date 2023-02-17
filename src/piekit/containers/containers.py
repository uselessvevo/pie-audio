from piekit.objects.base import PieObject


class BaseContainer(PieObject):

    def addOn(self, container: str) -> None:
        pass

    def removeFrom(self, container: str) -> None:
        pass


class DockableContainer(BaseContainer):
    pass
