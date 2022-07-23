from abc import abstractclassmethod

import discord


class BasePlayer:
    def __init_subclass__(cls, name: str):
        super().__init_subclass__()
        if not name:
            raise AttributeError('Player must had name')
        cls.name = name

    @abstractclassmethod
    async def from_url(cls, url: str, stream: bool = False) -> discord.PCMVolumeTransformer:
        raise NotImplementedError
