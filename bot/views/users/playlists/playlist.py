import math
import typing as t

from nextcord import Member

from bot import database
from bot.config import Config
from bot.database.models.playlist import PlaylistModel
from bot.database.models.paginator import PaginatorModel
from bot.database.models.songs import SongModel
from bot.views import BaseView
from bot.buttons.users.playlists import Cancel
from bot.buttons.users.playlists.playlist import AddSong, Play
from bot.buttons.users.playlists.pagination import ArrowLeft, ArrowRight


class PlaylistView(BaseView):
    def __init__(self, member: Member, member_content: str, playlist: PlaylistModel, count_songs: int):
        super().__init__(member)
        self.member_content = member_content
        self.add_item(Cancel())
        self.playlist = playlist
        self.name = playlist.name
        self.is_playlist_owner = self.member.id == playlist.member_id
        self.page = 1
        self.count_songs = count_songs
        self.limit = Config.playlist_limit
        self.songs_on_page = ''
        self.refresh_buttons()

    def remove_pagination(self):
        for child in self.children:
            if isinstance(child, (ArrowLeft, ArrowRight, Play)):
                child.remove_button()

    def refresh_buttons(self):
        self.clear_items()
        self.add_item(AddSong(not self.is_playlist_owner))
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

    def refresh_song_on_page(self, songs: t.List[SongModel]):
        self.songs_on_page = ''
        for idx, song in enumerate(songs):
            number_song = idx + 1 + (self.page - 1) * self.limit
            if idx + 1 != len(songs):
                self.songs_on_page += f'{number_song} -- {song.title}\n'
                continue
            self.songs_on_page += f'{number_song} -- {song.title}'

    async def refresh_view(self):
        songs = await database.get_playlist_songs(
            self.playlist,
            PaginatorModel(self.page)
        )
        if not songs:
            return
        self.count_songs = await database.get_count_songs_in_playlists(self.playlist)
        self.refresh_buttons()
        self.refresh_song_on_page(songs)

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
    async def show(cls, member: Member, member_content: str, playlist: PlaylistModel):
        count_songs = await database.get_count_songs_in_playlists(playlist)
        self = cls(member, member_content, playlist, count_songs)
        self.base_content = f'Playlist with name **{playlist.name}** was created by {playlist.tag_member}'
        songs = await database.get_playlist_songs(
            self.playlist,
            PaginatorModel(self.page)
        )
        if songs:
            self.refresh_song_on_page(songs)
        return self

    @classmethod
    async def create(cls, member: Member, member_content: str, name: str):
        playlist = await database.create_playlist(member, name)
        self = await cls.show(member, member_content, playlist)
        return self
