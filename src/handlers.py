import asyncio

from discord import VoiceChannel
from discord.ext import commands

from src.queue import MuzlagQueue
from src.players import player_factory


@commands.command(name='ping', help='Healthcheck')
async def ping(ctx: commands.context.Context):
    await ctx.send('pong')


@commands.command(name='play', help='Play song by link or add to queue')
async def play(ctx: commands.context.Context, url: str):
    if not ctx.message.author.voice:
        await ctx.send(f'**{ctx.message.author.name}** ты как сюда дозвонился шизоид?')
        return

    channel: VoiceChannel = ctx.message.author.voice.channel

    queue = MuzlagQueue()
    await queue.push(channel.id, url)

    if ctx.voice_client is not None:
        return

    await channel.connect()

    while True:
        try:
            while ctx.voice_client.is_paused():
                await asyncio.sleep(1)

            song = queue.get(channel.id)
            async with ctx.typing():
                player = player_factory(song)
                ctx.voice_client.play(
                    player.from_url(song, stream=True),
                    after=lambda e: print('Player error: %s' % e) if e else None
                )
            if not queue.is_repeat(channel.id):
                await ctx.send(f'Now playing: **{player.title}**')

            while ctx.voice_client.is_playing():
                await asyncio.sleep(1)
        except asyncio.QueueEmpty:
            break
        except AttributeError:
            return

    ctx.voice_client.stop()
    await ctx.voice_client.disconnect()


@commands.command(name='stop', help='Stop all songs in queue')
async def stop(ctx: commands.context.Context):
    queue = MuzlagQueue()
    if not ctx.message.author.voice or ctx.message.author.voice.channel.id not in queue:
        await ctx.send(f'**{ctx.message.author.name}** ты как сюда дозвонился шизоид?')
        return
    if ctx.voice_client.is_connected():
        ctx.voice_client.stop()
        queue.drop(ctx.message.author.voice.channel.id)
        await ctx.voice_client.disconnect()
    else:
        await ctx.send(f'**{ctx.message.author.name}** меня даже в голосовом канале нет!')


@commands.command(name='skip', help='Skip current song (default) or several songs')
async def skip(ctx: commands.context.Context, count: int = 1):
    queue = MuzlagQueue()
    if not ctx.message.author.voice or ctx.message.author.voice.channel.id not in queue:
        await ctx.send(f'**{ctx.message.author.name}** ты как сюда дозвонился шизоид?')
        return
    if ctx.voice_client.is_connected():
        try:
            ctx.voice_client.pause()
            queue.skip(ctx.message.author.voice.channel.id, count)
            ctx.voice_client.resume()
        except asyncio.QueueEmpty:
            ctx.voice_client.stop()
            await ctx.voice_client.disconnect()
    else:
        await ctx.send(f'**{ctx.message.author.name}** меня даже в голосовом канале нет!')


@commands.command(name='repeat', help='Set song to repeat')
async def repeat(ctx: commands.context.Context):
    queue = MuzlagQueue()
    if not ctx.message.author.voice or ctx.message.author.voice.channel.id not in queue:
        await ctx.send(f'**{ctx.message.author.name}** ты как сюда дозвонился шизоид?')
        return
    if ctx.voice_client.is_connected():
        try:
            ctx.voice_client.pause()
            queue.switch_repeat(ctx.message.author.voice.channel.id)
            ctx.voice_client.resume()
        except asyncio.QueueEmpty:
            ctx.voice_client.stop()
            await ctx.voice_client.disconnect()
    else:
        await ctx.send(f'**{ctx.message.author.name}** меня даже в голосовом канале нет!')


@commands.command(name='queue', help='Show songs queue')
async def queue(ctx: commands.context.Context):
    queue = MuzlagQueue()
    if not ctx.message.author.voice or ctx.message.author.voice.channel.id not in queue:
        await ctx.send(f'**{ctx.message.author.name}** ты как сюда дозвонился шизоид?')
        return
    if ctx.voice_client.is_connected():
        try:
            titles = 'Current queue:\n'
            res = queue.show_queue(ctx.message.author.voice.channel.id)
            if not res:
                await ctx.send(':anger: :japanese_goblin:**One song is not queue** :anger:')
                return
            for idx, item in enumerate(res):
                titles += f'{idx + 1}. {item};\n'
            await ctx.send(f'**{titles}**')
        except asyncio.QueueEmpty:
            ctx.voice_client.stop()
            await ctx.voice_client.disconnect()
    else:
        await ctx.send(f'**{ctx.message.author.name}** меня даже в голосовом канале нет!')


@commands.command(name='danilo', help='Play Danilo song', hidden=True)
async def danilo(ctx: commands.context.Context):
    await play(ctx, 'https://youtu.be/jZlkINQLGro')


@commands.command(name='vovan', help='Play Vovan song', hidden=True)
async def vovan(ctx: commands.context.Context):
    await play(ctx, 'https://youtu.be/wt-jj1qNScI')


@commands.command(name='nikita', help='Play Nikita song', hidden=True)
async def nikita(ctx: commands.context.Context):
    await play(ctx, 'https://youtu.be/7w9huXMoZF0')


@commands.command(name='vadick', help='Play Vadick song', hidden=True)
async def vadick(ctx: commands.context.Context):
    await play(ctx, 'https://youtu.be/L4hPnTpE2JE')


@commands.command(name='vadoom', help='Play Vadoom song', hidden=True)
async def vadoom(ctx: commands.context.Context):
    await play(ctx, 'https://youtu.be/vCb1SGRceik')
