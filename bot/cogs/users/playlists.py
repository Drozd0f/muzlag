from nextcord.ext import commands

from bot.views.users.playlists import Playlists


@commands.command()
async def playlists(ctx: commands.context.Context):
    view = Playlists(member=ctx.author)
    msg = await ctx.send('Playlists', view=view)
    await view.wait()
    await msg.delete(delay=1)
