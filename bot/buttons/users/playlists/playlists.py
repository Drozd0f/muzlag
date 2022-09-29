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
        self.playlists = playlists

    async def callback(self, interaction: nextcord.Interaction):
        chose_playlist = self.values[0]
        for playlist in self.playlists:
            if playlist.name == chose_playlist:
                chose_playlist = playlist
                break
        playlist_view = await PlaylistView.show(self.view.limit, self.view.member, chose_playlist)
        await playlist_view.refresh_view()
        await interaction.response.edit_message(content=playlist_view.content_on_page, view=playlist_view)
        await playlist_view.wait()
        await interaction.edit_original_message(content=self.view.content_on_page, view=self.view)


class PlaylistButton(nextcord.ui.Button):
    def __init__(self, playlist: PlaylistModel):
        super().__init__(
            label=playlist.name,
            style=nextcord.ButtonStyle.blurple,
        )
        self.playlist = playlist

    async def callback(self, interaction: nextcord.Interaction):
        playlist_view = await PlaylistView.show(self.view.limit, self.view.member, self.playlist)
        await playlist_view.refresh_view()
        await interaction.response.edit_message(content=playlist_view.content_on_page, view=playlist_view)
        await playlist_view.wait()
        await interaction.edit_original_message(content=self.view.base_content, view=self.view)
