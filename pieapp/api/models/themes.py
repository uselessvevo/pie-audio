"""
Theme properties
"""
import dataclasses as dt


@dt.dataclass(eq=False, frozen=True, slots=True)
class Icons:
    pass


@dt.dataclass(eq=False, frozen=True)
class ThemeProperties:
    AppIconColor: str = "appIconColor"
    ActionIconColor: str = "actionIconColor"
    ErrorColor: str = "errorColor"
    DangerColor: str = "dangerColor"
    MainFontColor: str = "mainFontColor"
