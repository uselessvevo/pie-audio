"""
Component mixins
"""


class ComponentMixin:
    """
    Use this mixin to register your object
    on the `BaseComponent` based objects
    """

    def placeOn(self, target: str, **kwargs) -> None:
        """
        Register/render widget on one
        of the listed components of `MainWindow`

        Args:
            target (str): registered component name
            kwargs (dict): component's `register` method parameters
        """
        self._parent.placeOn(self, target, **kwargs)

    def removeFrom(self, target: str) -> None:
        """
        Remover/de-render widget from `MainWindow` component(-s)

        Args:
            target (str): registered component name
        """
        self._parent.removeFrom(self, target)
