from nextcord.ext import commands

from bot.src.emoji import HelpEmoji
from bot.cogs.help.help import HelpCommand


class HelpCog(commands.Cog, name='Help'):
    """Show help info about commands"""

    COG_EMOJI = HelpEmoji.help_

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = HelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self._original_help_command
