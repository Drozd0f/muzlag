import asyncio
import logging
import typing as t

import nextcord
from nextcord import VoiceChannel
from nextcord.ext import commands

from bot.src.decorators import c_voice_required, s_voice_required
from bot.src.queue import MuzlagQueue
from bot.src.players import player_factory
from bot.src.emoji import DefaultEmoji


def logging_player_error(error):
    if error:
        logging.error(f'Player error: {error}')


@c_voice_required
async def c_play(ctx: commands.Context, url: str):
    channel: VoiceChannel = ctx.message.author.voice.channel
    queue = MuzlagQueue()
    player = player_factory(url)
    await queue.push(channel.id, player)
    await ctx.send(f'{DefaultEmoji.white_chk_m} Added to playback {DefaultEmoji.ok}: **{player.title}**')

    if ctx.voice_client is not None:
        return

    await channel.connect()

    while True:
        try:
            async with ctx.typing():
                player = queue.get(channel.id)
                ctx.voice_client.play(
                    player.play(),
                    after=logging_player_error
                )
            if not queue.is_repeat(channel.id):
                await ctx.send(
                    f'{DefaultEmoji.musical_note} Now playing {DefaultEmoji.musical_note} : **{player.title}**'
                )

            while ctx.voice_client.is_playing():
                await asyncio.sleep(1)
                vc_usr_list = channel.voice_states
                if len(vc_usr_list) <= 1:
                    await ctx.send(
                        f'{DefaultEmoji.scream_cat} No one in voice channel {DefaultEmoji.anger}, leaving ...'
                    )
                    queue.drop(channel.id)
        except asyncio.QueueEmpty:
            break
        except AttributeError:
            return
    await ctx.voice_client.disconnect()
    await ctx.send(f'Playback stopped, bye {DefaultEmoji.sleeping}')


@s_voice_required
async def s_play(interaction: nextcord.Interaction, url: str):
    channel: VoiceChannel = interaction.user.voice.channel
    queue = MuzlagQueue()
    player = player_factory(url)
    await queue.push(channel.id, player)
    await interaction.send(
        f'{DefaultEmoji.white_chk_m} '
        f'Added to playback {DefaultEmoji.ok}: **{player.title}**'
    )

    await play_with_interaction(queue, interaction)


async def play_with_interaction(queue: MuzlagQueue, interaction: nextcord.Interaction):
    channel: VoiceChannel = interaction.user.voice.channel
    voice_client: t.Optional[nextcord.utils.T] = nextcord.utils.get(
        interaction.client.voice_clients,
        guild=interaction.guild
    )

    if voice_client is not None:
        return

    await channel.connect()

    voice_client: t.Optional[nextcord.utils.T] = nextcord.utils.get(
        interaction.client.voice_clients,
        guild=interaction.guild
    )

    while True:
        try:
            player = queue.get(channel.id)
            voice_client.play(
                player.play(),
                after=logging_player_error
            )
            if not queue.is_repeat(channel.id):
                await interaction.send(
                    f'{DefaultEmoji.musical_note} Now playing {DefaultEmoji.musical_note} '
                    f': **{player.title}**', delete_after=10
                )

            while voice_client.is_playing():
                await asyncio.sleep(1)
                vc_usr_list = channel.voice_states
                if len(vc_usr_list) <= 1:
                    await interaction.send(
                        f'{DefaultEmoji.scream_cat} No one in voice channel'
                        f'{DefaultEmoji.anger}, leaving ...', delete_after=3
                    )
                    queue.drop(channel.id)
        except asyncio.QueueEmpty:
            break
    await voice_client.disconnect()
    await interaction.send('Playback stopped, bye {DefaultEmoji.sleeping}', delete_after=3)
