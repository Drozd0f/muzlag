import typing as t

import nextcord

from bot.src.emoji import Emoji, HelpEmoji
from bot.config import ViewConfig


class HelpDropdown(nextcord.ui.Select):
    home_option_name = 'Home'
    cancel_option_name = 'Cancel'

    def __init__(self, help_command, options: t.List[nextcord.SelectOption]):
        options.insert(0, nextcord.SelectOption(
            label=self.home_option_name,
            emoji=HelpEmoji.home,
            description='Go back to the main menu'
        ))
        options.append(nextcord.SelectOption(
            label=self.cancel_option_name,
            emoji=Emoji.abuffering,
            description='Cancel from the help menu'
        ))
        super().__init__(
            placeholder='Choose command...',
            options=options
        )
        self._help_command = help_command

    async def callback(self, interaction: nextcord.Interaction):
        chose_option = self.values[0]
        if chose_option == self.cancel_option_name:
            self.view.set_disable_select_menu(True)
            await interaction.response.edit_message(view=self.view, delete_after=2)
            self.view.stop()
            return
        elif chose_option == self.home_option_name:
            embed = await self._help_command.bot_help_embed(self._help_command.get_bot_mapping())
        else:
            embed = await self._help_command.cog_help_embed(self._help_command.context.bot.get_cog(chose_option))
        await interaction.response.edit_message(embed=embed)


class HelpView(nextcord.ui.View):
    def __init__(self, help_command,
                 options: t.List[nextcord.SelectOption],
                 timeout: t.Optional[float] = ViewConfig.delete_after):
        super().__init__(timeout=timeout)
        self._help_command = help_command
        self.add_item(HelpDropdown(self._help_command, options))

    async def interaction_check(self, interaction: nextcord.Interaction) -> bool:
        return self._help_command.context.author == interaction.user

    def set_disable_select_menu(self, disabled: bool):
        for child in self.children:
            child.disabled = disabled
