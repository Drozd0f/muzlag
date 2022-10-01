import logging

import nextcord
from nextcord.message import Message
from nextcord import errors

from bot.errors import playlist
from bot.src.emoji import Emoji, CenterEmoji
from bot.views import BaseView
from bot.views.users.playlists.playlist import PlaylistView
from bot.views.users.playlists.playlists import PlaylistsView
from bot.buttons.users.playlists import Cancel


log = logging.getLogger(__name__)


class PlaylistsMenu(BaseView):
    def __init__(self, member: nextcord.Member):
        super().__init__(member, timeout=None)
        self.member_content = f'Playlists menu for {self.tag_member}'
        self.add_item(Cancel())

    @nextcord.ui.button(label='Create playlist', style=nextcord.ButtonStyle.blurple, emoji=CenterEmoji.nqnm)
    async def create_playlist(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.set_disable_buttons(True)
        prev_emoji = button.emoji
        button.emoji = Emoji.loading
        await interaction.response.edit_message(
            content=f'{self.base_content}\nGive your playlist name',
            view=self
        )
        button.emoji = prev_emoji
        self.set_disable_buttons(False)

        def check(msg):
            return msg.author == self.member and msg.channel == interaction.message.channel
        msg: Message = await interaction.client.wait_for('message', check=check)

        try:
            await msg.delete(delay=1)
            playlist_view = await PlaylistView.create(self.member, self.member_content, msg.content)
            log.info(f'Playlist with name {playlist_view.name} was created')
            await msg.delete(delay=1)
            await interaction.edit_original_message(
                content=playlist_view.base_content,
                view=playlist_view
            )
            await playlist_view.wait()
        except errors.NotFound as exc:
            log.error(exc)
            await interaction.send(f'The problem of deleting {self.tag_member} message, try again!')
        except playlist.PlaylistNameExists:
            content = f'Playlist with name **{msg.content}** already exists'
            log.info(content)
            await interaction.send(content, delete_after=5)
        await interaction.edit_original_message(
            content=self.base_content,
            view=self
        )

    @nextcord.ui.button(label='My playlists', style=nextcord.ButtonStyle.green, emoji=Emoji.crabrave)
    async def get_user_playlists(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        playlists_view = await PlaylistsView.show(self.member, self.member_content, member_playlists=True)
        if playlists_view:
            await interaction.response.edit_message(
                content=playlists_view.content_on_page,
                view=playlists_view
            )
            await playlists_view.wait()
            await interaction.edit_original_message(
                content=self.base_content,
                view=self
            )
            return
        await interaction.send(f'{self.tag_member} have\'t created playlists', delete_after=5)

    @nextcord.ui.button(label='All playlists', style=nextcord.ButtonStyle.grey, emoji=Emoji.feels_beats_man)
    async def get_all_playlists(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        playlists_view = await PlaylistsView.show(self.member, self.member_content)
        if playlists_view:
            await interaction.response.edit_message(
                content=playlists_view.content_on_page,
                view=playlists_view
            )
            await playlists_view.wait()
            await interaction.edit_original_message(
                content=self.base_content,
                view=self
            )
            return
        await interaction.send('No one has created a playlist', delete_after=5)
