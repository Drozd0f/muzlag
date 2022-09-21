import logging
import os
import re
import typing as t

from discord.ext import commands
from youtubesearchpython import VideosSearch

from src import handlers
from src.log import setup_logging

log = logging.getLogger(__name__)

BOT = commands.Bot(
    command_prefix='?',
    help_command=commands.DefaultHelpCommand(
        no_category='Commands'
    )
)


class FilterStrLenError(Exception):
    """Exception raised for errors in the input value.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Input lenght of srting is too long"):
        self.message = message
        super().__init__(self.message)


class InputValueError(Exception):
    """Exception raised for errors in the input value.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Input value is not valid"):
        self.message = message
        super().__init__(self.message)


class YTLinks:  # cделат синг тона шоб токо 1 экземпляр
    watch_link = r"^https://www\.youtube\.com/watch\?v="
    shorts_link = r"^https://www\.youtube\.com/shorts/"
    base_link = r"^https://youtu\.be.*"
    base_str = "https://youtu.be/"

    def link_rebaser(self, link: str, regex: str) -> str:
        return re.sub(regex, self.base_str, link)

    def yt_search(self, text: str) -> str:
        videosSearch = VideosSearch(text, limit=3)
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
        elif len(text) > 42:  # v config vinesti kak variable
            raise FilterStrLenError


@BOT.event
async def on_message(message):
    if '?play' in message.content:
        if not message.author.voice:
            log.info(f"1.{message.author} not in voice channel")
            return
        command, *text = message.content.split()
        text = ' '.join(text)
        request_proc = YTLinks()
        try:
            result = request_proc.filter(text)  # sdelat try-exept na oshibky svoiy
        except FilterStrLenError:
            await message.channel.send("Query lenght is too long(>42)")
            return
        if not result:
            titles, links = request_proc.yt_search(text)  # vinesti limit poiska suda i v config ego
            choice_dialog = 'Type num of the song 1-3 (example: "2") \n' + \
                ' '.join(titles)  # eta toje menyeatsa budes f-stringa
            await message.channel.send(choice_dialog)

            def is_my_message(msg):
                return msg.author == message.author and msg.channel == message.channel
            user_message = await BOT.wait_for('message', check=is_my_message)
            # vinesti v otdelnyiy function

            try:
                num = int(user_message.content)
                if num in range(1, 4):
                    await message.channel.send(f"You choose {num} - {titles[num-1]}:{links[num-1]}")
                    result = links[num-1]
                else:
                    raise InputValueError
                # vinesti v otdelnyiy function
            except ValueError:
                await message.channel.send(
                    f"**{user_message.content}** mean that hoisting crane, but you are adopted :scream_cat: ))"
                )
                return
            except InputValueError:
                await message.channel.send(
                    f"Abort! :anger: You choose **{num}** - which is not valid,"
                    "type number only in range(1-3) :anger:"
                )
                return
        message.content = f"{command} {result}"
    await BOT.process_commands(message)


def setup_command():
    BOT.add_command(handlers.ping)
    BOT.add_command(handlers.play)
    BOT.add_command(handlers.stop)
    BOT.add_command(handlers.skip)
    BOT.add_command(handlers.repeat)
    BOT.add_command(handlers.queue)

    BOT.add_command(handlers.danilo)
    BOT.add_command(handlers.vovan)
    BOT.add_command(handlers.nikita)
    BOT.add_command(handlers.vadick)
    BOT.add_command(handlers.vadoom)

    for command in BOT.commands:
        log.info(f"command --> {command}")


def main():
    setup_logging()
    token = os.getenv('TOKEN')

    log.info("setuping handlers...")
    setup_command()

    log.info("running bot...")
    BOT.run(token)


if __name__ == '__main__':
    main()
