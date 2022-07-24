import discord

from src.players.youtube import YoutubePlayer

players = [
    YoutubePlayer
]


async def player_factory(url: str, stream: bool = False) -> discord.PCMVolumeTransformer:
    for player in players:
        if player.name in url:
            return await player.from_url(url, stream)
