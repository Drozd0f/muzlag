import typing as t

import nextcord


class BaseView(nextcord.ui.View):
    member_content: str
    _base_content: t.Optional[str] = None

    def __init__(self, member: nextcord.Member, timeout: t.Optional[float] = 60):
        super().__init__(timeout=timeout)
        self.member = member

    def insert_item(self, idx: int, item: nextcord.ui.Item):
        if len(self.children) > 25:
            raise ValueError("Maximum number of children exceeded")

        if not isinstance(item, nextcord.ui.Item):
            raise TypeError(f"Expected Item not {item.__class__!r}")

        item._view = self
        self.children.insert(idx, item)

    async def interaction_check(self, interaction: nextcord.Interaction) -> bool:
        is_member = self.member == interaction.user
        if not is_member:
            await interaction.send(f"Don't touch me <@{interaction.user.id}>", delete_after=5)
        return is_member

    def set_disable_buttons(self, disabled: bool):
        for child in self.children:
            child.disabled = disabled

    @property
    def base_content(self) -> str:
        return self._base_content if self._base_content else self.member_content

    @base_content.setter
    def base_content(self, content: str):
        self._base_content = f'{self.member_content}\n{content}'

    @property
    def tag_member(self) -> str:
        return f'<@{self.member.id}>'
