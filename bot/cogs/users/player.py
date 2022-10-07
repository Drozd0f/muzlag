from nextcord.ext import commands

from bot.src.emoji import CenterEmoji
from bot.cogs.users.play import play
from bot.cogs.users.queue import queue
from bot.cogs.users.repeat import repeat
from bot.cogs.users.skip import skip
from bot.cogs.users.stop import stop


class Player(commands.Cog):
    """Show player commands"""

    COG_EMOJI = CenterEmoji.rem_dance

    @commands.command(name='play', help='Play song by link or add to queue')
    async def play(self, ctx: commands.context.Context, url: str):
        await play(ctx, url)

    @commands.command(name='stop', help='Stop all songs in queue')
    async def stop(self, ctx: commands.context.Context):
        await stop(ctx)

    @commands.command(name='skip', help='Skip current song (default) or several songs')
    async def skip(self, ctx: commands.context.Context, count: int = 1):
        await skip(ctx, count)

    @commands.command(name='repeat', help='Set song to repeat')
    async def repeat(self, ctx: commands.context.Context):
        await repeat(ctx)

    @commands.command(name='queue', help='Show songs queue')
    async def queue(self, ctx: commands.context.Context):
        await queue(ctx)
