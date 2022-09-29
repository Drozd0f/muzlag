from nextcord.ext.commands import Bot

from bot.cogs.users.ping import ping
from bot.cogs.users.play import play
from bot.cogs.users.queue import queue
from bot.cogs.users.repeat import repeat
from bot.cogs.users.skip import skip
from bot.cogs.users.stop import stop
from bot.cogs.users.playlists import playlists


def register_cogs(bot: Bot):
    bot.add_command(ping)
    bot.add_command(play)
    bot.add_command(stop)
    bot.add_command(skip)
    bot.add_command(repeat)
    bot.add_command(queue)
    bot.add_command(playlists)
