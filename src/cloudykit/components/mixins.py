from PyQt5.QtCore import pyqtSignal


class ComponentMixin:
    """
    Use this mixin to register your object
    on the `BaseComponent` based objects
    """
    signalQuitRequested = pyqtSignal()
    signalRestartRequested = pyqtSignal()
    signalExceptionOccurred = pyqtSignal(dict)

    signalOnComponentClose = pyqtSignal()
    signalOnComponentMoved = pyqtSignal("QMoveEvent")
    signalOnComponentResized = pyqtSignal("QResizeEvent")

    def prepareComponentSignals(self) -> None:
        self.signalQuitRequested.connect(self._parent)
        self.signalRestartRequested.connect(self._parent)
        self.signalExceptionOccurred.connect(self._parent)

    def placeOn(self, target: str, **kwargs) -> None:
        """
        Register/render widget on one
        of the listed components of `AppWindow`

        Args:
            target (str): registered component name
            kwargs (dict): component's `register` method parameters
        """
        self._parent.placeOn(self, target, **kwargs)

    def removeFrom(self, target: str) -> None:
        """
        Remover/de-render widget from `AppWindow` component(-s)

        Args:
            target (str): registered component name
        """
        self._parent.removeFrom(self, target)
