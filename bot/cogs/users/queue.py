from nextcord.ext import commands

from bot.src.queue import MuzlagQueue
from bot.src.decorators import voice_required


@voice_required
async def queue(ctx: commands.context.Context):
    queue = MuzlagQueue()
    if ctx.message.author.voice.channel.id not in queue:
        await ctx.send(f'**{ctx.message.author.name}** from where you sad that? :thinking: ')
        return
    if ctx.voice_client.is_connected():
        async with ctx.typing():
            titles = ':coffee: Current queue :coffee: :\n'
            res = queue.show_queue(ctx.message.author.voice.channel.id)
            if not res:
                await ctx.send(':anger: :japanese_goblin:**One song is not enought for queue** :anger:')
                return
            titles += res
            await ctx.send(f'**{titles}**')
    else:
        await ctx.send(f'**{ctx.message.author.name}** i`m not even in voice channel! :kissing_heart: ')
