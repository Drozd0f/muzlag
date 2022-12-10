import nextcord
from nextcord.ext import commands
from nextcord import slash_command

from bot.src.emoji import CenterEmoji
from bot.cogs.users.player.play import c_play, s_play
from bot.cogs.users.player.queue import c_queue, s_queue
from bot.cogs.users.player.repeat import c_repeat, s_repeat
from bot.cogs.users.player.skip import c_skip, s_skip
from bot.cogs.users.player.stop import c_stop, s_stop


class Player(commands.Cog):
    """Show player commands"""

    COG_EMOJI = CenterEmoji.rem_dance

    @commands.command(name='play', help='Play song by link or add to queue')
    async def c_play(self, ctx: commands.context.Context, url: str):
        await c_play(ctx, url)

    @slash_command(name='play', description='Play song by link or add to queue')
    async def s_play(self, interaction: nextcord.Interaction, url: str):
        await s_play(interaction, url)

    @commands.command(name='stop', help='Stop all songs in queue')
    async def c_stop(self, ctx: commands.context.Context):
        await c_stop(ctx)

    @commands.command(name='skip', help='Skip current song (default) or several songs')
    async def c_skip(self, ctx: commands.context.Context, count: int = 1):
        await c_skip(ctx, count)

    @commands.command(name='repeat', help='Set current song to repeat')
    async def c_repeat(self, ctx: commands.context.Context):
        await c_repeat(ctx)

    @commands.command(name='queue', help='Show songs queue')
    async def c_queue(self, ctx: commands.context.Context):
        await c_queue(ctx)

    @slash_command(name='stop', description='Stop all songs in queue')
    async def s_stop(self, interaction: nextcord.Interaction):
        await s_stop(interaction)

    @slash_command(name='skip', description='Skip current song (default) or several songs')
    async def s_skip(self, interaction: nextcord.Interaction, count: int = 1):
        await s_skip(interaction, count)

    @slash_command(name='repeat', description='Set current song to repeat')
    async def s_repeat(self, interaction: nextcord.Interaction):
        await s_repeat(interaction)

    @slash_command(name='queue', description='Show songs queue')
    async def s_queue(self, interaction: nextcord.Interaction):
        await s_queue(interaction)
