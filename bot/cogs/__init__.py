import logging

from nextcord.ext.commands import Bot

from bot.cogs import users, easter_egg


def register_all_cogs(bot: Bot):
    users.register_cogs(bot)
    easter_egg.register_cogs(bot)

    for command in bot.commands:
        logging.info(f"command --> {command}")
