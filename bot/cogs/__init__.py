import logging

from nextcord.ext.commands import Bot

from bot.cogs import users, easter_egg, help


log = logging.getLogger(__name__)


def register_all_cogs(bot: Bot):
    users.register_cogs(bot)
    easter_egg.register_cogs(bot)

    bot.add_cog(help.HelpCog(bot))

    for command in bot.commands:
        log.info(f"command --> {command}")
