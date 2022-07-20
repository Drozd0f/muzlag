import os
import time

import discord
from discord.ext import commands


bot = commands.Bot(command_prefix='>>')


@bot.command()
async def ping(ctx: commands.context.Context) -> discord.Message:
    await ctx.send('pong')


@bot.command()
async def play(ctx: commands.context.Context):
    await ctx.author.voice.channel.connect()
    time.sleep(5)
    await ctx.voice_client.disconnect()


def main():
    token = os.getenv('TOKEN')
    bot.run(token)


if __name__ == '__main__':
    main()
