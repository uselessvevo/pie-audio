import uuid
from typing import Optional, Any

import datetime
import dataclasses as dt
from pathlib import Path


@dt.dataclass
class AlbumCover:
    image_path: Path = dt.field(default=None)
    image_file_format: str = dt.field(default=None)
    image_small_path: Path = dt.field(default=None)
    image_small_file_format: str = dt.field(default=None)


@dt.dataclass
class Codec:
    name: str
    type: str
    long_name: str


@dt.dataclass(frozen=True)
class ChannelsLayout:
    mono: str = "mono"
    stereo: str = "stereo"


@dt.dataclass
class FileInfo:
    filename: str
    file_format: str
    bit_rate: int
    bit_depth: int
    sample_rate: float
    duration: float
    codec: Codec
    channels: int = dt.field(default=2)
    channels_layout: ChannelsLayout = dt.field(default=ChannelsLayout.stereo)


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
    year_of_composition: datetime.date = dt.field(default=datetime.date(1970, 1, 1))


@dt.dataclass(eq=True, slots=True)
class MediaFile:
    uuid: str
    name: str
    path: Path
    info: Optional[FileInfo] = None
    metadata: Optional[Metadata] = None


def update_media_file(media_file: MediaFile, field_path: str, value: Any) -> MediaFile:
    path, _, target = field_path.rpartition(".")
    for attrname in path.split("."):
        base = getattr(media_file, attrname)
        setattr(base, target, value)

    media_file.uuid = str(uuid.uuid4())
    return media_file
