from __future__ import annotations

from abc import abstractmethod, abstractclassmethod

import discord


class BasePlayer:
    def __init__(self, data: dict):
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @staticmethod
    def _play(source: discord.FFmpegPCMAudio, volume: float):
        return discord.PCMVolumeTransformer(source, volume)

    @abstractmethod
    def play(self) -> discord.PCMVolumeTransformer:
        raise NotImplementedError

    @abstractclassmethod
    def from_url(cls, url: str) -> BasePlayer:
        raise NotImplementedError
