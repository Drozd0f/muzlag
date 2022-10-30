import nextcord


class SongChooserButton(nextcord.ui.Button):
    def __init__(self, emoji: str, song_number: int):
        self.song_number = song_number
        super().__init__(
            style=nextcord.ButtonStyle.green,
            emoji=emoji
        )

    async def callback(self, interaction: nextcord.Interaction):
        self.view.chosen_song = self.song_number
        self.view.set_disable_buttons(True)
        await interaction.response.edit_message(view=self.view)
        self.view.stop()
