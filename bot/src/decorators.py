import nextcord
from nextcord.ext import commands

from bot.config import Config


def c_voice_required(cog):
    async def wrapped(ctx: commands.Context, *args, **kwargs):
        if not ctx.message.author.voice:
            await ctx.send(Config.voice_required_text.format(ctx.message.author.name))
            return
        await cog(ctx, *args, **kwargs)
    return wrapped


def s_voice_required(cog):
    async def wrapped(interaction: nextcord.Interaction, *args, **kwargs):
        if not interaction.user.voice:
            await interaction.send(Config.voice_required_text.format(interaction.user.name))
            return
        await cog(interaction, *args, **kwargs)
    return wrapped
