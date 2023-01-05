import typing


# TODO: Add Expandable types mixing. For example: `EList[EDict, ...]`

# Expandable list
EList = typing.TypeVar('EList')

# Expandable dict
EDict = typing.TypeVar('EDict')

# Use it in `AssetsManager`
DirectoryType = type("DirectoryType", (), {})
