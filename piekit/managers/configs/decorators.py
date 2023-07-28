import functools
from typing import Union

from piekit.managers.structs import Scope, Section
from piekit.config.exceptions import PieException


def on_configuration_update(
    func: callable = None,
    scope: str = Section.Root,
    section: str = Section.Inner,
    key: str = None,
) -> callable:
    pass
