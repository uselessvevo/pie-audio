import dataclasses as dt
from pieapp.api.converter.models import *


class QueryBuilder:

    def __init__(self, media_file: MediaFile) -> None:
        self._media_file = media_file
        self._metadata = None
        self._file_info = None

    def build_metadata(self):
        """
        Default output metadata builder

        Tested on next file formats:
            * mp3
            * wav
        """
        arguments = []
        for field, value in dt.asdict(self._media_file.metadata).items():
            if value is not None:
                arguments.append(f"{field}={value}")

        arguments.extend(arguments)
        self._metadata = {f"metadata:g:{i}": e for i, e in enumerate(arguments)}

    def build_file_info(self):
        self._file_info = {}

    def build(self) -> dict[str, str]:
        self.build_metadata()
        self.build_file_info()
        return {**self._metadata, **self._file_info}


class VorbisBuilder(QueryBuilder):
    pass


_BUILDER_FILE_FORMAT_MAP = {
    "mp3": QueryBuilder,
    "mp4": QueryBuilder,
    "wav": QueryBuilder,
}


def get_query_builder(media_file: MediaFile) -> QueryBuilder:
    file_format = media_file.info.file_format
    if file_format not in _BUILDER_FILE_FORMAT_MAP:
        return

    query_builder = _BUILDER_FILE_FORMAT_MAP.get(file_format)
    query_builder = query_builder(media_file)
    return query_builder
