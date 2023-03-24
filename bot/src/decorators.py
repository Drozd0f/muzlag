import nextcord
from nextcord.ext import commands

from bot.src.emoji import DefaultEmoji

VOICE_REQUIRED_TEXT = '**{user_name}** from where you sad that? {emoji} '


def c_voice_required(cog):
    async def wrapped(ctx: commands.Context, *args, **kwargs):
        if not ctx.message.author.voice:
            await ctx.send(
                VOICE_REQUIRED_TEXT.format(
                    user_name=ctx.message.author.name,
                    emoji=DefaultEmoji.thinking
                )
            )
            return
        await cog(ctx, *args, **kwargs)
    return wrapped


def s_voice_required(cog):
    async def wrapped(interaction: nextcord.Interaction, *args, **kwargs):
        if not interaction.user.voice:
            await interaction.send(
                VOICE_REQUIRED_TEXT.format(
                    user_name=interaction.user.name,
                    emoji=DefaultEmoji.thinking
                )
            )
            return
        await cog(interaction, *args, **kwargs)
    return wrapped
