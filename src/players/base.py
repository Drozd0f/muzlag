from __future__ import annotations

from abc import ABC, abstractclassmethod

import discord


class BasePlayer(ABC, discord.PCMVolumeTransformer):
    name: str
    title: str
    url: str

    def __init_subclass__(cls, domain_name: str, **kwargs):
        super().__init_subclass__(**kwargs)
        if not domain_name:
            raise AttributeError('Player must had name')
        cls.name = domain_name

    def __int__(self, source, volume=1):
        super().__init__(source, volume)

    @abstractclassmethod
    def from_url(cls, url: str, stream: bool = False) -> BasePlayer:
        raise NotImplementedError
