import nextcord
from nextcord.ext import commands

from bot.src.queue import MuzlagQueue
from bot.src.emoji import DefaultEmoji
from bot.src.decorators import c_voice_required, s_voice_required


@c_voice_required
async def c_repeat(ctx: commands.Context):
    queue = MuzlagQueue()
    if ctx.message.author.voice.channel.id not in queue:
        await ctx.send(f'**{ctx.message.author.name}** from where you sad that? {DefaultEmoji.thinking} ')
        return
    if ctx.voice_client.is_connected():
        queue.switch_repeat(ctx.message.author.voice.channel.id)
    else:
        await ctx.send(f'**{ctx.message.author.name}** i`m not even in voice channel! {DefaultEmoji.kissing_heart} ')


@s_voice_required
async def s_repeat(interaction: nextcord.Interaction):
    queue = MuzlagQueue()
    if interaction.user.voice.channel.id not in queue:
        await interaction.send(f'**{interaction.user.name}** from where you sad that? {DefaultEmoji.thinking} ')
        return
    voice_client = nextcord.utils.get(
        interaction.client.voice_clients,
        guild=interaction.guild
    )
    if voice_client.is_connected():
        queue.switch_repeat(interaction.user.voice.channel.id)
        await interaction.send('Current song set to repeat')
    else:
        await interaction.send(
            f'**{interaction.user.name}** i`m not even in voice channel! {DefaultEmoji.kissing_heart} '
        )
