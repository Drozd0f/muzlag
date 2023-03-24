import asyncio

import nextcord
from nextcord.ext import commands

from bot.src.queue import MuzlagQueue
from bot.src.emoji import DefaultEmoji
from bot.src.decorators import c_voice_required, s_voice_required


@c_voice_required
async def c_stop(ctx: commands.Context):
    queue = MuzlagQueue()
    if ctx.message.author.voice.channel.id not in queue:
        await ctx.send(f'**{ctx.message.author.name}** from where you sad that? {DefaultEmoji.thinking} ')
        return
    if ctx.voice_client.is_connected():
        try:
            queue.drop(ctx.message.author.voice.channel.id)
        except asyncio.QueueEmpty:
            ctx.voice_client.stop()
    else:
        await ctx.send(f'**{ctx.message.author.name}** i`m not even in voice channel! {DefaultEmoji.kissing_heart} ')


@s_voice_required
async def s_stop(interaction: nextcord.Interaction):
    queue = MuzlagQueue()
    if interaction.user.voice.channel.id not in queue:
        await interaction.send('The queue was already empty. '
                               f'**{interaction.user.name}** from where you sad that? {DefaultEmoji.thinking} ')
        return
    voice_client = nextcord.utils.get(
        interaction.client.voice_clients,
        guild=interaction.guild
    )
    if voice_client.is_connected():
        try:
            queue.drop(interaction.user.voice.channel.id)
        except asyncio.QueueEmpty:
            await interaction.send('Try stopping playback')
            voice_client.stop()
    else:
        await interaction.send(
            f'**{interaction.user.name}** i`m not even in voice channel! {DefaultEmoji.kissing_heart} '
        )
