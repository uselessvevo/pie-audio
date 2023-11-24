import datetime
import dataclasses as dt
from typing import Optional


@dt.dataclass
class AlbumCover:
    image_path: str = dt.field(default=None)
    image_file_format: str = dt.field(default=None)
    image_small_path: str = dt.field(default=None)


@dt.dataclass
class Codec:
    name: str
    type: str
    long_name: str


class ChannelsLayout:
    mono: str = "mono"
    stereo: str = "stereo"


@dt.dataclass
class FileInfo:
    filename: str
    bit_rate: int
    bit_depth: int
    sample_rate: float
    duration: float
    codec: Codec
    channels: int = dt.field(default=2)
    channels_layout: ChannelsLayout = dt.field(default=ChannelsLayout.stereo)

    def as_dict(self) -> dict:
        return dt.asdict(self)

    def as_tuple(self) -> tuple:
        return dt.astuple(self)


@dt.dataclass
class Metadata:
    title: str
    genre: Optional[str] = None
    subgenre: Optional[str] = None
    track_number: Optional[int] = None
    album_cover: Optional[AlbumCover] = None
    primary_artist: Optional[str] = None
    publisher: Optional[str] = None
    explicit_content: Optional[bool] = None
    lyrics_language: Optional[str] = None
    lyrics_publisher: Optional[str] = None
    composition_owner: Optional[str] = None
    release_language: Optional[str] = None
    featured_artist: str = dt.field(default_factory=str)
    additional_contributors: list[str] = dt.field(default_factory=list)
    year_of_composition: datetime.date = dt.field(default=datetime.date(1999, 1, 1))

    def as_dict(self) -> dict:
        return dt.asdict(self)

    def as_tuple(self) -> tuple:
        return dt.astuple(self)


@dt.dataclass
class MediaFile:
    info: FileInfo
    metadata: Metadata
