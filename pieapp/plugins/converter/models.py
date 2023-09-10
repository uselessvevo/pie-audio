import datetime
import dataclasses as dt


@dt.dataclass
class CoverImage:
    image_big: str
    image_small: str
    file_format: str


@dt.dataclass
class FileFormat:
    name: str
    description: str = dt.field(default="")


@dt.dataclass
class FileInfo:
    bitrate: int
    bit_depth: int
    sample_rate: float
    file_format: FileFormat


@dt.dataclass
class Metadata:
    title: str
    genre: str
    subgenre: str
    track_number: int
    cover_image: CoverImage
    primary_artist: str
    featured_artist: str
    publisher: str
    additional_contributors: list[str]
    explicit_content: bool
    lyrics_language: str
    lyrics_publisher: str
    composition_owner: str
    year_of_composition: datetime.date
    release_language: str


@dt.dataclass
class MediaFile:
    info: FileInfo
    metadata: Metadata
