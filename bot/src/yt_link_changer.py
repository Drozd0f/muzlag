import re
import typing as t

from nextcord import Message
from nextcord.ext.commands import Bot
from youtubesearchpython import VideosSearch

from bot.config import Config
from bot.errors import filter
from bot.src.emoji import DefaultEmoji


class YTLinks:
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
            video_titles.append(f"{idx + 1}. {res.get('title')}")
            video_links.append(f"{res.get('link')}")
        return video_titles, video_links

    async def filter(self, bot: Bot, message: Message) -> t.Optional[str]:
        command, *text = message.content.split()
        text = ' '.join(text)
        if len(text) > Config.query_len:
            raise filter.FilterStrLenError
        if re.match(self.watch_link, text):
            url = self.link_rebaser(text, self.watch_link)
        elif re.match(self.shorts_link, text):
            url = self.link_rebaser(text, self.shorts_link)
        elif re.match(self.base_link, text):
            url = text
        else:
            url = await self.link_extractor(bot, message, text)
        return f'{command} {url}'

    async def link_extractor(self, bot: Bot, message: Message, text: str) -> t.Optional[str]:
        titles, links = self.yt_search(text, Config.result_len)
        choice_dialog = f'Type num of the song 1-{Config.result_len} (example: 2) \n' + '\n'.join(titles)
        await message.channel.send(choice_dialog)

        def is_author(msg):
            return msg.author == message.author and msg.channel == message.channel
        user_message = await bot.wait_for('message', check=is_author)
        try:
            return await self.get_link(user_message, links, titles)
        except ValueError as exc:
            await message.channel.send(
                f'{user_message.content} mean that hoisting crane, but you are adopted {DefaultEmoji.scream_cat} ))'
            )
            raise exc

    @staticmethod
    async def get_link(message: Message, links: t.List[str], titles: t.List[str]) -> t.Optional[str]:
        num = int(message.content)
        if num in range(1, Config.result_len + 1):
            await message.channel.send(f'You choose {num} - {titles[num-1]}:{links[num-1]}')
            return links[num-1]
        await message.channel.send(
            f'Abort! {DefaultEmoji.anger} You choose {num} - which is not valid,'
            f'type number only in range(1-{Config.result_len}) {DefaultEmoji.anger}'
        )
