import nextcord

from bot.src import PaginationEmoji


class ArrowLeft(nextcord.ui.Button):
    def __init__(self, disabled: bool = True):
        super().__init__(
            style=nextcord.ButtonStyle.grey,
            emoji=PaginationEmoji.arrow_left
        )
        self.disabled = disabled

    async def callback(self, interaction: nextcord.Interaction):
        page = self.view.page - 1
        self.view.page = max(page, 1)
        await self.view.refresh_view()
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
        page = self.view.page + 1
        self.view.page = min(page, self.view.count_page)
        await self.view.refresh_view()
        await interaction.response.edit_message(
            content=self.view.content_on_page,
            view=self.view
        )

    def remove_button(self):
        self.view.remove_item(self)
