import logging
import re
import typing as t

from nextcord import Message
from youtubesearchpython import VideosSearch
from nextcord.ext.commands import Bot
from bot.config import Config
from bot.errors import chat, filter

log = logging.getLogger(__name__)


class YTLinks:  # вынести это говно  в SRC кудато
    watch_link = r'^https://www\.youtube\.com/watch\?v='
    shorts_link = r'^https://www\.youtube\.com/shorts/'
    base_link = r'^https://youtu\.be.*'
    base_str = 'https://youtu.be/'

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def link_rebaser(self, link: str, regex: str) -> str:
        return re.sub(regex, self.base_str, link)

    def yt_search(self, text: str, res_len: int = 3) -> str:
        videosSearch = VideosSearch(text, limit=res_len)
        search_result = videosSearch.result()
        video_titles = []
        video_links = []
        for idx, res in enumerate(search_result.get('result')):
            video_titles.append(f"{idx + 1}. {res.get('title')} \n")
            video_links.append(f"{res.get('link')}")
        return video_titles, video_links

    def filter(self, text: str) -> t.Optional[str]:
        if re.match(self.watch_link, text):
            return self.link_rebaser(text, self.watch_link)
        elif re.match(self.shorts_link, text):
            return self.link_rebaser(text, self.shorts_link)
        elif re.match(self.base_link, text):
            return text
        elif len(text) > Config.query_len:  # v config vinesti kak variable
            raise filter.FilterStrLenError


def play(bot: Bot):  # эту хуйню порезать на шашлык
    async def on_message(message: Message):
        if message.content.startswith('?play'):
            command, *text = message.content.split()
            text = ' '.join(text)
            request_proc = YTLinks()
            try:
                result = request_proc.filter(text)
            except filter.FilterStrLenError:
                await message.channel.send(f'Query lenght is too long(more than {Config.query_len} symbols)')
                return
            if not result:
                titles, links = request_proc.yt_search(text, Config.result_len)
                choice_dialog = f'Type num of the song 1-{Config.result_len} (example: 2) \n' + ' '.join(titles)
                await message.channel.send(choice_dialog)

                def is_my_message(msg):
                    return msg.author == message.author and msg.channel == message.channel
                user_message = await bot.wait_for('message', check=is_my_message)
                # vinesti v otdelnyiy function

                try:
                    num = int(user_message.content)
                    if num in range(1, Config.result_len + 1):
                        await message.channel.send(f'You choose {num} - {titles[num-1]}:{links[num-1]}')
                        result = links[num-1]
                    else:
                        raise chat.InputValueError
                    # vinesti v otdelnyiy function
                except ValueError:
                    await message.channel.send(
                        f'{user_message.content} mean that hoisting crane, but you are adopted :scream_cat: ))'
                    )
                    return
                except chat.InputValueError:
                    await message.channel.send(
                        f'Abort! :anger: You choose {num} - which is not valid,'
                        f'type number only in range(1-{Config.result_len}) :anger:'
                    )
                    return
            message.content = f'{command} {result}'
        await bot.process_commands(message)
    return on_message
