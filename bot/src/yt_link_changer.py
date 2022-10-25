import re
import typing as t

from nextcord import Message
from nextcord.ext.commands import Bot
from youtubesearchpython import VideosSearch

from bot.config import Config
from bot.errors import filter
from bot.views.users.yt_link_changer import SongChooserView


class YTLinks:
    watch_link = r'^https://www\.youtube\.com/watch\?v='
    shorts_link = r'^https://www\.youtube\.com/shorts/'
    music_link = r'^https://music\.youtube\.com/watch\?v='
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
            dur = res.get('duration')
            title = res.get('title')
            content = f'{idx + 1}. {title}'[:Config.len_video_titles]
            if not dur:
                dur = 'Live'
            video_titles.append(f'{content.ljust(Config.len_video_titles)} {dur}')
            video_links.append(res.get('link'))
        return video_titles, video_links

    async def filter(self, bot: Bot, message: Message) -> t.Optional[str]:
        command, *text = message.content.split()
        text = ' '.join(text)
        if re.match(self.watch_link, text):
            url = self.link_rebaser(text, self.watch_link)
        elif re.match(self.shorts_link, text):
            url = self.link_rebaser(text, self.shorts_link)
        elif re.match(self.music_link, text):
            url = self.link_rebaser(text, self.music_link)
        elif re.match(self.base_link, text):
            url = text
        elif len(text) > Config.query_len:
            raise filter.FilterStrLenError
        else:
            links, num = await self.link_extractor(bot, message, text)
            if num is None:
                return
            url = links[num]
        return f'{command} {url}'

    async def link_extractor(self, bot: Bot, message: Message, text: str) -> t.Tuple[list, t.Optional[int]]:
        titles, links = self.yt_search(text, Config.result_len)
        choice_dialog = f'Click button of the song 1-{Config.result_len} or hit cancell to abort\n'+'\n'.join(
            titles)
        num = await self.song_chooser_view(message, choice_dialog)
        return links, num

    @staticmethod
    async def _song_chooser_view(message: Message, choice_dialog: str) -> int:
        view = SongChooserView(member=message.author)
        choice_dialog = f'```{choice_dialog}```'
        msg = await message.channel.send(choice_dialog, view=view)
        await view.wait()
        await msg.delete(delay=2)
        return view.chosen_song
