import os
import ffmpeg
import datetime
from pathlib import Path

from pieapp.api.converter.models import MediaFile
from pieapp.api.converter.models import Metadata
from pieapp.api.converter.models import Codec
from pieapp.api.converter.models import FileInfo
from pieapp.api.converter.models import ChannelsLayout


# YOU NEED TO PUT FFMPEG BINARY RIGHT IN THE TEST FOLDER

def build_media_file() -> None:
    os.environ.update({"FFMPEG_BIN": r"C:\Users\KIvanov\.pie\ffmpeg\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe"})
    file_path = Path("C:/Users/KIvanov/.pie/temp/80b5f16d56ab446f8c5e91dc9a2f5574/WAV_file_example_1MG.wav")
    codec = Codec(
        name="pcm_s16le",
        type="audio",
        long_name="PCM_S16LE CODEC"
    )
    file_info = FileInfo(
        filename="WAV_file_example_1MG.wav",
        file_format="wav",
        bit_rate=1411200,
        bit_depth=None,
        sample_rate=44100,
        duration=262094,
        codec=codec,
        channels=2,
        channels_layout=ChannelsLayout.Mono
    )
    metadata = Metadata(
        title="123",
        genre="Rock",
        subgenre="Math-Rock",
        track_number=0,
        primary_artist=None,
        publisher=None,
        explicit_content=None,
        lyrics_language=None,
        lyrics_publisher=None,
        composition_owner=None,
        release_language=None,
        featured_artist="Test",
        additional_contributors=None,
        year_of_composition=datetime.date(1970, 1, 1)
    )
    media_file = MediaFile(
        uuid="b9f75497-312d-4a33-8191-73e797d5234d",
        name="80b5f16d56ab446f8c5e91dc9a2f5574/WAV_file_example_1MG.wav",
        path=file_path,
        output_path=file_path.parent / "output" / file_path.name,
        info=file_info,
        metadata=metadata
    )
    try:
        stream = ffmpeg.input(media_file.path.as_posix()).audio
        converter_query = media_file.metadata.build()
        output_file = (media_file.path.parent / "output.mp3").as_posix()
        stream = stream.output(output_file, **converter_query)
        ffmpeg.run(stream, overwrite_output=True)
    except Exception as e:
        print(e)


build_media_file()
