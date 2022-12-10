import nextcord
from nextcord.ext import commands

from bot.src.queue import MuzlagQueue
from bot.src.decorators import c_voice_required, s_voice_required


@c_voice_required
async def c_queue(ctx: commands.Context):
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


@s_voice_required
async def s_queue(interaction: nextcord.Interaction):
    queue = MuzlagQueue()
    if interaction.user.voice.channel.id not in queue:
        await interaction.send(f'**{interaction.user.name}** from where you sad that? :thinking: ')
        return
    voice_client = nextcord.utils.get(
        interaction.client.voice_clients,
        guild=interaction.guild
    )
    if voice_client.is_connected():
        titles = ':coffee: Current queue :coffee: :\n'
        res = queue.show_queue(interaction.user.voice.channel.id)
        if not res:
            await interaction.send(':anger: :japanese_goblin:**One song is not enought for queue** :anger:')
            return
        titles += res
        await interaction.send(f'**{titles}**')
    else:
        await interaction.send(f'**{interaction.user.name}** i`m not even in voice channel! :kissing_heart: ')
