from typing import TypedDict, Union

from PySide6.QtGui import QShortcut


class ShortcutDict(TypedDict):
    shortcut: QShortcut
    target: str
    title: Union[str, None]
    description: Union[str, None]
