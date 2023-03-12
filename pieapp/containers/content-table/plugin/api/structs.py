"""
ContentTable structs
"""

from piekit.system.loader import Config


DEFAULT_CONTENT_TABLE_COLUMNS: tuple = (
    "filename", "filepath", "filesize",
    "latency", "information", "status"
)

DEFAULT_CONTENT_TABLE_COUNT: int = len(DEFAULT_CONTENT_TABLE_COLUMNS)


class ContentTableStruct:
    count: int = DEFAULT_CONTENT_TABLE_COUNT
    columns: tuple = getattr(Config, "CONTENT_TABLE_COLUMNS", DEFAULT_CONTENT_TABLE_COLUMNS)


class ContentTableSectionSize:
    pass
