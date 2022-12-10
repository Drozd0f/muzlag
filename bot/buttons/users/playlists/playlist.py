import asyncio
import logging

import nextcord
from nextcord import Message
from nextcord.errors import NotFound

from bot.src.queue import MuzlagQueue
from bot.src.players import player_factory
from bot.cogs.users.player.play import play_with_interaction

from bot.src.emoji import Emoji, CenterEmoji
from bot.src.yt_search import YoutubeSearch
from bot import database
from bot.errors.playlist import SongInPlaylistExists
from bot.errors.yt_search import URLNotValid

log = logging.getLogger(__name__)


class AddSong(nextcord.ui.Button):
    def __init__(self, disabled=False):
        super().__init__(
            label='Add song',
            style=nextcord.ButtonStyle.grey,
            emoji=Emoji.squirtle_hype,
            disabled=disabled,
        )
        self.save = False

    async def callback(self, interaction: nextcord.Interaction):
        if interaction.user.id != self.view.member.id:
            self.disabled = True
            return

        save_button = Save(self)
        self.disabled = True
        self.emoji = Emoji.loading
        self.view.insert_item(1, save_button)
        self.view.remove_pagination()

        await interaction.response.edit_message(content='Send YouTube video link', view=self.view)

        def check(msg):
            return msg.author == self.view.member and msg.channel == interaction.message.channel

        while not self.save:
            msg: Message = await interaction.client.wait_for('message', check=check)
            await msg.delete()

            try:
                song = await database.create_song(YoutubeSearch.from_url(msg.content))
                await database.update_playlist(self.view.playlist, song)
            except URLNotValid:
                msg = await interaction.send(f'**{msg.content}**: is not YouTube video link')
            except SongInPlaylistExists:
                msg = await interaction.send(f'Song: **{song.title}** already in playlist')
            else:
                msg = await interaction.send(f'Song: **{song.title}** was add in playlist')

            await msg.delete(delay=3)

            await asyncio.sleep(1)
        self.save = False


class Save(nextcord.ui.Button):
    def __init__(self, disable_button: nextcord.ui.Button):
        super().__init__(
            label='Save',
            style=nextcord.ButtonStyle.green,
            emoji=CenterEmoji.chika
        )
        self.disable_button = disable_button
        self.disable_emoji = disable_button.emoji

    async def callback(self, interaction: nextcord.Interaction):
        self.disable_button.save = True
        self.disable_button.disabled = False
        self.disable_button.emoji = self.disable_emoji
        self.view.remove_item(self)
        await self.view.refresh_view()
        await interaction.response.edit_message(content=self.view.content_on_page, view=self.view)


class Play(nextcord.ui.Button):
    def __init__(self):
        super().__init__(
            label='Play',
            style=nextcord.ButtonStyle.green,
            emoji=CenterEmoji.rem_dance
        )

    async def callback(self, interaction: nextcord.Interaction):
        channel_id = interaction.user.voice.channel.id
        songs = await database.get_all_songs_from_playlist(self.view.playlist)
        queue = MuzlagQueue()

        for song in songs:
            await queue.push(channel_id, player_factory(song.url))

        try:
            self.disabled = True
            await interaction.response.edit_message(content=self.view.content_on_page, view=self.view)

            await play_with_interaction(queue, interaction)

            self.disabled = False
            await interaction.edit_original_message(content=self.view.content_on_page, view=self.view)
        except NotFound as exc:
            log.error(exc)
            await interaction.send(
                f'The problem of deleting {self.view.tag_member} message, try again!', delete_after=3
            )

    def remove_button(self):
        self.view.remove_item(self)
