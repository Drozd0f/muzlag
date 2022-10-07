import nextcord
from nextcord import slash_command
from nextcord.ext import commands

from bot.src.emoji import HelpEmoji


class Ping(commands.Cog):
    """Receives ping commands"""

    COG_EMOJI = HelpEmoji.ping

    @commands.command(name='ping', help='Healthcheck')
    async def ping(self, ctx: commands.context.Context):
        await ctx.send('pong', delete_after=5)

    @slash_command(name='ping', description='Healthcheck')
    async def slash_ping(self, interaction: nextcord.Interaction):
        await interaction.send('pong', delete_after=5)
