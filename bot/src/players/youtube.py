from __future__ import annotations

import nextcord

from bot.src.yt_search import YoutubeSearch
from bot.src.players.base import BasePlayer

ffmpeg_options = {
    'options': '-vn'
}


class YoutubePlayer(BasePlayer):
    def __init__(self, data: dict):
        self.start_time = data.get('start_time', 0)
        super().__init__(data)

    def play(self) -> nextcord.PCMVolumeTransformer:
        return self._play(
            nextcord.FFmpegPCMAudio(
                self.url,
                **ffmpeg_options,
                before_options=f'-ss {self.start_time}'
            ),
            volume=1
        )

    @classmethod
    def from_url(cls, url: str) -> YoutubePlayer:
        yt_search = YoutubeSearch.from_url(url)
        return cls(yt_search.data)
