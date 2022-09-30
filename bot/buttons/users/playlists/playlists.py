import typing as t

import nextcord

from bot.database.models.playlist import PlaylistModel
from bot.views.users.playlists.playlist import PlaylistView


class PlaylistSelect(nextcord.ui.Select):
    def __init__(self, playlists: t.List[PlaylistModel]):
        super().__init__(
            placeholder='Chose playlist name',
            options=[nextcord.SelectOption(label=playlist.name) for playlist in playlists]
        )
        self.playlists = {playlist.name: playlist for playlist in playlists}

    async def callback(self, interaction: nextcord.Interaction):
        chose_playlist = self.playlists[self.values[0]]
        playlist_view = await PlaylistView.show(self.view.member, self.view.member_content, chose_playlist)
        await playlist_view.refresh_view()
        await interaction.response.edit_message(content=playlist_view.content_on_page, view=playlist_view)
        await playlist_view.wait()
        await interaction.edit_original_message(content=self.view.content_on_page, view=self.view)
