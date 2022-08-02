from src.players.youtube import YoutubePlayer
from src.players.base import BasePlayer

players = {
    'youtu': YoutubePlayer
}


def player_factory(url: str) -> BasePlayer:
    for domain_name, player in players.items():
        if domain_name in url:
            return player.from_url(url)
