import math

import nextcord
from nextcord import Member

from bot import database
from bot.database.models.playlist import PlaylistModel
from bot.views import BaseView
from bot.buttons.users.playlists import Cancel
from bot.buttons.users.playlists.playlist import AddSong, Play
from bot.buttons.users.playlists.pagination import ArrowLeft, ArrowRight


class PlaylistView(BaseView):
    songs_on_page: str

    def __init__(self, member: nextcord.Member, playlist: PlaylistModel, count_songs: int, limit: int):
        super().__init__(member, timeout=None)
        self.add_item(Cancel())
        self.playlist = playlist
        self.name = playlist.name
        self.page = 1
        self.count_songs = count_songs
        self.limit = limit
        self.refresh_buttons()

    def remove_pagination(self):
        for child in self.children:
            if isinstance(child, (ArrowLeft, ArrowRight, Play)):
                child.remove_button()

    def refresh_buttons(self):
        self.clear_items()
        self.add_item(AddSong())
        self.add_item(Cancel())
        if self.is_paginated:
            arrow_left = ArrowLeft(self.page == 1)
            arrow_right = ArrowRight(self.page == self.count_page)
            self.insert_item(1, arrow_left)
            self.insert_item(-1, arrow_right)
            self.insert_item(
                len(self.children) // 2,
                Play()
            )

    async def refresh_view(self):
        songs = await database.get_playlist_songs(
            self.playlist,
            self.page,
            self.limit
        )
        if not songs:
            return
        self.refresh_buttons()
        self.songs_on_page = ''
        for idx, song_title in enumerate(songs):
            number_song = idx + 1 + (self.page - 1) * self.limit
            if idx + 1 != len(songs):
                self.songs_on_page += f'{number_song} -- {song_title}\n'
                continue
            self.songs_on_page += f'{number_song} -- {song_title}'

    @property
    def content_on_page(self) -> str:
        content = self.base_content
        if self.songs_on_page:
            content += f'\n{self.songs_on_page}'
        return content

    @property
    def count_page(self) -> int:
        return math.ceil(self.count_songs / self.limit)

    @property
    def is_paginated(self) -> bool:
        return self.count_page > 1

    @classmethod
    async def show(cls, count: int, member: Member, playlist: PlaylistModel):
        count_songs = await database.get_count_songs_in_playlists(playlist)
        self = cls(member, playlist, count_songs, count)
        self.base_content = f'Playlist with name **{playlist.name}** was created by {playlist.tag_member}'
        songs = await database.get_playlist_songs(
            self.playlist,
            self.page,
            self.limit
        )
        self.songs_on_page = ''
        if songs:
            for idx, song_title in enumerate(songs):
                if idx + 1 != len(songs):
                    self.songs_on_page += f'{idx + 1} -- {song_title}\n'
                    continue
                self.songs_on_page += f'{idx + 1} -- {song_title}'
        return self

    @classmethod
    async def create(cls, count: int,  member: Member, name: str):
        playlist = await database.create_playlist(member, name)
        self = await cls.show(count, member, playlist)
        return self
