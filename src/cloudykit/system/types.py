import typing

# TODO: Add Expandable types mixing. For example: `EList[EDict, ...]`

__all__ = (
    "EList",
    "EDict",
    "DirectoryType",
    "SharedSection"
)

# Expandable list
EList = typing.TypeVar("EList")

# Expandable dict
EDict = typing.TypeVar("EDict")

# Use it in `AssetsManager`
DirectoryType = type("DirectoryType", (), {})

# Manager's types and constants
SharedSection = "shared"
