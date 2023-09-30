# Converter API


## Method `open_files/openFiles`
Description:
    Let's you add selected files and add them into converter's list view

Returns:
    NoneType


## Method `commit`
Description:
    Save/commit changes in memmory

Arguments:
    files (list[MediaFile] | NoneType): list of `MediaFile` models or `NoneType`

Returns:
    NoneType


## Method `convert`
Description:
    Start the ffmpeg process to convert files

Arguments:
    files (list[MediaFile] | NoneType): list of `MediaFile` models or `NoneType`

Returns:
    NoneType
