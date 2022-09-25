from nextcord.ext import commands

from bot.src.queue import MuzlagQueue
from bot.src.decorators import voice_required


@commands.command(name='skip', help='Skip current song (default) or several songs')
@voice_required
async def skip(ctx: commands.context.Context, count: int = 1):
    queue = MuzlagQueue()
    if ctx.message.author.voice.channel.id not in queue:
        await ctx.send(f'**{ctx.message.author.name}** from where you sad that? :thinking: ')
        return
    if ctx.voice_client.is_connected():
        queue.skip(ctx.message.author.voice.channel.id, count)
        ctx.voice_client.stop()
    else:
        await ctx.send(f'**{ctx.message.author.name}** i`m not even in voice channel! :kissing_heart: ')
