from typing import Union

from piekit.managers.base import BaseManager
from piekit.managers.structs import Sections
from piekit.config.exceptions import PieException

from PySide6.QtWidgets import QWidget


class ManagerRefs(BaseManager):
    """
    The premise of this manager is to simplify common for this project data organization and access:
    * `<parent 1>: <item 1, item 2, ..., item n>, ..., <parent n>: ...`
    """

    def __init__(self) -> None:
        self._parent_refs: dict[str, QWidget] = {}
        self._children_refs: dict[str, dict[str, QWidget]] = {}

    def add_section(self, name: Union[str, Sections], target_instance: QWidget) -> None:
        if name in self._parent_refs:
            raise PieException(f"Parent object `{name}` already registered")

        self._parent_refs[name] = target_instance

        return target_instance

    def add_item(self, section: Union[str, Sections], item_name: str, item_instance: QWidget) -> QWidget:
        if section not in self._children_refs:
            self._children_refs[section] = {}

        self._children_refs[section][item_name] = item_instance
        return item_instance

    def get_section(self, section: Union[str, Sections]) -> QWidget:
        if section not in self._parent_refs:
            raise KeyError(f"Parent object `{section}` already registered")
        
        return self._parent_refs[section]
    
    def get_sections(self, *sections: Union[str, Sections]) -> list[QWidget]:
        collect: list[QWidget] = []

        for section in sections:
            if section not in self._parent_refs:
                raise KeyError(f"Parent object `{section}` already registered")
            
            if section not in collect:
                collect.append(self._parent_refs[section])

        return collect

    def get_item(self, section: Union[str, Sections], name: Union[str, Sections]) -> QWidget:
        if section not in self._children_refs:
            raise PieException(f"Section {section} not found")

        if name not in self._children_refs[section]:
            raise PieException(f"ToolBar item {section}.{name} not found")

        return self._children_refs[section][name]

    def get_items(self, section: Union[str, Sections], *names: Union[str, Sections]) -> list[QWidget]:
        collect: list[QWidget] = []

        if section not in self._parent_refs[section]:
            raise KeyError(f"Parent object `{section}` already registered")

        for name in names:
            if name not in self._children_refs[section]:
                raise KeyError(f"Parent object `{section}` already registered")
                
            if name not in collect:
                collect.append(self._children_refs[section][name])

        return collect
