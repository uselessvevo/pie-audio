from __feature__ import snake_case

from typing import Any

from PySide6.QtWidgets import QTableWidgetItem

from pieapp.api.exceptions import PieError
from pieapp.api.registries.locales.helpers import translate


class MediaTableWidgetItem(QTableWidgetItem):

    def __init__(
        self,
        media_file_name: str,
        field: Any,
        value: Any,
        validators: list[callable] = None,
    ) -> None:
        super(MediaTableWidgetItem, self).__init__()
        super().set_text(str(value or ""))
        self._field = field
        self._value = value
        self._media_file_name = media_file_name
        self._validators = validators or []

    @property
    def value(self) -> Any:
        return self._value

    @property
    def field(self) -> str:
        return self._field

    @property
    def media_file_name(self) -> str:
        return self._media_file_name

    def set_text(self, value: Any) -> None:
        if self._validators:
            for validator in self._validators:
                try:
                    value = validator(value)
                except Exception as e:
                    raise PieError(translate("Validation error"), str(e))

        self._value = value
        super().set_text(str(value))
