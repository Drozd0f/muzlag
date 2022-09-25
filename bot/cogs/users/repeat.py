from discord.ext import commands

from bot.src.queue import MuzlagQueue
from bot.src.decorators import voice_required


@commands.command(name='repeat', help='Set song to repeat')
@voice_required
async def repeat(ctx: commands.context.Context):
    queue = MuzlagQueue()
    if ctx.message.author.voice.channel.id not in queue:
        await ctx.send(f'**{ctx.message.author.name}** from where you sad that? :thinking: ')
        return
    if ctx.voice_client.is_connected():
        queue.switch_repeat(ctx.message.author.voice.channel.id)
    else:
        await ctx.send(f'**{ctx.message.author.name}** i`m not even in voice channel! :kissing_heart: ')
