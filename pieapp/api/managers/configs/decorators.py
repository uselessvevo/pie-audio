import functools
from typing import Union

from pieapp.api.managers.structs import Scope, Section
from pieapp.api.exceptions import PieException


def on_configuration_update(
    func: callable = None,
    scope: str = Section.Root,
    section: str = Section.Inner,
    key: str = None,
) -> callable:
    pass
