import math
import typing as t

import nextcord

from bot.views import BaseView
from bot import database
from bot.database.models.playlist import PlaylistModel
from bot.buttons.users.playlists.playlists import PlaylistSelect
from bot.buttons.users.playlists import Cancel
from bot.buttons.users.playlists.pagination import ArrowLeft, ArrowRight


class PlaylistsView(BaseView):
    playlists_on_page: str

    def __init__(self, member: nextcord.Member, playlists: t.List[PlaylistModel], count_playlists: int, limit: int):
        super().__init__(member, timeout=None)
        self.is_personal = False
        self.page = 1
        self.count_playlists = count_playlists
        self.limit = limit
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

    async def refresh_view(self):
        if self.is_personal:
            playlists = await database.get_member_playlists(self.member, self.page, self.limit)
            self.count_playlists = await database.get_member_count_playlists(self.member)
        else:
            playlists = await database.get_all_playlists(self.page, self.limit)
            self.count_playlists = await database.get_count_playlists()
        self.refresh_buttons(playlists)
        self.playlists_on_page = ''
        for idx, playlist in enumerate(playlists):
            number_playlist = idx + 1 + (self.page - 1) * self.limit
            if idx + 1 != len(playlists):
                self.playlists_on_page += f'{number_playlist} -- {playlist.name}\n'
                continue
            self.playlists_on_page += f'{number_playlist} -- {playlist.name}'

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
    async def show(cls, count: int, member: nextcord.Member, member_playlists: bool = False):
        if member_playlists:
            playlists = await database.get_member_playlists(member, page=1, limit=count)
            count_playlists = await database.get_member_count_playlists(member)
            base_content = f'<@{member.id}> playlists'
            is_personal = False
        else:
            playlists = await database.get_all_playlists(page=1, limit=count)
            count_playlists = await database.get_count_playlists()
            base_content = 'All playlists'
            is_personal = True

        if playlists is not None:
            self = cls(member, playlists, count_playlists, count)
            self.is_personal = is_personal
            self.base_content = base_content
            playlists_on_page = ''
            for idx, playlist in enumerate(playlists):
                if idx + 1 != len(playlists):
                    playlists_on_page += f'{idx + 1} -- {playlist.name}\n'
                    continue
                playlists_on_page += f'{idx + 1} -- {playlist.name}'
            self.playlists_on_page = playlists_on_page
            return self
