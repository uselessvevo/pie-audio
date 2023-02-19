""" This observer serves """
from piekit.managers.types import AllPieObjects


class PieObjectObserverMixin:

    def __init__(self) -> None:
        self._object_availability_listeners = {}
        self._object_unmount_listeners = {}

        for method_name in dir(self):
            method = getattr(self, method_name, None)
            if hasattr(method, "_object_listen"):
                pie_object_listen = method._object_listen

                if pie_object_listen not in self.requires + self.optional:
                    raise Exception(
                        f"Method {method_name} of {self} is trying to watch "
                        f"PieObject {pie_object_listen}, but that pie_object is not "
                        f"listed in REQUIRES nor OPTIONAL."
                    )

                self._object_availability_listeners[pie_object_listen] = method_name

            if hasattr(method, "_object_unmount"):
                object_unmount = method._object_unmount

                if object_unmount not in self.requires + self.optional:
                    raise Exception(
                        f"Method {method_name} of {self} is trying to watch "
                        f"PieObject {object_unmount}, but that PieObject is not "
                        f"listed in `requires` nor `optional`."
                    )

                self._object_unmount_listeners[object_unmount] = method_name

    def on_object_available(self, target: str) -> None:
        if target in self._object_availability_listeners:
            method_name = self._object_availability_listeners[target]
            method = getattr(self, method_name)
            method()

        # Call global PieObject handler
        if AllPieObjects in self._object_availability_listeners:
            method_name = self._object_availability_listeners[AllPieObjects]
            method = getattr(self, method_name)
            method(target)

    def on_object_unmount(self, target: str) -> None:
        if target in self._object_unmount_listeners:
            method_name = self._object_unmount_listeners[target]
            method = getattr(self, method_name)
            method()

    onPieObjectAvailable = on_object_available
    onPieObjectUnmount = on_object_unmount
