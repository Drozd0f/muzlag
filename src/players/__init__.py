from src.players.youtube import YoutubePlayer
from src.players.base import BasePlayer

players = [
    YoutubePlayer
]


def player_factory(url: str) -> BasePlayer:
    for player in players:
        if player.name in url:
            return player
