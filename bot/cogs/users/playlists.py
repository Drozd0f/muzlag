from nextcord.ext import commands

from bot.views.users.playlists.menu import PlaylistsMenu
from bot.src.emoji import CenterEmoji


class Playlists(commands.Cog):
    """Show playlists menu"""

    COG_EMOJI = CenterEmoji.nqnm

    @commands.command(name='playlists', help='Command show buttons for use playlists')
    async def playlists(self, ctx: commands.context.Context):
        await ctx.message.delete()
        view = PlaylistsMenu(member=ctx.author)
        msg = await ctx.send(view.base_content, view=view)
        await view.wait()
        await msg.delete(delay=1)
