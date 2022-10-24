import logging

from nextcord import Message
from nextcord.ext.commands import Bot

from bot.config import Config
from bot.errors import filter
from bot.src.yt_link_changer import YTLinks


log = logging.getLogger(__name__)


def play(bot: Bot):
    async def on_message(message: Message):
        if message.content.startswith('?play '):
            request_proc = YTLinks()
            try:
                content = await request_proc.filter(bot, message)
            except filter.FilterStrLenError:
                await message.channel.send(f'Query lenght is too long (more than {Config.query_len} symbols)')
                return
            except ValueError:
                return
            message.content = content
        await bot.process_commands(message)
    return on_message
