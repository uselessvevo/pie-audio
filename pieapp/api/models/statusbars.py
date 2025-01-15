"""
Status bar index struct
"""
import dataclasses as dt


@dt.dataclass(eq=False, frozen=True)
class MessageStatus:
    NoStatus: str = "default"
    Info: str = "info"
    Warning: str = "warning"
    Error: str = "error"
