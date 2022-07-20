import os
import asyncio

from discord import VoiceChannel, VoiceClient, FFmpegPCMAudio, PCMVolumeTransformer
from discord.ext import commands

from src.youtube import YTDLSource


bot = commands.Bot(command_prefix='>>')


@bot.command(name='ping', help='Healthcheck')
async def ping(ctx: commands.context.Context):
    await ctx.send('pong')


@bot.command()
async def danillo(ctx: commands.context.Context):
    if not ctx.message.author.voice:
        await ctx.send(f"{ctx.message.author.name} is not connected to a voice channel")
        return
    channel: VoiceChannel = ctx.message.author.voice.channel
    try:
        await channel.connect()
        player = PCMVolumeTransformer(FFmpegPCMAudio('./meme/danillo.mp4'))
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
    except commands.errors.ClientException:
        pass

    while ctx.voice_client.is_playing():
        await asyncio.sleep(1)

    ctx.voice_client.stop()
    await ctx.voice_client.disconnect()


@bot.command()
async def play(ctx: commands.context.Context, url: str):
    if not ctx.message.author.voice:
        await ctx.send(f"{ctx.message.author.name} is not connected to a voice channel")
        return
    channel: VoiceChannel = ctx.message.author.voice.channel
    try:
        await channel.connect()
        server = ctx.message.guild
        voice_channel = server.voice_client
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
            voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        await ctx.send(f'Now playing: **{player.title}**')
    except commands.errors.ClientException:
        pass

    while ctx.voice_client.is_playing():
        await asyncio.sleep(1)

    ctx.voice_client.stop()
    await ctx.voice_client.disconnect()


@bot.command()
async def stop(ctx: commands.context.Context):
    voice_client: VoiceClient = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


def main():
    token = os.getenv('TOKEN')
    bot.run(token)


if __name__ == '__main__':
    main()
