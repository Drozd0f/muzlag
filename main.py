import logging
import os

from discord.ext import commands

from src import handlers
from src.log import setup_logging

log = logging.getLogger(__name__)

BOT = commands.Bot(
    command_prefix='?',
    help_command=commands.DefaultHelpCommand(
        no_category='Commands'
    )
)


def setup_command():
    BOT.add_command(handlers.ping)
    BOT.add_command(handlers.play)
    BOT.add_command(handlers.stop)
    BOT.add_command(handlers.skip)

    BOT.add_command(handlers.danilo)
    BOT.add_command(handlers.vovan)
    BOT.add_command(handlers.nikita)
    BOT.add_command(handlers.vadick)
    BOT.add_command(handlers.vadoom)

    for command in BOT.commands:
        log.info(f"command --> {command}")


def main():
    setup_logging()
    token = os.getenv('TOKEN')

    log.info("setuping handlers...")
    setup_command()

    log.info("running bot...")
    BOT.run(token)


if __name__ == '__main__':
    main()
