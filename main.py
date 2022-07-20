import os

import discord
from discord.ext import commands


bot = commands.Bot(command_prefix='->')


@bot.command()
async def ping(ctx: commands.context.Context) -> discord.Message:
    await ctx.send('pong')


def main():
    token = os.getenv('TOKEN')
    bot.run(token)


if __name__ == '__main__':
    main()
