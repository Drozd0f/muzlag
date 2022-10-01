from dataclasses import dataclass


@dataclass
class SongModel:
    song_id: int
    title: str
    url: str
    start_time: int
