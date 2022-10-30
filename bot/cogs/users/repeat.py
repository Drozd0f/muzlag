from nextcord.ext import commands

from bot.src.queue import MuzlagQueue
from bot.src.decorators import voice_required


@voice_required
async def repeat(ctx: commands.context.Context):
    queue = MuzlagQueue()
    channel_id = ctx.message.author.voice.channel.id
    if channel_id not in queue:
        await ctx.send(f'**{ctx.message.author.name}** from where you sad that? :thinking: ')
        return
    if ctx.voice_client.is_connected():
        queue.switch_repeat(channel_id)
        await ctx.send(f':white_check_mark: **{queue.current_song(channel_id)}** is on repeat.')
    else:
        await ctx.send(f'**{ctx.message.author.name}** i`m not even in voice channel! :kissing_heart: ')
