from __future__ import annotations

import logging

import youtube_dl
import discord

from src.players.base import BasePlayer

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YoutubePlayer(BasePlayer):
    def __init__(self, data: dict):
        self.start_time = data.get('start_time', 0)
        super().__init__(data)

    def play(self) -> discord.PCMVolumeTransformer:
        return self._play(
            discord.FFmpegPCMAudio(
                self.url,
                **ffmpeg_options,
                before_options=f'-ss {self.start_time}'
            ),
            volume=1
        )

    @classmethod
    def from_url(cls, url: str) -> YoutubePlayer:
        data = ytdl.extract_info(url, download=False)
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        return cls(data)
