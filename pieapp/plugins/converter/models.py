"""
Converter theme properties
"""
import dataclasses as dt


@dt.dataclass(eq=False, frozen=True)
class ConverterThemeProperties:
    ConverterItemColors: str = "converterItemColors"
    DefaultColor: str = "default"
