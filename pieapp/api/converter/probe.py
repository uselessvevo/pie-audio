from pieapp.api.converter.models import *


class ProbeBuilder:

    def probe_metadata(self) -> Metadata:
        raise NotImplementedError

    def probe_file_info(self) -> FileInfo:
        raise NotImplementedError


class VorbisProbe(ProbeBuilder):

    def __init__(self, filepath: Path) -> None:
        self._filepath = filepath

    def probe_metadata(self) -> Metadata:
        pass

    def probe_file_info(self) -> FileInfo:
        pass


_PROBE_FILE_FORMAT_MAP = {
    "mp3": ProbeBuilder,
    "mp4": ProbeBuilder,
    "wav": ProbeBuilder,
}


def get_probe_builder(filepath: Path) -> ProbeBuilder:
    file_format = filepath.suffix
    if file_format not in _PROBE_FILE_FORMAT_MAP:
        raise KeyError("Unsupported file format")

    probe = _PROBE_FILE_FORMAT_MAP.get(file_format)()
    probe = probe(filepath)
    return probe
