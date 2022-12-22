import nextcord

from bot.src.emoji import PaginationEmoji


class ArrowLeft(nextcord.ui.Button):
    def __init__(self, disabled: bool = True):
        super().__init__(
            style=nextcord.ButtonStyle.grey,
            emoji=PaginationEmoji.arrow_left
        )
        self.disabled = disabled

    async def callback(self, interaction: nextcord.Interaction):
        self.view.page = max(self.view.page - 1, 1)
        await self.view.refresh_view()
        self.view.refresh_timeout()
        await interaction.response.edit_message(
            content=self.view.content_on_page,
            view=self.view
        )

    def remove_button(self):
        self.view.remove_item(self)


class ArrowRight(nextcord.ui.Button):
    def __init__(self, disabled: bool = False):
        super().__init__(
            style=nextcord.ButtonStyle.grey,
            emoji=PaginationEmoji.arrow_right
        )
        self.disabled = disabled

    async def callback(self, interaction: nextcord.Interaction):
        self.view.page = min(self.view.page + 1, self.view.count_page)
        await self.view.refresh_view()
        self.view.refresh_timeout()
        await interaction.response.edit_message(
            content=self.view.content_on_page,
            view=self.view
        )

    def remove_button(self):
        self.view.remove_item(self)
