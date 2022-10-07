import nextcord
from nextcord.ext import commands

from bot.src.queue import MuzlagQueue
from bot.src.decorators import c_voice_required, s_voice_required


@c_voice_required
async def c_skip(ctx: commands.Context, count: int = 1):
    queue = MuzlagQueue()
    if ctx.message.author.voice.channel.id not in queue:
        await ctx.send(f'**{ctx.message.author.name}** from where you sad that? :thinking: ')
        return
    if ctx.voice_client.is_connected():
        queue.skip(ctx.message.author.voice.channel.id, count)
        ctx.voice_client.stop()
    else:
        await ctx.send(f'**{ctx.message.author.name}** i`m not even in voice channel! :kissing_heart: ')


@s_voice_required
async def s_skip(interaction: nextcord.Interaction, count: int = 1):
    queue = MuzlagQueue()
    if interaction.user.voice.channel.id not in queue:
        await interaction.send(f'**{interaction.user.name}** from where you sad that? :thinking: ')
        return
    voice_client = nextcord.utils.get(
        interaction.client.voice_clients,
        guild=interaction.guild
    )
    if voice_client.is_connected():
        queue.skip(interaction.user.voice.channel.id, count)
        if count <= 1:
            await interaction.send('Current song skipped')
        else:
            await interaction.send(f'{count} songs were skipped')
        voice_client.stop()
    else:
        await interaction.send(f'**{interaction.user.name}** i`m not even in voice channel! :kissing_heart: ')
