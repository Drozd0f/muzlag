import logging

from discord.ext import commands

from bot.cogs import register_all_cogs
from bot.config import Config
from bot.src.log import setup_logging


log = logging.getLogger(__name__)

BOT = commands.Bot(
    command_prefix=Config.prefix,
    help_command=commands.DefaultHelpCommand(
        no_category='Commands'
    )
)


def start_bot():
    setup_logging()

    log.info("setuping cogs...")
    register_all_cogs(BOT)

    log.info("running bot...")
    BOT.run(Config.token)
