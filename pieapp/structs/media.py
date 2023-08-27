import attrs
import datetime


@attrs.define(frozen=True)
class FileFormat:
    name: str
    description: str = attrs
    is_compressed: bool


@attrs.define(frozen=True)
class Bitrate:
    b320: int = 320
    b240: int = 240
    b128: int = 128
    b64: int = 64


@attrs.define
class FileInfo:
    bitrate: int
    bit_depth: int
    sample_rate: float
    file_size: float
    file_format: FileFormat


@attrs.define
class MetadataInfo:
    title: str
    genre: str
    subgenre: str
    track_number: int
    cover_image_big: str
    cover_image_small: str
    primary_artist: str
    featured_artist: str
    publisher: str
    additional_contributors: list[str] = attrs.Factory(list)
    explicit_content: bool = attrs.field(default=False)
    lyrics_language: str
    lyrics_publisher: str
    composition_owner: str
    master_recording_owner: str
    year_of_composition: datetime.date
    release_language: str
