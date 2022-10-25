import typing as t

import nextcord
from nextcord import Member

from bot.config import Config
from bot.src.emoji import DefaultEmoji
from bot.buttons.users.playlists import Cancel
from bot.buttons.users.yt_link_changer import SongChooserButton


class SongChooserView(nextcord.ui.View):
    chosen_song: t.Optional[int] = None

    def __init__(self, member: Member, timeout: t.Optional[float] = 60):
        super().__init__(timeout=timeout)
        self.member = member
        emoji_list = list(DefaultEmoji.gen_num_emoji(Config.playlist_limit))
        if emoji_list:
            for idx in range(Config.playlist_limit):
                self.add_item(
                    SongChooserButton(emoji_list[idx], idx)
                )
        self.add_item(Cancel())

    def set_disable_buttons(self, disabled: bool):
        for child in self.children:
            child.disabled = disabled

    async def interaction_check(self, interaction: nextcord.Interaction) -> bool:
        is_member = self.member == interaction.user
        if not is_member:
            await interaction.send(f"Don't touch me <@{interaction.user.id}>", delete_after=5)
        return is_member
