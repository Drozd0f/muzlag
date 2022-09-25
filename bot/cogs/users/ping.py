from nextcord.ext import commands


@commands.command(name='ping', help='Healthcheck')
async def ping(ctx: commands.context.Context):
    await ctx.send('pong')
