import discord

from src.players.youtube import YoutubePlayer

players = [
    YoutubePlayer
]


def player_factory(url: str, stream: bool = False) -> discord.PCMVolumeTransformer:
    for player in players:
        if player.name in url:
            return player.from_url(url, stream)
