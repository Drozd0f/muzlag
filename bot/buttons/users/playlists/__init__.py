import nextcord

from bot.src import Emoji


class Cancel(nextcord.ui.Button):
    def __init__(self):
        super().__init__(
            label='Cancel',
            style=nextcord.ButtonStyle.red,
            emoji=Emoji.abuffering
        )

    async def callback(self, interaction: nextcord.Interaction):
        self.view.set_disable_buttons(True)
        await interaction.response.edit_message(view=self.view)
        self.view.stop()
