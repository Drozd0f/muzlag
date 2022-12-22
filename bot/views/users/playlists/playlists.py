import math
import typing as t

import nextcord

from bot.config import Config
from bot.views import BaseView
from bot import database
from bot.database.models.playlist import PlaylistModel
from bot.database.models.paginator import PaginatorModel
from bot.buttons.users.playlists.playlists import PlaylistSelect
from bot.buttons.users.playlists import Cancel
from bot.buttons.users.playlists.pagination import ArrowLeft, ArrowRight


class PlaylistsView(BaseView):
    def __init__(self, member: nextcord.Member, member_content: str,
                 playlists: t.List[PlaylistModel], count_playlists: int):
        super().__init__(member)
        self.member_content = member_content
        self.is_personal = False
        self.page = 1
        self.count_playlists = count_playlists
        self.limit = Config.playlist_limit
        self.playlists_on_page = ''
        self.refresh_buttons(playlists)

    def refresh_buttons(self, playlists: t.List[PlaylistModel]):
        self.clear_items()
        if playlists:
            select_menu = PlaylistSelect(playlists)
            self.add_item(select_menu)
        if self.is_paginated:
            arrow_left = ArrowLeft(self.page == 1)
            arrow_right = ArrowRight(self.page == self.count_page)
            self.add_item(arrow_left)
            self.add_item(arrow_right)
        self.add_item(Cancel())

    def refresh_playlists_on_page(self, playlists: t.List[PlaylistModel]):
        self.playlists_on_page = ''
        for idx, playlist in enumerate(playlists):
            number_playlist = idx + 1 + (self.page - 1) * self.limit
            if idx + 1 != len(playlists):
                self.playlists_on_page += f'{number_playlist} -- {playlist.name}\n'
                continue
            self.playlists_on_page += f'{number_playlist} -- {playlist.name}'

    async def refresh_view(self):
        if self.is_personal:
            playlists = await database.get_member_playlists(self.member, PaginatorModel(self.page))
            self.count_playlists = await database.get_member_count_playlists(self.member)
        else:
            playlists = await database.get_all_playlists(PaginatorModel(self.page))
            self.count_playlists = await database.get_count_playlists()
        self.refresh_buttons(playlists)
        self.refresh_playlists_on_page(playlists)

    @property
    def content_on_page(self) -> str:
        content = self.base_content
        if self.playlists_on_page:
            content += f'\n{self.playlists_on_page}'
        return content

    @property
    def count_page(self) -> int:
        return math.ceil(self.count_playlists / self.limit)

    @property
    def is_paginated(self) -> bool:
        return self.count_page > 1

    @classmethod
    async def show(cls, member: nextcord.Member, member_content: str, member_playlists: bool = False):
        if member_playlists:
            playlists = await database.get_member_playlists(member, PaginatorModel(page=1))
            count_playlists = await database.get_member_count_playlists(member)
            base_content = 'Your playlists'
        else:
            playlists = await database.get_all_playlists(PaginatorModel(page=1))
            count_playlists = await database.get_count_playlists()
            base_content = 'All playlists'

        if playlists is not None:
            self = cls(member, member_content, playlists, count_playlists)
            self.is_personal = member_playlists
            self.base_content = base_content
            self.refresh_playlists_on_page(playlists)
            return self
