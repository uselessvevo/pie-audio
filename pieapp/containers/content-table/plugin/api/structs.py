"""
ContentTable structs
"""

from piekit.config import Config


DEFAULT_CONTENT_TABLE_COLUMNS: tuple = (
    "filename", "filepath", "filesize",
    "latency", "information", "status"
)

DEFAULT_CONTENT_TABLE_COUNT: int = len(DEFAULT_CONTENT_TABLE_COLUMNS)


class ContentTableStruct:
    count: int = DEFAULT_CONTENT_TABLE_COUNT
    columns: tuple = Config.CONTENT_TABLE_COLUMNS or DEFAULT_CONTENT_TABLE_COLUMNS


class ContentTableSectionSize:
    pass
