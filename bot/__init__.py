import asyncio
import logging

import nextcord
from nextcord.ext import commands

from bot.cogs import register_all_cogs
from bot.events import register_all_events
from bot.config import Config
from bot.database.migrations import Migrator
from bot.src.log import setup_logging


log = logging.getLogger(__name__)

intents = nextcord.Intents.default()
intents.message_content = True

BOT = commands.Bot(
    command_prefix=Config.prefix,
    intents=intents
)


def start_bot():
    setup_logging()

    log.info('applying migrations...')
    asyncio.run(Migrator.start())

    log.info('setuping cogs...')
    register_all_cogs(BOT)

    log.info('setuping events...')
    register_all_events(BOT)

    log.info('running bot...')
    BOT.run(Config.token)
