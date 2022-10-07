from nextcord.ext.commands import Bot

from bot.cogs.users.ping import Ping
from bot.cogs.users.player import Player
from bot.cogs.users.playlists import Playlists


def register_cogs(bot: Bot):
    bot.add_cog(Ping())
    bot.add_cog(Player())
    bot.add_cog(Playlists())
