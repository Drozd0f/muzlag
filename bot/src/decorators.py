from nextcord.ext import commands


def voice_required(cog):
    async def wrapped(ctx: commands.context.Context, *args, **kwargs):
        if not ctx.message.author.voice:
            await ctx.send(f'**{ctx.message.author.name}** from where you sad that? :thinking: ')
            return
        return await cog(ctx, *args, **kwargs)
    return wrapped
