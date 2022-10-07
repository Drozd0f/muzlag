import asyncio

from nextcord.ext import commands

from bot.src.queue import MuzlagQueue
from bot.src.decorators import voice_required


@voice_required
async def stop(ctx: commands.context.Context):
    queue = MuzlagQueue()
    if ctx.message.author.voice.channel.id not in queue:
        await ctx.send(f'**{ctx.message.author.name}** from where you sad that? :thinking: ')
        return
    if ctx.voice_client.is_connected():
        try:
            queue.drop(ctx.message.author.voice.channel.id)
        except asyncio.QueueEmpty:
            ctx.voice_client.stop()
    else:
        await ctx.send(f'**{ctx.message.author.name}** i`m not even in voice channel! :kissing_heart: ')
