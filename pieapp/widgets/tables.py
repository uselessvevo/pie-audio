from __feature__ import snake_case

from typing import Any

from PySide6.QtWidgets import QTableWidgetItem

from pieapp.api.exceptions import PieException
from pieapp.api.registries.locales.helpers import translate


class MediaTableItemValue(QTableWidgetItem):

    def __init__(self, media_file_name, field, value, validator: callable = None) -> None:
        super(MediaTableItemValue, self).__init__()
        super().set_text(str(value or ""))
        self._media_file_name = media_file_name
        self._value = value
        self._field = field
        self._validator = validator

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
        if self._validator:
            try:
                value = self._validator(value)
            except Exception as e:
                raise PieException(translate("Validation error"), str(e))

        self._value = value
        super().set_text(str(value))
