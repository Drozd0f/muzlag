from __future__ import annotations

from abc import abstractmethod, abstractclassmethod

import nextcord


class BasePlayer:
    def __init__(self, data: dict):
        self.title = data.get('title')
        self.url = data.get('url')

    @staticmethod
    def _play(source: nextcord.FFmpegPCMAudio, volume: float):
        return nextcord.PCMVolumeTransformer(source, volume)

    @abstractmethod
    def play(self) -> nextcord.PCMVolumeTransformer:
        raise NotImplementedError

    @abstractclassmethod
    def from_url(cls, url: str) -> BasePlayer:
        raise NotImplementedError
