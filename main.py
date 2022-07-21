import os

from discord.ext import commands

from src import handlers

BOT = commands.Bot(command_prefix='!')


def setup_command():
    BOT.add_command(handlers.ping)
    BOT.add_command(handlers.play)
    BOT.add_command(handlers.stop)
    BOT.add_command(handlers.danilo)
    BOT.add_command(handlers.vovan)
    BOT.add_command(handlers.nikita)
    BOT.add_command(handlers.vadick)
    BOT.add_command(handlers.vadoom)


def main():
    token = os.getenv('TOKEN')
    setup_command()
    BOT.run(token)


if __name__ == '__main__':
    main()
