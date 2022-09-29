from nextcord.ext import commands

from bot.views.users.playlists.menu import PlaylistsMenu


@commands.command(name='playlists', help='Command show buttons for use playlists')
async def playlists(ctx: commands.context.Context):
    await ctx.message.delete()
    view = PlaylistsMenu(member=ctx.author)
    msg = await ctx.send(view.base_content, view=view)
    await view.wait()
    await msg.delete(delay=1)
