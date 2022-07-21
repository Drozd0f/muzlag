import asyncio

from discord import VoiceChannel
from discord.ext import commands

from src.queue import MuzlagQueue
from src.youtube import YTDLSource


@commands.command(name='ping', help='Healthcheck')
async def ping(ctx: commands.context.Context):
    await ctx.send('pong')


@commands.command()
async def danilo(ctx: commands.context.Context):
    await play(ctx, 'https://youtu.be/jZlkINQLGro')


@commands.command()
async def vovan(ctx: commands.context.Context):
    await play(ctx, 'https://youtu.be/wt-jj1qNScI')


@commands.command()
async def nikita(ctx: commands.context.Context):
    await play(ctx, 'https://youtu.be/7w9huXMoZF0')


@commands.command()
async def vadick(ctx: commands.context.Context):
    await play(ctx, 'https://youtu.be/L4hPnTpE2JE')


@commands.command()
async def vadoom(ctx: commands.context.Context):
    await play(ctx, 'https://youtu.be/vCb1SGRceik')


@commands.command()
async def play(ctx: commands.context.Context, url: str):
    if not ctx.message.author.voice:
        await ctx.send(f"**{ctx.message.author.name}** ты как сюда дозвонился шизоид?")
        return

    channel: VoiceChannel = ctx.message.author.voice.channel

    queue = MuzlagQueue()
    await queue.push(channel.id, url)

    if ctx.voice_client is not None:
        return

    await channel.connect()

    while True:
        try:
            song = queue.get(channel.id)
            async with ctx.typing():
                player = await YTDLSource.from_url(song, stream=True)
                ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
            await ctx.send(f'Now playing: **{player.title}**')

            while ctx.voice_client.is_playing():
                await asyncio.sleep(1)

        except asyncio.QueueEmpty:
            break
        except AttributeError:
            return

    ctx.voice_client.stop()
    await ctx.voice_client.disconnect()


@commands.command()
async def stop(ctx: commands.context.Context):
    queue = MuzlagQueue()
    if ctx.voice_client.is_connected():
        ctx.voice_client.stop()
        queue.drop(ctx.message.author.voice.channel.id)
        await ctx.voice_client.disconnect()
    else:
        await ctx.send(f'**{ctx.message.author.name}** меня даже в голосовом канале нет!')


@commands.command()
async def skip(ctx: commands.context.Context):
    queue = MuzlagQueue()
    if not ctx.message.author.voice or ctx.message.author.voice.channel.id not in queue:
        await ctx.send(f"**{ctx.message.author.name}** ты как сюда дозвонился шизоид?")
        return
    if ctx.voice_client.is_connected():
        ctx.voice_client.pause()
        queue.skip(ctx.message.author.voice.channel.id)
    else:
        await ctx.send(f'**{ctx.message.author.name}** меня даже в голосовом канале нет!')
