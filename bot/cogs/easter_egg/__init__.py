from nextcord.ext import commands

from bot.cogs.users.player.play import c_play


@commands.command(name='danilo', help='Play Danilo song', hidden=True)
async def danilo(ctx: commands.context.Context):
    await c_play(ctx, 'https://youtu.be/jZlkINQLGro')


@commands.command(name='vovan', help='Play Vovan song', hidden=True)
async def vovan(ctx: commands.context.Context):
    await c_play(ctx, 'https://youtu.be/wt-jj1qNScI')


@commands.command(name='nikita', help='Play Nikita song', hidden=True)
async def nikita(ctx: commands.context.Context):
    await c_play(ctx, 'https://youtu.be/7w9huXMoZF0')


@commands.command(name='vadick', help='Play Vadick song', hidden=True)
async def vadick(ctx: commands.context.Context):
    await c_play(ctx, 'https://youtu.be/L4hPnTpE2JE')


@commands.command(name='vadoom', help='Play Vadoom song', hidden=True)
async def vadoom(ctx: commands.context.Context):
    await c_play(ctx, 'https://youtu.be/vCb1SGRceik')


def register_cogs(bot: commands.Bot):
    bot.add_command(danilo)
    bot.add_command(vovan)
    bot.add_command(nikita)
    bot.add_command(vadick)
    bot.add_command(vadoom)
