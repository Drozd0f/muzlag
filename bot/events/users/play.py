import logging
import re
import asyncio
from urllib.parse import urlparse, parse_qs
from datetime import datetime

from nextcord import Message
from nextcord.ext.commands import Bot
from nextcord import VoiceChannel
from pytube import Playlist
from yt_dlp.utils import DownloadError

from bot.config import Config
from bot.errors import filter
from bot.src.yt_link_changer import YTLinks
from bot.src.queue import MuzlagQueue
from bot.src.players import player_factory


log = logging.getLogger(__name__)


def play(bot: Bot):
    async def on_message(message: Message):
        if message.content.startswith('?play ') and not has_link(message.content):
            request_proc = YTLinks()
            try:
                content = await request_proc.filter(bot, message)
            except filter.FilterStrLenError:
                await message.channel.send(f'Query lenght is too long (more than {Config.query_len} symbols)')
                return
            except ValueError:
                return
            if not content:
                return
            message.content = content
        if message.content.startswith('?play '):
            plst_ids = get_plst_id(message.content.replace('?play ', ''))
            if not plst_ids:
                return
            # todo: ^_^ add some comment if plailyst id not contain in message

            try:
                playlist = Playlist(f'https://www.youtube.com/playlist?list={plst_ids[0]}')
                urls = []
                for url in playlist:
                    urls.append(url)
                message.content = f'?play {urls[0]}'
                playlist_urls = urls[1:15]
                channel: VoiceChannel = message.author.voice.channel
                asyncio.create_task(push_rest(channel, playlist_urls))
            except IndexError:
                return
        await bot.process_commands(message)
    return on_message


async def push_rest(channel, playlist_urls):

    await asyncio.sleep(5)
    queue = MuzlagQueue()
    for url in playlist_urls:
        start = datetime.now()
        try:
            await asyncio.sleep(1)
            player = player_factory(url)
            await queue.push(channel.id, player)
            print(f'{datetime.now() - start} elapsed on push entity in queue')
        except asyncio.QueueEmpty:
            return
        except DownloadError:
            pass
        except AttributeError:
            return


def has_link(msg: str) -> bool:
    return bool(re.match(r"^\?play\shttp[s]?://", msg))


def get_plst_id(msg: str) -> bool:
    url = urlparse(msg)
    list_param = parse_qs(url.query).get('list')
    return list_param
