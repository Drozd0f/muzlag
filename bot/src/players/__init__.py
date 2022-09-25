from bot.src.players.base import BasePlayer
from bot.src.players.youtube import YoutubePlayer

players = {
    'youtu': YoutubePlayer
}


def player_factory(url: str) -> BasePlayer:
    for domain_name, player in players.items():
        if domain_name in url:
            return player.from_url(url)
